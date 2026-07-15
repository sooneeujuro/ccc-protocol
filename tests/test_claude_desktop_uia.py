from __future__ import annotations

import tempfile
import unittest
from dataclasses import dataclass, field
from pathlib import Path
from unittest.mock import patch

from cccp_supervisor.claude_desktop import ClaudeDesktopBuild
from cccp_supervisor.claude_desktop_uia import (
    BoundClaudeDesktopSendPort,
    ClaudeDesktopExactSessionMessenger,
    ClaudeDesktopUiaBinding,
    PywinautoUiaBackend,
    SemanticSelector,
    restricted_wake_text,
)
from cccp_supervisor.errors import SupervisorError


PID = 4242
WINDOW = SemanticSelector("Window", "", "Claude")
SURFACE = SemanticSelector("Group", "", "기본 창")
SESSION = SemanticSelector("Button", "", "C1 shadow-manifest review")
WORKSPACE = SemanticSelector("Button", "", "Synthetic Workspace")
GROUP = SemanticSelector("Group", "", "프롬프트")
PROMPT_TEXT = SemanticSelector("Text", "", "\n")
EDIT = SemanticSelector("Edit", "PromptEditor", "Write a message")
SEND = SemanticSelector("Button", "send-message", "Send message")
WAKE_ID = "11111111-1111-4111-8111-111111111111"
WAKE = restricted_wake_text(WAKE_ID)
PINNED_BUILD = ClaudeDesktopBuild(
    package_name="Claude",
    package_version="1.21459.0.0",
    package_family="Claude_pzs8sxrjxfjjc",
    bundle_sha256=(
        "d9a896beca555b86e6e773c065b75d3bc21c246f260578a42ca532e76fa155bd"
    ),
    protocol_progid="AppXaem4n1tckgw588q10avtdbzpbgt71c77",
    app_user_model_id="Claude_pzs8sxrjxfjjc!Claude",
)


class FakeBuildProbe:
    def __init__(self, build: ClaudeDesktopBuild = PINNED_BUILD) -> None:
        self.build = build
        self.calls = 0

    def inspect(self) -> ClaudeDesktopBuild:
        self.calls += 1
        return self.build


@dataclass
class FakeElement:
    semantic: SemanticSelector
    runtime_id: tuple[int, ...]
    pid: int = PID
    children: list["FakeElement"] = field(default_factory=list)
    visible: bool = True
    enabled: bool = True
    value: str = ""
    focused: bool = False


class FakeBackend:
    def __init__(self) -> None:
        self.window = FakeElement(WINDOW, (1,))
        self.surface = FakeElement(SURFACE, (2,))
        self.session = FakeElement(SESSION, (3,))
        self.workspace = FakeElement(WORKSPACE, (4,))
        self.group = FakeElement(GROUP, (5,))
        self.text = FakeElement(PROMPT_TEXT, (6,))
        self.edit = FakeElement(EDIT, (7,))
        self.send = FakeElement(SEND, (8,), enabled=False)
        self.global_session = FakeElement(SESSION, (9,))
        self.global_workspace = FakeElement(WORKSPACE, (10,))
        self.group.children = [self.text]
        self.surface.children = [
            self.session,
            self.workspace,
            self.group,
            self.send,
        ]
        # Real Desktop exposes duplicate title/workspace controls outside the
        # unique semantic surface.  They must not make the surface ambiguous.
        self.window.children = [
            self.global_session,
            self.global_workspace,
            self.surface,
        ]
        self.windows = [self.window]
        self.enumeration_calls = 0
        self.image = str((Path(tempfile.gettempdir()) / "Claude.exe").resolve())
        self.set_calls: list[str] = []
        self.focus_calls = 0
        self.type_calls: list[str] = []
        self.invoke_calls = 0
        self.mismatch_after_input = False
        self.focus_confirmed = True
        self.enable_send_after_input = True
        self.raise_on_invoke = False
        self.after_input = None

    def top_level_windows(self):
        self.enumeration_calls += 1
        return tuple(self.windows)

    def descendants(self, element):
        result = []
        pending = list(element.children)
        while pending:
            child = pending.pop(0)
            result.append(child)
            pending[0:0] = child.children
        return tuple(result)

    @staticmethod
    def selector(element):
        return element.semantic

    @staticmethod
    def process_id(element):
        return element.pid

    def process_image(self, process_id):
        self.last_process_image_pid = process_id
        return self.image

    @staticmethod
    def identity(element):
        return element.runtime_id

    @staticmethod
    def is_visible(element):
        return element.visible

    @staticmethod
    def is_enabled(element):
        return element.enabled

    @staticmethod
    def value(element):
        return element.value

    def set_value(self, element, value):
        self.set_calls.append(value)
        element.value = value + ("!" if self.mismatch_after_input else "")
        if self.enable_send_after_input:
            self.send.enabled = True
        if self.after_input is not None:
            self.after_input()

    def set_focus(self, element):
        self.focus_calls += 1
        element.focused = self.focus_confirmed

    @staticmethod
    def has_keyboard_focus(element):
        return element.focused

    def type_vk_packet(self, element, value):
        self.type_calls.append(value)
        rendered = value + ("!" if self.mismatch_after_input else "")
        self.text.semantic = SemanticSelector("Text", "", rendered)
        if self.enable_send_after_input:
            self.send.enabled = True
        if self.after_input is not None:
            self.after_input()

    def invoke(self, element):
        self.invoke_calls += 1
        if self.raise_on_invoke:
            raise RuntimeError("synthetic invoke ambiguity")


