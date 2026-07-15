from __future__ import annotations

import ctypes
import hashlib
import importlib
import os
import threading
import uuid
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .claude_desktop import (
    ClaudeDesktopBuild,
    DesktopBuildProbe,
    WindowsClaudeDesktopProbe,
)
from .errors import SupervisorError


_MAX_PROPERTY_BYTES = 2_048
_WAKE_PREFIX = "CCCP WAKE "
_WAKE_SUFFIX = " CHECK STOP RUN_STATE AND INBOX PROCESS ONE PENDING TASK ONLY"


@dataclass(frozen=True)
class SemanticSelector:
    """An exact UIA selector; no fuzzy labels, coordinates, or OCR."""

    control_type: str
    automation_id: str
    name: str

    def validate(self) -> None:
        values = (self.control_type, self.automation_id, self.name)
        if any(not isinstance(value, str) for value in values):
            raise SupervisorError("claude_desktop_uia_selector_invalid")
        if not self.control_type or not (self.automation_id or self.name):
            raise SupervisorError("claude_desktop_uia_selector_invalid")
        if any(
            "\x00" in value
            or len(value.encode("utf-8")) > _MAX_PROPERTY_BYTES
            for value in values
        ):
            raise SupervisorError("claude_desktop_uia_selector_invalid")


@dataclass(frozen=True)
class ClaudeDesktopUiaBinding:
    process_id: int
    process_image: str
    desktop_build: ClaudeDesktopBuild
    window: SemanticSelector
    surface: SemanticSelector
    session_title: SemanticSelector
    workspace: SemanticSelector
    prompt_group: SemanticSelector
    send_button: SemanticSelector
    input_mode: str
    prompt_edit: SemanticSelector | None = None
    prompt_text: SemanticSelector | None = None
    # The empty Chromium contenteditable is exposed as a Text element named
    # "\n".  After typing, the same element's accessible name is the exact
    # wake text without that placeholder newline.
    prompt_text_suffix: str = ""

    def validate(self) -> None:
        if (
            not isinstance(self.process_id, int)
            or isinstance(self.process_id, bool)
            or self.process_id <= 0
            or not isinstance(self.process_image, str)
            or not self.process_image
            or "\x00" in self.process_image
            or not Path(self.process_image).is_absolute()
        ):
            raise SupervisorError("claude_desktop_uia_binding_invalid")
        if not isinstance(self.desktop_build, ClaudeDesktopBuild):
            raise SupervisorError("claude_desktop_uia_binding_invalid")
        self.desktop_build.require_supported()
        selectors = (
            self.window,
            self.surface,
            self.session_title,
            self.workspace,
            self.prompt_group,
            self.send_button,
        )
        if any(not isinstance(selector, SemanticSelector) for selector in selectors):
            raise SupervisorError("claude_desktop_uia_binding_invalid")
        for selector in selectors:
            selector.validate()
        if self.input_mode not in ("value_pattern", "focused_vk_packet"):
            raise SupervisorError("claude_desktop_uia_binding_invalid")
        if self.input_mode == "value_pattern":
            if not isinstance(self.prompt_edit, SemanticSelector) or self.prompt_text is not None:
                raise SupervisorError("claude_desktop_uia_binding_invalid")
            self.prompt_edit.validate()
        else:
            if not isinstance(self.prompt_text, SemanticSelector) or self.prompt_edit is not None:
                raise SupervisorError("claude_desktop_uia_binding_invalid")
            self.prompt_text.validate()
            if (
                not isinstance(self.prompt_text_suffix, str)
                or "\x00" in self.prompt_text_suffix
                or len(self.prompt_text_suffix.encode("utf-8")) > 16
            ):
                raise SupervisorError("claude_desktop_uia_binding_invalid")
        if self.session_title == self.workspace:
            raise SupervisorError("claude_desktop_uia_binding_invalid")


@dataclass(frozen=True)
class ClaudeDesktopSendReceipt:
    state: str
    prompt_sha256: str
    prompt_bytes: int
    message_send_requested: bool = True
    turn_started: bool = False
    completion_observed: bool = False


