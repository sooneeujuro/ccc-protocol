from __future__ import annotations

import threading
import time
import uuid
from collections.abc import Callable, Mapping
from typing import Protocol

from .errors import AdapterUnavailable, SupervisorError
from .models import (
    AGENT_IDS,
    AdapterResult,
    AdapterStatus,
    DispatchResult,
    EffectClass,
    Lease,
    RunState,
    TaskRecord,
)
from .store import StateStore


class AgentAdapter(Protocol):
    """The small synchronous boundary between lifecycle state and an agent."""

    def run(
        self,
        *,
        payload: str,
        task: TaskRecord,
        conversation_id: str | None,
        max_output_bytes: int,
        cancel_requested: Callable[[], bool],
    ) -> AdapterResult: ...


class Supervisor:
    """Dispatch queued work exactly once per fenced task attempt.

    The supervisor owns lifecycle decisions. Adapters may execute one turn and
    propose bounded handoffs, but they cannot claim work, retry themselves, or
    decide whether a run is stopped.
    """

    def __init__(
        self,
        store: StateStore,
        adapters: Mapping[str, AgentAdapter],
        *,
        uuid_factory: Callable[[], str] | None = None,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        self.store = store
        self.adapters = dict(adapters)
        self.uuid_factory = uuid_factory or (lambda: str(uuid.uuid4()))
        self.sleeper = sleeper

    def run_once(
        self,
        *,
        run_id: str,
        agent_id: str,
        wake_id: str | None = None,
        source: str = "event",
    ) -> DispatchResult:
        wake_id = wake_id or self.uuid_factory()
        wake_state = self.store.begin_wake(
            run_id=run_id,
            agent_id=agent_id,
            wake_id=wake_id,
            source=source,
        )
        if wake_state == "duplicate":
            return DispatchResult("duplicate", run_id, agent_id, wake_id)
        if wake_state != "accepted":
            self.store.end_wake(
                run_id=run_id,
                agent_id=agent_id,
                wake_id=wake_id,
                result_code="suppressed",
            )
            return DispatchResult("suppressed", run_id, agent_id, wake_id)

        lease: Lease | None = None
        task: TaskRecord | None = None
        result_code = "dispatch_failed"
        failure_code: str | None = None
        handoff_count = 0
        try:
            worker_session_id = self.uuid_factory()
            try:
                lease = self.store.acquire_lease(
                    run_id=run_id,
                    agent_id=agent_id,
                    worker_session_id=worker_session_id,
                )
            except SupervisorError as exc:
                if exc.code == "lease_held_by_other_session":
                    result_code = "lease_busy"
                    failure_code = exc.code
                    return DispatchResult(
                        result_code,
                        run_id,
                        agent_id,
                        wake_id,
                        failure_code=_public_failure_code(failure_code),
                    )
                raise

            task = self.store.claim_next_task(lease)
            if task is None:
                result_code = "idle"
                return DispatchResult(result_code, run_id, agent_id, wake_id)

            task = self.store.start_task(lease, task)
            payload = self.store.read_task_payload(task)
            run = self.store.run_row(run_id)
            adapter = self.adapters.get(agent_id)
            if adapter is None:
                result = AdapterResult(
                    status=AdapterStatus.BLOCKED,
                    summary="adapter unavailable",
                    failure_code="adapter_unavailable",
                )
            else:
                heartbeat = _LeaseHeartbeat(
                    self.store,
                    lease,
                    interval_seconds=max(
                        0.1, min(30.0, run["lease_ttl_seconds"] / 3)
                    ),
                )
                heartbeat.start()
                try:
                    result = adapter.run(
                        payload=payload,
                        task=task,
                        conversation_id=self.store.conversation_id(run_id, agent_id),
                        max_output_bytes=run["max_output_bytes"],
                        cancel_requested=lambda: (
                            heartbeat.failed or self.store.should_cancel(run_id)
                        ),
                    )
                except AdapterUnavailable as exc:
                    result = AdapterResult(
                        status=AdapterStatus.BLOCKED,
                        summary="adapter unavailable",
                        failure_code=exc.code,
                    )
                except Exception:
                    result = AdapterResult(
                        status=AdapterStatus.FAILED,
                        summary="adapter execution failed",
                        failure_code="adapter_execution_failed",
                        retryable=True,
                    )
                finally:
                    heartbeat.stop()
                if heartbeat.failed:
                    raise SupervisorError("lease_renewal_failed")

            if not isinstance(result, AdapterResult):
                result = AdapterResult(
                    status=AdapterStatus.BLOCKED,
                    summary="adapter contract violation",
                    failure_code="adapter_result_invalid",
                )
            if self.store.should_cancel(run_id) and result.status != AdapterStatus.CANCELLED:
                result = AdapterResult(
                    status=AdapterStatus.CANCELLED,
                    summary="cancelled by stop request",
                    failure_code="task_cancelled_by_stop",
                    conversation_id=result.conversation_id,
                    safe_metrics=result.safe_metrics,
                )
            if result.status != AdapterStatus.SUCCEEDED and result.handoffs:
                result = AdapterResult(
                    status=AdapterStatus.BLOCKED,
                    summary="handoffs require a successful turn",
                    failure_code="handoff_on_unsuccessful_result",
                    conversation_id=result.conversation_id,
                )
            if len(result.handoffs) > run["max_handoffs_per_result"]:
                result = AdapterResult(
                    status=AdapterStatus.BLOCKED,
                    summary="handoff budget exceeded",
                    failure_code="handoff_count_exceeded",
                    conversation_id=result.conversation_id,
                )

            try:
                final_state = self.store.finish_task(
                    lease=lease, task=task, result=result
                )
            except SupervisorError as exc:
                if exc.code not in _ADAPTER_CONTRACT_FAILURES:
                    raise
                result = AdapterResult(
                    status=AdapterStatus.BLOCKED,
                    summary="adapter result rejected by supervisor",
                    failure_code=exc.code,
                    conversation_id=result.conversation_id,
                )
                final_state = self.store.finish_task(
                    lease=lease, task=task, result=result
                )
            handoff_count = len(result.handoffs) if final_state == "succeeded" else 0
            result_code = final_state
            failure_code = (
                "task_cancelled_by_stop"
                if final_state == "cancelled"
                else _public_failure_code(result.failure_code)
            )
            return DispatchResult(
                result_code,
                run_id,
                agent_id,
                wake_id,
                task_id=task.task_id,
                failure_code=failure_code,
                handoff_count=handoff_count,
            )
        except SupervisorError as exc:
            failure_code = exc.code
            result_code = "dispatch_failed"
            return DispatchResult(
                result_code,
                run_id,
                agent_id,
                wake_id,
                task_id=task.task_id if task else None,
                failure_code=_public_failure_code(failure_code),
            )
        finally:
            if lease is not None:
                try:
                    self.store.release_lease(lease, reason_code=result_code)
                except SupervisorError:
                    if failure_code is None:
                        failure_code = "lease_release_failed"
            try:
                self.store.end_wake(
                    run_id=run_id,
                    agent_id=agent_id,
                    wake_id=wake_id,
                    result_code=result_code,
                )
            except SupervisorError:
                pass

    def serve(
        self,
        *,
        run_id: str,
        poll_seconds: float = 1.0,
        max_cycles: int | None = None,
    ) -> int:
        """Process available tasks; wait only when explicitly run as a service."""

        if poll_seconds <= 0:
            raise ValueError("poll_seconds must be positive")
        cycles = 0
        dispatched = 0
        while max_cycles is None or cycles < max_cycles:
            cycles += 1
            self.store.recover(run_id)
            run = self.store.run_row(run_id)
            if run["state"] in (
                RunState.STOPPED.value,
                RunState.EXPIRED.value,
                RunState.WAITING_OPERATOR.value,
            ):
                break
            work_found = False
            progress_made = False
            for agent_id in AGENT_IDS:
                if agent_id in self.adapters and self.store.has_queued_task(
                    run_id, agent_id
                ):
                    work_found = True
                    outcome = self.run_once(run_id=run_id, agent_id=agent_id)
                    if outcome.task_id is not None:
                        dispatched += 1
                        progress_made = True
            if not work_found or not progress_made:
                self.sleeper(poll_seconds)
        return dispatched


class _LeaseHeartbeat:
    def __init__(
        self,
        store: StateStore,
        lease: Lease,
        *,
        interval_seconds: float,
    ) -> None:
        self.store = store
        self.lease = lease
        self.interval_seconds = interval_seconds
        self.failed = False
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join(timeout=max(1.0, self.interval_seconds * 2))

    def _run(self) -> None:
        while not self._stop.wait(self.interval_seconds):
            try:
                self.lease = self.store.renew_lease(self.lease)
            except SupervisorError:
                self.failed = True
                self._stop.set()
                return


_ADAPTER_CONTRACT_FAILURES = {
    "adapter_result_invalid",
    "duplicate_handoff_key",
    "handoff_count_exceeded",
    "handoff_depth_exceeded",
    "handoff_invalid",
    "handoff_on_unsuccessful_result",
    "idempotency_conflict",
    "idempotency_key_invalid",
    "agent_id_invalid",
    "payload_too_large",
    "result_too_large",
    "task_kind_invalid",
    "unsafe_event_detail",
}

_PUBLIC_FAILURE_EXACT = {
    "agent_id_invalid",
    "adapter_execution_failed",
    "adapter_result_invalid",
    "adapter_unavailable",
    "claude_cli_cancelled",
    "claude_cli_exit_nonzero",
    "claude_cli_output_limit",
    "claude_cli_timeout",
    "claude_cli_transport_error",
    "claude_cli_transport_failed",
    "claude_cli_unavailable",
    "codex_agent_message_missing",
    "codex_app_server_cancelled",
    "codex_app_server_event_limit",
    "codex_app_server_incomplete",
    "codex_app_server_output_limit",
    "codex_app_server_protocol_error",
    "codex_app_server_remote_error",
    "codex_app_server_response_id_invalid",
    "codex_app_server_timeout",
    "codex_app_server_transport_error",
    "codex_app_server_transport_failed",
    "codex_app_server_unavailable",
    "codex_server_request_unsupported",
    "codex_thread_id_invalid",
    "codex_thread_id_mismatch",
    "codex_thread_id_missing",
    "codex_turn_failed",
    "codex_turn_interrupted",
    "duplicate_handoff_key",
    "effect_class_invalid",
    "external_failure",
    "handoff_count_exceeded",
    "handoff_depth_exceeded",
    "handoff_invalid",
    "handoff_on_unsuccessful_result",
    "idempotency_conflict",
    "idempotency_key_invalid",
    "lease_held_by_other_session",
    "lease_renewal_failed",
    "temporary_failure",
    "operator_required",
    "payload_too_large",
    "result_too_large",
    "run_not_active",
    "task_cancelled_by_stop",
    "task_kind_invalid",
    "ui_nudge_cancelled",
    "ui_nudge_failed",
    "ui_nudge_result_invalid",
    "ui_nudge_timeout",
    "ui_nudge_unavailable",
    "unsafe_event_detail",
    "watch_expired",
}


def _public_failure_code(value: str | None) -> str | None:
    if value is None:
        return None
    if value in _PUBLIC_FAILURE_EXACT:
        return value
    return "failure_other"
