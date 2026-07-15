from __future__ import annotations

import json
import re
import subprocess
import threading
import time
import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Callable, Protocol, Sequence

from .errors import AdapterUnavailable, SupervisorError
from .models import AdapterResult, AdapterStatus, TaskRecord


CancelRequested = Callable[[], bool]

_CODEX_THREAD_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")
_MAX_CONFIGURED_BYTES = 16 * 1024 * 1024
_MAX_TIMEOUT_SECONDS = 3_600.0


class TransportStatus(StrEnum):
    """Payload-free outcomes shared by mockable transport boundaries."""

    COMPLETED = "completed"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"
    OUTPUT_LIMIT = "output_limit"
    UNAVAILABLE = "unavailable"
    FAILED = "failed"


@dataclass(frozen=True)
class ProcessOutcome:
    status: TransportStatus
    stdout: bytes = b""
    stderr: bytes = b""
    returncode: int | None = None


class OneShotProcessTransport(Protocol):
    """A bounded, shell-free subprocess boundary.

    Implementations MUST enforce the supplied byte limits while reading, poll
    ``cancel_requested`` while the child is live, and terminate the child on a
    timeout, cancellation, or limit breach.  The adapter repeats the size
    checks so a faulty transport fails closed.
    """

    def invoke(
        self,
        command: Sequence[str],
        *,
        stdin: bytes,
        timeout_seconds: float,
        max_stdout_bytes: int,
        max_stderr_bytes: int,
        cancel_requested: CancelRequested,
        working_directory: str | None = None,
    ) -> ProcessOutcome: ...


class SubprocessOneShotTransport:
    """Live-capable bounded transport for a single owned child process.

    There is deliberately no shell, process-name lookup, process-tree sweep,
    or implicit executable.  On cancellation, timeout, or overflow this class
    terminates only the ``Popen`` instance it created for this invocation.
    """

    def __init__(
        self,
        *,
        poll_interval_seconds: float = 0.02,
        terminate_grace_seconds: float = 1.0,
    ) -> None:
        if not 0 < poll_interval_seconds <= 1.0:
            raise SupervisorError("process_poll_interval_invalid")
        if not 0 < terminate_grace_seconds <= 10.0:
            raise SupervisorError("process_terminate_grace_invalid")
        self.poll_interval_seconds = poll_interval_seconds
        self.terminate_grace_seconds = terminate_grace_seconds

    def invoke(
        self,
        command: Sequence[str],
        *,
        stdin: bytes,
        timeout_seconds: float,
        max_stdout_bytes: int,
        max_stderr_bytes: int,
        cancel_requested: CancelRequested,
        working_directory: str | None = None,
    ) -> ProcessOutcome:
        argv = _validated_command(command)
        if not isinstance(stdin, bytes):
            raise SupervisorError("process_stdin_invalid")
        timeout_seconds = _validated_timeout(timeout_seconds)
        max_stdout_bytes = _validated_byte_limit(
            max_stdout_bytes, "process_stdout_limit_invalid"
        )
        max_stderr_bytes = _validated_byte_limit(
            max_stderr_bytes, "process_stderr_limit_invalid"
        )
        if cancel_requested():
            return ProcessOutcome(TransportStatus.CANCELLED)
        cwd = (
            _validated_working_directory(working_directory)
            if working_directory is not None
            else None
        )

        try:
            process = subprocess.Popen(
                argv,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
                cwd=cwd,
            )
        except OSError:
            return ProcessOutcome(TransportStatus.UNAVAILABLE)

        stdout_buffer = bytearray()
        stderr_buffer = bytearray()
        overflow = threading.Event()
        io_failed = threading.Event()

        assert process.stdin is not None
        assert process.stdout is not None
        assert process.stderr is not None

        writer = threading.Thread(
            target=_write_all_and_close,
            args=(process.stdin, stdin, io_failed),
            name="cccp-stdin-writer",
            daemon=True,
        )
        stdout_reader = threading.Thread(
            target=_read_bounded,
            args=(
                process.stdout,
                stdout_buffer,
                max_stdout_bytes,
                overflow,
                io_failed,
            ),
            name="cccp-stdout-reader",
            daemon=True,
        )
        stderr_reader = threading.Thread(
            target=_read_bounded,
            args=(
                process.stderr,
                stderr_buffer,
                max_stderr_bytes,
                overflow,
                io_failed,
            ),
            name="cccp-stderr-reader",
            daemon=True,
        )
        threads = (writer, stdout_reader, stderr_reader)
        for thread in threads:
            thread.start()

        started_at = time.monotonic()
        status = TransportStatus.COMPLETED
        try:
            while process.poll() is None:
                if cancel_requested():
                    status = TransportStatus.CANCELLED
                    break
                if overflow.is_set():
                    status = TransportStatus.OUTPUT_LIMIT
                    break
                if io_failed.is_set():
                    status = TransportStatus.FAILED
                    break
                elapsed = time.monotonic() - started_at
                if elapsed >= timeout_seconds:
                    status = TransportStatus.TIMED_OUT
                    break
                time.sleep(
                    min(self.poll_interval_seconds, timeout_seconds - elapsed)
                )
        except Exception:
            status = TransportStatus.FAILED

        if status != TransportStatus.COMPLETED:
            _terminate_owned_process(process, self.terminate_grace_seconds)
        else:
            # poll() observed exit; wait() finalizes the return code without
            # targeting any process other than this exact child.
            process.wait()

        for thread in threads:
            thread.join(timeout=self.terminate_grace_seconds)
        for pipe in (process.stdin, process.stdout, process.stderr):
            try:
                pipe.close()
            except OSError:
                pass

        if overflow.is_set():
            status = TransportStatus.OUTPUT_LIMIT
        elif io_failed.is_set() and status == TransportStatus.COMPLETED:
            status = TransportStatus.FAILED

        return ProcessOutcome(
            status=status,
            stdout=bytes(stdout_buffer),
            stderr=bytes(stderr_buffer),
            returncode=process.returncode,
        )


