from __future__ import annotations

import json
import re
import sqlite3
import time
import uuid
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Iterator

from .errors import SupervisorError
from .files import (
    atomic_write_json,
    atomic_write_text,
    canonical_json_bytes,
    resolve_local_ref,
    sha256_bytes,
)
from .models import (
    AGENT_IDS,
    NONTERMINAL_RUN_STATES,
    AdapterResult,
    AdapterStatus,
    EffectClass,
    Handoff,
    Lease,
    RunPolicy,
    RunState,
    TaskRecord,
    TaskState,
    task_from_row,
)


SCHEMA_VERSION = 3
_TOKEN_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:@-]{0,127}$")
_SAFE_EVENT_KEY_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
_SAFE_EVENT_VALUE_RE = re.compile(r"^[A-Za-z0-9_.:@+-]{0,127}$")
_STOP_REASON_CODES = {
    "operator_stop",
    "safety_stop",
    "budget_exhausted",
    "watch_expired",
    "completed",
    "legacy_stop_file",
    "test_stop",
    "race_stop",
    "stop_before_nudge",
}


class StateStore:
    """SQLite-backed local-only state with fenced transitions."""

    def __init__(
        self,
        coop_root: str | Path,
        *,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self.coop_root = Path(coop_root).resolve()
        self.state_root = self.coop_root / ".ccc"
        self.db_path = self.state_root / "state.sqlite3"
        self.clock = clock

    def initialize(self) -> None:
        self.state_root.mkdir(parents=True, exist_ok=True)
        for name in ("payloads", "results"):
            (self.state_root / name).mkdir(exist_ok=True)
        with self._connect() as connection:
            connection.executescript(_SCHEMA)
            connection.execute(
                "INSERT OR IGNORE INTO meta(key, value) VALUES('schema_version', ?)",
                (str(SCHEMA_VERSION),),
            )
            version = connection.execute(
                "SELECT value FROM meta WHERE key='schema_version'"
            ).fetchone()[0]
            if int(version) == 2:
                self._migrate_v2_to_v3(connection)
                version = str(SCHEMA_VERSION)
            if int(version) != SCHEMA_VERSION:
                raise SupervisorError("schema_incompatible")

    @staticmethod
    def _migrate_v2_to_v3(connection: sqlite3.Connection) -> None:
        """Add the Desktop-focus policy without rewriting any local payload."""

        connection.execute("BEGIN IMMEDIATE")
        try:
            run_columns = {
                row[1] for row in connection.execute("PRAGMA table_info(runs)")
            }
            if "claude_desktop_focus_enabled" not in run_columns:
                connection.execute(
                    "ALTER TABLE runs ADD COLUMN claude_desktop_focus_enabled "
                    "INTEGER NOT NULL DEFAULT 0 "
                    "CHECK(claude_desktop_focus_enabled IN (0,1))"
                )
            if "claude_desktop_focus_cooldown_seconds" not in run_columns:
                connection.execute(
                    "ALTER TABLE runs ADD COLUMN "
                    "claude_desktop_focus_cooldown_seconds "
                    "INTEGER NOT NULL DEFAULT 600"
                )
            participant_columns = {
                row[1]
                for row in connection.execute("PRAGMA table_info(participants)")
            }
            if "last_claude_desktop_focus_at" not in participant_columns:
                connection.execute(
                    "ALTER TABLE participants ADD COLUMN "
                    "last_claude_desktop_focus_at REAL"
                )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS claude_desktop_focus_receipts(
                    run_id TEXT NOT NULL REFERENCES runs(run_id),
                    agent_id TEXT NOT NULL CHECK(agent_id='claude'),
                    focus_id TEXT NOT NULL,
                    state TEXT NOT NULL,
                    result_code TEXT,
                    created_at REAL NOT NULL,
                    completed_at REAL,
                    PRIMARY KEY(run_id, agent_id, focus_id)
                )
                """
            )
            connection.execute(
                "UPDATE meta SET value=? WHERE key='schema_version'",
                (str(SCHEMA_VERSION),),
            )
        except Exception:
            connection.rollback()
            raise
        else:
            connection.commit()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        self.state_root.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(
            self.db_path,
            timeout=5,
            isolation_level=None,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=5000")
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA synchronous=FULL")
        try:
            yield connection
        finally:
            connection.close()

    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                yield connection
            except Exception:
                connection.rollback()
                raise
            else:
                connection.commit()

    def init_run(
        self,
        *,
        project_alias: str,
        policy: RunPolicy | None = None,
        run_id: str | None = None,
    ) -> str:
        self.initialize()
        policy = policy or RunPolicy()
        try:
            policy.validate()
        except ValueError as exc:
            raise SupervisorError("policy_invalid") from exc
        project_alias = _validated_token(project_alias, "project_alias_invalid")
        if (self.coop_root / "STOP.md").exists():
            raise SupervisorError("stale_stop_file")
        run_id = _validated_uuid(run_id or str(uuid.uuid4()), "run_id_invalid")
        now = self.clock()
        with self._transaction() as connection:
            existing = connection.execute(
                "SELECT run_id FROM runs WHERE state IN "
                "('active','quiet_watch','draining','waiting_operator') "
                "ORDER BY created_at DESC LIMIT 1",
            ).fetchone()
            if existing:
                raise SupervisorError("run_already_active")
            generation = connection.execute(
                "SELECT COALESCE(MAX(generation), 0) + 1 FROM runs WHERE project_alias=?",
                (project_alias,),
            ).fetchone()[0]
            prior = connection.execute(
                "SELECT project_ref FROM runs WHERE project_alias=? "
                "ORDER BY generation DESC LIMIT 1",
                (project_alias,),
            ).fetchone()
            project_ref = prior["project_ref"] if prior else f"prj_{uuid.uuid4().hex}"
            connection.execute(
                """
                INSERT INTO runs(
                    run_id, generation, project_alias, project_ref, state, created_at, updated_at,
                    watch_expires_at, lease_ttl_seconds, claim_ttl_seconds,
                    max_wakes_per_agent, max_handoff_depth, max_handoffs_per_result,
                    max_payload_bytes, max_output_bytes, auto_wake_allowed,
                    ui_nudge_enabled, ui_nudge_after_failures,
                    ui_nudge_cooldown_seconds,
                    claude_desktop_focus_enabled,
                    claude_desktop_focus_cooldown_seconds, row_version
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0)
                """,
                (
                    run_id,
                    generation,
                    project_alias,
                    project_ref,
                    RunState.ACTIVE.value,
                    now,
                    now,
                    now + policy.watch_ttl_seconds,
                    policy.lease_ttl_seconds,
                    policy.claim_ttl_seconds,
                    policy.max_wakes_per_agent,
                    policy.max_handoff_depth,
                    policy.max_handoffs_per_result,
                    policy.max_payload_bytes,
                    policy.max_output_bytes,
                    int(policy.auto_wake_allowed),
                    int(policy.ui_nudge_enabled),
                    policy.ui_nudge_after_failures,
                    policy.ui_nudge_cooldown_seconds,
                    int(policy.claude_desktop_focus_enabled),
                    policy.claude_desktop_focus_cooldown_seconds,
                ),
            )
            for agent_id in AGENT_IDS:
                connection.execute(
                    "INSERT INTO participants(run_id, agent_id, enabled, state) "
                    "VALUES(?,?,1,'idle')",
                    (run_id, agent_id),
                )
            self._event(
                connection,
                run_id,
                "run_initialized",
                entity_type="run",
                entity_id=run_id,
                details={"generation": generation},
                now=now,
            )
        return run_id

    def active_run_id(self) -> str:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT run_id FROM runs WHERE state IN "
                "('active','quiet_watch','draining','waiting_operator') "
                "ORDER BY created_at DESC LIMIT 1"
            ).fetchone()
        if not row:
            raise SupervisorError("run_not_found")
        return row["run_id"]

    def latest_run_id(self) -> str:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT run_id FROM runs ORDER BY created_at DESC, generation DESC LIMIT 1"
            ).fetchone()
        if not row:
            raise SupervisorError("run_not_found")
        return row["run_id"]

    def run_row(self, run_id: str) -> sqlite3.Row:
        run_id = _validated_uuid(run_id, "run_id_invalid")
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM runs WHERE run_id=?", (run_id,)
            ).fetchone()
        if not row:
            raise SupervisorError("run_not_found")
        return row

    def enqueue_task(
        self,
        *,
        run_id: str,
        target_agent: str,
        payload: str,
        idempotency_key: str,
        effect_class: EffectClass = EffectClass.READ_ONLY,
        kind: str = "task",
        parent_task_id: str | None = None,
        correlation_id: str | None = None,
        max_attempts: int | None = None,
    ) -> tuple[TaskRecord, bool]:
        run_id = _validated_uuid(run_id, "run_id_invalid")
        target_agent = _validated_agent(target_agent)
        idempotency_key = _validated_token(
            idempotency_key, "idempotency_key_invalid"
        )
        kind = _validated_token(kind, "task_kind_invalid")
        try:
            effect_class = EffectClass(effect_class)
        except ValueError as exc:
            raise SupervisorError("effect_class_invalid") from exc
        if not isinstance(payload, str):
            raise SupervisorError("payload_schema_invalid")
        if parent_task_id is not None:
            parent_task_id = _validated_uuid(
                parent_task_id, "parent_task_id_invalid"
            )
        requested_correlation_id = (
            _validated_uuid(correlation_id, "correlation_id_invalid")
            if correlation_id is not None
            else None
        )
        if max_attempts is None:
            max_attempts = (
                3
                if effect_class in (EffectClass.READ_ONLY, EffectClass.REVERSIBLE)
                else 1
            )
        if max_attempts <= 0 or max_attempts > 10:
            raise SupervisorError("max_attempts_invalid")
        payload_value = {"schema": "ccc.task.payload.v1", "payload": payload}
        payload_bytes = canonical_json_bytes(payload_value)
        payload_hash = sha256_bytes(payload_bytes)
        now = self.clock()
        payload_path: Path | None = None
        try:
            with self._transaction() as connection:
                run = self._active_run_locked(connection, run_id, now)
                if len(payload_bytes) > run["max_payload_bytes"]:
                    raise SupervisorError("payload_too_large")

                depth = 0
                resolved_correlation_id = requested_correlation_id
                if parent_task_id:
                    parent = connection.execute(
                        "SELECT * FROM tasks WHERE task_id=? AND run_id=?",
                        (parent_task_id, run_id),
                    ).fetchone()
                    if not parent:
                        raise SupervisorError("parent_task_not_found")
                    depth = parent["depth"] + 1
                    if (
                        resolved_correlation_id is not None
                        and resolved_correlation_id != parent["correlation_id"]
                    ):
                        raise SupervisorError("correlation_mismatch")
                    resolved_correlation_id = parent["correlation_id"]
                if depth > run["max_handoff_depth"]:
                    raise SupervisorError("handoff_depth_exceeded")

                existing = connection.execute(
                    "SELECT * FROM tasks WHERE run_id=? AND idempotency_key=?",
                    (run_id, idempotency_key),
                ).fetchone()
                if existing:
                    same_correlation = (
                        requested_correlation_id is None
                        or existing["correlation_id"] == resolved_correlation_id
                    )
                    if (
                        existing["payload_sha256"] != payload_hash
                        or existing["target_agent"] != target_agent
                        or existing["effect_class"] != effect_class.value
                        or existing["kind"] != kind
                        or existing["parent_task_id"] != parent_task_id
                        or existing["depth"] != depth
                        or existing["max_attempts"] != max_attempts
                        or not same_correlation
                    ):
                        raise SupervisorError("idempotency_conflict")
                    return task_from_row(existing), False

                resolved_correlation_id = resolved_correlation_id or str(uuid.uuid4())
                task_id = str(uuid.uuid4())
                payload_ref = f"payloads/{task_id}.json"
                payload_path = resolve_local_ref(self.state_root, payload_ref)
                atomic_write_json(payload_path, payload_value)
                connection.execute(
                    """
                    INSERT INTO tasks(
                        task_id, run_id, target_agent, kind, effect_class, state,
                        idempotency_key, payload_ref, payload_sha256, created_at,
                        updated_at, available_at, attempt_count, max_attempts,
                        depth, correlation_id, parent_task_id
                    ) VALUES(?,?,?,?,?,'queued',?,?,?,?,?,?,0,?,?,?,?)
                    """,
                    (
                        task_id,
                        run_id,
                        target_agent,
                        kind,
                        effect_class.value,
                        idempotency_key,
                        payload_ref,
                        payload_hash,
                        now,
                        now,
                        now,
                        max_attempts,
                        depth,
                        resolved_correlation_id,
                        parent_task_id,
                    ),
                )
                self._event(
                    connection,
                    run_id,
                    "task_enqueued",
                    entity_type="task",
                    entity_id=task_id,
                    actor_id=target_agent,
                    details={
                        "effect_class": effect_class.value,
                        "depth": depth,
                        "payload_bytes": len(payload_bytes),
                    },
                    now=now,
                )
                row = connection.execute(
                    "SELECT * FROM tasks WHERE task_id=?", (task_id,)
                ).fetchone()
                return task_from_row(row), True
        except Exception:
            if payload_path is not None:
                payload_path.unlink(missing_ok=True)
            raise

    def read_task_payload(self, task: TaskRecord) -> str:
        path = resolve_local_ref(self.state_root, task.payload_ref)
        data = path.read_bytes()
        if sha256_bytes(data) != task.payload_sha256:
            raise SupervisorError("payload_hash_mismatch")
        value = json.loads(data)
        if set(value) != {"schema", "payload"} or value["schema"] != "ccc.task.payload.v1":
            raise SupervisorError("payload_schema_invalid")
        if not isinstance(value["payload"], str):
            raise SupervisorError("payload_schema_invalid")
        return value["payload"]

    def begin_wake(
        self,
        *,
        run_id: str,
        agent_id: str,
        wake_id: str,
        source: str = "event",
    ) -> str:
        run_id = _validated_uuid(run_id, "run_id_invalid")
        agent_id = _validated_agent(agent_id)
        wake_id = _validated_uuid(wake_id, "wake_id_invalid")
        source = _validated_token(source, "wake_source_invalid")
        now = self.clock()
        with self._transaction() as connection:
            run = self._run_locked(connection, run_id)
            self._apply_legacy_stop_locked(connection, run, now)
            run = self._run_locked(connection, run_id)
            duplicate = connection.execute(
                "SELECT * FROM wakes WHERE run_id=? AND agent_id=? AND wake_id=?",
                (run_id, agent_id, wake_id),
            ).fetchone()
            if duplicate:
                active_lease = connection.execute(
                    "SELECT 1 FROM leases WHERE run_id=? AND agent_id=? "
                    "AND state='active' AND expires_at>?",
                    (run_id, agent_id, now),
                ).fetchone()
                replayable = (
                    duplicate["state"] == "accepted"
                    and duplicate["completed_at"] is None
                    and now - duplicate["received_at"] >= run["lease_ttl_seconds"]
                    and not active_lease
                    and run["state"]
                    in (RunState.ACTIVE.value, RunState.QUIET_WATCH.value)
                    and now < run["watch_expires_at"]
                )
                if replayable:
                    connection.execute(
                        "UPDATE wakes SET source=?, failure_code='wake_replayed', "
                        "result_code=NULL, received_at=? WHERE run_id=? AND agent_id=? "
                        "AND wake_id=?",
                        (source, now, run_id, agent_id, wake_id),
                    )
                    self._event(
                        connection,
                        run_id,
                        "wake_replayed",
                        entity_type="wake",
                        entity_id=wake_id,
                        actor_id=agent_id,
                        details={"state": "accepted"},
                        now=now,
                    )
                    return "accepted"
                return "duplicate"
            result = "accepted"
            failure_code: str | None = None
            if run["state"] not in (RunState.ACTIVE.value, RunState.QUIET_WATCH.value):
                result, failure_code = "suppressed", "run_not_active"
            elif now >= run["watch_expires_at"]:
                self._expire_run_locked(connection, run_id, now)
                result, failure_code = "suppressed", "watch_expired"
            elif source == "timer" and not run["auto_wake_allowed"]:
                result, failure_code = "suppressed", "auto_wake_denied"
            else:
                wake_count = connection.execute(
                    "SELECT COUNT(*) FROM wakes WHERE run_id=? AND agent_id=? AND state='accepted'",
                    (run_id, agent_id),
                ).fetchone()[0]
                if wake_count >= run["max_wakes_per_agent"]:
                    connection.execute(
                        "UPDATE runs SET state='waiting_operator', updated_at=?, "
                        "row_version=row_version+1 WHERE run_id=?",
                        (now, run_id),
                    )
                    result, failure_code = "suppressed", "wake_budget_exhausted"
            connection.execute(
                "INSERT INTO wakes(run_id,agent_id,wake_id,source,state,failure_code,received_at) "
                "VALUES(?,?,?,?,?,?,?)",
                (run_id, agent_id, wake_id, source, result, failure_code, now),
            )
            self._event(
                connection,
                run_id,
                "wake_received",
                entity_type="wake",
                entity_id=wake_id,
                actor_id=agent_id,
                details={"state": result, "failure_code": failure_code or "none"},
                now=now,
            )
            return result

    def end_wake(
        self,
        *,
        run_id: str,
        agent_id: str,
        wake_id: str,
        result_code: str,
    ) -> None:
        result_code = _validated_token(result_code, "wake_result_invalid")
        now = self.clock()
        with self._transaction() as connection:
            updated = connection.execute(
                "UPDATE wakes SET completed_at=?, result_code=?, "
                "state=CASE WHEN ?='lease_busy' THEN 'suppressed' ELSE state END, "
                "failure_code=CASE WHEN ?='lease_busy' THEN 'lease_busy' ELSE failure_code END "
                "WHERE run_id=? "
                "AND agent_id=? AND wake_id=? AND completed_at IS NULL",
                (
                    now,
                    result_code,
                    result_code,
                    result_code,
                    run_id,
                    agent_id,
                    wake_id,
                ),
            ).rowcount
            if not updated:
                raise SupervisorError("wake_not_active")

    def acquire_lease(
        self,
        *,
        run_id: str,
        agent_id: str,
        worker_session_id: str,
    ) -> Lease:
        run_id = _validated_uuid(run_id, "run_id_invalid")
        agent_id = _validated_agent(agent_id)
        worker_session_id = _validated_uuid(
            worker_session_id, "worker_session_id_invalid"
        )
        now = self.clock()
        with self._transaction() as connection:
            run = self._active_run_locked(connection, run_id, now)
            participant = connection.execute(
                "SELECT * FROM participants WHERE run_id=? AND agent_id=? AND enabled=1",
                (run_id, agent_id),
            ).fetchone()
            if not participant:
                raise SupervisorError("agent_not_participant")
            existing = connection.execute(
                "SELECT * FROM leases WHERE run_id=? AND agent_id=?",
                (run_id, agent_id),
            ).fetchone()
            if existing and existing["state"] == "active" and existing["expires_at"] > now:
                if existing["worker_session_id"] != worker_session_id:
                    raise SupervisorError("lease_held_by_other_session")
                expires_at = now + run["lease_ttl_seconds"]
                connection.execute(
                    "UPDATE leases SET renewed_at=?, expires_at=?, heartbeat_seq=heartbeat_seq+1 "
                    "WHERE run_id=? AND agent_id=?",
                    (now, expires_at, run_id, agent_id),
                )
                return Lease(
                    run_id,
                    agent_id,
                    worker_session_id,
                    existing["lease_token"],
                    existing["fence_epoch"],
                    expires_at,
                )
            epoch = (existing["fence_epoch"] if existing else 0) + 1
            lease_token = str(uuid.uuid4())
            expires_at = now + run["lease_ttl_seconds"]
            connection.execute(
                """
                INSERT INTO leases(
                    run_id,agent_id,worker_session_id,lease_token,fence_epoch,state,
                    acquired_at,renewed_at,expires_at,heartbeat_seq,current_task_id
                ) VALUES(?,?,?,?,?,'active',?,?,?,?,NULL)
                ON CONFLICT(run_id,agent_id) DO UPDATE SET
                    worker_session_id=excluded.worker_session_id,
                    lease_token=excluded.lease_token,
                    fence_epoch=excluded.fence_epoch,
                    state='active', acquired_at=excluded.acquired_at,
                    renewed_at=excluded.renewed_at, expires_at=excluded.expires_at,
                    heartbeat_seq=0, current_task_id=NULL
                """,
                (
                    run_id,
                    agent_id,
                    worker_session_id,
                    lease_token,
                    epoch,
                    now,
                    now,
                    expires_at,
                    0,
                ),
            )
            connection.execute(
                "UPDATE participants SET state='leased', updated_at=? "
                "WHERE run_id=? AND agent_id=?",
                (now, run_id, agent_id),
            )
            self._event(
                connection,
                run_id,
                "lease_acquired",
                entity_type="agent",
                entity_id=agent_id,
                actor_id=agent_id,
                details={"fence_epoch": epoch},
                now=now,
            )
            return Lease(
                run_id,
                agent_id,
                worker_session_id,
                lease_token,
                epoch,
                expires_at,
            )

    def renew_lease(self, lease: Lease) -> Lease:
        now = self.clock()
        with self._transaction() as connection:
            run = self._run_locked(connection, lease.run_id)
            updated = connection.execute(
                """
                UPDATE leases SET renewed_at=?, expires_at=?, heartbeat_seq=heartbeat_seq+1
                WHERE run_id=? AND agent_id=? AND worker_session_id=?
                  AND lease_token=? AND fence_epoch=? AND state='active' AND expires_at>?
                """,
                (
                    now,
                    now + run["lease_ttl_seconds"],
                    lease.run_id,
                    lease.agent_id,
                    lease.worker_session_id,
                    lease.lease_token,
                    lease.fence_epoch,
                    now,
                ),
            ).rowcount
            if not updated:
                raise SupervisorError("lease_fence_stale")
            connection.execute(
                "UPDATE tasks SET claim_expires_at=? WHERE run_id=? AND task_id=("
                "SELECT current_task_id FROM leases WHERE run_id=? AND agent_id=?"
                ") AND state IN ('claimed','running') AND claim_worker_session_id=? "
                "AND claim_fence_epoch=?",
                (
                    now + run["claim_ttl_seconds"],
                    lease.run_id,
                    lease.run_id,
                    lease.agent_id,
                    lease.worker_session_id,
                    lease.fence_epoch,
                ),
            )
            return Lease(
                lease.run_id,
                lease.agent_id,
                lease.worker_session_id,
                lease.lease_token,
                lease.fence_epoch,
                now + run["lease_ttl_seconds"],
            )

    def release_lease(self, lease: Lease, reason_code: str = "worker_complete") -> None:
        reason_code = _validated_token(reason_code, "release_reason_invalid")
        now = self.clock()
        with self._transaction() as connection:
            updated = connection.execute(
                "UPDATE leases SET state='released', renewed_at=?, expires_at=?, "
                "release_reason=? WHERE run_id=? AND agent_id=? AND worker_session_id=? "
                "AND lease_token=? AND fence_epoch=? AND state='active'",
                (
                    now,
                    now,
                    reason_code,
                    lease.run_id,
                    lease.agent_id,
                    lease.worker_session_id,
                    lease.lease_token,
                    lease.fence_epoch,
                ),
            ).rowcount
            if not updated:
                raise SupervisorError("lease_fence_stale")
            connection.execute(
                "UPDATE participants SET state='idle', updated_at=? "
                "WHERE run_id=? AND agent_id=?",
                (now, lease.run_id, lease.agent_id),
            )
            self._complete_stop_if_drained_locked(connection, lease.run_id, now)

    def claim_next_task(self, lease: Lease) -> TaskRecord | None:
        now = self.clock()
        with self._transaction() as connection:
            run = self._active_run_locked(connection, lease.run_id, now)
            self._assert_lease_locked(connection, lease, now)
            row = connection.execute(
                """
                SELECT * FROM tasks
                WHERE run_id=? AND target_agent=? AND state='queued' AND available_at<=?
                ORDER BY created_at, task_id LIMIT 1
                """,
                (lease.run_id, lease.agent_id, now),
            ).fetchone()
            if not row:
                return None
            claim_token = str(uuid.uuid4())
            updated = connection.execute(
                """
                UPDATE tasks SET state='claimed', claim_token=?, claim_worker_session_id=?,
                    claim_fence_epoch=?, claim_expires_at=?, claimed_at=?, updated_at=?,
                    attempt_count=attempt_count+1
                WHERE task_id=? AND state='queued'
                """,
                (
                    claim_token,
                    lease.worker_session_id,
                    lease.fence_epoch,
                    now + run["claim_ttl_seconds"],
                    now,
                    now,
                    row["task_id"],
                ),
            ).rowcount
            if not updated:
                raise SupervisorError("task_already_claimed")
            connection.execute(
                "UPDATE leases SET current_task_id=? WHERE run_id=? AND agent_id=?",
                (row["task_id"], lease.run_id, lease.agent_id),
            )
            claimed = connection.execute(
                "SELECT * FROM tasks WHERE task_id=?", (row["task_id"],)
            ).fetchone()
            self._event(
                connection,
                lease.run_id,
                "task_claimed",
                entity_type="task",
                entity_id=row["task_id"],
                actor_id=lease.agent_id,
                details={"attempt": claimed["attempt_count"]},
                now=now,
            )
            return task_from_row(claimed)

    def start_task(self, lease: Lease, task: TaskRecord) -> TaskRecord:
        now = self.clock()
        with self._transaction() as connection:
            run = self._run_locked(connection, lease.run_id)
            self._apply_legacy_stop_locked(connection, run, now)
            run = self._run_locked(connection, lease.run_id)
            if run["state"] not in (RunState.ACTIVE.value, RunState.QUIET_WATCH.value):
                raise SupervisorError("run_stop_requested")
            self._assert_lease_locked(connection, lease, now)
            updated = connection.execute(
                """
                UPDATE tasks SET state='running', started_at=?, updated_at=?
                WHERE task_id=? AND state='claimed' AND claim_token=?
                  AND claim_worker_session_id=? AND claim_fence_epoch=?
                """,
                (
                    now,
                    now,
                    task.task_id,
                    task.claim_token,
                    lease.worker_session_id,
                    lease.fence_epoch,
                ),
            ).rowcount
            if not updated:
                raise SupervisorError("task_fence_stale")
            connection.execute(
                "INSERT INTO task_attempts(task_id,attempt_no,worker_session_id,"
                "fence_epoch,started_at,state) VALUES(?,?,?,?,?,'running')",
                (
                    task.task_id,
                    task.attempt_count,
                    lease.worker_session_id,
                    lease.fence_epoch,
                    now,
                ),
            )
            return task_from_row(
                connection.execute(
                    "SELECT * FROM tasks WHERE task_id=?", (task.task_id,)
                ).fetchone()
            )

    def finish_task(
        self,
        *,
        lease: Lease,
        task: TaskRecord,
        result: AdapterResult,
    ) -> str:
        now = self.clock()
        self._validate_adapter_result(result, validate_safe=False)
        result_ref = f"results/{task.task_id}.{task.attempt_count}.json"
        result_path = resolve_local_ref(self.state_root, result_ref)
        published_paths: list[Path] = []
        try:
            with self._transaction() as connection:
                run = self._run_locked(connection, lease.run_id)
                self._assert_lease_locked(connection, lease, now, allow_expired=False)
                current = connection.execute(
                    "SELECT * FROM tasks WHERE task_id=?", (task.task_id,)
                ).fetchone()
                if (
                    not current
                    or current["state"] != TaskState.RUNNING.value
                    or current["claim_token"] != task.claim_token
                    or current["claim_worker_session_id"] != lease.worker_session_id
                    or current["claim_fence_epoch"] != lease.fence_epoch
                ):
                    raise SupervisorError("task_fence_stale")

                effective = result
                effective_handoffs: list[dict[str, Any]] = []
                if run["state"] in (
                    RunState.DRAINING.value,
                    RunState.STOPPED.value,
                    RunState.EXPIRED.value,
                ) or (self.coop_root / "STOP.md").exists():
                    effective = AdapterResult(
                        status=AdapterStatus.CANCELLED,
                        summary="cancelled by run state",
                        failure_code="task_cancelled_by_stop",
                        conversation_id=result.conversation_id,
                        safe_metrics={},
                    )
                else:
                    self._validate_adapter_result(result, validate_safe=True)
                    if result.handoffs and result.status != AdapterStatus.SUCCEEDED:
                        raise SupervisorError("handoff_on_unsuccessful_result")
                    if len(result.handoffs) > run["max_handoffs_per_result"]:
                        raise SupervisorError("handoff_count_exceeded")
                    if (
                        result.handoffs
                        and task.depth + 1 > run["max_handoff_depth"]
                    ):
                        raise SupervisorError("handoff_depth_exceeded")
                    effective_handoffs = self._prepare_handoffs(
                        run_snapshot=run,
                        parent=task,
                        handoffs=result.handoffs,
                    )
                    if (
                        run["state"] == RunState.WAITING_OPERATOR.value
                        and effective_handoffs
                    ):
                        effective = AdapterResult(
                            status=AdapterStatus.BLOCKED,
                            summary="operator hold rejects new handoffs",
                            failure_code="run_not_accepting_handoffs",
                            conversation_id=result.conversation_id,
                        )
                        effective_handoffs = []

                result_value = {
                    "schema": "ccc.task.result.v1",
                    "status": effective.status.value,
                    "summary": effective.summary,
                    "failure_code": effective.failure_code,
                    "safe_metrics": effective.safe_metrics,
                }
                if len(canonical_json_bytes(result_value)) > run["max_output_bytes"]:
                    raise SupervisorError("result_too_large")

                final_state: str
                available_at = now
                if effective.status == AdapterStatus.SUCCEEDED:
                    final_state = TaskState.SUCCEEDED.value
                elif effective.status == AdapterStatus.BLOCKED:
                    final_state = TaskState.BLOCKED.value
                elif effective.status == AdapterStatus.CANCELLED:
                    final_state = TaskState.CANCELLED.value
                else:
                    safe_retry = current["effect_class"] in (
                        EffectClass.READ_ONLY.value,
                        EffectClass.REVERSIBLE.value,
                    )
                    if (
                        effective.retryable
                        and safe_retry
                        and current["attempt_count"] < current["max_attempts"]
                        and run["state"] in (RunState.ACTIVE.value, RunState.QUIET_WATCH.value)
                    ):
                        final_state = TaskState.QUEUED.value
                        available_at = now + min(60, 2 ** current["attempt_count"])
                    else:
                        final_state = (
                            TaskState.DEAD_LETTER.value
                            if safe_retry
                            else TaskState.BLOCKED.value
                        )

                result_hash, _ = atomic_write_json(result_path, result_value)
                published_paths.append(result_path)
                terminal = final_state != TaskState.QUEUED.value
                connection.execute(
                    """
                    UPDATE tasks SET state=?, result_ref=?, result_sha256=?, failure_code=?,
                        finished_at=?, updated_at=?, available_at=?, claim_token=NULL,
                        claim_worker_session_id=NULL, claim_fence_epoch=NULL,
                        claim_expires_at=NULL
                    WHERE task_id=?
                    """,
                    (
                        final_state,
                        result_ref,
                        result_hash,
                        effective.failure_code,
                        now if terminal else None,
                        now,
                        available_at,
                        task.task_id,
                    ),
                )
                connection.execute(
                    "UPDATE task_attempts SET state=?, finished_at=?, failure_code=? "
                    "WHERE task_id=? AND attempt_no=?",
                    (
                        effective.status.value,
                        now,
                        effective.failure_code,
                        task.task_id,
                        task.attempt_count,
                    ),
                )
                connection.execute(
                    "UPDATE leases SET current_task_id=NULL WHERE run_id=? AND agent_id=?",
                    (lease.run_id, lease.agent_id),
                )
                if effective.status == AdapterStatus.SUCCEEDED:
                    connection.execute(
                        "UPDATE participants SET conversation_id=COALESCE(?,conversation_id), "
                        "consecutive_failures=0, last_failure_code=NULL, state='idle', updated_at=? "
                        "WHERE run_id=? AND agent_id=?",
                        (effective.conversation_id, now, lease.run_id, lease.agent_id),
                    )
                elif effective.status == AdapterStatus.CANCELLED:
                    connection.execute(
                        "UPDATE participants SET conversation_id=COALESCE(?,conversation_id), "
                        "state='idle', updated_at=? WHERE run_id=? AND agent_id=?",
                        (effective.conversation_id, now, lease.run_id, lease.agent_id),
                    )
                else:
                    connection.execute(
                        "UPDATE participants SET conversation_id=COALESCE(?,conversation_id), "
                        "consecutive_failures=consecutive_failures+1, last_failure_code=?, "
                        "state='idle', updated_at=? WHERE run_id=? AND agent_id=?",
                        (
                            effective.conversation_id,
                            effective.failure_code or effective.status.value,
                            now,
                            lease.run_id,
                            lease.agent_id,
                        ),
                    )
                if final_state in (TaskState.BLOCKED.value, TaskState.DEAD_LETTER.value):
                    connection.execute(
                        "UPDATE runs SET state='waiting_operator', updated_at=?, "
                        "row_version=row_version+1 WHERE run_id=? AND state IN ('active','quiet_watch')",
                        (now, lease.run_id),
                    )
                if final_state == TaskState.SUCCEEDED.value:
                    for handoff in effective_handoffs:
                        existing = connection.execute(
                            "SELECT * FROM tasks WHERE run_id=? AND idempotency_key=?",
                            (lease.run_id, handoff["idempotency_key"]),
                        ).fetchone()
                        if existing:
                            if not self._handoff_matches(existing, handoff, task):
                                raise SupervisorError("idempotency_conflict")
                            continue
                        atomic_write_json(
                            handoff["payload_path"], handoff["payload_value"]
                        )
                        published_paths.append(handoff["payload_path"])
                        connection.execute(
                            """
                            INSERT INTO tasks(
                                task_id, run_id, target_agent, kind, effect_class, state,
                                idempotency_key, payload_ref, payload_sha256, created_at,
                                updated_at, available_at, attempt_count, max_attempts,
                                depth, correlation_id, parent_task_id
                            ) VALUES(?,?,?,?,?,'queued',?,?,?,?,?,?,0,?,?,?,?)
                            """,
                            (
                                handoff["task_id"],
                                lease.run_id,
                                handoff["target_agent"],
                                handoff["kind"],
                                handoff["effect_class"],
                                handoff["idempotency_key"],
                                handoff["payload_ref"],
                                handoff["payload_sha256"],
                                now,
                                now,
                                now,
                                handoff["max_attempts"],
                                task.depth + 1,
                                task.correlation_id,
                                task.task_id,
                            ),
                        )
                        self._event(
                            connection,
                            lease.run_id,
                            "task_enqueued",
                            entity_type="task",
                            entity_id=handoff["task_id"],
                            actor_id=handoff["target_agent"],
                            details={
                                "effect_class": handoff["effect_class"],
                                "depth": task.depth + 1,
                                "payload_bytes": handoff["payload_bytes"],
                            },
                            now=now,
                        )
                self._event(
                    connection,
                    lease.run_id,
                    "task_finished",
                    entity_type="task",
                    entity_id=task.task_id,
                    actor_id=lease.agent_id,
                    details={
                        "state": final_state,
                        "failure_class": _failure_class(effective.failure_code),
                        "retryable": effective.retryable,
                    },
                    now=now,
                )
                self._complete_stop_if_drained_locked(connection, lease.run_id, now)
            return final_state
        except Exception:
            for path in published_paths:
                path.unlink(missing_ok=True)
            raise

    @staticmethod
    def _validate_adapter_result(
        result: AdapterResult, *, validate_safe: bool
    ) -> None:
        if (
            not isinstance(result, AdapterResult)
            or not isinstance(result.status, AdapterStatus)
            or not isinstance(result.summary, str)
            or not isinstance(result.retryable, bool)
            or not isinstance(result.handoffs, tuple)
            or not isinstance(result.safe_metrics, dict)
        ):
            raise SupervisorError("adapter_result_invalid")
        if validate_safe:
            _validated_safe_details(result.safe_metrics)
            if result.failure_code is not None:
                _validated_token(result.failure_code, "adapter_result_invalid")

    def _prepare_handoffs(
        self,
        *,
        run_snapshot: sqlite3.Row,
        parent: TaskRecord,
        handoffs: tuple[Handoff, ...],
    ) -> list[dict[str, Any]]:
        prepared: list[dict[str, Any]] = []
        seen_keys: set[str] = set()
        for handoff in handoffs:
            if not isinstance(handoff, Handoff) or not isinstance(handoff.payload, str):
                raise SupervisorError("handoff_invalid")
            target_agent = _validated_agent(handoff.target_agent)
            idempotency_key = _validated_token(
                handoff.idempotency_key, "idempotency_key_invalid"
            )
            if idempotency_key in seen_keys:
                raise SupervisorError("duplicate_handoff_key")
            seen_keys.add(idempotency_key)
            kind = _validated_token(handoff.kind, "task_kind_invalid")
            try:
                effect_class = EffectClass(handoff.effect_class)
            except ValueError as exc:
                raise SupervisorError("handoff_invalid") from exc
            payload_value = {
                "schema": "ccc.task.payload.v1",
                "payload": handoff.payload,
            }
            payload_bytes = canonical_json_bytes(payload_value)
            if len(payload_bytes) > run_snapshot["max_payload_bytes"]:
                raise SupervisorError("payload_too_large")
            task_id = str(uuid.uuid4())
            payload_ref = f"payloads/{task_id}.json"
            payload_path = resolve_local_ref(self.state_root, payload_ref)
            payload_hash = sha256_bytes(payload_bytes)
            prepared.append(
                {
                    "task_id": task_id,
                    "target_agent": target_agent,
                    "kind": kind,
                    "effect_class": effect_class.value,
                    "idempotency_key": idempotency_key,
                    "payload_ref": payload_ref,
                    "payload_path": payload_path,
                    "payload_value": payload_value,
                    "payload_sha256": payload_hash,
                    "payload_bytes": len(payload_bytes),
                    "max_attempts": (
                        3
                        if effect_class
                        in (EffectClass.READ_ONLY, EffectClass.REVERSIBLE)
                        else 1
                    ),
                    "parent_task_id": parent.task_id,
                }
            )
        return prepared

    @staticmethod
    def _handoff_matches(
        existing: sqlite3.Row,
        prepared: dict[str, Any],
        parent: TaskRecord,
    ) -> bool:
        return (
            existing["target_agent"] == prepared["target_agent"]
            and existing["kind"] == prepared["kind"]
            and existing["effect_class"] == prepared["effect_class"]
            and existing["payload_sha256"] == prepared["payload_sha256"]
            and existing["parent_task_id"] == parent.task_id
            and existing["correlation_id"] == parent.correlation_id
            and existing["max_attempts"] == prepared["max_attempts"]
        )

    def conversation_id(self, run_id: str, agent_id: str) -> str | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT conversation_id FROM participants WHERE run_id=? AND agent_id=?",
                (run_id, agent_id),
            ).fetchone()
        if not row:
            raise SupervisorError("agent_not_participant")
        return row["conversation_id"]

    def should_cancel(self, run_id: str) -> bool:
        try:
            run = self.run_row(run_id)
        except SupervisorError:
            return True
        return run["state"] in (
            RunState.DRAINING.value,
            RunState.STOPPED.value,
            RunState.EXPIRED.value,
        ) or (self.coop_root / "STOP.md").exists()

    def request_stop(
        self,
        *,
        run_id: str,
        requested_by: str,
        reason_code: str,
    ) -> str:
        run_id = _validated_uuid(run_id, "run_id_invalid")
        requested_by = _validated_token(requested_by, "stop_actor_invalid")
        reason_code = _validated_token(reason_code, "stop_reason_invalid")
        if reason_code not in _STOP_REASON_CODES:
            raise SupervisorError("stop_reason_invalid")
        stop_id = str(uuid.uuid4())
        now = self.clock()
        mirror_reason = reason_code
        mirror_requested_at = now
        with self._transaction() as connection:
            run = self._run_locked(connection, run_id)
            existing = connection.execute(
                "SELECT stop_id,reason_code,requested_at FROM stop_requests "
                "WHERE run_id=? ORDER BY requested_at DESC LIMIT 1",
                (run_id,),
            ).fetchone()
            if existing:
                stop_id = existing["stop_id"]
                mirror_reason = existing["reason_code"]
                mirror_requested_at = existing["requested_at"]
            else:
                if run["state"] in (RunState.STOPPED.value, RunState.EXPIRED.value):
                    raise SupervisorError("run_stopped")
                connection.execute(
                    "INSERT INTO stop_requests(stop_id,run_id,requested_by,reason_code,state,requested_at) "
                    "VALUES(?,?,?,?, 'requested', ?)",
                    (stop_id, run_id, requested_by, reason_code, now),
                )
                connection.execute(
                    "UPDATE runs SET state='draining', active_stop_id=?, stop_reason_code=?, "
                    "updated_at=?, row_version=row_version+1 WHERE run_id=?",
                    (stop_id, reason_code, now, run_id),
                )
                connection.execute(
                    "UPDATE tasks SET state='cancelled', failure_code='task_cancelled_by_stop', "
                    "finished_at=?, updated_at=? WHERE run_id=? AND state IN ('queued','claimed')",
                    (now, now, run_id),
                )
                self._event(
                    connection,
                    run_id,
                    "stop_requested",
                    entity_type="stop",
                    entity_id=stop_id,
                    actor_id=requested_by,
                    details={"reason_code": reason_code},
                    now=now,
                )
                self._complete_stop_if_drained_locked(connection, run_id, now)

        requested_at = datetime.fromtimestamp(
            mirror_requested_at, tz=UTC
        ).isoformat()
        mirror = (
            "schema: ccc.stop.v1\n"
            f"run_id: {run_id}\n"
            f"stop_id: {stop_id}\n"
            f"reason_code: {mirror_reason}\n"
            f"requested_at: {requested_at}\n"
        )
        try:
            atomic_write_text(self.coop_root / "STOP.md", mirror)
        except OSError as exc:
            raise SupervisorError("stop_mirror_failed") from exc
        return stop_id

    def recover(self, run_id: str) -> dict[str, int]:
        run_id = _validated_uuid(run_id, "run_id_invalid")
        now = self.clock()
        requeued = 0
        blocked = 0
        cancelled = 0
        released = 0
        with self._transaction() as connection:
            run = self._run_locked(connection, run_id)
            self._apply_legacy_stop_locked(connection, run, now)
            run = self._run_locked(connection, run_id)
            if (
                run["state"] in (RunState.ACTIVE.value, RunState.QUIET_WATCH.value)
                and now >= run["watch_expires_at"]
            ):
                cancelled += self._expire_run_locked(connection, run_id, now)
                run = self._run_locked(connection, run_id)
            elif run["state"] == RunState.EXPIRED.value:
                cancelled += self._expire_run_locked(connection, run_id, now)
            rows = connection.execute(
                "SELECT * FROM tasks WHERE run_id=? AND state IN ('claimed','running')",
                (run_id,),
            ).fetchall()
            for row in rows:
                healthy_lease = connection.execute(
                    "SELECT 1 FROM leases WHERE run_id=? AND agent_id=? "
                    "AND state='active' AND expires_at>? AND worker_session_id=? "
                    "AND fence_epoch=? AND current_task_id=?",
                    (
                        run_id,
                        row["target_agent"],
                        now,
                        row["claim_worker_session_id"],
                        row["claim_fence_epoch"],
                        row["task_id"],
                    ),
                ).fetchone()
                if (
                    healthy_lease
                    and run["state"]
                    in (RunState.ACTIVE.value, RunState.QUIET_WATCH.value)
                ):
                    if row["claim_expires_at"] <= now:
                        connection.execute(
                            "UPDATE tasks SET claim_expires_at=?, updated_at=? WHERE task_id=?",
                            (now + run["claim_ttl_seconds"], now, row["task_id"]),
                        )
                    continue
                safe_retry = row["effect_class"] in (
                    EffectClass.READ_ONLY.value,
                    EffectClass.REVERSIBLE.value,
                )
                if run["state"] in (
                    RunState.DRAINING.value,
                    RunState.STOPPED.value,
                    RunState.EXPIRED.value,
                ):
                    connection.execute(
                        "UPDATE tasks SET state='cancelled', finished_at=?, updated_at=?, "
                        "claim_token=NULL, claim_worker_session_id=NULL, "
                        "claim_fence_epoch=NULL, claim_expires_at=NULL, "
                        "failure_code='task_cancelled_by_run_state' WHERE task_id=?",
                        (now, now, row["task_id"]),
                    )
                    cancelled += 1
                    attempt_state = "cancelled"
                elif (
                    safe_retry
                    and row["attempt_count"] < row["max_attempts"]
                    and run["state"] in (RunState.ACTIVE.value, RunState.QUIET_WATCH.value)
                ):
                    connection.execute(
                        "UPDATE tasks SET state='queued', available_at=?, updated_at=?, "
                        "claim_token=NULL, claim_worker_session_id=NULL, "
                        "claim_fence_epoch=NULL, claim_expires_at=NULL, "
                        "failure_code='stale_worker_fenced' WHERE task_id=?",
                        (now, now, row["task_id"]),
                    )
                    requeued += 1
                    attempt_state = "fenced"
                else:
                    connection.execute(
                        "UPDATE tasks SET state='blocked', finished_at=?, updated_at=?, "
                        "failure_code='recovery_operator_required' WHERE task_id=?",
                        (now, now, row["task_id"]),
                    )
                    blocked += 1
                    attempt_state = "blocked"
                connection.execute(
                    "UPDATE task_attempts SET state=?, finished_at=?, "
                    "failure_code='stale_worker_fenced' WHERE task_id=? AND attempt_no=? "
                    "AND finished_at IS NULL",
                    (attempt_state, now, row["task_id"], row["attempt_count"]),
                )
            released = connection.execute(
                "UPDATE leases SET state='expired', release_reason='lease_expired', "
                "current_task_id=NULL "
                "WHERE run_id=? AND state='active' AND expires_at<=?",
                (run_id, now),
            ).rowcount
            connection.execute(
                "UPDATE participants SET state='idle', updated_at=? WHERE run_id=? "
                "AND NOT EXISTS (SELECT 1 FROM leases WHERE leases.run_id=participants.run_id "
                "AND leases.agent_id=participants.agent_id AND leases.state='active' "
                "AND leases.expires_at>?)",
                (now, run_id, now),
            )
            if blocked:
                connection.execute(
                    "UPDATE runs SET state='waiting_operator', updated_at=?, "
                    "row_version=row_version+1 WHERE run_id=? AND state IN ('active','quiet_watch')",
                    (now, run_id),
                )
            self._complete_stop_if_drained_locked(connection, run_id, now)
        return {
            "requeued": requeued,
            "blocked": blocked,
            "cancelled": cancelled,
            "released_leases": released,
        }

    def has_queued_task(self, run_id: str, agent_id: str) -> bool:
        now = self.clock()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT 1 FROM tasks WHERE run_id=? AND target_agent=? AND state='queued' "
                "AND available_at<=? LIMIT 1",
                (run_id, agent_id, now),
            ).fetchone()
        return bool(row)

    def safe_status(self, run_id: str | None = None) -> dict[str, Any]:
        self.initialize()
        run_id = run_id or self.latest_run_id()
        now = self.clock()
        with self._connect() as connection:
            run = self._run_locked(connection, run_id)
            task_counts = {
                row["state"]: row["count"]
                for row in connection.execute(
                    "SELECT state, COUNT(*) AS count FROM tasks WHERE run_id=? GROUP BY state",
                    (run_id,),
                )
            }
            wake_counts = {
                row["agent_id"]: row["count"]
                for row in connection.execute(
                    "SELECT agent_id, COUNT(*) AS count FROM wakes "
                    "WHERE run_id=? AND state='accepted' GROUP BY agent_id",
                    (run_id,),
                )
            }
            agents = {
                row["agent_id"]: {
                    "state": row["state"],
                    "conversation_bound": bool(row["conversation_id"]),
                    "consecutive_failures": row["consecutive_failures"],
                    "failure_present": row["last_failure_code"] is not None,
                    "last_failure_class": _failure_class(row["last_failure_code"]),
                }
                for row in connection.execute(
                    "SELECT agent_id,state,conversation_id,consecutive_failures,last_failure_code "
                    "FROM participants WHERE run_id=? ORDER BY agent_id",
                    (run_id,),
                )
            }
        return {
            "schema": "ccc.supervisor.status.v1",
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "generation": run["generation"],
            "project_ref": run["project_ref"],
            "state": run["state"],
            "watch_expired": now >= run["watch_expires_at"],
            "stop_present": (self.coop_root / "STOP.md").exists(),
            "task_counts": task_counts,
            "wake_counts": wake_counts,
            "agents": agents,
        }

    def nudge_allowed(self, run_id: str, agent_id: str, nudge_id: str) -> bool:
        run_id = _validated_uuid(run_id, "run_id_invalid")
        agent_id = _validated_agent(agent_id)
        nudge_id = _validated_uuid(nudge_id, "nudge_id_invalid")
        now = self.clock()
        with self._transaction() as connection:
            run = self._run_locked(connection, run_id)
            self._apply_legacy_stop_locked(connection, run, now)
            run = self._run_locked(connection, run_id)
            if (
                run["state"] in (RunState.ACTIVE.value, RunState.QUIET_WATCH.value)
                and now >= run["watch_expires_at"]
            ):
                self._expire_run_locked(connection, run_id, now)
                return False
            if (
                run["state"]
                not in (RunState.ACTIVE.value, RunState.QUIET_WATCH.value)
                or not run["ui_nudge_enabled"]
            ):
                return False
            participant = connection.execute(
                "SELECT * FROM participants WHERE run_id=? AND agent_id=?",
                (run_id, agent_id),
            ).fetchone()
            if not participant or participant["consecutive_failures"] < run["ui_nudge_after_failures"]:
                return False
            duplicate = connection.execute(
                "SELECT 1 FROM nudge_receipts WHERE run_id=? AND agent_id=? AND nudge_id=?",
                (run_id, agent_id, nudge_id),
            ).fetchone()
            if duplicate:
                return False
            if participant["last_nudge_at"] is not None and (
                now - participant["last_nudge_at"] < run["ui_nudge_cooldown_seconds"]
            ):
                return False
            connection.execute(
                "INSERT INTO nudge_receipts(run_id,agent_id,nudge_id,state,created_at) "
                "VALUES(?,?,?,'intent_recorded',?)",
                (run_id, agent_id, nudge_id, now),
            )
            connection.execute(
                "UPDATE participants SET last_nudge_at=? WHERE run_id=? AND agent_id=?",
                (now, run_id, agent_id),
            )
            return True

    def finish_nudge(
        self, run_id: str, agent_id: str, nudge_id: str, result_code: str
    ) -> None:
        result_code = _validated_token(result_code, "nudge_result_invalid")
        with self._transaction() as connection:
            updated = connection.execute(
                "UPDATE nudge_receipts SET state='completed', result_code=?, completed_at=? "
                "WHERE run_id=? AND agent_id=? AND nudge_id=? AND state='intent_recorded'",
                (result_code, self.clock(), run_id, agent_id, nudge_id),
            ).rowcount
            if not updated:
                raise SupervisorError("ui_nudge_duplicate")

    def reserve_claude_desktop_focus(self, run_id: str, focus_id: str) -> bool:
        """Reserve one explicit operator focus without authorizing UIA."""

        run_id = _validated_uuid(run_id, "run_id_invalid")
        focus_id = _validated_uuid(focus_id, "focus_id_invalid")
        now = self.clock()
        with self._transaction() as connection:
            run = self._run_locked(connection, run_id)
            self._apply_legacy_stop_locked(connection, run, now)
            run = self._run_locked(connection, run_id)
            if (
                run["state"] in (RunState.ACTIVE.value, RunState.QUIET_WATCH.value)
                and now >= run["watch_expires_at"]
            ):
                self._expire_run_locked(connection, run_id, now)
                return False
            if (
                run["state"]
                not in (RunState.ACTIVE.value, RunState.QUIET_WATCH.value)
                or not run["claude_desktop_focus_enabled"]
            ):
                return False
            participant = connection.execute(
                "SELECT * FROM participants WHERE run_id=? AND agent_id='claude'",
                (run_id,),
            ).fetchone()
            if not participant or not participant["enabled"]:
                return False
            duplicate = connection.execute(
                "SELECT 1 FROM claude_desktop_focus_receipts "
                "WHERE run_id=? AND agent_id='claude' AND focus_id=?",
                (run_id, focus_id),
            ).fetchone()
            if duplicate:
                return False
            if participant["last_claude_desktop_focus_at"] is not None and (
                now - participant["last_claude_desktop_focus_at"]
                < run["claude_desktop_focus_cooldown_seconds"]
            ):
                return False
            connection.execute(
                "INSERT INTO claude_desktop_focus_receipts("
                "run_id,agent_id,focus_id,state,created_at) "
                "VALUES(?,'claude',?,'intent_recorded',?)",
                (run_id, focus_id, now),
            )
            connection.execute(
                "UPDATE participants SET last_claude_desktop_focus_at=? "
                "WHERE run_id=? AND agent_id='claude'",
                (now, run_id),
            )
            return True

    def finish_claude_desktop_focus(
        self, run_id: str, focus_id: str, result_code: str
    ) -> None:
        run_id = _validated_uuid(run_id, "run_id_invalid")
        focus_id = _validated_uuid(focus_id, "focus_id_invalid")
        result_code = _validated_token(result_code, "focus_result_invalid")
        with self._transaction() as connection:
            updated = connection.execute(
                "UPDATE claude_desktop_focus_receipts "
                "SET state='completed', result_code=?, completed_at=? "
                "WHERE run_id=? AND agent_id='claude' AND focus_id=? "
                "AND state='intent_recorded'",
                (result_code, self.clock(), run_id, focus_id),
            ).rowcount
            if not updated:
                raise SupervisorError("claude_desktop_focus_duplicate")

    def _run_locked(self, connection: sqlite3.Connection, run_id: str) -> sqlite3.Row:
        row = connection.execute(
            "SELECT * FROM runs WHERE run_id=?", (run_id,)
        ).fetchone()
        if not row:
            raise SupervisorError("run_not_found")
        return row

    def _active_run_locked(
        self, connection: sqlite3.Connection, run_id: str, now: float
    ) -> sqlite3.Row:
        run = self._run_locked(connection, run_id)
        self._apply_legacy_stop_locked(connection, run, now)
        run = self._run_locked(connection, run_id)
        if run["state"] not in (
            RunState.ACTIVE.value,
            RunState.QUIET_WATCH.value,
        ):
            raise SupervisorError("run_not_active")
        if now >= run["watch_expires_at"]:
            self._expire_run_locked(connection, run_id, now)
            raise SupervisorError("watch_expired")
        return run

    def _expire_run_locked(
        self, connection: sqlite3.Connection, run_id: str, now: float
    ) -> int:
        connection.execute(
            "UPDATE runs SET state='expired', updated_at=?, row_version=row_version+1 "
            "WHERE run_id=? AND state IN ('active','quiet_watch')",
            (now, run_id),
        )
        return connection.execute(
            "UPDATE tasks SET state='cancelled', failure_code='watch_expired', "
            "finished_at=?, updated_at=? WHERE run_id=? AND state IN ('queued','claimed')",
            (now, now, run_id),
        ).rowcount

    def _apply_legacy_stop_locked(
        self, connection: sqlite3.Connection, run: sqlite3.Row, now: float
    ) -> None:
        if not (self.coop_root / "STOP.md").exists():
            return
        if run["state"] not in (
            RunState.ACTIVE.value,
            RunState.QUIET_WATCH.value,
            RunState.WAITING_OPERATOR.value,
        ):
            return
        stop_id = str(uuid.uuid4())
        connection.execute(
            "INSERT INTO stop_requests(stop_id,run_id,requested_by,reason_code,state,requested_at) "
            "VALUES(?,?, 'legacy_file', 'legacy_stop_file', 'requested', ?)",
            (stop_id, run["run_id"], now),
        )
        connection.execute(
            "UPDATE runs SET state='draining', active_stop_id=?, "
            "stop_reason_code='legacy_stop_file', updated_at=?, row_version=row_version+1 "
            "WHERE run_id=?",
            (stop_id, now, run["run_id"]),
        )
        connection.execute(
            "UPDATE tasks SET state='cancelled', failure_code='task_cancelled_by_stop', "
            "finished_at=?, updated_at=? WHERE run_id=? AND state IN ('queued','claimed')",
            (now, now, run["run_id"]),
        )
        self._complete_stop_if_drained_locked(connection, run["run_id"], now)

    def _assert_lease_locked(
        self,
        connection: sqlite3.Connection,
        lease: Lease,
        now: float,
        *,
        allow_expired: bool = False,
    ) -> None:
        row = connection.execute(
            "SELECT * FROM leases WHERE run_id=? AND agent_id=?",
            (lease.run_id, lease.agent_id),
        ).fetchone()
        if (
            not row
            or row["state"] != "active"
            or row["worker_session_id"] != lease.worker_session_id
            or row["lease_token"] != lease.lease_token
            or row["fence_epoch"] != lease.fence_epoch
            or (not allow_expired and row["expires_at"] <= now)
        ):
            raise SupervisorError("lease_fence_stale")

    def _complete_stop_if_drained_locked(
        self, connection: sqlite3.Connection, run_id: str, now: float
    ) -> None:
        run = self._run_locked(connection, run_id)
        if run["state"] != RunState.DRAINING.value:
            return
        connection.execute(
            "UPDATE tasks SET state='cancelled', failure_code='task_cancelled_by_stop', "
            "finished_at=?, updated_at=? WHERE run_id=? AND state IN ('queued','claimed')",
            (now, now, run_id),
        )
        connection.execute(
            "UPDATE leases SET state='expired', release_reason='lease_expired', "
            "current_task_id=NULL WHERE run_id=? AND state='active' AND expires_at<=?",
            (run_id, now),
        )
        active_tasks = connection.execute(
            "SELECT COUNT(*) FROM tasks WHERE run_id=? "
            "AND state IN ('queued','claimed','running')",
            (run_id,),
        ).fetchone()[0]
        active_leases = connection.execute(
            "SELECT COUNT(*) FROM leases WHERE run_id=? AND state='active' AND expires_at>?",
            (run_id, now),
        ).fetchone()[0]
        if active_tasks or active_leases:
            return
        connection.execute(
            "UPDATE runs SET state='stopped', updated_at=?, row_version=row_version+1 "
            "WHERE run_id=?",
            (now, run_id),
        )
        connection.execute(
            "UPDATE stop_requests SET state='completed', completed_at=? "
            "WHERE stop_id=?",
            (now, run["active_stop_id"]),
        )

    def _event(
        self,
        connection: sqlite3.Connection,
        run_id: str,
        event_type: str,
        *,
        entity_type: str,
        entity_id: str,
        now: float,
        actor_id: str = "supervisor",
        details: dict[str, str | int | float | bool] | None = None,
    ) -> None:
        safe_details = _validated_safe_details(details or {})
        connection.execute(
            "INSERT INTO events(event_id,run_id,event_type,entity_type,entity_id,"
            "actor_id,occurred_at,safe_detail_json) VALUES(?,?,?,?,?,?,?,?)",
            (
                str(uuid.uuid4()),
                run_id,
                _validated_token(event_type, "event_type_invalid"),
                _validated_token(entity_type, "entity_type_invalid"),
                entity_id,
                actor_id,
                now,
                json.dumps(safe_details, sort_keys=True, separators=(",", ":")),
            ),
        )


def _validated_uuid(value: str, code: str) -> str:
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError, TypeError) as exc:
        raise SupervisorError(code) from exc
    return str(parsed)


def _validated_token(value: str, code: str) -> str:
    if not isinstance(value, str) or not _TOKEN_RE.fullmatch(value):
        raise SupervisorError(code)
    return value


def _validated_agent(value: str) -> str:
    if value not in AGENT_IDS:
        raise SupervisorError("agent_id_invalid")
    return value


def _failure_class(value: str | None) -> str:
    if value is None:
        return "none"
    if value.startswith(("claude_", "codex_", "adapter_", "ui_nudge_")):
        return "adapter"
    if value.startswith(("lease_", "stale_worker_")):
        return "lease"
    if value.startswith(("task_", "handoff_", "idempotency_", "recovery_")):
        return "lifecycle"
    if value.startswith(("stop_", "watch_", "run_")):
        return "run"
    return "other"


def _validated_safe_details(
    details: dict[str, str | int | float | bool],
) -> dict[str, str | int | float | bool]:
    safe: dict[str, str | int | float | bool] = {}
    for key, value in details.items():
        if not _SAFE_EVENT_KEY_RE.fullmatch(key):
            raise SupervisorError("unsafe_event_detail")
        if isinstance(value, str):
            if not _SAFE_EVENT_VALUE_RE.fullmatch(value):
                raise SupervisorError("unsafe_event_detail")
        elif not isinstance(value, (bool, int, float)):
            raise SupervisorError("unsafe_event_detail")
        safe[key] = value
    return safe


_SCHEMA = """
CREATE TABLE IF NOT EXISTS meta(
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS runs(
    run_id TEXT PRIMARY KEY,
    generation INTEGER NOT NULL,
    project_alias TEXT NOT NULL,
    project_ref TEXT NOT NULL,
    state TEXT NOT NULL CHECK(state IN (
        'active','quiet_watch','draining','waiting_operator','stopped','expired'
    )),
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    watch_expires_at REAL NOT NULL,
    lease_ttl_seconds INTEGER NOT NULL,
    claim_ttl_seconds INTEGER NOT NULL,
    max_wakes_per_agent INTEGER NOT NULL,
    max_handoff_depth INTEGER NOT NULL,
    max_handoffs_per_result INTEGER NOT NULL,
    max_payload_bytes INTEGER NOT NULL,
    max_output_bytes INTEGER NOT NULL,
    auto_wake_allowed INTEGER NOT NULL CHECK(auto_wake_allowed IN (0,1)),
    ui_nudge_enabled INTEGER NOT NULL CHECK(ui_nudge_enabled IN (0,1)),
    ui_nudge_after_failures INTEGER NOT NULL,
    ui_nudge_cooldown_seconds INTEGER NOT NULL,
    claude_desktop_focus_enabled INTEGER NOT NULL
        CHECK(claude_desktop_focus_enabled IN (0,1)),
    claude_desktop_focus_cooldown_seconds INTEGER NOT NULL,
    active_stop_id TEXT,
    stop_reason_code TEXT,
    row_version INTEGER NOT NULL DEFAULT 0
);

CREATE UNIQUE INDEX IF NOT EXISTS one_nonterminal_run_per_root
ON runs((1))
WHERE state IN ('active','quiet_watch','draining','waiting_operator');

CREATE TABLE IF NOT EXISTS participants(
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    agent_id TEXT NOT NULL CHECK(agent_id IN ('claude','codex')),
    enabled INTEGER NOT NULL CHECK(enabled IN (0,1)),
    state TEXT NOT NULL,
    conversation_id TEXT,
    consecutive_failures INTEGER NOT NULL DEFAULT 0,
    last_failure_code TEXT,
    last_nudge_at REAL,
    last_claude_desktop_focus_at REAL,
    updated_at REAL,
    PRIMARY KEY(run_id, agent_id)
);

CREATE TABLE IF NOT EXISTS leases(
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    agent_id TEXT NOT NULL,
    worker_session_id TEXT NOT NULL,
    lease_token TEXT NOT NULL,
    fence_epoch INTEGER NOT NULL,
    state TEXT NOT NULL CHECK(state IN ('active','released','expired')),
    acquired_at REAL NOT NULL,
    renewed_at REAL NOT NULL,
    expires_at REAL NOT NULL,
    heartbeat_seq INTEGER NOT NULL DEFAULT 0,
    current_task_id TEXT,
    release_reason TEXT,
    PRIMARY KEY(run_id, agent_id),
    FOREIGN KEY(run_id, agent_id) REFERENCES participants(run_id, agent_id)
);

CREATE TABLE IF NOT EXISTS wakes(
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    agent_id TEXT NOT NULL,
    wake_id TEXT NOT NULL,
    source TEXT NOT NULL,
    state TEXT NOT NULL CHECK(state IN ('accepted','suppressed')),
    failure_code TEXT,
    result_code TEXT,
    received_at REAL NOT NULL,
    completed_at REAL,
    PRIMARY KEY(run_id, agent_id, wake_id)
);

CREATE TABLE IF NOT EXISTS tasks(
    task_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    target_agent TEXT NOT NULL CHECK(target_agent IN ('claude','codex')),
    kind TEXT NOT NULL,
    effect_class TEXT NOT NULL CHECK(effect_class IN (
        'read_only','reversible','mutating','external'
    )),
    state TEXT NOT NULL CHECK(state IN (
        'queued','claimed','running','succeeded','blocked','dead_letter','cancelled'
    )),
    idempotency_key TEXT NOT NULL,
    payload_ref TEXT NOT NULL,
    payload_sha256 TEXT NOT NULL,
    result_ref TEXT,
    result_sha256 TEXT,
    failure_code TEXT,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    available_at REAL NOT NULL,
    claimed_at REAL,
    started_at REAL,
    finished_at REAL,
    claim_token TEXT,
    claim_worker_session_id TEXT,
    claim_fence_epoch INTEGER,
    claim_expires_at REAL,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL,
    depth INTEGER NOT NULL DEFAULT 0,
    correlation_id TEXT NOT NULL,
    parent_task_id TEXT REFERENCES tasks(task_id),
    UNIQUE(run_id, idempotency_key)
);

CREATE TABLE IF NOT EXISTS task_attempts(
    task_id TEXT NOT NULL REFERENCES tasks(task_id),
    attempt_no INTEGER NOT NULL,
    worker_session_id TEXT NOT NULL,
    fence_epoch INTEGER NOT NULL,
    started_at REAL NOT NULL,
    finished_at REAL,
    state TEXT NOT NULL,
    failure_code TEXT,
    PRIMARY KEY(task_id, attempt_no)
);

CREATE TABLE IF NOT EXISTS stop_requests(
    stop_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    requested_by TEXT NOT NULL,
    reason_code TEXT NOT NULL,
    state TEXT NOT NULL CHECK(state IN ('requested','draining','completed')),
    requested_at REAL NOT NULL,
    completed_at REAL
);

CREATE TABLE IF NOT EXISTS nudge_receipts(
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    agent_id TEXT NOT NULL,
    nudge_id TEXT NOT NULL,
    state TEXT NOT NULL,
    result_code TEXT,
    created_at REAL NOT NULL,
    completed_at REAL,
    PRIMARY KEY(run_id, agent_id, nudge_id)
);

CREATE TABLE IF NOT EXISTS claude_desktop_focus_receipts(
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    agent_id TEXT NOT NULL CHECK(agent_id='claude'),
    focus_id TEXT NOT NULL,
    state TEXT NOT NULL,
    result_code TEXT,
    created_at REAL NOT NULL,
    completed_at REAL,
    PRIMARY KEY(run_id, agent_id, focus_id)
);

CREATE TABLE IF NOT EXISTS events(
    seq INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL UNIQUE,
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    event_type TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    occurred_at REAL NOT NULL,
    safe_detail_json TEXT NOT NULL
);
"""
