from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import asdict
from pathlib import Path
from typing import IO, Sequence

from .claude_desktop import (
    WindowsClaudeDesktopLauncher,
    WindowsClaudeDesktopProbe,
    bind_claude_desktop_session,
    focus_claude_desktop_session,
)
from .errors import SupervisorError
from .models import EffectClass, RunPolicy
from .store import StateStore
from .supervisor import Supervisor


def main(
    argv: Sequence[str] | None = None,
    *,
    stdin: IO[str] | None = None,
    stdout: IO[str] | None = None,
    stderr: IO[str] | None = None,
) -> int:
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        value = args.handler(args, stdin)
    except SupervisorError as exc:
        _print_json(stderr, {"ok": False, "failure_code": exc.code})
        return 2
    except (OSError, UnicodeError, ValueError):
        _print_json(stderr, {"ok": False, "failure_code": "local_io_error"})
        return 2
    if value is not None:
        _print_json(stdout, value)
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ccc-supervisor",
        description="Deterministic local CCCP lifecycle supervisor",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="create one local run")
    _coop_argument(init)
    init.add_argument("--project-alias", required=True)
    init.add_argument("--run-id")
    init.add_argument("--lease-ttl", type=_positive_int, default=120)
    init.add_argument("--claim-ttl", type=_positive_int, default=1_200)
    init.add_argument("--watch-ttl", type=_positive_int, default=86_400)
    init.add_argument("--max-wakes", type=_positive_int, default=100)
    init.add_argument("--max-depth", type=_positive_int, default=8)
    init.add_argument("--max-handoffs", type=_positive_int, default=4)
    init.add_argument("--max-payload-bytes", type=_positive_int, default=262_144)
    init.add_argument("--max-output-bytes", type=_positive_int, default=1_048_576)
    init.add_argument("--allow-timer-wakes", action="store_true")
    init.add_argument("--allow-claude-desktop-focus", action="store_true")
    init.add_argument(
        "--desktop-focus-cooldown", type=_positive_int, default=600
    )
    init.set_defaults(handler=_init)

    enqueue = commands.add_parser(
        "enqueue", help="read one UTF-8 task payload from stdin"
    )
    _coop_argument(enqueue)
    enqueue.add_argument("--run-id")
    enqueue.add_argument("--target", required=True, choices=("claude", "codex"))
    enqueue.add_argument("--idempotency-key", required=True)
    enqueue.add_argument("--kind", default="task")
    enqueue.add_argument(
        "--effect",
        choices=tuple(value.value for value in EffectClass),
        default=EffectClass.READ_ONLY.value,
    )
    enqueue.add_argument("--max-attempts", type=_positive_int)
    enqueue.set_defaults(handler=_enqueue)

    once = commands.add_parser("run-once", help="dispatch at most one queued task")
    _coop_argument(once)
    once.add_argument("--run-id")
    once.add_argument("--agent", required=True, choices=("claude", "codex"))
    once.add_argument("--wake-id")
    once.add_argument("--source", default="operator")
    _live_adapter_arguments(once)
    once.set_defaults(handler=_run_once)

    serve = commands.add_parser(
        "serve", help="run a finite number of local polling cycles"
    )
    _coop_argument(serve)
    serve.add_argument("--run-id")
    serve.add_argument("--max-cycles", required=True, type=_positive_int)
    serve.add_argument("--poll-seconds", type=_positive_float, default=1.0)
    _live_adapter_arguments(serve)
    serve.set_defaults(handler=_serve)

    recover = commands.add_parser("recover", help="fence expired local work")
    _coop_argument(recover)
    recover.add_argument("--run-id")
    recover.set_defaults(handler=_recover)

    status = commands.add_parser("status", help="print scrubbed lifecycle status")
    _coop_argument(status)
    status.add_argument("--run-id")
    status.set_defaults(handler=_status)

    stop = commands.add_parser("stop", help="request monotonic STOP")
    _coop_argument(stop)
    stop.add_argument("--run-id")
    stop.add_argument("--requested-by", required=True)
    stop.add_argument("--reason-code", required=True)
    stop.set_defaults(handler=_stop)

    probe = commands.add_parser("probe", help="report adapter capability only")
    probe.add_argument("--claude-executable", default="claude")
    probe.set_defaults(handler=_probe)

    bind_desktop = commands.add_parser(
        "bind-claude-desktop-session",
        help="bind one copied Desktop Code session link from stdin",
    )
    _coop_argument(bind_desktop)
    bind_desktop.add_argument("--run-id")
    bind_desktop.add_argument("--confirm-pinned-desktop-route", action="store_true")
    bind_desktop.set_defaults(handler=_bind_claude_desktop_session)

    focus_desktop = commands.add_parser(
        "focus-claude-desktop-session",
        help="request focus for one bound Desktop Code session",
    )
    _coop_argument(focus_desktop)
    focus_desktop.add_argument("--run-id")
    focus_desktop.add_argument("--focus-id", required=True)
    focus_desktop.add_argument("--profile-sha256", required=True)
    focus_desktop.add_argument("--session-ref", required=True)
    focus_desktop.add_argument("--enable-claude-desktop-focus", action="store_true")
    focus_desktop.add_argument("--confirm-focus-only", action="store_true")
    focus_desktop.set_defaults(handler=_focus_claude_desktop_session)
    return parser