@dataclass(frozen=True)
class ClaudeCliConfig:
    working_directory: str
    executable: str = "claude"
    timeout_seconds: float = 900.0
    max_prompt_bytes: int = 262_144
    max_stderr_bytes: int = 65_536
    hard_max_output_bytes: int = 1_048_576
    permission_mode: str = "plan"
    allowed_tools: tuple[str, ...] = ("Read", "Glob", "Grep")

    def validate(self) -> None:
        _validated_executable(self.executable)
        _validated_working_directory(self.working_directory)
        _validated_timeout(self.timeout_seconds)
        _validated_byte_limit(self.max_prompt_bytes, "claude_prompt_limit_invalid")
        _validated_byte_limit(self.max_stderr_bytes, "claude_stderr_limit_invalid")
        _validated_byte_limit(
            self.hard_max_output_bytes, "claude_output_limit_invalid"
        )
        if self.permission_mode != "plan":
            raise SupervisorError("claude_permission_mode_unsafe")
        if (
            not isinstance(self.allowed_tools, tuple)
            or not self.allowed_tools
            or any(tool not in {"Read", "Glob", "Grep"} for tool in self.allowed_tools)
            or len(set(self.allowed_tools)) != len(self.allowed_tools)
        ):
            raise SupervisorError("claude_tool_allowlist_invalid")