class UiaBackend(Protocol):
    """Small testable boundary around pywinauto's UIA wrappers."""

    def top_level_windows(self) -> Sequence[object]: ...

    def descendants(self, element: object) -> Sequence[object]: ...

    def selector(self, element: object) -> SemanticSelector: ...

    def process_id(self, element: object) -> int: ...

    def process_image(self, process_id: int) -> str: ...

    def identity(self, element: object) -> tuple[int, ...]: ...

    def is_visible(self, element: object) -> bool: ...

    def is_enabled(self, element: object) -> bool: ...

    def value(self, element: object) -> str: ...

    def set_value(self, element: object, value: str) -> None: ...

    def set_focus(self, element: object) -> None: ...

    def has_keyboard_focus(self, element: object) -> bool: ...

    def type_vk_packet(self, element: object, value: str) -> None: ...

    def invoke(self, element: object) -> None: ...


@dataclass(frozen=True)
class _ResolvedControls:
    window: object
    surface: object
    session_title: object
    workspace: object
    prompt_group: object
    input_control: object
    send_button: object
    identities: tuple[tuple[int, ...], ...]


class ClaudeDesktopExactSessionMessenger:
    """Send once through a pinned Claude Desktop UIA surface.

    A successful return proves only that UIA Invoke was requested on the exact
    pinned send button.  It is deliberately not evidence that a model turn
    started or completed.
    """

    def __init__(
        self,
        backend: UiaBackend | None = None,
        *,
        build_probe: DesktopBuildProbe | None = None,
    ) -> None:
        self.backend = backend or PywinautoUiaBackend()
        self.build_probe = build_probe or WindowsClaudeDesktopProbe()
        self._lock = threading.Lock()

    def send(
        self,
        *,
        binding: ClaudeDesktopUiaBinding,
        prompt: str,
        cancel_requested: Callable[[], bool],
    ) -> ClaudeDesktopSendReceipt:
        binding.validate()
        prompt_bytes = _validated_wake_text(prompt)
        if not callable(cancel_requested):
            raise SupervisorError("claude_desktop_uia_cancel_callback_invalid")
        if not self._lock.acquire(blocking=False):
            raise SupervisorError("claude_desktop_uia_busy")
        try:
            if cancel_requested():
                raise SupervisorError("claude_desktop_uia_cancelled")
            # The UIA surface is version-specific and is not a public Claude
            # automation API.  Reuse the canonical package probe and compare it
            # with the build pinned into this exact session binding before the
            # first window/control enumeration or other UI action.
            current_build = self.build_probe.inspect()
            current_build.require_supported()
            if current_build != binding.desktop_build:
                raise SupervisorError("claude_desktop_build_drift")
            if cancel_requested():
                raise SupervisorError("claude_desktop_uia_cancelled")
            controls = self._resolve(binding)
            if cancel_requested():
                raise SupervisorError("claude_desktop_uia_cancelled")
            if binding.input_mode == "value_pattern":
                if self.backend.value(controls.input_control) != "":
                    raise SupervisorError("claude_desktop_uia_composer_not_empty")
                try:
                    self.backend.set_value(controls.input_control, prompt)
                except Exception as exc:
                    raise SupervisorError("claude_desktop_uia_prompt_set_failed") from exc
                try:
                    verified = self.backend.value(controls.input_control)
                except Exception as exc:
                    raise SupervisorError(
                        "claude_desktop_uia_prompt_verification_failed"
                    ) from exc
                if verified != prompt:
                    raise SupervisorError("claude_desktop_uia_prompt_verification_failed")
            else:
                try:
                    self.backend.set_focus(controls.prompt_group)
                    if not self.backend.has_keyboard_focus(controls.prompt_group):
                        raise SupervisorError("claude_desktop_uia_focus_unconfirmed")
                    self.backend.type_vk_packet(controls.prompt_group, prompt)
                except SupervisorError:
                    raise
                except Exception as exc:
                    raise SupervisorError("claude_desktop_uia_typing_failed") from exc
            if cancel_requested():
                raise SupervisorError("claude_desktop_uia_cancelled_before_invoke")

            # Resolve the entire semantic surface again immediately before the
            # irreversible Invoke.  A session switch, rerender, modal, or DOM
            # replacement consumes this attempt rather than targeting a new UI.
            final_controls = self._resolve(binding, expected_prompt=prompt)
            if final_controls.identities != controls.identities:
                raise SupervisorError("claude_desktop_uia_context_changed")
            if binding.input_mode == "value_pattern":
                if self.backend.value(final_controls.input_control) != prompt:
                    raise SupervisorError("claude_desktop_uia_prompt_verification_failed")
            if cancel_requested():
                raise SupervisorError("claude_desktop_uia_cancelled_before_invoke")
            try:
                self.backend.invoke(final_controls.send_button)
            except Exception as exc:
                # Invoke may have crossed the application boundary before the
                # local error.  Never retry this result automatically.
                raise SupervisorError("claude_desktop_uia_send_ambiguous") from exc
            return ClaudeDesktopSendReceipt(
                state="message_send_requested_unverified",
                prompt_sha256=hashlib.sha256(prompt_bytes).hexdigest(),
                prompt_bytes=len(prompt_bytes),
            )
        finally:
            self._lock.release()

    def _resolve(
        self,
        binding: ClaudeDesktopUiaBinding,
        *,
        expected_prompt: str | None = None,
    ) -> _ResolvedControls:
        try:
            all_windows = tuple(self.backend.top_level_windows())
        except Exception as exc:
            raise SupervisorError("claude_desktop_uia_enumeration_failed") from exc
        process_windows = tuple(
            window
            for window in all_windows
            if self.backend.process_id(window) == binding.process_id
            and self.backend.is_visible(window)
        )
        if not process_windows:
            raise SupervisorError("claude_desktop_uia_window_missing")
        if len(process_windows) != 1:
            raise SupervisorError("claude_desktop_uia_window_ambiguous")
        window = process_windows[0]
        if self.backend.selector(window) != binding.window:
            raise SupervisorError("claude_desktop_uia_window_mismatch")
        if _normalized_windows_path(self.backend.process_image(binding.process_id)) != (
            _normalized_windows_path(binding.process_image)
        ):
            raise SupervisorError("claude_desktop_uia_process_mismatch")

        descendants = tuple(self.backend.descendants(window))
        surface = self._require_unique(descendants, binding.surface, "surface")
        surface_descendants = tuple(self.backend.descendants(surface))
        session_title = self._require_unique(
            surface_descendants, binding.session_title, "session_title"
        )
        workspace = self._require_unique(
            surface_descendants, binding.workspace, "workspace"
        )
        prompt_group = self._require_unique(
            surface_descendants, binding.prompt_group, "prompt_group"
        )
        send_button = self._require_unique(
            surface_descendants, binding.send_button, "send_button"
        )
        group_descendants = tuple(self.backend.descendants(prompt_group))
        if binding.input_mode == "value_pattern":
            assert binding.prompt_edit is not None
            input_control = self._require_unique(
                group_descendants, binding.prompt_edit, "prompt_edit"
            )
        else:
            assert binding.prompt_text is not None
            input_control = self._require_prompt_text(
                group_descendants,
                binding.prompt_text,
                expected_name=(
                    binding.prompt_text.name
                    if expected_prompt is None
                    else expected_prompt + binding.prompt_text_suffix
                ),
                initial=expected_prompt is None,
            )
        for element in (
            surface,
            session_title,
            workspace,
            prompt_group,
            input_control,
            send_button,
        ):
            if self.backend.process_id(element) != binding.process_id:
                raise SupervisorError("claude_desktop_uia_process_mismatch")
            if not self.backend.is_visible(element):
                raise SupervisorError("claude_desktop_uia_control_not_visible")
        for element in (prompt_group, input_control):
            if not self.backend.is_enabled(element):
                raise SupervisorError("claude_desktop_uia_control_disabled")
        # Text readback alone cannot see a queued attachment or other composer
        # chip.  A truly empty composer must expose a disabled send button; it
        # may become enabled only after the exact restricted wake is present.
        send_enabled = self.backend.is_enabled(send_button)
        if expected_prompt is None and send_enabled:
            raise SupervisorError("claude_desktop_uia_composer_not_empty")
        if expected_prompt is not None and not send_enabled:
            raise SupervisorError("claude_desktop_uia_control_disabled")
        identities = tuple(
            self.backend.identity(element)
            for element in (
                window,
                surface,
                session_title,
                workspace,
                prompt_group,
                input_control,
                send_button,
            )
        )
        if any(not identity for identity in identities) or len(set(identities)) != 7:
            raise SupervisorError("claude_desktop_uia_identity_invalid")
        return _ResolvedControls(
            window,
            surface,
            session_title,
            workspace,
            prompt_group,
            input_control,
            send_button,
            identities,
        )

    def _require_unique(
        self,
        elements: Sequence[object],
        selector: SemanticSelector,
        label: str,
    ) -> object:
        matches = tuple(
            element for element in elements if self.backend.selector(element) == selector
        )
        if not matches:
            raise SupervisorError(f"claude_desktop_uia_{label}_missing")
        if len(matches) != 1:
            raise SupervisorError(f"claude_desktop_uia_{label}_ambiguous")
        return matches[0]

    def _require_prompt_text(
        self,
        elements: Sequence[object],
        selector: SemanticSelector,
        *,
        expected_name: str,
        initial: bool,
    ) -> object:
        matches = tuple(
            element
            for element in elements
            if self.backend.selector(element).control_type == selector.control_type
            and self.backend.selector(element).automation_id == selector.automation_id
        )
        if not matches:
            raise SupervisorError("claude_desktop_uia_prompt_text_missing")
        if len(matches) != 1:
            raise SupervisorError("claude_desktop_uia_prompt_text_ambiguous")
        if self.backend.selector(matches[0]).name != expected_name:
            raise SupervisorError(
                "claude_desktop_uia_composer_not_empty"
                if initial
                else "claude_desktop_uia_prompt_verification_failed"
            )
        return matches[0]