def _coop_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--coop-root", required=True, type=Path)


def _live_adapter_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--enable-claude-cli", action="store_true")
    parser.add_argument("--confirm-live-agent-call", action="store_true")
    parser.add_argument("--claude-executable", default="claude")
    parser.add_argument("--adapter-timeout", type=_positive_float, default=900.0)


def _store(args: argparse.Namespace) -> StateStore:
    root = args.coop_root.resolve()
    if not root.is_dir():
        raise SupervisorError("coop_root_missing")
    return StateStore(root)


def _run_id(store: StateStore, value: str | None) -> str:
    return value or store.active_run_id()


def _init(args: argparse.Namespace, _stdin: IO[str]) -> dict[str, object]:
    store = _store(args)
    policy = RunPolicy(
        lease_ttl_seconds=args.lease_ttl,
        claim_ttl_seconds=args.claim_ttl,
        watch_ttl_seconds=args.watch_ttl,
        max_wakes_per_agent=args.max_wakes,
        max_handoff_depth=args.max_depth,
        max_handoffs_per_result=args.max_handoffs,
        max_payload_bytes=args.max_payload_bytes,
        max_output_bytes=args.max_output_bytes,
        auto_wake_allowed=args.allow_timer_wakes,
        claude_desktop_focus_enabled=args.allow_claude_desktop_focus,
        claude_desktop_focus_cooldown_seconds=args.desktop_focus_cooldown,
    )
    run_id = store.init_run(
        project_alias=args.project_alias,
        policy=policy,
        run_id=args.run_id,
    )
    return {"ok": True, "run_id": run_id, "state": "active"}


def _enqueue(args: argparse.Namespace, stdin: IO[str]) -> dict[str, object]:
    store = _store(args)
    run_id = _run_id(store, args.run_id)
    limit = store.run_row(run_id)["max_payload_bytes"]
    payload = _read_stdin_utf8(stdin, limit)
    if not payload:
        raise SupervisorError("payload_empty")
    task, created = store.enqueue_task(
        run_id=run_id,
        target_agent=args.target,
        payload=payload,
        idempotency_key=args.idempotency_key,
        effect_class=EffectClass(args.effect),
        kind=args.kind,
        max_attempts=args.max_attempts,
    )
    return {
        "ok": True,
        "run_id": run_id,
        "task_id": task.task_id,
        "created": created,
        "state": task.state.value,
    }


def _run_once(args: argparse.Namespace, _stdin: IO[str]) -> dict[str, object]:
    store = _store(args)
    run_id = _run_id(store, args.run_id)
    adapters = _adapters(args)
    if args.agent not in adapters:
        raise SupervisorError(f"{args.agent}_adapter_not_enabled")
    outcome = Supervisor(store, adapters).run_once(
        run_id=run_id,
        agent_id=args.agent,
        wake_id=args.wake_id,
        source=args.source,
    )
    return {"ok": outcome.status not in ("dispatch_failed", "blocked"), **asdict(outcome)}


def _serve(args: argparse.Namespace, _stdin: IO[str]) -> dict[str, object]:
    store = _store(args)
    run_id = _run_id(store, args.run_id)
    adapters = _adapters(args)
    if not adapters:
        raise SupervisorError("no_live_adapter_enabled")
    dispatched = Supervisor(store, adapters).serve(
        run_id=run_id,
        poll_seconds=args.poll_seconds,
        max_cycles=args.max_cycles,
    )
    return {
        "ok": True,
        "run_id": run_id,
        "cycle_budget": args.max_cycles,
        "dispatched": dispatched,
    }