class ClaudeCliAdapter:
    """One Claude CLI turn with an explicit session and a stdin-only prompt."""

    def __init__(
        self,
        transport: OneShotProcessTransport,
        *,
        config: ClaudeCliConfig | None = None,
    ) -> None:
        self.transport = transport
        if config is None:
            raise SupervisorError("claude_config_required")
        self.config = config
        self.config.validate()

    def run(
        self,
        *,
        payload: str,
        task: TaskRecord,
        conversation_id: str | None,
        max_output_bytes: int,
        cancel_requested: CancelRequested,
    ) -> AdapterResult:
        _validated_task_target(task, "claude")
        prompt = _validated_payload(payload, self.config.max_prompt_bytes)
        output_limit = min(
            _validated_byte_limit(max_output_bytes, "adapter_output_limit_invalid"),
            self.config.hard_max_output_bytes,
        )
        session_id = _claude_session_id(conversation_id, task.run_id)

        if cancel_requested():
            return _cancelled("claude_cli_cancelled", session_id)

        # The prompt is intentionally absent from argv.  ``--print`` makes the
        # invocation one-shot; ``--session-id`` prevents accidental attachment
        # to an implicit/default conversation.
        session_args = (
            ("--resume", session_id)
            if conversation_id is not None
            else ("--session-id", session_id)
        )
        command = (
            self.config.executable,
            "--print",
            "--output-format",
            "text",
            "--permission-mode",
            self.config.permission_mode,
            "--tools",
            ",".join(self.config.allowed_tools),
            "--strict-mcp-config",
            "--settings",
            "{}",
            "--setting-sources",
            "",
            *session_args,
        )
        try:
            outcome = self.transport.invoke(
                command,
                stdin=prompt,
                timeout_seconds=self.config.timeout_seconds,
                max_stdout_bytes=output_limit,
                max_stderr_bytes=self.config.max_stderr_bytes,
                cancel_requested=cancel_requested,
                working_directory=_validated_working_directory(
                    self.config.working_directory
                ),
            )
        except Exception as exc:
            raise AdapterUnavailable("claude_cli_transport_error") from exc

        if len(outcome.stdout) > output_limit or len(outcome.stderr) > self.config.max_stderr_bytes:
            return _failed(
                "claude_cli_output_limit",
                conversation_id=session_id,
                output_bytes=min(len(outcome.stdout), output_limit + 1),
            )
        if outcome.status == TransportStatus.CANCELLED or cancel_requested():
            return _cancelled("claude_cli_cancelled", session_id)
        if outcome.status == TransportStatus.TIMED_OUT:
            return _failed(
                "claude_cli_timeout", retryable=True, conversation_id=session_id
            )
        if outcome.status == TransportStatus.OUTPUT_LIMIT:
            return _failed("claude_cli_output_limit", conversation_id=session_id)
        if outcome.status == TransportStatus.UNAVAILABLE:
            return _blocked("claude_cli_unavailable", session_id)
        if outcome.status != TransportStatus.COMPLETED:
            return _failed(
                "claude_cli_transport_failed",
                retryable=True,
                conversation_id=session_id,
            )
        if outcome.returncode != 0:
            return _failed(
                "claude_cli_exit_nonzero",
                conversation_id=session_id,
                exit_code=outcome.returncode,
                stderr_bytes=len(outcome.stderr),
            )

        summary = outcome.stdout.decode("utf-8", errors="replace")
        return AdapterResult(
            status=AdapterStatus.SUCCEEDED,
            summary=summary,
            conversation_id=session_id,
            safe_metrics={
                "output_bytes": len(outcome.stdout),
                "stderr_bytes": len(outcome.stderr),
            },
        )


