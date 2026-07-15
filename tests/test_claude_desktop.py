from __future__ import annotations

import json
import os
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

from cccp_supervisor.claude_desktop import (
    ClaudeDesktopBuild,
    bind_claude_desktop_session,
    canonical_session_uri,
    focus_claude_desktop_session,
    parse_session_link,
    WindowsClaudeDesktopLauncher,
    WindowsClaudeDesktopProbe,
)
from cccp_supervisor.errors import SupervisorError
from cccp_supervisor.files import canonical_json_bytes, sha256_bytes
from cccp_supervisor.models import RunPolicy
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
DRIFTED_BUILD = ClaudeDesktopBuild(
    package_name="Claude",
    package_version="1.20186.8.0",
    package_family="Claude_pzs8sxrjxfjjc",
    bundle_sha256="1" * 64,
    protocol_progid="AppXaem4n1tckgw588q10avtdbzpbgt71c77",
    app_user_model_id="Claude_pzs8sxrjxfjjc!Claude",
)
SESSION_ID = "session_ABCDEFGHIJKLMNOPQRSTUVWX"
SESSION_LINK = f"https://claude.ai/code/{SESSION_ID}"


class FakeProbe:
    def __init__(self, build: ClaudeDesktopBuild = SUPPORTED_BUILD) -> None:
        self.build = build
        self.calls = 0

    def inspect(self) -> ClaudeDesktopBuild:
        self.calls += 1
        return self.build


class SequenceProbe:
    def __init__(self, *builds: ClaudeDesktopBuild) -> None:
        self.builds = list(builds)

    def inspect(self) -> ClaudeDesktopBuild:
        if not self.builds:
            raise AssertionError("unexpected extra probe")
        return self.builds.pop(0)


class StopOnSecondProbe:
    def __init__(self, coop_root: Path) -> None:
        self.coop_root = coop_root
        self.calls = 0

    def inspect(self) -> ClaudeDesktopBuild:
        self.calls += 1
        if self.calls == 2:
            (self.coop_root / "STOP.md").write_text("stop", encoding="utf-8")
        return SUPPORTED_BUILD


class FakeLauncher:
    def __init__(self, *, accepted: bool = True, fail: bool = False) -> None:
        self.accepted = accepted
        self.fail = fail
        self.calls: list[str] = []
        self.before_dispatch = None

    def dispatch(
        self,
        uri: str,
        *,
        expected_progid: str,
        expected_app_user_model_id: str,
    ) -> bool:
        if self.before_dispatch is not None:
            self.before_dispatch()
        self.calls.append(uri)
        if self.fail:
            raise OSError("synthetic launch failure")
        return self.accepted


class FakeClock:
    def __init__(self, value: float = 1_000.0) -> None:
        self.value = value

    def __call__(self) -> float:
        return self.value


class StopAfterIntentStore(StateStore):
    def reserve_claude_desktop_focus(self, run_id: str, focus_id: str) -> bool:
        allowed = super().reserve_claude_desktop_focus(run_id, focus_id)
        if allowed:
            (self.coop_root / "STOP.md").write_text("stop", encoding="utf-8")
        return allowed


