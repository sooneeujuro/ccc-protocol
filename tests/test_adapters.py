from __future__ import annotations

import json
import sys
import time
import uuid
import unittest
from pathlib import Path

from cccp_supervisor.adapters import (
    ClaudeCliAdapter,
    ClaudeCliConfig,
    CodexAppServerAdapter,
    CodexJsonlOutcome,
    ProcessOutcome,
    SubprocessOneShotTransport,
    TransportStatus,
    UiNudgeAdapter,
    UiNudgeCommand,
    UiNudgeConfig,
    UiNudgeOutcome,
    UiNudgeTarget,
)
from cccp_supervisor.errors import AdapterUnavailable, SupervisorError
from cccp_supervisor.models import (
    AdapterStatus,
    EffectClass,
    TaskRecord,
    TaskState,
)


def _task(target_agent: str, *, run_id: str | None = None) -> TaskRecord:
    return TaskRecord(
        task_id=str(uuid.uuid4()),
        run_id=run_id or str(uuid.uuid4()),
        target_agent=target_agent,
        kind="task",
        effect_class=EffectClass.READ_ONLY,
        state=TaskState.RUNNING,
        idempotency_key="adapter-test",
        payload_ref="payloads/test.json",
        payload_sha256="0" * 64,
        attempt_count=1,
        max_attempts=3,
        depth=0,
        correlation_id=str(uuid.uuid4()),
        claim_token="claim-token",
    )


def _line(value: dict[str, object]) -> bytes:
    return (json.dumps(value, separators=(",", ":")) + "\n").encode()


def _claude_adapter(transport) -> ClaudeCliAdapter:
    return ClaudeCliAdapter(
        transport,
        config=ClaudeCliConfig(working_directory="."),
    )


class FakeProcessTransport:
    def __init__(self, outcome: ProcessOutcome) -> None:
        self.outcome = outcome
        self.calls: list[dict[str, object]] = []

    def invoke(self, command, **kwargs):
        self.calls.append({"command": tuple(command), **kwargs})
        return self.outcome


class FakeCodexTransport:
    def __init__(
        self,
        *,
        thread_id: str = "thr_test",
        summary: str = "done",
        status: TransportStatus = TransportStatus.COMPLETED,
        lines: tuple[bytes, ...] | None = None,
    ) -> None:
        self.thread_id = thread_id
        self.summary = summary
        self.status = status
        self.lines = lines
        self.calls: list[dict[str, object]] = []

    def exchange(self, plan, **kwargs):
        resolved_thread = plan.conversation_id or self.thread_id
        self.calls.append(
            {
                "plan": plan,
                "initialize": plan.initialize_line,
                "initialized": plan.initialized_line,
                "thread": plan.thread_line,
                "turn": plan.turn_line(resolved_thread),
                **kwargs,
            }
        )
        lines = self.lines
        if lines is None:
            lines = _completed_codex_lines(resolved_thread, self.summary)
        return CodexJsonlOutcome(
            status=self.status,
            lines=lines,
            thread_id=resolved_thread,
        )


def _completed_codex_lines(thread_id: str, summary: str) -> tuple[bytes, ...]:
    return (
        _line({"id": 0, "result": {"platformFamily": "windows"}}),
        _line({"id": 1, "result": {"thread": {"id": thread_id}}}),
        _line(
            {
                "id": 2,
                "result": {
                    "turn": {
                        "id": "turn_test",
                        "status": "inProgress",
                        "items": [],
                        "error": None,
                    }
                },
            }
        ),
        _line(
            {
                "method": "item/completed",
                "params": {
                    "threadId": thread_id,
                    "item": {
                        "id": "item_test",
                        "type": "agentMessage",
                        "text": summary,
                    },
                },
            }
        ),
        _line(
            {
                "method": "turn/completed",
                "params": {
                    "threadId": thread_id,
                    "turn": {"id": "turn_test", "status": "completed"},
                },
            }
        ),
    )


class FakeUiExecutor:
    def __init__(self, outcome: UiNudgeOutcome | None = None) -> None:
        self.outcome = outcome or UiNudgeOutcome(TransportStatus.COMPLETED)
        self.calls: list[dict[str, object]] = []

    def execute_exact(self, **kwargs):
        self.calls.append(kwargs)
        return self.outcome