def focused_binding(backend: FakeBackend) -> ClaudeDesktopUiaBinding:
    return ClaudeDesktopUiaBinding(
        process_id=PID,
        process_image=backend.image,
        desktop_build=PINNED_BUILD,
        window=WINDOW,
        surface=SURFACE,
        session_title=SESSION,
        workspace=WORKSPACE,
        prompt_group=GROUP,
        send_button=SEND,
        input_mode="focused_vk_packet",
        prompt_text=PROMPT_TEXT,
    )


def value_binding(backend: FakeBackend) -> ClaudeDesktopUiaBinding:
    backend.group.children = [backend.edit]
    return ClaudeDesktopUiaBinding(
        process_id=PID,
        process_image=backend.image,
        desktop_build=PINNED_BUILD,
        window=WINDOW,
        surface=SURFACE,
        session_title=SESSION,
        workspace=WORKSPACE,
        prompt_group=GROUP,
        send_button=SEND,
        input_mode="value_pattern",
        prompt_edit=EDIT,
    )


class ClaudeDesktopUiaTests(unittest.TestCase):
    def assert_code(self, code: str):
        return self.assertRaisesRegex(SupervisorError, f"^{code}$")

    def send(self, backend: FakeBackend, **kwargs):
        messenger = kwargs.pop(
            "messenger",
            ClaudeDesktopExactSessionMessenger(
                backend, build_probe=FakeBuildProbe()
            ),
        )
        return messenger.send(
            binding=kwargs.pop("binding", focused_binding(backend)),
            prompt=kwargs.pop("prompt", WAKE),
            cancel_requested=kwargs.pop("cancel_requested", lambda: False),
            **kwargs,
        )

    def test_actual_surface_shape_types_vk_packet_then_invokes_once(self) -> None:
        backend = FakeBackend()
        self.assertFalse(backend.send.enabled)
        receipt = self.send(backend)
        self.assertEqual(1, backend.focus_calls)
        self.assertEqual([WAKE], backend.type_calls)
        self.assertEqual([], backend.set_calls)
        self.assertEqual(1, backend.invoke_calls)
        self.assertTrue(backend.send.enabled)
        self.assertEqual("message_send_requested_unverified", receipt.state)
        self.assertTrue(receipt.message_send_requested)
        self.assertFalse(receipt.turn_started)
        self.assertFalse(receipt.completion_observed)

    def test_bound_send_port_accepts_only_message_id_derived_wake(self) -> None:
        backend = FakeBackend()
        port = BoundClaudeDesktopSendPort(
            focused_binding(backend),
            ClaudeDesktopExactSessionMessenger(
                backend, build_probe=FakeBuildProbe()
            ),
        )
        self.assertTrue(
            port.send_message(
                message=WAKE,
                message_id=WAKE_ID,
                cancel_requested=lambda: False,
            )
        )
        self.assertEqual(1, backend.invoke_calls)

        other_message = restricted_wake_text(
            "22222222-2222-4222-8222-222222222222"
        )
        with self.assert_code("claude_desktop_uia_wake_text_not_allowed"):
            port.send_message(
                message=other_message,
                message_id=WAKE_ID,
                cancel_requested=lambda: False,
            )

    def test_global_duplicate_title_and_workspace_are_scoped_by_surface(self) -> None:
        backend = FakeBackend()
        self.send(backend)
        self.assertEqual(1, backend.invoke_calls)

    def test_surface_title_workspace_prompt_and_send_are_unique(self) -> None:
        cases = (
            (backend_attr, selector, code)
            for backend_attr, selector, code in (
                ("surface", SURFACE, "claude_desktop_uia_surface_ambiguous"),
                ("session", SESSION, "claude_desktop_uia_session_title_ambiguous"),
                ("workspace", WORKSPACE, "claude_desktop_uia_workspace_ambiguous"),
                ("group", GROUP, "claude_desktop_uia_prompt_group_ambiguous"),
                ("send", SEND, "claude_desktop_uia_send_button_ambiguous"),
            )
        )
        for attr, selector, code in cases:
            backend = FakeBackend()
            duplicate = FakeElement(selector, (100 + len(attr),))
            if attr == "surface":
                backend.window.children.append(duplicate)
            else:
                backend.surface.children.append(duplicate)
            with self.subTest(control=attr), self.assert_code(code):
                self.send(backend)
            self.assertEqual(0, backend.invoke_calls)

    def test_wrong_surface_session_or_workspace_fails_closed(self) -> None:
        for attr, code in (
            ("surface", "claude_desktop_uia_surface_missing"),
            ("session", "claude_desktop_uia_session_title_missing"),
            ("workspace", "claude_desktop_uia_workspace_missing"),
        ):
            backend = FakeBackend()
            target = getattr(backend, attr)
            parent = backend.window if attr == "surface" else backend.surface
            parent.children.remove(target)
            with self.subTest(control=attr), self.assert_code(code):
                self.send(backend)
            self.assertEqual(0, backend.invoke_calls)

    def test_keyboard_focus_must_be_confirmed(self) -> None:
        backend = FakeBackend()
        backend.focus_confirmed = False
        with self.assert_code("claude_desktop_uia_focus_unconfirmed"):
            self.send(backend)
        self.assertEqual([], backend.type_calls)
        self.assertEqual(0, backend.invoke_calls)

    def test_text_readback_must_match_exactly(self) -> None:
        backend = FakeBackend()
        backend.mismatch_after_input = True
        with self.assert_code("claude_desktop_uia_prompt_verification_failed"):
            self.send(backend)
        self.assertEqual([WAKE], backend.type_calls)
        self.assertEqual(0, backend.invoke_calls)

    def test_existing_draft_is_not_typed_over(self) -> None:
        backend = FakeBackend()
        backend.text.semantic = SemanticSelector("Text", "", "operator draft\n")
        with self.assert_code("claude_desktop_uia_composer_not_empty"):
            self.send(backend)
        self.assertEqual([], backend.type_calls)
        self.assertEqual(0, backend.invoke_calls)

    def test_initially_enabled_send_signals_nontext_composer_content(self) -> None:
        backend = FakeBackend()
        backend.send.enabled = True
        with self.assert_code("claude_desktop_uia_composer_not_empty"):
            self.send(backend)
        self.assertEqual([], backend.type_calls)
        self.assertEqual(0, backend.invoke_calls)

    def test_pinned_build_is_checked_before_ui_enumeration(self) -> None:
        backend = FakeBackend()
        drifted = ClaudeDesktopBuild(
            package_name="Claude",
            package_version="1.20186.7.0",
            package_family="Claude_pzs8sxrjxfjjc",
            bundle_sha256=(
                "63355bc0fafca4d3eaa3fd53bbd372104820d30006a0bf27df792a78598e0655"
            ),
            protocol_progid="AppXaem4n1tckgw588q10avtdbzpbgt71c77",
            app_user_model_id="Claude_pzs8sxrjxfjjc!Claude",
        )
        probe = FakeBuildProbe(drifted)
        messenger = ClaudeDesktopExactSessionMessenger(
            backend, build_probe=probe
        )
        with self.assert_code("claude_desktop_build_drift"):
            self.send(backend, messenger=messenger)
        self.assertEqual(1, probe.calls)
        self.assertEqual(0, backend.enumeration_calls)
        self.assertEqual([], backend.type_calls)
        self.assertEqual(0, backend.invoke_calls)

    def test_rerender_or_session_switch_after_typing_blocks_invoke(self) -> None:
        for case in ("runtime", "session"):
            backend = FakeBackend()
            if case == "runtime":
                backend.after_input = lambda: setattr(backend.send, "runtime_id", (999,))
                code = "claude_desktop_uia_context_changed"
            else:
                backend.after_input = lambda: setattr(
                    backend.session,
                    "semantic",
                    SemanticSelector("Button", "", "Other task"),
                )
                code = "claude_desktop_uia_session_title_missing"
            with self.subTest(case=case), self.assert_code(code):
                self.send(backend)
            self.assertEqual(0, backend.invoke_calls)

    def test_disabled_or_cross_process_control_never_sends(self) -> None:
        for case, code in (
            ("disabled", "claude_desktop_uia_control_disabled"),
            ("process", "claude_desktop_uia_process_mismatch"),
        ):
            backend = FakeBackend()
            if case == "disabled":
                backend.enable_send_after_input = False
            else:
                backend.send.pid = PID + 1
            with self.subTest(case=case), self.assert_code(code):
                self.send(backend)
            self.assertEqual(0, backend.invoke_calls)

    def test_same_process_must_have_one_visible_top_window(self) -> None:
        backend = FakeBackend()
        backend.windows.append(
            FakeElement(SemanticSelector("Window", "", "Unexpected dialog"), (50,))
        )
        with self.assert_code("claude_desktop_uia_window_ambiguous"):
            self.send(backend)
        self.assertEqual(0, backend.invoke_calls)

    def test_process_image_and_window_selector_are_exact(self) -> None:
        for case, code in (
            ("image", "claude_desktop_uia_process_mismatch"),
            ("window", "claude_desktop_uia_window_mismatch"),
        ):
            backend = FakeBackend()
            expected = focused_binding(backend)
            if case == "image":
                backend.image = str(Path("C:/Other.exe"))
            else:
                backend.window.semantic = SemanticSelector("Window", "", "Other")
            with self.subTest(case=case), self.assert_code(code):
                self.send(backend, binding=expected)

    def test_only_generated_short_wake_text_is_allowed(self) -> None:
        backend = FakeBackend()
        letter_id = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
        uppercase_id = restricted_wake_text(letter_id).replace(
            letter_id, letter_id.upper()
        )
        for text in (
            "read this raw handoff",
            WAKE + " EXTRA",
            uppercase_id,
        ):
            with self.subTest(text=text), self.assert_code(
                "claude_desktop_uia_wake_text_not_allowed"
            ):
                self.send(backend, prompt=text)
        self.assertEqual([], backend.type_calls)
        self.assertEqual(0, backend.invoke_calls)

    def test_value_pattern_mode_remains_available_without_clipboard(self) -> None:
        backend = FakeBackend()
        receipt = self.send(backend, binding=value_binding(backend))
        self.assertEqual([WAKE], backend.set_calls)
        self.assertEqual([], backend.type_calls)
        self.assertEqual(1, backend.invoke_calls)
        self.assertEqual("message_send_requested_unverified", receipt.state)

    def test_cancel_before_input_or_before_invoke_never_sends(self) -> None:
        backend = FakeBackend()
        with self.assert_code("claude_desktop_uia_cancelled"):
            self.send(backend, cancel_requested=lambda: True)
        self.assertEqual([], backend.type_calls)

        backend = FakeBackend()
        calls = 0

        def cancel_after_input() -> bool:
            nonlocal calls
            calls += 1
            return calls >= 4

        with self.assert_code("claude_desktop_uia_cancelled_before_invoke"):
            self.send(backend, cancel_requested=cancel_after_input)
        self.assertEqual([WAKE], backend.type_calls)
        self.assertEqual(0, backend.invoke_calls)

    def test_invoke_exception_is_ambiguous_and_not_retried(self) -> None:
        backend = FakeBackend()
        backend.raise_on_invoke = True
        with self.assert_code("claude_desktop_uia_send_ambiguous"):
            self.send(backend)
        self.assertEqual(1, backend.invoke_calls)

    def test_pywinauto_is_optional_and_loaded_lazily(self) -> None:
        with patch(
            "cccp_supervisor.claude_desktop_uia.importlib.import_module",
            side_effect=ImportError,
        ):
            with self.assert_code("claude_desktop_uia_unavailable"):
                PywinautoUiaBackend()


if __name__ == "__main__":
    unittest.main()