class ClaudeDesktopLinkTests(unittest.TestCase):
    def test_supported_link_forms_canonicalize_to_one_exact_uri(self) -> None:
        links = (
            SESSION_LINK,
            f"claude://claude.ai/code/{SESSION_ID}",
            SESSION_LINK + "\r\n",
        )
        for link in links:
            with self.subTest(link=link):
                session_id = parse_session_link(link)
                self.assertEqual(SESSION_ID, session_id)
                self.assertEqual(
                    f"claude://claude.ai/code/{SESSION_ID}",
                    canonical_session_uri(session_id),
                )

    def test_cse_bridge_id_is_supported(self) -> None:
        value = "cse_1234567890abcdef"
        self.assertEqual(value, parse_session_link(f"https://claude.ai/code/{value}"))

    def test_adversarial_links_are_rejected(self) -> None:
        bad_links = (
            "https://claude.ai/code/new",
            f"https://claude.ai/code/{SESSION_ID}?q=send",
            f"https://claude.ai/code/{SESSION_ID}?",
            f"https://claude.ai/code/{SESSION_ID}#fragment",
            f"https://claude.ai/code/{SESSION_ID}/extra",
            f"https://claude.ai/code/{SESSION_ID}/",
            f"https://user@claude.ai/code/{SESSION_ID}",
            f"https://claude.ai:443/code/{SESSION_ID}",
            f"https://code.claude.ai/code/{SESSION_ID}",
            f"https://claude.ai.evil.invalid/code/{SESSION_ID}",
            f"http://claude.ai/code/{SESSION_ID}",
            f"https://claude.ai/code/session_abc%2fdefghijklmnop",
            f"https://claude.ai/code/session_abc\\defghijklmnop",
            f"https://claude.ai/code/{SESSION_ID}\nsecond",
            f" https://claude.ai/code/{SESSION_ID}",
            f"https://claude。ai/code/{SESSION_ID}",
            "claude://code/new",
            f"claude://code/{SESSION_ID}",
            "claude://code/session_short",
            "claude://cowork/session_ABCDEFGHIJKLMNOP",
        )
        for link in bad_links:
            with self.subTest(link=link):
                with self.assertRaises(SupervisorError):
                    parse_session_link(link)

    def test_windows_launcher_accepts_only_internal_canonical_uri(self) -> None:
        execute = mock.Mock(return_value=33)
        shell32 = mock.Mock()
        shell32.ShellExecuteW = execute
        with mock.patch(
            "cccp_supervisor.claude_desktop._current_claude_protocol_handler",
            return_value=(
                SUPPORTED_BUILD.protocol_progid,
                SUPPORTED_BUILD.app_user_model_id,
            ),
        ), mock.patch(
            "cccp_supervisor.claude_desktop.ctypes.WinDLL", return_value=shell32
        ):
            self.assertTrue(
                WindowsClaudeDesktopLauncher().dispatch(
                    f"claude://claude.ai/code/{SESSION_ID}",
                    expected_progid=SUPPORTED_BUILD.protocol_progid,
                    expected_app_user_model_id=SUPPORTED_BUILD.app_user_model_id,
                )
            )
        execute.assert_called_once_with(
            None, "open", f"claude://claude.ai/code/{SESSION_ID}", None, None, 1
        )
        with mock.patch(
            "cccp_supervisor.claude_desktop.ctypes.WinDLL"
        ) as win_dll:
            with self.assertRaises(SupervisorError):
                WindowsClaudeDesktopLauncher().dispatch(
                    f"https://claude.ai/code/{SESSION_ID}",
                    expected_progid=SUPPORTED_BUILD.protocol_progid,
                    expected_app_user_model_id=SUPPORTED_BUILD.app_user_model_id,
                )
            win_dll.assert_not_called()

    def test_windows_launcher_rejects_wrong_current_handler(self) -> None:
        with mock.patch(
            "cccp_supervisor.claude_desktop._current_claude_protocol_handler",
            return_value=("AppXattacker", "Other_publisher!App"),
        ), mock.patch(
            "cccp_supervisor.claude_desktop.ctypes.WinDLL"
        ) as win_dll:
            with self.assertRaisesRegex(
                SupervisorError, "claude_desktop_protocol_handler_mismatch"
            ):
                WindowsClaudeDesktopLauncher().dispatch(
                    f"claude://claude.ai/code/{SESSION_ID}",
                    expected_progid=SUPPORTED_BUILD.protocol_progid,
                    expected_app_user_model_id=SUPPORTED_BUILD.app_user_model_id,
                )
            win_dll.assert_not_called()

    @unittest.skipUnless(
        os.environ.get("CCCP_TEST_INSTALLED_CLAUDE") == "1",
        "opt-in installed Claude Desktop probe",
    )
    def test_installed_desktop_build_matches_release_pin(self) -> None:
        build = WindowsClaudeDesktopProbe().inspect()
        build.require_supported()
        self.assertEqual(SUPPORTED_BUILD, build)


class ClaudeDesktopBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.coop = Path(self.temp.name) / "coop"
        self.coop.mkdir()
        self.clock = FakeClock()
        self.store = StateStore(self.coop, clock=self.clock)
        self.run_id = self.store.init_run(
            project_alias="fixture",
            policy=RunPolicy(
                claude_desktop_focus_enabled=True,
                claude_desktop_focus_cooldown_seconds=600,
            ),
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def bind(self):
        return bind_claude_desktop_session(
            self.store,
            run_id=self.run_id,
            raw_link=SESSION_LINK,
            probe=FakeProbe(),
        )

    def test_bind_is_deterministic_create_only_and_local(self) -> None:
        first = self.bind()
        second = self.bind()
        self.assertTrue(first.created)
        self.assertFalse(second.created)
        self.assertEqual(first.profile_sha256, second.profile_sha256)
        self.assertEqual(first.session_ref, second.session_ref)
        profile_path = (
            self.store.state_root
            / "profiles"
            / "claude-desktop"
            / f"{self.run_id}.json"
        )
        self.assertTrue(profile_path.is_file())
        self.assertIn(SESSION_ID, profile_path.read_text(encoding="utf-8"))

    def test_same_session_ref_is_scoped_to_one_run(self) -> None:
        first = self.bind()
        other = Path(self.temp.name) / "other-ref"
        other.mkdir()
        store = StateStore(other, clock=self.clock)
        run_id = store.init_run(
            project_alias="other",
            policy=RunPolicy(claude_desktop_focus_enabled=True),
        )
        second = bind_claude_desktop_session(
            store,
            run_id=run_id,
            raw_link=SESSION_LINK,
            probe=FakeProbe(),
        )
        self.assertNotEqual(first.session_ref, second.session_ref)

    def test_uppercase_uuid_argument_uses_canonical_run_profile(self) -> None:
        upper_run_id = self.run_id.upper()
        receipt = bind_claude_desktop_session(
            self.store,
            run_id=upper_run_id,
            raw_link=SESSION_LINK,
            probe=FakeProbe(),
        )
        self.assertTrue(receipt.created)
        canonical_path = (
            self.store.state_root
            / "profiles"
            / "claude-desktop"
            / f"{self.run_id}.json"
        )
        self.assertTrue(canonical_path.is_file())
        self.assertEqual(
            self.run_id,
            json.loads(canonical_path.read_text(encoding="utf-8"))["run_id"],
        )
        self.assertEqual(
            1, len(list(canonical_path.parent.glob("*.json")))
        )

    def test_bind_rejects_policy_off_before_probe_or_profile(self) -> None:
        other = Path(self.temp.name) / "other"
        other.mkdir()
        store = StateStore(other, clock=self.clock)
        run_id = store.init_run(project_alias="off")
        probe = FakeProbe()
        with self.assertRaisesRegex(
            SupervisorError, "claude_desktop_focus_policy_disabled"
        ):
            bind_claude_desktop_session(
                store, run_id=run_id, raw_link=SESSION_LINK, probe=probe
            )
        self.assertEqual(0, probe.calls)

    def test_unsupported_build_never_creates_profile(self) -> None:
        with self.assertRaisesRegex(
            SupervisorError, "claude_desktop_build_unsupported"
        ):
            bind_claude_desktop_session(
                self.store,
                run_id=self.run_id,
                raw_link=SESSION_LINK,
                probe=FakeProbe(DRIFTED_BUILD),
            )
        profile_dir = self.store.state_root / "profiles"
        self.assertFalse(profile_dir.exists())

    def test_different_binding_cannot_replace_existing_profile(self) -> None:
        self.bind()
        with self.assertRaisesRegex(
            SupervisorError, "claude_desktop_profile_conflict"
        ):
            bind_claude_desktop_session(
                self.store,
                run_id=self.run_id,
                raw_link="https://claude.ai/code/cse_1234567890abcdef",
                probe=FakeProbe(),
            )

    def test_focus_records_intent_before_one_canonical_dispatch(self) -> None:
        binding = self.bind()
        focus_id = str(uuid.uuid4())
        launcher = FakeLauncher()

        def assert_intent_exists() -> None:
            with self.store._connect() as connection:
                row = connection.execute(
                    "SELECT state FROM claude_desktop_focus_receipts "
                    "WHERE focus_id=?",
                    (focus_id,),
                ).fetchone()
            self.assertIsNotNone(row)
            self.assertEqual("intent_recorded", row["state"])

        launcher.before_dispatch = assert_intent_exists
        receipt = focus_claude_desktop_session(
            self.store,
            run_id=self.run_id,
            focus_id=focus_id,
            expected_profile_sha256=binding.profile_sha256,
            expected_session_ref=binding.session_ref,
            probe=FakeProbe(),
            launcher=launcher,
        )
        self.assertEqual(
            [f"claude://claude.ai/code/{SESSION_ID}"], launcher.calls
        )
        self.assertEqual("focus_requested_unverified", receipt.navigation_state)
        self.assertTrue(receipt.navigation_requested)
        self.assertFalse(receipt.message_sent)
        self.assertFalse(receipt.turn_started)
        self.assertFalse(receipt.completion_observed)

    def test_duplicate_id_never_dispatches_twice(self) -> None:
        binding = self.bind()
        focus_id = str(uuid.uuid4())
        launcher = FakeLauncher()
        arguments = {
            "run_id": self.run_id,
            "focus_id": focus_id,
            "expected_profile_sha256": binding.profile_sha256,
            "expected_session_ref": binding.session_ref,
            "probe": FakeProbe(),
            "launcher": launcher,
        }
        focus_claude_desktop_session(self.store, **arguments)
        with self.assertRaisesRegex(
            SupervisorError, "claude_desktop_focus_not_allowed"
        ):
            focus_claude_desktop_session(self.store, **arguments)
        self.assertEqual(1, len(launcher.calls))

    def test_different_id_is_still_bounded_by_cooldown(self) -> None:
        binding = self.bind()
        launcher = FakeLauncher()
        for index in range(2):
            kwargs = {
                "run_id": self.run_id,
                "focus_id": str(uuid.uuid4()),
                "expected_profile_sha256": binding.profile_sha256,
                "expected_session_ref": binding.session_ref,
                "probe": FakeProbe(),
                "launcher": launcher,
            }
            if index == 0:
                focus_claude_desktop_session(self.store, **kwargs)
            else:
                with self.assertRaisesRegex(
                    SupervisorError, "claude_desktop_focus_not_allowed"
                ):
                    focus_claude_desktop_session(self.store, **kwargs)
        self.assertEqual(1, len(launcher.calls))

    def test_stop_after_intent_blocks_dispatch_and_replay(self) -> None:
        stopping_store = StopAfterIntentStore(self.coop, clock=self.clock)
        binding = self.bind()
        focus_id = str(uuid.uuid4())
        launcher = FakeLauncher()
        kwargs = {
            "run_id": self.run_id,
            "focus_id": focus_id,
            "expected_profile_sha256": binding.profile_sha256,
            "expected_session_ref": binding.session_ref,
            "probe": FakeProbe(),
            "launcher": launcher,
        }
        with self.assertRaisesRegex(
            SupervisorError, "claude_desktop_focus_cancelled"
        ):
            focus_claude_desktop_session(stopping_store, **kwargs)
        self.assertEqual([], launcher.calls)
        with self.assertRaises(SupervisorError):
            focus_claude_desktop_session(stopping_store, **kwargs)
        self.assertEqual([], launcher.calls)

    def test_build_drift_hash_or_ref_mismatch_blocks_before_intent(self) -> None:
        binding = self.bind()
        launcher = FakeLauncher()
        cases = (
            ("0" * 64, binding.session_ref, FakeProbe()),
            (binding.profile_sha256, "cds_" + "0" * 24, FakeProbe()),
            (binding.profile_sha256, binding.session_ref, FakeProbe(DRIFTED_BUILD)),
        )
        for profile_hash, ref, probe in cases:
            with self.subTest(profile_hash=profile_hash, ref=ref):
                with self.assertRaises(SupervisorError):
                    focus_claude_desktop_session(
                        self.store,
                        run_id=self.run_id,
                        focus_id=str(uuid.uuid4()),
                        expected_profile_sha256=profile_hash,
                        expected_session_ref=ref,
                        probe=probe,
                        launcher=launcher,
                    )
        self.assertEqual([], launcher.calls)
        with self.store._connect() as connection:
            self.assertEqual(
                0,
                connection.execute(
                    "SELECT COUNT(*) FROM claude_desktop_focus_receipts"
                ).fetchone()[0],
            )

    def test_build_update_after_intent_is_consumed_without_dispatch(self) -> None:
        binding = self.bind()
        focus_id = str(uuid.uuid4())
        launcher = FakeLauncher()
        kwargs = {
            "run_id": self.run_id,
            "focus_id": focus_id,
            "expected_profile_sha256": binding.profile_sha256,
            "expected_session_ref": binding.session_ref,
            "probe": SequenceProbe(SUPPORTED_BUILD, DRIFTED_BUILD),
            "launcher": launcher,
        }
        with self.assertRaisesRegex(SupervisorError, "claude_desktop_build_drift"):
            focus_claude_desktop_session(self.store, **kwargs)
        self.assertEqual([], launcher.calls)
        with self.assertRaisesRegex(
            SupervisorError, "claude_desktop_focus_not_allowed"
        ):
            focus_claude_desktop_session(
                self.store,
                **{**kwargs, "probe": FakeProbe()},
            )
        self.assertEqual([], launcher.calls)

    def test_noncanonical_or_extended_profile_is_rejected(self) -> None:
        binding = self.bind()
        profile_path = (
            self.store.state_root
            / "profiles"
            / "claude-desktop"
            / f"{self.run_id}.json"
        )
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        profile["prompt"] = "type this"
        data = canonical_json_bytes(profile)
        profile_path.write_bytes(data)
        launcher = FakeLauncher()
        with self.assertRaisesRegex(SupervisorError, "claude_desktop_profile_invalid"):
            focus_claude_desktop_session(
                self.store,
                run_id=self.run_id,
                focus_id=str(uuid.uuid4()),
                expected_profile_sha256=sha256_bytes(data),
                expected_session_ref=binding.session_ref,
                probe=FakeProbe(),
                launcher=launcher,
            )
        self.assertEqual([], launcher.calls)

    def test_rejected_or_failed_dispatch_is_not_retried(self) -> None:
        for launcher in (FakeLauncher(accepted=False), FakeLauncher(fail=True)):
            with self.subTest(launcher=launcher):
                # Each case uses a fresh run because one uncertain intent must
                # never be reset merely to retry it.
                with tempfile.TemporaryDirectory() as temp:
                    coop = Path(temp) / "coop"
                    coop.mkdir()
                    store = StateStore(coop, clock=FakeClock())
                    run_id = store.init_run(
                        project_alias="fixture",
                        policy=RunPolicy(
                            claude_desktop_focus_enabled=True,
                        ),
                    )
                    binding = bind_claude_desktop_session(
                        store,
                        run_id=run_id,
                        raw_link=SESSION_LINK,
                        probe=FakeProbe(),
                    )
                    focus_id = str(uuid.uuid4())
                    kwargs = {
                        "run_id": run_id,
                        "focus_id": focus_id,
                        "expected_profile_sha256": binding.profile_sha256,
                        "expected_session_ref": binding.session_ref,
                        "probe": FakeProbe(),
                        "launcher": launcher,
                    }
                    with self.assertRaises(SupervisorError):
                        focus_claude_desktop_session(store, **kwargs)
                    with self.assertRaisesRegex(
                        SupervisorError, "claude_desktop_focus_not_allowed"
                    ):
                        focus_claude_desktop_session(store, **kwargs)
                    self.assertEqual(1, len(launcher.calls))

    def test_stop_during_final_probe_blocks_dispatch(self) -> None:
        binding = self.bind()
        focus_id = str(uuid.uuid4())
        launcher = FakeLauncher()
        with self.assertRaisesRegex(
            SupervisorError, "claude_desktop_focus_cancelled"
        ):
            focus_claude_desktop_session(
                self.store,
                run_id=self.run_id,
                focus_id=focus_id,
                expected_profile_sha256=binding.profile_sha256,
                expected_session_ref=binding.session_ref,
                probe=StopOnSecondProbe(self.coop),
                launcher=launcher,
            )
        self.assertEqual([], launcher.calls)
        with self.store._connect() as connection:
            row = connection.execute(
                "SELECT state,result_code FROM claude_desktop_focus_receipts "
                "WHERE focus_id=?",
                (focus_id,),
            ).fetchone()
        self.assertEqual("completed", row["state"])
        self.assertEqual("cancelled_before_dispatch", row["result_code"])


if __name__ == "__main__":
    unittest.main()