class ClaudeCliAdapterTests(unittest.TestCase):
    def test_prompt_is_stdin_and_session_is_always_explicit(self) -> None:
        run_id = str(uuid.uuid4())
        task = _task("claude", run_id=run_id)
        transport = FakeProcessTransport(
            ProcessOutcome(
                TransportStatus.COMPLETED,
                stdout=b"answer",
                stderr=b"",
                returncode=0,
            )
        )

        result = _claude_adapter(transport).run(
            payload="private prompt",
            task=task,
            conversation_id=None,
            max_output_bytes=1_024,
            cancel_requested=lambda: False,
        )

        self.assertEqual(AdapterStatus.SUCCEEDED, result.status)
        self.assertEqual("answer", result.summary)
        self.assertEqual(1, len(transport.calls))
        call = transport.calls[0]
        command = call["command"]
        self.assertEqual(b"private prompt", call["stdin"])
        self.assertNotIn("private prompt", command)
        self.assertIn("--print", command)
        self.assertEqual("plan", command[command.index("--permission-mode") + 1])
        self.assertEqual("Read,Glob,Grep", command[command.index("--tools") + 1])
        self.assertIn("--strict-mcp-config", command)
        self.assertEqual(str(Path(".").resolve()), call["working_directory"])
        session_index = command.index("--session-id") + 1
        self.assertEqual(result.conversation_id, command[session_index])
        self.assertEqual(
            result.conversation_id,
            str(uuid.uuid5(uuid.UUID(run_id), "cccp:claude")),
        )

    def test_provided_session_is_preserved(self) -> None:
        session_id = str(uuid.uuid4())
        transport = FakeProcessTransport(
            ProcessOutcome(TransportStatus.COMPLETED, stdout=b"ok", returncode=0)
        )
        result = _claude_adapter(transport).run(
            payload="go",
            task=_task("claude"),
            conversation_id=session_id,
            max_output_bytes=100,
            cancel_requested=lambda: False,
        )
        self.assertEqual(session_id, result.conversation_id)
        command = transport.calls[0]["command"]
        self.assertNotIn("--session-id", command)
        self.assertEqual(session_id, command[command.index("--resume") + 1])

    def test_cancel_before_call_never_invokes_transport(self) -> None:
        transport = FakeProcessTransport(
            ProcessOutcome(TransportStatus.COMPLETED, stdout=b"not used", returncode=0)
        )
        result = _claude_adapter(transport).run(
            payload="go",
            task=_task("claude"),
            conversation_id=None,
            max_output_bytes=100,
            cancel_requested=lambda: True,
        )
        self.assertEqual(AdapterStatus.CANCELLED, result.status)
        self.assertEqual([], transport.calls)

    def test_faulty_transport_cannot_bypass_output_limit(self) -> None:
        transport = FakeProcessTransport(
            ProcessOutcome(
                TransportStatus.COMPLETED,
                stdout=b"x" * 11,
                returncode=0,
            )
        )
        result = _claude_adapter(transport).run(
            payload="go",
            task=_task("claude"),
            conversation_id=None,
            max_output_bytes=10,
            cancel_requested=lambda: False,
        )
        self.assertEqual(AdapterStatus.FAILED, result.status)
        self.assertEqual("claude_cli_output_limit", result.failure_code)

    def test_target_mismatch_is_rejected_before_transport(self) -> None:
        transport = FakeProcessTransport(
            ProcessOutcome(TransportStatus.COMPLETED, stdout=b"unused", returncode=0)
        )
        with self.assertRaisesRegex(SupervisorError, "adapter_target_mismatch"):
            _claude_adapter(transport).run(
                payload="go",
                task=_task("codex"),
                conversation_id=None,
                max_output_bytes=100,
                cancel_requested=lambda: False,
            )
        self.assertEqual([], transport.calls)