@dataclass(frozen=True)
class CodexJsonlPlan:
    """Exact, versioned app-server messages for one supervised turn.

    The app-server omits the JSON-RPC ``jsonrpc`` header on the wire.  A
    transport sends ``initialize_line`` then ``initialized_line``.  It sends
    ``thread_line`` and resolves the returned thread ID before calling
    ``turn_line(thread_id)``.  Existing threads use ``thread/resume``; new
    threads use ``thread/start``.
    """

    payload: str
    conversation_id: str | None
    client_user_message_id: str
    client_name: str = "cccp_supervisor"
    client_title: str = "CCCP Supervisor"
    client_version: str = "0.1.0"

    @property
    def initialize_line(self) -> bytes:
        return _jsonl(
            {
                "method": "initialize",
                "id": 0,
                "params": {
                    "clientInfo": {
                        "name": self.client_name,
                        "title": self.client_title,
                        "version": self.client_version,
                    }
                },
            }
        )

    @property
    def initialized_line(self) -> bytes:
        return _jsonl({"method": "initialized"})

    @property
    def thread_method(self) -> str:
        return "thread/resume" if self.conversation_id else "thread/start"

    @property
    def thread_line(self) -> bytes:
        params: dict[str, str] = {}
        if self.conversation_id:
            params["threadId"] = self.conversation_id
        return _jsonl({"method": self.thread_method, "id": 1, "params": params})

    def turn_line(self, thread_id: str) -> bytes:
        thread_id = _validated_codex_thread_id(thread_id)
        return _jsonl(
            {
                "method": "turn/start",
                "id": 2,
                "params": {
                    "threadId": thread_id,
                    "clientUserMessageId": self.client_user_message_id,
                    "input": [{"type": "text", "text": self.payload}],
                },
            }
        )


@dataclass(frozen=True)
class CodexJsonlOutcome:
    status: TransportStatus
    lines: tuple[bytes, ...] = field(default_factory=tuple)
    thread_id: str | None = None


class CodexJsonlTransport(Protocol):
    """Interactive JSONL boundary for one app-server turn.

    Implementations own process I/O but not protocol policy.  They MUST send
    only the lines supplied by ``plan``, resolve ``thread/start`` before
    building the turn line, enforce all budgets while reading, interrupt the
    active turn on cancellation, and return bounded complete JSONL lines.
    """

    def exchange(
        self,
        plan: CodexJsonlPlan,
        *,
        timeout_seconds: float,
        max_line_bytes: int,
        max_total_bytes: int,
        max_events: int,
        cancel_requested: CancelRequested,
    ) -> CodexJsonlOutcome: ...


@dataclass(frozen=True)
class CodexAppServerConfig:
    timeout_seconds: float = 900.0
    max_prompt_bytes: int = 262_144
    max_line_bytes: int = 262_144
    max_events: int = 4_096
    hard_max_output_bytes: int = 1_048_576

    def validate(self) -> None:
        _validated_timeout(self.timeout_seconds)
        _validated_byte_limit(self.max_prompt_bytes, "codex_prompt_limit_invalid")
        _validated_byte_limit(self.max_line_bytes, "codex_line_limit_invalid")
        _validated_byte_limit(
            self.hard_max_output_bytes, "codex_output_limit_invalid"
        )
        if self.max_events <= 0 or self.max_events > 100_000:
            raise SupervisorError("codex_event_limit_invalid")


