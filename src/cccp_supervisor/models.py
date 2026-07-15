from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class RunState(StrEnum):
    ACTIVE = "active"
    QUIET_WATCH = "quiet_watch"
    DRAINING = "draining"
    WAITING_OPERATOR = "waiting_operator"
    STOPPED = "stopped"
    EXPIRED = "expired"


class TaskState(StrEnum):
    QUEUED = "queued"
    CLAIMED = "claimed"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    BLOCKED = "blocked"
    DEAD_LETTER = "dead_letter"
    CANCELLED = "cancelled"


class EffectClass(StrEnum):
    READ_ONLY = "read_only"
    REVERSIBLE = "reversible"
    MUTATING = "mutating"
    EXTERNAL = "external"


class AdapterStatus(StrEnum):
    SUCCEEDED = "succeeded"
    BLOCKED = "blocked"
    FAILED = "failed"
    CANCELLED = "cancelled"


AGENT_IDS = ("claude", "codex")
TERMINAL_TASK_STATES = {
    TaskState.SUCCEEDED.value,
    TaskState.BLOCKED.value,
    TaskState.DEAD_LETTER.value,
    TaskState.CANCELLED.value,
}
NONTERMINAL_RUN_STATES = {
    RunState.ACTIVE.value,
    RunState.QUIET_WATCH.value,
    RunState.DRAINING.value,
    RunState.WAITING_OPERATOR.value,
}


@dataclass(frozen=True)
class RunPolicy:
    lease_ttl_seconds: int = 120
    claim_ttl_seconds: int = 1_200
    watch_ttl_seconds: int = 86_400
    max_wakes_per_agent: int = 100
    max_handoff_depth: int = 8
    max_handoffs_per_result: int = 4
    max_payload_bytes: int = 262_144
    max_output_bytes: int = 1_048_576
    auto_wake_allowed: bool = False
    ui_nudge_enabled: bool = False
    ui_nudge_after_failures: int = 2
    ui_nudge_cooldown_seconds: int = 600
    claude_desktop_focus_enabled: bool = False
    claude_desktop_focus_cooldown_seconds: int = 600

    def validate(self) -> None:
        positive = {
            "lease_ttl_seconds": self.lease_ttl_seconds,
            "claim_ttl_seconds": self.claim_ttl_seconds,
            "watch_ttl_seconds": self.watch_ttl_seconds,
            "max_wakes_per_agent": self.max_wakes_per_agent,
            "max_handoff_depth": self.max_handoff_depth,
            "max_handoffs_per_result": self.max_handoffs_per_result,
            "max_payload_bytes": self.max_payload_bytes,
            "max_output_bytes": self.max_output_bytes,
            "ui_nudge_after_failures": self.ui_nudge_after_failures,
            "ui_nudge_cooldown_seconds": self.ui_nudge_cooldown_seconds,
            "claude_desktop_focus_cooldown_seconds": (
                self.claude_desktop_focus_cooldown_seconds
            ),
        }
        if any(value <= 0 for value in positive.values()):
            raise ValueError("run policy values must be positive")
        limits = {
            "lease_ttl_seconds": 3_600,
            "claim_ttl_seconds": 86_400,
            "watch_ttl_seconds": 2_592_000,
            "max_wakes_per_agent": 10_000,
            "max_handoff_depth": 64,
            "max_handoffs_per_result": 64,
            "max_payload_bytes": 16 * 1024 * 1024,
            "max_output_bytes": 16 * 1024 * 1024,
            "ui_nudge_after_failures": 100,
            "ui_nudge_cooldown_seconds": 86_400,
            "claude_desktop_focus_cooldown_seconds": 86_400,
        }
        if any(positive[name] > maximum for name, maximum in limits.items()):
            raise ValueError("run policy value exceeds hard limit")


@dataclass(frozen=True)
class Lease:
    run_id: str
    agent_id: str
    worker_session_id: str
    lease_token: str
    fence_epoch: int
    expires_at: float


@dataclass(frozen=True)
class TaskRecord:
    task_id: str
    run_id: str
    target_agent: str
    kind: str
    effect_class: EffectClass
    state: TaskState
    idempotency_key: str
    payload_ref: str
    payload_sha256: str
    attempt_count: int
    max_attempts: int
    depth: int
    correlation_id: str
    parent_task_id: str | None = None
    claim_token: str | None = None


@dataclass(frozen=True)
class Handoff:
    target_agent: str
    payload: str
    idempotency_key: str
    effect_class: EffectClass = EffectClass.READ_ONLY
    kind: str = "task"


@dataclass(frozen=True)
class AdapterResult:
    status: AdapterStatus
    summary: str
    failure_code: str | None = None
    retryable: bool = False
    conversation_id: str | None = None
    handoffs: tuple[Handoff, ...] = field(default_factory=tuple)
    safe_metrics: dict[str, int | bool | str] = field(default_factory=dict)


@dataclass(frozen=True)
class DispatchResult:
    status: str
    run_id: str
    agent_id: str
    wake_id: str
    task_id: str | None = None
    failure_code: str | None = None
    handoff_count: int = 0


def task_from_row(row: Any) -> TaskRecord:
    return TaskRecord(
        task_id=row["task_id"],
        run_id=row["run_id"],
        target_agent=row["target_agent"],
        kind=row["kind"],
        effect_class=EffectClass(row["effect_class"]),
        state=TaskState(row["state"]),
        idempotency_key=row["idempotency_key"],
        payload_ref=row["payload_ref"],
        payload_sha256=row["payload_sha256"],
        attempt_count=row["attempt_count"],
        max_attempts=row["max_attempts"],
        depth=row["depth"],
        correlation_id=row["correlation_id"],
        parent_task_id=row["parent_task_id"],
        claim_token=row["claim_token"],
    )
