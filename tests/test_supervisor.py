from __future__ import annotations

import tempfile
import unittest
import uuid
from pathlib import Path

from cccp_supervisor.models import (
    AdapterResult,
    AdapterStatus,
    EffectClass,
    Handoff,
    RunPolicy,
)
from cccp_supervisor.store import StateStore
from cccp_supervisor.supervisor import Supervisor


class Clock:
    def __init__(self) -> None:
        self.value = 5_000.0

    def __call__(self) -> float:
        return self.value

    def advance(self, seconds: float) -> None:
        self.value += seconds


class SequenceAdapter:
    def __init__(self, *results: AdapterResult) -> None:
        self.results = list(results)
        self.calls = 0
        self.payloads: list[str] = []

    def run(self, **kwargs) -> AdapterResult:
        self.calls += 1
        self.payloads.append(kwargs["payload"])
        return self.results.pop(0)


class SupervisorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.coop = Path(self.temp.name) / "coop"
        self.coop.mkdir()
        self.clock = Clock()
        self.store = StateStore(self.coop, clock=self.clock)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_with_task(
        self,
        adapter,
        *,
        effect: EffectClass = EffectClass.READ_ONLY,
        policy: RunPolicy | None = None,
    ):
        run_id = self.store.init_run(
            project_alias="fixture", policy=policy or RunPolicy()
        )
        task, _ = self.store.enqueue_task(
            run_id=run_id,
            target_agent="claude",
            payload="payload",
            idempotency_key="root",
            effect_class=effect,
        )
        supervisor = Supervisor(self.store, {"claude": adapter})
        return run_id, task, supervisor

    def test_duplicate_wake_does_not_execute_twice(self) -> None:
        adapter = SequenceAdapter(AdapterResult(AdapterStatus.SUCCEEDED, "ok"))
        run_id, task, supervisor = self.run_with_task(adapter)
        wake_id = str(uuid.uuid4())
        first = supervisor.run_once(
            run_id=run_id, agent_id="claude", wake_id=wake_id
        )
        second = supervisor.run_once(
            run_id=run_id, agent_id="claude", wake_id=wake_id
        )
        self.assertEqual("succeeded", first.status)
        self.assertEqual(task.task_id, first.task_id)
        self.assertEqual("duplicate", second.status)
        self.assertEqual(1, adapter.calls)

    def test_retry_is_bounded_to_safe_effects(self) -> None:
        adapter = SequenceAdapter(
            AdapterResult(
                AdapterStatus.FAILED,
                "temporary",
                failure_code="temporary_failure",
                retryable=True,
            ),
            AdapterResult(AdapterStatus.SUCCEEDED, "ok"),
        )
        run_id, _, supervisor = self.run_with_task(adapter)
        first = supervisor.run_once(run_id=run_id, agent_id="claude")
        self.assertEqual("queued", first.status)
        self.clock.advance(3)
        second = supervisor.run_once(run_id=run_id, agent_id="claude")
        self.assertEqual("succeeded", second.status)
        self.assertEqual(2, adapter.calls)

        with tempfile.TemporaryDirectory() as directory:
            coop = Path(directory) / "coop"
            coop.mkdir()
            store = StateStore(coop)
            run = store.init_run(project_alias="mutating")
            store.enqueue_task(
                run_id=run,
                target_agent="claude",
                payload="mutate",
                idempotency_key="root",
                effect_class=EffectClass.MUTATING,
            )
            one_failure = SequenceAdapter(
                AdapterResult(
                    AdapterStatus.FAILED,
                    "failed",
                    failure_code="external_failure",
                    retryable=True,
                )
            )
            outcome = Supervisor(store, {"claude": one_failure}).run_once(
                run_id=run, agent_id="claude"
            )
            self.assertEqual("blocked", outcome.status)
            self.assertEqual("waiting_operator", store.safe_status(run)["state"])

    def test_excess_handoffs_are_rejected_without_children(self) -> None:
        handoffs = tuple(
            Handoff("codex", f"child {index}", f"child-{index}")
            for index in range(3)
        )
        adapter = SequenceAdapter(
            AdapterResult(AdapterStatus.SUCCEEDED, "ok", handoffs=handoffs)
        )
        policy = RunPolicy(max_handoffs_per_result=2)
        run_id, _, supervisor = self.run_with_task(adapter, policy=policy)
        outcome = supervisor.run_once(run_id=run_id, agent_id="claude")
        self.assertEqual("blocked", outcome.status)
        self.assertEqual("handoff_count_exceeded", outcome.failure_code)
        self.assertEqual({"blocked": 1}, self.store.safe_status(run_id)["task_counts"])

    def test_handoff_idempotency_conflict_becomes_operator_block(self) -> None:
        adapter = SequenceAdapter(
            AdapterResult(
                AdapterStatus.SUCCEEDED,
                "ok",
                handoffs=(Handoff("codex", "new", "child"),),
            )
        )
        run_id, _, supervisor = self.run_with_task(adapter)
        self.store.enqueue_task(
            run_id=run_id,
            target_agent="codex",
            payload="old",
            idempotency_key="child",
        )
        outcome = supervisor.run_once(run_id=run_id, agent_id="claude")
        self.assertEqual("blocked", outcome.status)
        self.assertEqual("idempotency_conflict", outcome.failure_code)
        self.assertEqual(
            {"blocked": 1, "queued": 1},
            self.store.safe_status(run_id)["task_counts"],
        )

    def test_stop_during_turn_cancels_result_and_handoffs(self) -> None:
        store = self.store

        class StopAdapter:
            def run(self, **kwargs) -> AdapterResult:
                store.request_stop(
                    run_id=kwargs["task"].run_id,
                    requested_by="operator",
                    reason_code="operator_stop",
                )
                return AdapterResult(
                    AdapterStatus.SUCCEEDED,
                    "too late",
                    handoffs=(Handoff("codex", "next", "child"),),
                )

        run_id, _, supervisor = self.run_with_task(StopAdapter())
        outcome = supervisor.run_once(run_id=run_id, agent_id="claude")
        self.assertEqual("cancelled", outcome.status)
        self.assertEqual(0, outcome.handoff_count)
        self.assertEqual("stopped", self.store.safe_status(run_id)["state"])

    def test_busy_lease_does_not_claim_or_execute(self) -> None:
        adapter = SequenceAdapter(AdapterResult(AdapterStatus.SUCCEEDED, "ok"))
        run_id, _, supervisor = self.run_with_task(adapter)
        lease = self.store.acquire_lease(
            run_id=run_id,
            agent_id="claude",
            worker_session_id=str(uuid.uuid4()),
        )
        outcome = supervisor.run_once(run_id=run_id, agent_id="claude")
        self.assertEqual("lease_busy", outcome.status)
        self.assertEqual(0, adapter.calls)
        self.assertEqual(1, self.store.safe_status(run_id)["task_counts"]["queued"])
        self.store.release_lease(lease)

    def test_serve_invokes_adapter_only_when_work_exists(self) -> None:
        adapter = SequenceAdapter(AdapterResult(AdapterStatus.SUCCEEDED, "ok"))
        run_id, _, _ = self.run_with_task(adapter)
        sleeps: list[float] = []
        supervisor = Supervisor(
            self.store,
            {"claude": adapter},
            sleeper=lambda seconds: sleeps.append(seconds),
        )
        dispatched = supervisor.serve(
            run_id=run_id, poll_seconds=0.25, max_cycles=3
        )
        self.assertEqual(1, dispatched)
        self.assertEqual(1, adapter.calls)
        self.assertEqual([0.25, 0.25], sleeps)

    def test_serve_backs_off_without_spending_wake_budget_on_busy_lease(self) -> None:
        adapter = SequenceAdapter(AdapterResult(AdapterStatus.SUCCEEDED, "ok"))
        run_id, _, _ = self.run_with_task(
            adapter, policy=RunPolicy(max_wakes_per_agent=2)
        )
        lease = self.store.acquire_lease(
            run_id=run_id,
            agent_id="claude",
            worker_session_id=str(uuid.uuid4()),
        )
        sleeps: list[float] = []
        supervisor = Supervisor(
            self.store,
            {"claude": adapter},
            sleeper=lambda seconds: sleeps.append(seconds),
        )
        self.assertEqual(
            0,
            supervisor.serve(run_id=run_id, poll_seconds=0.5, max_cycles=5),
        )
        self.assertEqual([0.5] * 5, sleeps)
        status = self.store.safe_status(run_id)
        self.assertEqual("active", status["state"])
        self.assertEqual({}, status["wake_counts"])
        self.assertEqual(0, adapter.calls)
        self.store.release_lease(lease)

    def test_unsafe_adapter_metrics_become_terminal_contract_block(self) -> None:
        adapter = SequenceAdapter(
            AdapterResult(
                AdapterStatus.SUCCEEDED,
                "ok",
                safe_metrics={"detail": "C:/private/path"},
            )
        )
        run_id, _, supervisor = self.run_with_task(adapter)
        outcome = supervisor.run_once(run_id=run_id, agent_id="claude")
        self.assertEqual("blocked", outcome.status)
        self.assertEqual("unsafe_event_detail", outcome.failure_code)
        self.assertEqual(
            {"blocked": 1}, self.store.safe_status(run_id)["task_counts"]
        )

    def test_arbitrary_adapter_failure_token_is_not_relayed(self) -> None:
        adapter = SequenceAdapter(
            AdapterResult(
                AdapterStatus.FAILED,
                "failed",
                failure_code="sk-SYNTHETICSECRET123456",
            )
        )
        run_id, _, supervisor = self.run_with_task(adapter)
        outcome = supervisor.run_once(run_id=run_id, agent_id="claude")
        self.assertEqual("dead_letter", outcome.status)
        self.assertEqual("failure_other", outcome.failure_code)

    def test_prefix_shaped_adapter_secret_is_not_relayed(self) -> None:
        adapter = SequenceAdapter(
            AdapterResult(
                AdapterStatus.FAILED,
                "private adapter detail",
                failure_code="adapter_private_secretvalue",
            )
        )
        run_id, _, supervisor = self.run_with_task(adapter)
        outcome = supervisor.run_once(run_id=run_id, agent_id="claude")
        self.assertEqual("failure_other", outcome.failure_code)
        self.assertNotIn("secretvalue", repr(outcome))


if __name__ == "__main__":
    unittest.main()