class CodexAppServerAdapter:
    """Bounded Codex app-server JSONL client with no implicit process launch."""

    def __init__(
        self,
        transport: CodexJsonlTransport,
        *,
        config: CodexAppServerConfig | None = None,
    ) -> None:
        self.transport = transport
        self.config = config or CodexAppServerConfig()
        self.config.validate()

    def run(
        self,
        *,
        payload: str,
        task: TaskRecord,
        conversation_id: str | None,
        max_output_bytes: int,
        cancel_requested: CancelRequested,
    ) -> AdapterResult:
        _validated_task_target(task, "codex")
        prompt = _validated_payload(payload, self.config.max_prompt_bytes)
        payload_text = prompt.decode("utf-8")
        if conversation_id is not None:
            conversation_id = _validated_codex_thread_id(conversation_id)
        output_limit = min(
            _validated_byte_limit(max_output_bytes, "adapter_output_limit_invalid"),
            self.config.hard_max_output_bytes,
        )

        if cancel_requested():
            return _cancelled("codex_app_server_cancelled", conversation_id)

        plan = CodexJsonlPlan(
            payload=payload_text,
            conversation_id=conversation_id,
            client_user_message_id=task.task_id,
        )
        try:
            outcome = self.transport.exchange(
                plan,
                timeout_seconds=self.config.timeout_seconds,
                max_line_bytes=min(self.config.max_line_bytes, output_limit),
                max_total_bytes=output_limit,
                max_events=self.config.max_events,
                cancel_requested=cancel_requested,
            )
        except Exception as exc:
            raise AdapterUnavailable("codex_app_server_transport_error") from exc

        resolved_thread_id = outcome.thread_id or conversation_id
        if resolved_thread_id is not None:
            try:
                resolved_thread_id = _validated_codex_thread_id(resolved_thread_id)
            except SupervisorError:
                return _failed("codex_thread_id_invalid")
        if conversation_id and resolved_thread_id != conversation_id:
            return _failed("codex_thread_id_mismatch", conversation_id=conversation_id)

        if outcome.status == TransportStatus.CANCELLED or cancel_requested():
            return _cancelled("codex_app_server_cancelled", resolved_thread_id)
        if outcome.status == TransportStatus.TIMED_OUT:
            return _failed(
                "codex_app_server_timeout",
                retryable=True,
                conversation_id=resolved_thread_id,
            )
        if outcome.status == TransportStatus.OUTPUT_LIMIT:
            return _failed(
                "codex_app_server_output_limit", conversation_id=resolved_thread_id
            )
        if outcome.status == TransportStatus.UNAVAILABLE:
            return _blocked("codex_app_server_unavailable", resolved_thread_id)
        if outcome.status != TransportStatus.COMPLETED:
            return _failed(
                "codex_app_server_transport_failed",
                retryable=True,
                conversation_id=resolved_thread_id,
            )

        return self._parse_completed_exchange(
            outcome.lines,
            expected_thread_id=resolved_thread_id,
            max_output_bytes=output_limit,
        )

    def _parse_completed_exchange(
        self,
        lines: tuple[bytes, ...],
        *,
        expected_thread_id: str | None,
        max_output_bytes: int,
    ) -> AdapterResult:
        total_bytes = 0
        agent_messages: list[str] = []
        terminal_status: str | None = None
        terminal_seen = False
        response_ids: set[int] = set()
        thread_id_from_response: str | None = None

        if len(lines) > self.config.max_events:
            return _failed(
                "codex_app_server_event_limit",
                conversation_id=expected_thread_id,
            )

        for raw_line in lines:
            if not isinstance(raw_line, bytes):
                return _failed(
                    "codex_app_server_protocol_error",
                    conversation_id=expected_thread_id,
                )
            if len(raw_line) > min(self.config.max_line_bytes, max_output_bytes):
                return _failed(
                    "codex_app_server_output_limit",
                    conversation_id=expected_thread_id,
                )
            total_bytes += len(raw_line)
            if total_bytes > max_output_bytes:
                return _failed(
                    "codex_app_server_output_limit",
                    conversation_id=expected_thread_id,
                )
            try:
                message = json.loads(raw_line)
            except (UnicodeDecodeError, json.JSONDecodeError):
                return _failed(
                    "codex_app_server_protocol_error",
                    conversation_id=expected_thread_id,
                )
            if not isinstance(message, dict):
                return _failed(
                    "codex_app_server_protocol_error",
                    conversation_id=expected_thread_id,
                )

            message_id = message.get("id")
            method = message.get("method")
            if method is not None and message_id is not None:
                # Server-initiated approvals/input requests must never be
                # guessed at by this unattended adapter.
                return _blocked(
                    "codex_server_request_unsupported", expected_thread_id
                )
            if message_id is not None:
                if not isinstance(message_id, int) or message_id not in (0, 1, 2):
                    return _failed(
                        "codex_app_server_response_id_invalid",
                        conversation_id=expected_thread_id,
                    )
                if message_id in response_ids or ("result" in message) == ("error" in message):
                    return _failed(
                        "codex_app_server_protocol_error",
                        conversation_id=expected_thread_id,
                    )
                response_ids.add(message_id)
                if "error" in message:
                    return _failed(
                        "codex_app_server_remote_error",
                        retryable=_codex_error_retryable(message["error"]),
                        conversation_id=expected_thread_id,
                    )
                if message_id == 1:
                    thread_id_from_response = _thread_id_from_result(message.get("result"))
                    if thread_id_from_response is None:
                        return _failed("codex_thread_id_missing")
                    if expected_thread_id and thread_id_from_response != expected_thread_id:
                        return _failed(
                            "codex_thread_id_mismatch",
                            conversation_id=expected_thread_id,
                        )
                continue

            if not isinstance(method, str) or not isinstance(message.get("params"), dict):
                return _failed(
                    "codex_app_server_protocol_error",
                    conversation_id=expected_thread_id,
                )
            params = message["params"]
            event_thread_id = params.get("threadId")
            if (
                event_thread_id is not None
                and expected_thread_id is not None
                and event_thread_id != expected_thread_id
            ):
                return _failed(
                    "codex_thread_id_mismatch", conversation_id=expected_thread_id
                )
            if method == "item/completed":
                item = params.get("item")
                if isinstance(item, dict) and item.get("type") == "agentMessage":
                    text = item.get("text")
                    if not isinstance(text, str):
                        return _failed(
                            "codex_app_server_protocol_error",
                            conversation_id=expected_thread_id,
                        )
                    agent_messages.append(text)
            elif method == "turn/completed":
                if terminal_seen:
                    return _failed(
                        "codex_app_server_protocol_error",
                        conversation_id=expected_thread_id,
                    )
                turn = params.get("turn")
                if not isinstance(turn, dict) or not isinstance(turn.get("status"), str):
                    return _failed(
                        "codex_app_server_protocol_error",
                        conversation_id=expected_thread_id,
                    )
                terminal_status = turn["status"]
                terminal_seen = True

        resolved_thread_id = expected_thread_id or thread_id_from_response
        if not {0, 1, 2}.issubset(response_ids) or not terminal_seen:
            return _failed(
                "codex_app_server_incomplete",
                retryable=True,
                conversation_id=resolved_thread_id,
            )
        if terminal_status == "interrupted":
            return _cancelled("codex_turn_interrupted", resolved_thread_id)
        if terminal_status != "completed":
            return _failed(
                "codex_turn_failed", conversation_id=resolved_thread_id
            )
        if not agent_messages:
            return _failed(
                "codex_agent_message_missing", conversation_id=resolved_thread_id
            )

        summary = agent_messages[-1]
        if len(summary.encode("utf-8")) > max_output_bytes:
            return _failed(
                "codex_app_server_output_limit", conversation_id=resolved_thread_id
            )
        return AdapterResult(
            status=AdapterStatus.SUCCEEDED,
            summary=summary,
            conversation_id=resolved_thread_id,
            safe_metrics={
                "event_count": len(lines),
                "wire_bytes": total_bytes,
                "agent_message_count": len(agent_messages),
            },
        )