@dataclass(frozen=True)
class BoundClaudeDesktopSendPort:
    """Adapt one immutable UIA binding to ``DesktopRoundTrip``'s send port."""

    binding: ClaudeDesktopUiaBinding
    messenger: ClaudeDesktopExactSessionMessenger

    def send_message(
        self,
        *,
        message: str,
        message_id: str,
        cancel_requested: Callable[[], bool],
    ) -> bool:
        if message != restricted_wake_text(message_id):
            raise SupervisorError("claude_desktop_uia_wake_text_not_allowed")
        receipt = self.messenger.send(
            binding=self.binding,
            prompt=message,
            cancel_requested=cancel_requested,
        )
        return receipt.message_send_requested


class PywinautoUiaBackend:
    """Optional production backend; importing this module does not need pywinauto."""

    def __init__(
        self,
        *,
        desktop_factory: Callable[..., object] | None = None,
        process_image_resolver: Callable[[int], str] | None = None,
    ) -> None:
        if desktop_factory is None:
            try:
                module = importlib.import_module("pywinauto")
                desktop_factory = module.Desktop
            except (ImportError, AttributeError) as exc:
                raise SupervisorError("claude_desktop_uia_unavailable") from exc
        self._desktop = desktop_factory(backend="uia")
        self._process_image_resolver = (
            process_image_resolver or _windows_process_image_path
        )

    def top_level_windows(self) -> Sequence[object]:
        return tuple(self._desktop.windows(visible_only=True, enabled_only=False))

    @staticmethod
    def descendants(element: object) -> Sequence[object]:
        return tuple(element.descendants())

    @staticmethod
    def selector(element: object) -> SemanticSelector:
        info = element.element_info
        return SemanticSelector(
            str(info.control_type or ""),
            str(info.automation_id or ""),
            str(info.name or ""),
        )

    @staticmethod
    def process_id(element: object) -> int:
        value = element.process_id()
        if not isinstance(value, int) or value <= 0:
            raise SupervisorError("claude_desktop_uia_process_invalid")
        return value

    def process_image(self, process_id: int) -> str:
        return self._process_image_resolver(process_id)

    @staticmethod
    def identity(element: object) -> tuple[int, ...]:
        value = getattr(element.element_info, "runtime_id", None)
        if not isinstance(value, (tuple, list)):
            raise SupervisorError("claude_desktop_uia_identity_invalid")
        if any(not isinstance(item, int) for item in value):
            raise SupervisorError("claude_desktop_uia_identity_invalid")
        return tuple(value)

    @staticmethod
    def is_visible(element: object) -> bool:
        return bool(element.is_visible())

    @staticmethod
    def is_enabled(element: object) -> bool:
        return bool(element.is_enabled())

    @staticmethod
    def value(element: object) -> str:
        interface = getattr(element, "iface_value", None)
        if interface is None:
            raise SupervisorError("claude_desktop_uia_value_pattern_missing")
        value = interface.CurrentValue
        if not isinstance(value, str):
            raise SupervisorError("claude_desktop_uia_value_invalid")
        return value

    @staticmethod
    def set_value(element: object, value: str) -> None:
        interface = getattr(element, "iface_value", None)
        if interface is None:
            raise SupervisorError("claude_desktop_uia_value_pattern_missing")
        interface.SetValue(value)

    @staticmethod
    def set_focus(element: object) -> None:
        element.set_focus()

    @staticmethod
    def has_keyboard_focus(element: object) -> bool:
        return bool(element.has_keyboard_focus())

    @staticmethod
    def type_vk_packet(element: object, value: str) -> None:
        # The restricted wake alphabet contains no pywinauto metacharacters.
        # vk_packet types Unicode directly and does not use the clipboard.
        element.type_keys(
            value,
            with_spaces=True,
            set_foreground=False,
            vk_packet=True,
            pause=0.0,
        )

    @staticmethod
    def invoke(element: object) -> None:
        interface = getattr(element, "iface_invoke", None)
        if interface is None:
            raise SupervisorError("claude_desktop_uia_invoke_pattern_missing")
        interface.Invoke()