class SubprocessOneShotTransportTests(unittest.TestCase):
    def test_stdin_is_delivered_without_shell_interpolation(self) -> None:
        transport = SubprocessOneShotTransport()
        outcome = transport.invoke(
            (
                sys.executable,
                "-c",
                "import sys; data=sys.stdin.buffer.read(); "
                "sys.stdout.buffer.write(data[::-1])",
            ),
            stdin=b"a b;$()",
            timeout_seconds=5,
            max_stdout_bytes=100,
            max_stderr_bytes=100,
            cancel_requested=lambda: False,
        )
        self.assertEqual(TransportStatus.COMPLETED, outcome.status)
        self.assertEqual(0, outcome.returncode)
        self.assertEqual(b")($;b a", outcome.stdout)

    def test_stdout_and_stderr_are_drained_concurrently(self) -> None:
        transport = SubprocessOneShotTransport()
        outcome = transport.invoke(
            (
                sys.executable,
                "-c",
                "import sys; "
                "sys.stdout.buffer.write(b'o'*200000); sys.stdout.flush(); "
                "sys.stderr.buffer.write(b'e'*200000); sys.stderr.flush()",
            ),
            stdin=b"",
            timeout_seconds=5,
            max_stdout_bytes=250_000,
            max_stderr_bytes=250_000,
            cancel_requested=lambda: False,
        )
        self.assertEqual(TransportStatus.COMPLETED, outcome.status)
        self.assertEqual(200_000, len(outcome.stdout))
        self.assertEqual(200_000, len(outcome.stderr))

    def test_output_overflow_terminates_owned_child(self) -> None:
        transport = SubprocessOneShotTransport(terminate_grace_seconds=0.5)
        started = time.monotonic()
        outcome = transport.invoke(
            (
                sys.executable,
                "-c",
                "import sys,time; "
                "sys.stdout.buffer.write(b'x'*200000); sys.stdout.flush(); "
                "time.sleep(10)",
            ),
            stdin=b"",
            timeout_seconds=5,
            max_stdout_bytes=1_024,
            max_stderr_bytes=1_024,
            cancel_requested=lambda: False,
        )
        self.assertEqual(TransportStatus.OUTPUT_LIMIT, outcome.status)
        self.assertLessEqual(len(outcome.stdout), 1_024)
        self.assertLess(time.monotonic() - started, 3)

    def test_timeout_terminates_owned_child(self) -> None:
        transport = SubprocessOneShotTransport(terminate_grace_seconds=0.5)
        started = time.monotonic()
        outcome = transport.invoke(
            (sys.executable, "-c", "import time; time.sleep(10)"),
            stdin=b"",
            timeout_seconds=0.1,
            max_stdout_bytes=100,
            max_stderr_bytes=100,
            cancel_requested=lambda: False,
        )
        self.assertEqual(TransportStatus.TIMED_OUT, outcome.status)
        self.assertLess(time.monotonic() - started, 3)

    def test_cancellation_terminates_owned_child(self) -> None:
        transport = SubprocessOneShotTransport(terminate_grace_seconds=0.5)
        started = time.monotonic()
        outcome = transport.invoke(
            (sys.executable, "-c", "import time; time.sleep(10)"),
            stdin=b"",
            timeout_seconds=5,
            max_stdout_bytes=100,
            max_stderr_bytes=100,
            cancel_requested=lambda: time.monotonic() - started >= 0.1,
        )
        self.assertEqual(TransportStatus.CANCELLED, outcome.status)
        self.assertLess(time.monotonic() - started, 3)