class UiNudgeCommand(StrEnum):
    INVOKE = "invoke"


@dataclass(frozen=True)
class UiNudgeTarget:
    selector: str
    command: UiNudgeCommand

    def __post_init__(self) -> None:
        if (
            not isinstance(self.selector, str)
            or not self.selector
            or len(self.selector) > 256
            or "\x00" in self.selector
        ):
            raise SupervisorError("ui_nudge_selector_invalid")
        if not isinstance(self.command, UiNudgeCommand):
            raise SupervisorError("ui_nudge_command_invalid")


@dataclass(frozen=True)
class UiNudgeConfig:
    enabled: bool = False
    allowed_targets: frozenset[UiNudgeTarget] = field(default_factory=frozenset)
    timeout_seconds: float = 5.0

    def validate(self) -> None:
        if not isinstance(self.enabled, bool):
            raise SupervisorError("ui_nudge_enabled_invalid")
        _validated_timeout(self.timeout_seconds)
        if not isinstance(self.allowed_targets, frozenset):
            raise SupervisorError("ui_nudge_allowlist_invalid")


@dataclass(frozen=True)
class UiNudgeOutcome:
    status: TransportStatus
    result_code: str = "completed"


class UiNudgeExecutor(Protocol):
    """Exact-selector UI boundary; text, coordinates, and scripts are absent."""

    def execute_exact(
        self,
        *,
        selector: str,
        command: UiNudgeCommand,
        timeout_seconds: float,
        cancel_requested: CancelRequested,
    ) -> UiNudgeOutcome: ...