def restricted_wake_text(wake_id: str) -> str:
    try:
        canonical = str(uuid.UUID(wake_id))
    except (ValueError, AttributeError) as exc:
        raise SupervisorError("claude_desktop_uia_wake_id_invalid") from exc
    if wake_id != canonical:
        raise SupervisorError("claude_desktop_uia_wake_id_invalid")
    return _WAKE_PREFIX + canonical + _WAKE_SUFFIX


def _validated_wake_text(prompt: str) -> bytes:
    if not isinstance(prompt, str):
        raise SupervisorError("claude_desktop_uia_wake_text_not_allowed")
    parts = prompt.removeprefix(_WAKE_PREFIX).removesuffix(_WAKE_SUFFIX)
    try:
        expected = restricted_wake_text(parts)
    except SupervisorError as exc:
        raise SupervisorError("claude_desktop_uia_wake_text_not_allowed") from exc
    if prompt != expected:
        raise SupervisorError("claude_desktop_uia_wake_text_not_allowed")
    return prompt.encode("ascii")


def _normalized_windows_path(value: str) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise SupervisorError("claude_desktop_uia_process_image_invalid")
    return os.path.normcase(os.path.abspath(value))


def _windows_process_image_path(process_id: int) -> str:
    if os.name != "nt":
        raise SupervisorError("claude_desktop_uia_platform_unsupported")
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    open_process = kernel32.OpenProcess
    open_process.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_uint]
    open_process.restype = ctypes.c_void_p
    query_image = kernel32.QueryFullProcessImageNameW
    query_image.argtypes = [
        ctypes.c_void_p,
        ctypes.c_uint,
        ctypes.c_wchar_p,
        ctypes.POINTER(ctypes.c_uint),
    ]
    query_image.restype = ctypes.c_int
    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [ctypes.c_void_p]
    close_handle.restype = ctypes.c_int
    handle = open_process(0x1000, 0, process_id)  # PROCESS_QUERY_LIMITED_INFORMATION
    if not handle:
        raise SupervisorError("claude_desktop_uia_process_unavailable")
    try:
        buffer = ctypes.create_unicode_buffer(32_768)
        length = ctypes.c_uint(len(buffer))
        if not query_image(handle, 0, buffer, ctypes.byref(length)):
            raise SupervisorError("claude_desktop_uia_process_unavailable")
        return buffer.value
    finally:
        close_handle(handle)
