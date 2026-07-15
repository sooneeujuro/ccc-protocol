from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path

from cccp_supervisor.cli import main


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


if __name__ == "__main__":
    unittest.main()