class UiNudgeAdapter:
    """Disabled-by-default, pairwise-allowlisted UI nudge."""

    def __init__(
        self,
        executor: UiNudgeExecutor,
        *,
        config: UiNudgeConfig | None = None,
    ) -> None:
        self.executor = executor
        self.config = config or UiNudgeConfig()
        self.config.validate()

    def nudge(
        self,
        target: UiNudgeTarget,
        *,
        cancel_requested: CancelRequested,
    ) -> AdapterResult:
        if not self.config.enabled:
            raise AdapterUnavailable("ui_nudge_disabled")
        if target not in self.config.allowed_targets:
            raise SupervisorError("ui_nudge_contract_denied")
        if cancel_requested():
            return _cancelled("ui_nudge_cancelled")
        try:
            outcome = self.executor.execute_exact(
                selector=target.selector,
                command=target.command,
                timeout_seconds=self.config.timeout_seconds,
                cancel_requested=cancel_requested,
            )
        except Exception as exc:
            raise AdapterUnavailable("ui_nudge_transport_error") from exc
        if outcome.status == TransportStatus.CANCELLED or cancel_requested():
            return _cancelled("ui_nudge_cancelled")
        if outcome.status == TransportStatus.TIMED_OUT:
            return _failed("ui_nudge_timeout", retryable=True)
        if outcome.status == TransportStatus.UNAVAILABLE:
            return _blocked("ui_nudge_unavailable")
        if outcome.status != TransportStatus.COMPLETED:
            return _failed("ui_nudge_failed")
        if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", outcome.result_code):
            return _failed("ui_nudge_result_invalid")
        return AdapterResult(
            status=AdapterStatus.SUCCEEDED,
            summary="ui_nudge_completed",
            safe_metrics={
                "command": target.command.value,
                "result_code": outcome.result_code,
            },
        )


def _claude_session_id(conversation_id: str | None, run_id: str) -> str:
    if conversation_id is not None:
        return _validated_uuid(conversation_id, "claude_session_id_invalid")
    run_uuid = uuid.UUID(_validated_uuid(run_id, "run_id_invalid"))
    return str(uuid.uuid5(run_uuid, "cccp:claude"))


def _validated_task_target(task: TaskRecord, expected: str) -> None:
    if task.target_agent != expected:
        raise SupervisorError("adapter_target_mismatch")


def _validated_payload(payload: str, max_bytes: int) -> bytes:
    if not isinstance(payload, str):
        raise SupervisorError("adapter_payload_invalid")
    encoded = payload.encode("utf-8")
    if not encoded:
        raise SupervisorError("adapter_payload_empty")
    if len(encoded) > max_bytes:
        raise SupervisorError("adapter_payload_too_large")
    return encoded


def _validated_executable(value: str) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise SupervisorError("claude_executable_invalid")
    return value


def _validated_working_directory(value: str) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise SupervisorError("claude_working_directory_invalid")
    path = Path(value).resolve()
    if not path.is_dir():
        raise SupervisorError("claude_working_directory_invalid")
    return str(path)


def _validated_command(command: Sequence[str]) -> tuple[str, ...]:
    if isinstance(command, (str, bytes)):
        raise SupervisorError("process_command_invalid")
    argv = tuple(command)
    if not argv:
        raise SupervisorError("process_command_invalid")
    for part in argv:
        if not isinstance(part, str) or not part or "\x00" in part:
            raise SupervisorError("process_command_invalid")
    return argv