class CodexAppServerAdapterTests(unittest.TestCase):
    def test_new_thread_uses_exact_jsonl_handshake_and_returns_thread_id(self) -> None:
        task = _task("codex")
        transport = FakeCodexTransport(thread_id="thr_new", summary="result")

        result = CodexAppServerAdapter(transport).run(
            payload="do the task",
            task=task,
            conversation_id=None,
            max_output_bytes=10_000,
            cancel_requested=lambda: False,
        )

        self.assertEqual(AdapterStatus.SUCCEEDED, result.status)
        self.assertEqual("result", result.summary)
        self.assertEqual("thr_new", result.conversation_id)
        call = transport.calls[0]
        initialize = json.loads(call["initialize"])
        initialized = json.loads(call["initialized"])
        thread = json.loads(call["thread"])
        turn = json.loads(call["turn"])
        self.assertNotIn("jsonrpc", initialize)
        self.assertEqual("initialize", initialize["method"])
        self.assertEqual({"method": "initialized"}, initialized)
        self.assertEqual("thread/start", thread["method"])
        self.assertEqual({}, thread["params"])
        self.assertEqual("turn/start", turn["method"])
        self.assertEqual("thr_new", turn["params"]["threadId"])
        self.assertEqual(task.task_id, turn["params"]["clientUserMessageId"])
        self.assertEqual(
            [{"type": "text", "text": "do the task"}], turn["params"]["input"]
        )

    def test_existing_thread_uses_resume(self) -> None:
        transport = FakeCodexTransport(thread_id="ignored")
        result = CodexAppServerAdapter(transport).run(
            payload="continue",
            task=_task("codex"),
            conversation_id="thr_existing",
            max_output_bytes=10_000,
            cancel_requested=lambda: False,
        )
        thread = json.loads(transport.calls[0]["thread"])
        self.assertEqual("thread/resume", thread["method"])
        self.assertEqual({"threadId": "thr_existing"}, thread["params"])
        self.assertEqual("thr_existing", result.conversation_id)

    def test_cancel_before_exchange_never_invokes_transport(self) -> None:
        transport = FakeCodexTransport()
        result = CodexAppServerAdapter(transport).run(
            payload="go",
            task=_task("codex"),
            conversation_id=None,
            max_output_bytes=100,
            cancel_requested=lambda: True,
        )
        self.assertEqual(AdapterStatus.CANCELLED, result.status)
        self.assertEqual([], transport.calls)

    def test_server_initiated_request_fails_closed(self) -> None:
        thread_id = "thr_test"
        lines = list(_completed_codex_lines(thread_id, "done"))
        lines.insert(
            3,
            _line(
                {
                    "method": "item/commandExecution/requestApproval",
                    "id": 61,
                    "params": {"threadId": thread_id},
                }
            ),
        )
        transport = FakeCodexTransport(thread_id=thread_id, lines=tuple(lines))
        result = CodexAppServerAdapter(transport).run(
            payload="go",
            task=_task("codex"),
            conversation_id=None,
            max_output_bytes=10_000,
            cancel_requested=lambda: False,
        )
        self.assertEqual(AdapterStatus.BLOCKED, result.status)
        self.assertEqual("codex_server_request_unsupported", result.failure_code)

    def test_response_id_mismatch_is_rejected(self) -> None:
        lines = list(_completed_codex_lines("thr_test", "done"))
        lines[2] = _line({"id": 99, "result": {}})
        transport = FakeCodexTransport(lines=tuple(lines))
        result = CodexAppServerAdapter(transport).run(
            payload="go",
            task=_task("codex"),
            conversation_id=None,
            max_output_bytes=10_000,
            cancel_requested=lambda: False,
        )
        self.assertEqual(AdapterStatus.FAILED, result.status)
        self.assertEqual("codex_app_server_response_id_invalid", result.failure_code)

    def test_faulty_transport_cannot_bypass_wire_limit(self) -> None:
        transport = FakeCodexTransport(lines=(b"{" + b"x" * 100 + b"}\n",))
        result = CodexAppServerAdapter(transport).run(
            payload="go",
            task=_task("codex"),
            conversation_id=None,
            max_output_bytes=50,
            cancel_requested=lambda: False,
        )
        self.assertEqual(AdapterStatus.FAILED, result.status)
        self.assertEqual("codex_app_server_output_limit", result.failure_code)

    def test_overload_error_is_retryable(self) -> None:
        lines = (
            _line({"id": 0, "result": {}}),
            _line({"id": 1, "result": {"thread": {"id": "thr_test"}}}),
            _line(
                {
                    "id": 2,
                    "error": {"code": -32001, "message": "overloaded"},
                }
            ),
        )
        transport = FakeCodexTransport(lines=lines)
        result = CodexAppServerAdapter(transport).run(
            payload="go",
            task=_task("codex"),
            conversation_id=None,
            max_output_bytes=10_000,
            cancel_requested=lambda: False,
        )
        self.assertEqual(AdapterStatus.FAILED, result.status)
        self.assertTrue(result.retryable)
        self.assertEqual("codex_app_server_remote_error", result.failure_code)


class UiNudgeAdapterTests(unittest.TestCase):
    def test_default_disabled_contract_never_touches_executor(self) -> None:
        target = UiNudgeTarget("codex.window.send", UiNudgeCommand.INVOKE)
        executor = FakeUiExecutor()
        adapter = UiNudgeAdapter(executor)
        with self.assertRaisesRegex(AdapterUnavailable, "ui_nudge_disabled"):
            adapter.nudge(target, cancel_requested=lambda: False)
        self.assertEqual([], executor.calls)

    def test_exact_pair_allowlist_is_required(self) -> None:
        allowed = UiNudgeTarget("codex.window.send", UiNudgeCommand.INVOKE)
        denied = UiNudgeTarget("codex.window.*", UiNudgeCommand.INVOKE)
        executor = FakeUiExecutor()
        adapter = UiNudgeAdapter(
            executor,
            config=UiNudgeConfig(enabled=True, allowed_targets=frozenset({allowed})),
        )
        with self.assertRaisesRegex(SupervisorError, "ui_nudge_contract_denied"):
            adapter.nudge(denied, cancel_requested=lambda: False)
        self.assertEqual([], executor.calls)

    def test_allowed_exact_command_is_forwarded_without_payload(self) -> None:
        target = UiNudgeTarget("codex.window.send", UiNudgeCommand.INVOKE)
        executor = FakeUiExecutor()
        adapter = UiNudgeAdapter(
            executor,
            config=UiNudgeConfig(enabled=True, allowed_targets=frozenset({target})),
        )
        result = adapter.nudge(target, cancel_requested=lambda: False)
        self.assertEqual(AdapterStatus.SUCCEEDED, result.status)
        self.assertEqual(1, len(executor.calls))
        self.assertEqual(
            {"selector", "command", "timeout_seconds", "cancel_requested"},
            set(executor.calls[0]),
        )

    def test_free_form_command_is_rejected(self) -> None:
        with self.assertRaisesRegex(SupervisorError, "ui_nudge_command_invalid"):
            UiNudgeTarget("codex.window.send", "type arbitrary text")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
