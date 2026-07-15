from __future__ import annotations

import io
import json
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

from cccp_supervisor.claude_desktop import ClaudeDesktopBuild
from cccp_supervisor.cli import main
from cccp_supervisor.store import StateStore


SUPPORTED_BUILD = ClaudeDesktopBuild(
    package_name="Claude",
    package_version="1.20186.7.0",
    package_family="Claude_pzs8sxrjxfjjc",
    bundle_sha256=(
        "63355bc0fafca4d3eaa3fd53bbd372104820d30006a0bf27df792a78598e0655"
    ),
    protocol_progid="AppXaem4n1tckgw588q10avtdbzpbgt71c77",
    app_user_model_id="Claude_pzs8sxrjxfjjc!Claude",
)


class CliFakeProbe:
    def inspect(self) -> ClaudeDesktopBuild:
        return SUPPORTED_BUILD


class CliFakeLauncher:
    calls: list[str] = []

    def dispatch(
        self,
        uri: str,
        *,
        expected_progid: str,
        expected_app_user_model_id: str,
    ) -> bool:
        self.calls.append(uri)
        return True


class CliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.coop = Path(self.temp.name) / "coop"
        self.coop.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def call(self, argv: list[str], payload: str = ""):
        stdout = io.StringIO()
        stderr = io.StringIO()
        code = main(
            argv,
            stdin=io.StringIO(payload),
            stdout=stdout,
            stderr=stderr,
        )
        out = json.loads(stdout.getvalue()) if stdout.getvalue() else None
        err = json.loads(stderr.getvalue()) if stderr.getvalue() else None
        return code, out, err, stdout.getvalue() + stderr.getvalue()

    def init(self) -> str:
        code, out, err, _ = self.call(
            [
                "init",
                "--coop-root",
                str(self.coop),
                "--project-alias",
                "fixture",
            ]
        )
        self.assertEqual(0, code, err)
        return out["run_id"]

    def test_init_enqueue_and_status_outputs_are_scrubbed(self) -> None:
        run_id = self.init()
        private_payload = "snippet https://example.invalid C:/private/source.pdf"
        code, out, err, rendered = self.call(
            [
                "enqueue",
                "--coop-root",
                str(self.coop),
                "--run-id",
                run_id,
                "--target",
                "claude",
                "--idempotency-key",
                "task-1",
            ],
            private_payload,
        )
        self.assertEqual(0, code, err)
        self.assertTrue(out["created"])
        self.assertNotIn("snippet", rendered)
        self.assertNotIn("example.invalid", rendered)
        self.assertNotIn("private", rendered)

        code, out, err, rendered = self.call(
            [
                "status",
                "--coop-root",
                str(self.coop),
                "--run-id",
                run_id,
            ]
        )
        self.assertEqual(0, code, err)
        self.assertEqual(1, out["task_counts"]["queued"])
        self.assertNotIn("snippet", rendered)
        self.assertNotIn("example.invalid", rendered)
        self.assertNotIn("fixture", rendered)
        self.assertIn("project_ref", out)

    def test_live_adapter_requires_two_explicit_flags(self) -> None:
        run_id = self.init()
        self.call(
            [
                "enqueue",
                "--coop-root",
                str(self.coop),
                "--target",
                "claude",
                "--idempotency-key",
                "task-1",
            ],
            "safe task",
        )
        code, out, err, _ = self.call(
            [
                "run-once",
                "--coop-root",
                str(self.coop),
                "--run-id",
                run_id,
                "--agent",
                "claude",
                "--enable-claude-cli",
            ]
        )
        self.assertEqual(2, code)
        self.assertIsNone(out)
        self.assertEqual("live_adapter_confirmation_required", err["failure_code"])
        code, status, _, _ = self.call(
            ["status", "--coop-root", str(self.coop), "--run-id", run_id]
        )
        self.assertEqual(0, code)
        self.assertEqual(1, status["task_counts"]["queued"])

        code, _, err, _ = self.call(
            [
                "run-once",
                "--coop-root",
                str(self.coop),
                "--run-id",
                run_id,
                "--agent",
                "claude",
                "--enable-claude-cli",
                "--confirm-live-agent-call",
            ]
        )
        self.assertEqual(2, code)
        self.assertEqual("live_adapter_profile_not_bound", err["failure_code"])

    def test_codex_contract_is_not_claimed_as_live_transport(self) -> None:
        run_id = self.init()
        code, _, err, _ = self.call(
            [
                "run-once",
                "--coop-root",
                str(self.coop),
                "--run-id",
                run_id,
                "--agent",
                "codex",
            ]
        )
        self.assertEqual(2, code)
        self.assertEqual("codex_adapter_not_enabled", err["failure_code"])

    def test_stop_reports_actual_terminal_state(self) -> None:
        run_id = self.init()
        code, out, err, _ = self.call(
            [
                "stop",
                "--coop-root",
                str(self.coop),
                "--run-id",
                run_id,
                "--requested-by",
                "operator",
                "--reason-code",
                "operator_stop",
            ]
        )
        self.assertEqual(0, code, err)
        self.assertEqual("stopped", out["state"])
        code, status, err, _ = self.call(
            ["status", "--coop-root", str(self.coop)]
        )
        self.assertEqual(0, code, err)
        self.assertEqual("stopped", status["state"])

    def test_missing_root_fails_without_creating_it(self) -> None:
        missing = Path(self.temp.name) / "typo"
        code, _, err, _ = self.call(
            [
                "init",
                "--coop-root",
                str(missing),
                "--project-alias",
                "fixture",
            ]
        )
        self.assertEqual(2, code)
        self.assertEqual("coop_root_missing", err["failure_code"])
        self.assertFalse(missing.exists())

    @mock.patch(
        "cccp_supervisor.cli.WindowsClaudeDesktopProbe",
        return_value=CliFakeProbe(),
    )
    def test_desktop_binding_and_focus_receipts_are_scrubbed(self, _probe) -> None:
        code, out, err, _ = self.call(
            [
                "init",
                "--coop-root",
                str(self.coop),
                "--project-alias",
                "fixture",
                "--allow-claude-desktop-focus",
            ]
        )
        self.assertEqual(0, code, err)
        run_id = out["run_id"]
        session_id = "session_ABCDEFGHIJKLMNOPQRSTUVWX"
        raw_link = f"https://claude.ai/code/{session_id}\n"
        code, binding, err, rendered = self.call(
            [
                "bind-claude-desktop-session",
                "--coop-root",
                str(self.coop),
                "--run-id",
                run_id,
                "--confirm-pinned-desktop-route",
            ],
            raw_link,
        )
        self.assertEqual(0, code, err)
        self.assertNotIn(session_id, rendered)
        self.assertNotIn("claude.ai", rendered)
        self.assertFalse(binding["message_send_supported"])

        CliFakeLauncher.calls = []
        with mock.patch(
            "cccp_supervisor.cli.WindowsClaudeDesktopLauncher",
            return_value=CliFakeLauncher(),
        ):
            code, focused, err, rendered = self.call(
                [
                    "focus-claude-desktop-session",
                    "--coop-root",
                    str(self.coop),
                    "--run-id",
                    run_id,
                    "--focus-id",
                    str(uuid.uuid4()),
                    "--profile-sha256",
                    binding["profile_sha256"],
                    "--session-ref",
                    binding["session_ref"],
                    "--enable-claude-desktop-focus",
                    "--confirm-focus-only",
                ]
            )
        self.assertEqual(0, code, err)
        self.assertEqual("focus_requested_unverified", focused["navigation_state"])
        self.assertTrue(focused["navigation_requested"])
        self.assertFalse(focused["message_sent"])
        self.assertFalse(focused["turn_started"])
        self.assertFalse(focused["completion_observed"])
        self.assertNotIn(session_id, rendered)
        self.assertNotIn("claude.ai", rendered)
        self.assertEqual(
            [f"claude://claude.ai/code/{session_id}"], CliFakeLauncher.calls
        )

    @mock.patch(
        "cccp_supervisor.cli.WindowsClaudeDesktopProbe",
        return_value=CliFakeProbe(),
    )
    def test_desktop_focus_requires_all_explicit_gates(self, _probe) -> None:
        code, out, err, _ = self.call(
            [
                "init",
                "--coop-root",
                str(self.coop),
                "--project-alias",
                "fixture",
                "--allow-claude-desktop-focus",
            ]
        )
        self.assertEqual(0, code, err)
        run_id = out["run_id"]
        code, binding, err, _ = self.call(
            [
                "bind-claude-desktop-session",
                "--coop-root",
                str(self.coop),
                "--run-id",
                run_id,
                "--confirm-pinned-desktop-route",
            ],
            "https://claude.ai/code/session_ABCDEFGHIJKLMNOPQRSTUVWX",
        )
        self.assertEqual(0, code, err)
        code, _, err, _ = self.call(
            [
                "focus-claude-desktop-session",
                "--coop-root",
                str(self.coop),
                "--run-id",
                run_id,
                "--focus-id",
                str(uuid.uuid4()),
                "--profile-sha256",
                binding["profile_sha256"],
                "--session-ref",
                binding["session_ref"],
                "--enable-claude-desktop-focus",
            ]
        )
        self.assertEqual(2, code)
        self.assertEqual(
            "claude_desktop_focus_confirmation_required", err["failure_code"]
        )


if __name__ == "__main__":
    unittest.main()