def _write_all_and_close(pipe, data: bytes, io_failed: threading.Event) -> None:
    try:
        pipe.write(data)
        pipe.flush()
    except (BrokenPipeError, OSError):
        # A child may intentionally exit without consuming all stdin.  Its
        # return code remains the authoritative outcome.
        pass
    except Exception:
        io_failed.set()
    finally:
        try:
            pipe.close()
        except OSError:
            pass


def _read_bounded(
    pipe,
    destination: bytearray,
    limit: int,
    overflow: threading.Event,
    io_failed: threading.Event,
) -> None:
    try:
        while True:
            chunk = pipe.read(8_192)
            if not chunk:
                return
            remaining = limit - len(destination)
            if remaining > 0:
                destination.extend(chunk[:remaining])
            if len(chunk) > remaining:
                overflow.set()
                return
    except (OSError, ValueError):
        # Closing an owned pipe is expected during termination.
        return
    except Exception:
        io_failed.set()


def _terminate_owned_process(
    process: subprocess.Popen[bytes], grace_seconds: float
) -> None:
    if process.poll() is not None:
        return
    try:
        process.terminate()
    except OSError:
        pass
    try:
        process.wait(timeout=grace_seconds)
        return
    except subprocess.TimeoutExpired:
        pass
    try:
        process.kill()
    except OSError:
        pass
    try:
        process.wait(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        # No broad fallback (taskkill/pkill) is allowed: ownership remains the
        # exact child handle, and the caller receives a failed transport.
        pass


def _validated_timeout(value: float) -> float:
    if not isinstance(value, (int, float)) or not 0 < value <= _MAX_TIMEOUT_SECONDS:
        raise SupervisorError("adapter_timeout_invalid")
    return float(value)


def _validated_byte_limit(value: int, code: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 < value <= _MAX_CONFIGURED_BYTES:
        raise SupervisorError(code)
    return value


def _validated_uuid(value: str, code: str) -> str:
    try:
        return str(uuid.UUID(value))
    except (ValueError, AttributeError, TypeError) as exc:
        raise SupervisorError(code) from exc


def _validated_codex_thread_id(value: str) -> str:
    if not isinstance(value, str) or not _CODEX_THREAD_ID_RE.fullmatch(value):
        raise SupervisorError("codex_thread_id_invalid")
    return value


def _jsonl(message: dict[str, object]) -> bytes:
    return (
        json.dumps(message, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _thread_id_from_result(result: object) -> str | None:
    if not isinstance(result, dict):
        return None
    thread = result.get("thread")
    if not isinstance(thread, dict):
        return None
    thread_id = thread.get("id")
    if not isinstance(thread_id, str):
        return None
    try:
        return _validated_codex_thread_id(thread_id)
    except SupervisorError:
        return None


def _codex_error_retryable(error: object) -> bool:
    if not isinstance(error, dict):
        return False
    return error.get("code") == -32001


def _cancelled(code: str, conversation_id: str | None = None) -> AdapterResult:
    return AdapterResult(
        status=AdapterStatus.CANCELLED,
        summary=code,
        failure_code=code,
        conversation_id=conversation_id,
    )


def _blocked(code: str, conversation_id: str | None = None) -> AdapterResult:
    return AdapterResult(
        status=AdapterStatus.BLOCKED,
        summary=code,
        failure_code=code,
        conversation_id=conversation_id,
    )


def _failed(
    code: str,
    *,
    retryable: bool = False,
    conversation_id: str | None = None,
    **metrics: int,
) -> AdapterResult:
    return AdapterResult(
        status=AdapterStatus.FAILED,
        summary=code,
        failure_code=code,
        retryable=retryable,
        conversation_id=conversation_id,
        safe_metrics=metrics,
    )
