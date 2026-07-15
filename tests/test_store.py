from __future__ import annotations

import json
import tempfile
import unittest
import uuid
from pathlib import Path

from cccp_supervisor.errors import SupervisorError
from cccp_supervisor.models import (
    AdapterResult,
    AdapterStatus,
    EffectClass,
    Handoff,
    RunPolicy,
)
from cccp_supervisor.store import StateStore


class FakeClock:
    def __init__(self, value: float = 1_000.0) -> None:
        self.value = value

    def __call__(self) -> float:
        return self.value

    def advance(self, seconds: float) -> None:
        self.value += seconds


class StoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.coop = Path(self.temp.name) / "coop"
        self.coop.mkdir()
        self.clock = FakeClock()
        self.store = StateStore(self.coop, clock=self.clock)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def init(self, **policy_values: object) -> str:
        policy = RunPolicy(**policy_values)
        return self.store.init_run(project_alias="fixture", policy=policy)

    def enqueue(
        self,
        run_id: str,
        *,
        key: str = "root",
        effect: EffectClass = EffectClass.READ_ONLY,
        payload: str = "work",
        target: str = "claude",
    ):
        return self.store.enqueue_task(
            run_id=run_id,
            target_agent=target,
            payload=payload,
            idempotency_key=key,
            effect_class=effect,
        )[0]

    def lease_and_start(self, run_id: str, *, agent: str = "claude"):
        lease = self.store.acquire_lease(
            run_id=run_id,
            agent_id=agent,
            worker_session_id=str(uuid.uuid4()),
        )
        task = self.store.claim_next_task(lease)
        self.assertIsNotNone(task)
        return lease, self.store.start_task(lease, task)

    def test_enqueue_is_idempotent_and_conflicts_fail_closed(self) -> None:
        run_id = self.init()
        first, created = self.store.enqueue_task(
            run_id=run_id,
            target_agent="claude",
            payload="same",
            idempotency_key="stable-key",
        )
        second, created_again = self.store.enqueue_task(
            run_id=run_id,
            target_agent="claude",
            payload="same",
            idempotency_key="stable-key",
        )
        self.assertTrue(created)
        self.assertFalse(created_again)
        self.assertEqual(first.task_id, second.task_id)
        with self.assertRaisesRegex(SupervisorError, "idempotency_conflict"):
            self.store.enqueue_task(
                run_id=run_id,
                target_agent="claude",
                payload="different",
                idempotency_key="stable-key",
            )

    def test_duplicate_wake_has_one_receipt(self) -> None:
        run_id = self.init()
        wake_id = str(uuid.uuid4())
        self.assertEqual(
            "accepted",
            self.store.begin_wake(
                run_id=run_id, agent_id="claude", wake_id=wake_id
            ),
        )
        self.assertEqual(
            "duplicate",
            self.store.begin_wake(
                run_id=run_id, agent_id="claude", wake_id=wake_id
            ),
        )
        with self.store._connect() as connection:
            count = connection.execute("SELECT COUNT(*) FROM wakes").fetchone()[0]
        self.assertEqual(1, count)

    def test_expired_lease_is_fenced_by_new_epoch(self) -> None:
        run_id = self.init(lease_ttl_seconds=2)
        old = self.store.acquire_lease(
            run_id=run_id,
            agent_id="claude",
            worker_session_id=str(uuid.uuid4()),
        )
        self.clock.advance(3)
        new = self.store.acquire_lease(
            run_id=run_id,
            agent_id="claude",
            worker_session_id=str(uuid.uuid4()),
        )
        self.assertGreater(new.fence_epoch, old.fence_epoch)
        with self.assertRaisesRegex(SupervisorError, "lease_fence_stale"):
            self.store.renew_lease(old)

    def test_recovery_requeues_only_retry_safe_work(self) -> None:
        for effect, expected in (
            (EffectClass.READ_ONLY, "requeued"),
            (EffectClass.MUTATING, "blocked"),
        ):
            with self.subTest(effect=effect):
                with tempfile.TemporaryDirectory() as directory:
                    coop = Path(directory) / "coop"
                    coop.mkdir()
                    clock = FakeClock()
                    store = StateStore(coop, clock=clock)
                    run_id = store.init_run(
                        project_alias="recovery",
                        policy=RunPolicy(
                            lease_ttl_seconds=2, claim_ttl_seconds=2
                        ),
                    )
                    store.enqueue_task(
                        run_id=run_id,
                        target_agent="claude",
                        payload="work",
                        idempotency_key="root",
                        effect_class=effect,
                    )
                    lease = store.acquire_lease(
                        run_id=run_id,
                        agent_id="claude",
                        worker_session_id=str(uuid.uuid4()),
                    )
                    task = store.claim_next_task(lease)
                    store.start_task(lease, task)
                    clock.advance(3)
                    counts = store.recover(run_id)
                    self.assertEqual(1, counts[expected])
                    state = store.safe_status(run_id)["task_counts"]
                    self.assertEqual(1, state["queued" if expected == "requeued" else "blocked"])
                    with store._connect() as connection:
                        attempt = connection.execute(
                            "SELECT state,finished_at FROM task_attempts"
                        ).fetchone()
                        participant = connection.execute(
                            "SELECT state FROM participants WHERE agent_id='claude'"
                        ).fetchone()
                    self.assertIsNotNone(attempt["finished_at"])
                    self.assertNotEqual("running", attempt["state"])
                    self.assertEqual("idle", participant["state"])

    def test_stop_is_monotonic_and_cancels_unstarted_work(self) -> None:
        run_id = self.init()
        self.enqueue(run_id)
        stop_id = self.store.request_stop(
            run_id=run_id,
            requested_by="operator",
            reason_code="operator_stop",
        )
        self.assertTrue(stop_id)
        status = self.store.safe_status(run_id)
        self.assertEqual("stopped", status["state"])
        self.assertEqual(1, status["task_counts"]["cancelled"])
        self.assertTrue((self.coop / "STOP.md").exists())
        self.assertEqual(
            stop_id,
            self.store.request_stop(
                run_id=run_id,
                requested_by="operator",
                reason_code="operator_stop",
            ),
        )
        with self.assertRaisesRegex(SupervisorError, "run_not_active"):
            self.enqueue(run_id, key="late")
        with self.assertRaisesRegex(SupervisorError, "stale_stop_file"):
            self.store.init_run(project_alias="another")

    def test_running_work_drains_before_stop_completes(self) -> None:
        run_id = self.init()
        self.enqueue(run_id)
        lease, task = self.lease_and_start(run_id)
        self.store.request_stop(
            run_id=run_id,
            requested_by="operator",
            reason_code="operator_stop",
        )
        self.assertEqual("draining", self.store.safe_status(run_id)["state"])
        self.store.finish_task(
            lease=lease,
            task=task,
            result=AdapterResult(
                AdapterStatus.CANCELLED,
                "cancelled",
                failure_code="task_cancelled_by_stop",
            ),
        )
        self.store.release_lease(lease)
        self.assertEqual("stopped", self.store.safe_status(run_id)["state"])

    def test_handoffs_are_committed_with_parent_result(self) -> None:
        run_id = self.init()
        self.enqueue(run_id)
        lease, task = self.lease_and_start(run_id)
        state = self.store.finish_task(
            lease=lease,
            task=task,
            result=AdapterResult(
                AdapterStatus.SUCCEEDED,
                "done",
                handoffs=(Handoff("codex", "next", "child-key"),),
            ),
        )
        self.assertEqual("succeeded", state)
        counts = self.store.safe_status(run_id)["task_counts"]
        self.assertEqual({"queued": 1, "succeeded": 1}, counts)
        with self.store._connect() as connection:
            child = connection.execute(
                "SELECT * FROM tasks WHERE idempotency_key='child-key'"
            ).fetchone()
        self.assertEqual(task.task_id, child["parent_task_id"])
        self.assertEqual(task.correlation_id, child["correlation_id"])

    def test_stop_race_overrides_success_and_discards_handoff(self) -> None:
        run_id = self.init()
        self.enqueue(run_id)
        lease, task = self.lease_and_start(run_id)
        self.store.request_stop(
            run_id=run_id,
            requested_by="operator",
            reason_code="race_stop",
        )
        state = self.store.finish_task(
            lease=lease,
            task=task,
            result=AdapterResult(
                AdapterStatus.SUCCEEDED,
                "late success",
                handoffs=(Handoff("codex", "must not run", "late-child"),),
            ),
        )
        self.assertEqual("cancelled", state)
        self.store.release_lease(lease)
        status = self.store.safe_status(run_id)
        self.assertEqual("stopped", status["state"])
        self.assertEqual({"cancelled": 1}, status["task_counts"])

    def test_stale_finalize_cannot_overwrite_authoritative_result(self) -> None:
        run_id = self.init()
        self.enqueue(run_id)
        lease, task = self.lease_and_start(run_id)
        self.store.finish_task(
            lease=lease,
            task=task,
            result=AdapterResult(AdapterStatus.SUCCEEDED, "authoritative"),
        )
        with self.store._connect() as connection:
            row = connection.execute(
                "SELECT result_ref,result_sha256 FROM tasks WHERE task_id=?",
                (task.task_id,),
            ).fetchone()
        result_path = self.store.state_root / row["result_ref"]
        original = result_path.read_bytes()
        with self.assertRaisesRegex(SupervisorError, "task_fence_stale"):
            self.store.finish_task(
                lease=lease,
                task=task,
                result=AdapterResult(AdapterStatus.SUCCEEDED, "overwrite"),
            )
        self.assertEqual(original, result_path.read_bytes())

    def test_healthy_lease_prevents_claim_ttl_recovery(self) -> None:
        run_id = self.init(lease_ttl_seconds=100, claim_ttl_seconds=2)
        self.enqueue(run_id)
        lease, task = self.lease_and_start(run_id)
        self.clock.advance(3)
        counts = self.store.recover(run_id)
        self.assertEqual(0, counts["requeued"])
        with self.store._connect() as connection:
            row = connection.execute(
                "SELECT state,claim_expires_at FROM tasks WHERE task_id=?",
                (task.task_id,),
            ).fetchone()
            attempt = connection.execute(
                "SELECT state,finished_at FROM task_attempts WHERE task_id=?",
                (task.task_id,),
            ).fetchone()
        self.assertEqual("running", row["state"])
        self.assertGreater(row["claim_expires_at"], self.clock())
        self.assertEqual("running", attempt["state"])
        self.assertIsNone(attempt["finished_at"])
        self.store.renew_lease(lease)

    def test_expired_lease_recovers_before_long_claim_ttl(self) -> None:
        run_id = self.init(lease_ttl_seconds=2, claim_ttl_seconds=100)
        self.enqueue(run_id)
        self.lease_and_start(run_id)
        self.clock.advance(3)
        counts = self.store.recover(run_id)
        self.assertEqual(1, counts["requeued"])
        self.assertEqual(1, counts["released_leases"])
        self.assertEqual(1, self.store.safe_status(run_id)["task_counts"]["queued"])

    def test_waiting_operator_is_a_mechanical_claim_hold(self) -> None:
        run_id = self.init()
        self.enqueue(run_id, key="first")
        self.enqueue(run_id, key="second", target="codex")
        lease, task = self.lease_and_start(run_id)
        self.store.finish_task(
            lease=lease,
            task=task,
            result=AdapterResult(
                AdapterStatus.BLOCKED,
                "operator needed",
                failure_code="operator_required",
            ),
        )
        self.store.release_lease(lease)
        self.assertEqual("waiting_operator", self.store.safe_status(run_id)["state"])
        with self.assertRaisesRegex(SupervisorError, "run_not_active"):
            self.store.acquire_lease(
                run_id=run_id,
                agent_id="codex",
                worker_session_id=str(uuid.uuid4()),
            )

    def test_idempotency_includes_parent_lineage(self) -> None:
        run_id = self.init()
        root = self.enqueue(run_id, key="shared", payload="same")
        parent = self.enqueue(run_id, key="parent")
        with self.assertRaisesRegex(SupervisorError, "idempotency_conflict"):
            self.store.enqueue_task(
                run_id=run_id,
                target_agent="claude",
                payload="same",
                idempotency_key="shared",
                parent_task_id=parent.task_id,
            )
        self.assertIsNotNone(root)

    def test_incomplete_wake_can_be_replayed_after_lease_ttl(self) -> None:
        run_id = self.init(lease_ttl_seconds=2)
        wake_id = str(uuid.uuid4())
        self.assertEqual(
            "accepted",
            self.store.begin_wake(
                run_id=run_id, agent_id="claude", wake_id=wake_id
            ),
        )
        self.assertEqual(
            "duplicate",
            self.store.begin_wake(
                run_id=run_id, agent_id="claude", wake_id=wake_id
            ),
        )
        self.clock.advance(3)
        self.assertEqual(
            "accepted",
            self.store.begin_wake(
                run_id=run_id, agent_id="claude", wake_id=wake_id
            ),
        )
        self.store.end_wake(
            run_id=run_id,
            agent_id="claude",
            wake_id=wake_id,
            result_code="recovered",
        )
        self.assertEqual(1, self.store.safe_status(run_id)["wake_counts"]["claude"])

    def test_idle_recovery_enforces_watch_expiry(self) -> None:
        run_id = self.init(watch_ttl_seconds=2)
        self.clock.advance(3)
        self.store.recover(run_id)
        self.assertEqual("expired", self.store.safe_status(run_id)["state"])

    def test_wake_observed_expiry_cancels_queued_work_idempotently(self) -> None:
        run_id = self.init(watch_ttl_seconds=2)
        self.enqueue(run_id)
        self.clock.advance(3)
        state = self.store.begin_wake(
            run_id=run_id,
            agent_id="claude",
            wake_id=str(uuid.uuid4()),
        )
        self.assertEqual("suppressed", state)
        self.assertEqual(
            {"cancelled": 1}, self.store.safe_status(run_id)["task_counts"]
        )
        self.store.recover(run_id)
        self.assertEqual(
            {"cancelled": 1}, self.store.safe_status(run_id)["task_counts"]
        )

    def test_watch_expiry_blocks_ui_nudge_and_expires_run(self) -> None:
        run_id = self.init(watch_ttl_seconds=2, ui_nudge_enabled=True)
        with self.store._transaction() as connection:
            connection.execute(
                "UPDATE participants SET consecutive_failures=3 "
                "WHERE run_id=? AND agent_id='claude'",
                (run_id,),
            )
        self.clock.advance(3)
        self.assertFalse(
            self.store.nudge_allowed(run_id, "claude", str(uuid.uuid4()))
        )
        self.assertEqual("expired", self.store.safe_status(run_id)["state"])
        with self.store._connect() as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM nudge_receipts WHERE run_id=?", (run_id,)
            ).fetchone()[0]
        self.assertEqual(0, count)

    def test_coop_root_allows_only_one_nonterminal_run(self) -> None:
        first = self.store.init_run(project_alias="first")
        with self.assertRaisesRegex(SupervisorError, "run_already_active"):
            self.store.init_run(project_alias="second")
        self.store.request_stop(
            run_id=first,
            requested_by="operator",
            reason_code="operator_stop",
        )
        (self.coop / "STOP.md").unlink()
        second = self.store.init_run(project_alias="second")
        self.assertNotEqual(first, second)

    def test_stopped_run_cannot_authorize_ui_nudge(self) -> None:
        run_id = self.init(ui_nudge_enabled=True)
        with self.store._transaction() as connection:
            connection.execute(
                "UPDATE participants SET consecutive_failures=3 "
                "WHERE run_id=? AND agent_id='claude'",
                (run_id,),
            )
        self.store.request_stop(
            run_id=run_id,
            requested_by="operator",
            reason_code="stop_before_nudge",
        )
        self.assertFalse(
            self.store.nudge_allowed(run_id, "claude", str(uuid.uuid4()))
        )

    def test_legacy_stop_applies_during_operator_hold(self) -> None:
        run_id = self.init()
        with self.store._transaction() as connection:
            connection.execute(
                "UPDATE runs SET state='waiting_operator' WHERE run_id=?", (run_id,)
            )
        (self.coop / "STOP.md").write_text("legacy stop", encoding="utf-8")
        self.store.recover(run_id)
        self.assertEqual("stopped", self.store.safe_status(run_id)["state"])

    def test_safe_status_scrubs_alias_and_arbitrary_failure_code(self) -> None:
        run_id = self.store.init_run(project_alias="Secret_Project")
        with self.store._transaction() as connection:
            connection.execute(
                "UPDATE participants SET last_failure_code='sk-SYNTHETICSECRET' "
                "WHERE run_id=? AND agent_id='claude'",
                (run_id,),
            )
        rendered = json.dumps(self.store.safe_status(run_id), sort_keys=True)
        self.assertNotIn("Secret_Project", rendered)
        self.assertNotIn("SYNTHETICSECRET", rendered)
        self.assertIn("project_ref", rendered)
        self.assertIn("failure_present", rendered)

    def test_handoff_conflict_rolls_back_parent_completion(self) -> None:
        run_id = self.init()
        self.enqueue(run_id, key="root")
        self.enqueue(run_id, key="child-key", payload="old", target="codex")
        lease, task = self.lease_and_start(run_id)
        with self.assertRaisesRegex(SupervisorError, "idempotency_conflict"):
            self.store.finish_task(
                lease=lease,
                task=task,
                result=AdapterResult(
                    AdapterStatus.SUCCEEDED,
                    "done",
                    handoffs=(Handoff("codex", "different", "child-key"),),
                ),
            )
        with self.store._connect() as connection:
            state = connection.execute(
                "SELECT state FROM tasks WHERE task_id=?", (task.task_id,)
            ).fetchone()[0]
        self.assertEqual("running", state)

    def test_output_budget_and_nudge_receipt_ordering(self) -> None:
        run_id = self.init(max_output_bytes=128, ui_nudge_enabled=True)
        self.enqueue(run_id)
        lease, task = self.lease_and_start(run_id)
        with self.assertRaisesRegex(SupervisorError, "result_too_large"):
            self.store.finish_task(
                lease=lease,
                task=task,
                result=AdapterResult(AdapterStatus.SUCCEEDED, "x" * 500),
            )
        with self.store._transaction() as connection:
            connection.execute(
                "UPDATE participants SET consecutive_failures=2 "
                "WHERE run_id=? AND agent_id='claude'",
                (run_id,),
            )
        nudge_id = str(uuid.uuid4())
        self.assertTrue(self.store.nudge_allowed(run_id, "claude", nudge_id))
        self.store.finish_nudge(run_id, "claude", nudge_id, "notified")
        with self.store._connect() as connection:
            row = connection.execute("SELECT * FROM nudge_receipts").fetchone()
        self.assertEqual("notified", row["result_code"])
        self.assertEqual(self.clock(), row["completed_at"])

    def test_safe_status_does_not_relay_payload_text(self) -> None:
        run_id = self.init()
        secretish = "snippet https://example.invalid C:/private/paper.pdf"
        self.enqueue(run_id, payload=secretish)
        serialized = json.dumps(self.store.safe_status(run_id), sort_keys=True)
        self.assertNotIn("snippet", serialized)
        self.assertNotIn("example.invalid", serialized)
        self.assertNotIn("private", serialized)


if __name__ == "__main__":
    unittest.main()