def _recover(args: argparse.Namespace, _stdin: IO[str]) -> dict[str, object]:
    store = _store(args)
    run_id = _run_id(store, args.run_id)
    return {"ok": True, "run_id": run_id, **store.recover(run_id)}


def _status(args: argparse.Namespace, _stdin: IO[str]) -> dict[str, object]:
    store = _store(args)
    return {"ok": True, **store.safe_status(args.run_id)}


def _stop(args: argparse.Namespace, _stdin: IO[str]) -> dict[str, object]:
    store = _store(args)
    run_id = _run_id(store, args.run_id)
    stop_id = store.request_stop(
        run_id=run_id,
        requested_by=args.requested_by,
        reason_code=args.reason_code,
    )
    return {
        "ok": True,
        "run_id": run_id,
        "stop_id": stop_id,
        "state": store.run_row(run_id)["state"],
    }


def _probe(args: argparse.Namespace, _stdin: IO[str]) -> dict[str, object]:
    return {
        "ok": True,
        "claude_cli": {
            "executable_resolvable": shutil.which(args.claude_executable) is not None,
            "live_call_enabled": False,
        },
        "codex_app_server": {
            "status": "transport_contract_only",
            "live_call_enabled": False,
        },
        "claude_desktop_session_focus": {
            "status": "contract_available_not_probed",
            "installed_build_checked": False,
            "live_call_enabled": False,
            "message_send_supported": False,
        },
        "ui_nudge": {"status": "disabled_by_default"},
    }


def _bind_claude_desktop_session(
    args: argparse.Namespace, stdin: IO[str]
) -> dict[str, object]:
    if not args.confirm_pinned_desktop_route:
        raise SupervisorError("claude_desktop_route_confirmation_required")
    store = _store(args)
    run_id = _run_id(store, args.run_id)
    raw_link = _read_stdin_utf8(stdin, 512)
    receipt = bind_claude_desktop_session(
        store,
        run_id=run_id,
        raw_link=raw_link,
        probe=WindowsClaudeDesktopProbe(),
    )
    return {
        "ok": True,
        "run_id": run_id,
        "profile_sha256": receipt.profile_sha256,
        "session_ref": receipt.session_ref,
        "created": receipt.created,
        "capability": "focus_only_unverified",
        "message_send_supported": False,
    }


def _focus_claude_desktop_session(
    args: argparse.Namespace, _stdin: IO[str]
) -> dict[str, object]:
    if not (args.enable_claude_desktop_focus and args.confirm_focus_only):
        raise SupervisorError("claude_desktop_focus_confirmation_required")
    store = _store(args)
    run_id = _run_id(store, args.run_id)
    receipt = focus_claude_desktop_session(
        store,
        run_id=run_id,
        focus_id=args.focus_id,
        expected_profile_sha256=args.profile_sha256,
        expected_session_ref=args.session_ref,
        probe=WindowsClaudeDesktopProbe(),
        launcher=WindowsClaudeDesktopLauncher(),
    )
    return {
        "ok": True,
        "run_id": run_id,
        "focus_id": args.focus_id,
        **asdict(receipt),
    }


def _adapters(args: argparse.Namespace):
    if args.enable_claude_cli != args.confirm_live_agent_call:
        raise SupervisorError("live_adapter_confirmation_required")
    if args.enable_claude_cli:
        # V1 ships the tested transport and adapter contract, but the CLI does
        # not infer a workspace/permission profile.  A maintainer-owned binding
        # must supply those values explicitly before this switch can go live.
        raise SupervisorError("live_adapter_profile_not_bound")
    return {}


def _read_stdin_utf8(stdin: IO[str], limit: int) -> str:
    binary = getattr(stdin, "buffer", None)
    if binary is not None:
        value = binary.read(limit + 1)
        if len(value) > limit:
            raise SupervisorError("payload_too_large")
        return value.decode("utf-8")
    value = stdin.read(limit + 1)
    if len(value.encode("utf-8")) > limit:
        raise SupervisorError("payload_too_large")
    return value


def _print_json(stream: IO[str], value: object) -> None:
    stream.write(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    )


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def _positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())
