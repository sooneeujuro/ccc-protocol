from __future__ import annotations

import ctypes
import json
import os
import re
import subprocess
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from urllib.parse import urlsplit

from .errors import SupervisorError
from .files import canonical_json_bytes, resolve_local_ref, sha256_bytes
from .models import RunState
from .store import StateStore


PROFILE_SCHEMA = "ccc.claude_desktop_session_profile.v1"
PROFILE_SCHEMA_VERSION = 1
CAPABILITY = "focus_only_unverified"
ROUTE_CONTRACT = "claude_desktop_code_bridge_v1"

_MAX_LINK_BYTES = 512
_MAX_PROFILE_BYTES = 4_096
_SESSION_ID_RE = re.compile(r"^(?:session|cse)_[A-Za-z0-9_-]{16,112}$")
_SESSION_REF_RE = re.compile(r"^cds_[0-9a-f]{24}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_VERSION_RE = re.compile(r"^[0-9]+(?:\.[0-9]+){1,3}$")
_PACKAGE_TOKEN_RE = re.compile(r"^[A-Za-z0-9_.-]{1,128}$")
_HANDLER_TOKEN_RE = re.compile(r"^[A-Za-z0-9_.!:-]{1,160}$")

# This route was inspected in this exact local Desktop bundle.  It is not a
# public Anthropic automation API, so an update must fail closed until the
# route is inspected again and this allowlist is deliberately changed.
_SUPPORTED_BUILDS = {
    (
        "Claude",
        "1.20186.7.0",
        "Claude_pzs8sxrjxfjjc",
        "63355bc0fafca4d3eaa3fd53bbd372104820d30006a0bf27df792a78598e0655",
        "AppXaem4n1tckgw588q10avtdbzpbgt71c77",
        "Claude_pzs8sxrjxfjjc!Claude",
    ),
    (
        "Claude",
        "1.21459.0.0",
        "Claude_pzs8sxrjxfjjc",
        "d9a896beca555b86e6e773c065b75d3bc21c246f260578a42ca532e76fa155bd",
        "AppXaem4n1tckgw588q10avtdbzpbgt71c77",
        "Claude_pzs8sxrjxfjjc!Claude",
    ),
}


@dataclass(frozen=True)
class ClaudeDesktopBuild:
    package_name: str
    package_version: str
    package_family: str
    bundle_sha256: str
    protocol_progid: str
    app_user_model_id: str

    def validate(self) -> None:
        if self.package_name != "Claude":
            raise SupervisorError("claude_desktop_package_mismatch")
        if not _VERSION_RE.fullmatch(self.package_version):
            raise SupervisorError("claude_desktop_version_invalid")
        if not _PACKAGE_TOKEN_RE.fullmatch(self.package_family):
            raise SupervisorError("claude_desktop_package_family_invalid")
        if not _SHA256_RE.fullmatch(self.bundle_sha256):
            raise SupervisorError("claude_desktop_bundle_hash_invalid")
        if not _HANDLER_TOKEN_RE.fullmatch(self.protocol_progid):
            raise SupervisorError("claude_desktop_protocol_progid_invalid")
        if not _HANDLER_TOKEN_RE.fullmatch(self.app_user_model_id):
            raise SupervisorError("claude_desktop_app_id_invalid")

    def require_supported(self) -> None:
        self.validate()
        identity = (
            self.package_name,
            self.package_version,
            self.package_family,
            self.bundle_sha256,
            self.protocol_progid,
            self.app_user_model_id,
        )
        if identity not in _SUPPORTED_BUILDS:
            raise SupervisorError("claude_desktop_build_unsupported")

    def as_profile_value(self) -> dict[str, str]:
        return {
            "bundle_sha256": self.bundle_sha256,
            "package_family": self.package_family,
            "package_name": self.package_name,
            "package_version": self.package_version,
            "protocol_progid": self.protocol_progid,
            "app_user_model_id": self.app_user_model_id,
        }


class DesktopBuildProbe(Protocol):
    def inspect(self) -> ClaudeDesktopBuild: ...


class DesktopUriLauncher(Protocol):
    def dispatch(
        self,
        uri: str,
        *,
        expected_progid: str,
        expected_app_user_model_id: str,
    ) -> bool: ...


class WindowsClaudeDesktopProbe:
    """Inspect only package identity, declared protocol, and bundle hash."""

    _SCRIPT = r"""
$ErrorActionPreference = 'Stop'
$packages = @(Get-AppxPackage -Name 'Claude' -ErrorAction Stop)
if ($packages.Count -ne 1) { exit 41 }
$package = $packages[0]
$bundle = Join-Path $package.InstallLocation 'app\resources\app.asar'
if (-not (Test-Path -LiteralPath $bundle -PathType Leaf)) { exit 42 }
$manifest = Get-AppxPackageManifest -Package $package
$protocols = @(
  $manifest.Package.Applications.Application.Extensions.Extension |
    ForEach-Object { $_.Protocol.Name } |
    Where-Object { $_ }
)
if ($protocols -notcontains 'claude') { exit 43 }
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$stream = [System.IO.File]::OpenRead($bundle)
try {
  $hasher = [System.Security.Cryptography.SHA256]::Create()
  try {
    $bundleHash = [System.BitConverter]::ToString($hasher.ComputeHash($stream)).Replace('-', '').ToLowerInvariant()
  } finally {
    $hasher.Dispose()
  }
} finally {
  $stream.Dispose()
}
[ordered]@{
  package_name = [string]$package.Name
  package_version = [string]$package.Version
  package_family = [string]$package.PackageFamilyName
  bundle_sha256 = $bundleHash
} | ConvertTo-Json -Compress
"""

    def inspect(self) -> ClaudeDesktopBuild:
        if os.name != "nt":
            raise SupervisorError("claude_desktop_platform_unsupported")
        system_root, system_directory = _windows_system_paths()
        executable = (
            system_directory
            / "WindowsPowerShell"
            / "v1.0"
            / "powershell.exe"
        )
        module_path = (
            system_root
            / "System32"
            / "WindowsPowerShell"
            / "v1.0"
            / "Modules"
        )
        if not executable.is_file():
            raise SupervisorError("claude_desktop_probe_unavailable")
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        try:
            result = subprocess.run(
                [
                    str(executable),
                    "-NoLogo",
                    "-NoProfile",
                    "-NonInteractive",
                    "-Command",
                    self._SCRIPT,
                ],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                check=False,
                shell=False,
                creationflags=flags,
                env={
                    "ComSpec": str(system_directory / "cmd.exe"),
                    "PATH": str(system_directory),
                    "PSModulePath": str(module_path),
                    "SystemDrive": system_root.drive,
                    "SystemRoot": str(system_root),
                    "WINDIR": str(system_root),
                },
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise SupervisorError("claude_desktop_probe_unavailable") from exc
        if result.returncode != 0 or len(result.stdout) > 4_096:
            raise SupervisorError("claude_desktop_probe_failed")
        try:
            value = json.loads(result.stdout.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise SupervisorError("claude_desktop_probe_invalid") from exc
        expected_keys = {
            "package_name",
            "package_version",
            "package_family",
            "bundle_sha256",
        }
        if not isinstance(value, dict) or set(value) != expected_keys:
            raise SupervisorError("claude_desktop_probe_invalid")
        if any(not isinstance(value[key], str) for key in expected_keys):
            raise SupervisorError("claude_desktop_probe_invalid")
        protocol_progid, app_user_model_id = _current_claude_protocol_handler()
        build = ClaudeDesktopBuild(
            **value,
            protocol_progid=protocol_progid,
            app_user_model_id=app_user_model_id,
        )
        build.validate()
        return build


class WindowsClaudeDesktopLauncher:
    """Ask Windows to dispatch one internally generated Claude URI."""

    def dispatch(
        self,
        uri: str,
        *,
        expected_progid: str,
        expected_app_user_model_id: str,
    ) -> bool:
        if os.name != "nt":
            raise SupervisorError("claude_desktop_platform_unsupported")
        session_id = parse_session_link(uri)
        if uri != canonical_session_uri(session_id):
            raise SupervisorError("claude_desktop_uri_not_canonical")
        if (
            not _HANDLER_TOKEN_RE.fullmatch(expected_progid)
            or not _HANDLER_TOKEN_RE.fullmatch(expected_app_user_model_id)
        ):
            raise SupervisorError("claude_desktop_protocol_handler_invalid")
        current_progid, current_app_id = _current_claude_protocol_handler()
        if (
            current_progid != expected_progid
            or current_app_id != expected_app_user_model_id
        ):
            raise SupervisorError("claude_desktop_protocol_handler_mismatch")
        shell32 = ctypes.WinDLL("shell32", use_last_error=True)
        execute = shell32.ShellExecuteW
        execute.argtypes = [
            ctypes.c_void_p,
            ctypes.c_wchar_p,
            ctypes.c_wchar_p,
            ctypes.c_wchar_p,
            ctypes.c_wchar_p,
            ctypes.c_int,
        ]
        execute.restype = ctypes.c_void_p
        result = execute(None, "open", uri, None, None, 1)
        return result is not None and int(result) > 32


@dataclass(frozen=True)
class DesktopBindingReceipt:
    profile_sha256: str
    session_ref: str
    created: bool


@dataclass(frozen=True)
class DesktopFocusReceipt:
    profile_sha256: str
    session_ref: str
    navigation_state: str = "focus_requested_unverified"
    navigation_requested: bool = True
    message_sent: bool = False
    turn_started: bool = False
    completion_observed: bool = False


def parse_session_link(raw_link: str) -> str:
    if not isinstance(raw_link, str):
        raise SupervisorError("claude_desktop_session_link_invalid")
    if len(raw_link.encode("utf-8")) > _MAX_LINK_BYTES:
        raise SupervisorError("claude_desktop_session_link_invalid")
    value = raw_link.rstrip("\r\n")
    if not value or "\r" in value or "\n" in value or value != value.strip():
        raise SupervisorError("claude_desktop_session_link_invalid")
    if any(ord(character) < 0x21 or ord(character) > 0x7E for character in value):
        raise SupervisorError("claude_desktop_session_link_invalid")
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError as exc:
        raise SupervisorError("claude_desktop_session_link_invalid") from exc
    if parsed.query or parsed.fragment or "?" in value or "#" in value:
        raise SupervisorError("claude_desktop_session_link_invalid")
    if parsed.username is not None or parsed.password is not None or port is not None:
        raise SupervisorError("claude_desktop_session_link_invalid")

    path: str
    if parsed.scheme == "https" and parsed.netloc == "claude.ai":
        path = parsed.path
    elif parsed.scheme == "claude" and parsed.netloc == "claude.ai":
        # This is the exact existing-session form emitted by the pinned
        # Desktop renderer.  The public code-host route documents only `new`.
        path = parsed.path
    else:
        raise SupervisorError("claude_desktop_session_link_invalid")

    parts = path.split("/")
    if len(parts) != 3 or parts[0] or parts[1] != "code":
        raise SupervisorError("claude_desktop_session_link_invalid")
    session_id = parts[2]
    if not _SESSION_ID_RE.fullmatch(session_id):
        raise SupervisorError("claude_desktop_session_id_invalid")
    return session_id


def canonical_session_uri(session_id: str) -> str:
    if not isinstance(session_id, str) or not _SESSION_ID_RE.fullmatch(session_id):
        raise SupervisorError("claude_desktop_session_id_invalid")
    return f"claude://claude.ai/code/{session_id}"


def session_ref(session_id: str, run_id: str) -> str:
    canonical_session_uri(session_id)
    if not isinstance(run_id, str):
        raise SupervisorError("run_id_invalid")
    try:
        canonical_run_id = str(uuid.UUID(run_id))
    except (ValueError, AttributeError) as exc:
        raise SupervisorError("run_id_invalid") from exc
    if run_id != canonical_run_id:
        raise SupervisorError("run_id_invalid")
    digest = sha256_bytes(
        b"ccc.claude-desktop-session-ref.v1\x00"
        + canonical_run_id.encode("ascii")
        + b"\x00"
        + session_id.encode("ascii")
    )
    return f"cds_{digest[:24]}"


def bind_claude_desktop_session(
    store: StateStore,
    *,
    run_id: str,
    raw_link: str,
    probe: DesktopBuildProbe,
) -> DesktopBindingReceipt:
    session_id = parse_session_link(raw_link)
    run = _binding_run(store, run_id)
    canonical_run_id = run["run_id"]
    build = probe.inspect()
    build.require_supported()
    ref = session_ref(session_id, canonical_run_id)
    profile = {
        "agent_id": "claude",
        "capability": CAPABILITY,
        "desktop_build": build.as_profile_value(),
        "generation": run["generation"],
        "route_contract": ROUTE_CONTRACT,
        "run_id": canonical_run_id,
        "schema": PROFILE_SCHEMA,
        "schema_version": PROFILE_SCHEMA_VERSION,
        "session_id": session_id,
        "session_ref": ref,
    }
    data = canonical_json_bytes(profile)
    digest = sha256_bytes(data)
    path = _profile_path(store, canonical_run_id)
    created = _create_or_match(path, data)
    return DesktopBindingReceipt(digest, ref, created)


def focus_claude_desktop_session(
    store: StateStore,
    *,
    run_id: str,
    focus_id: str,
    expected_profile_sha256: str,
    expected_session_ref: str,
    probe: DesktopBuildProbe,
    launcher: DesktopUriLauncher,
) -> DesktopFocusReceipt:
    if not _SHA256_RE.fullmatch(expected_profile_sha256):
        raise SupervisorError("claude_desktop_profile_hash_invalid")
    if not _SESSION_REF_RE.fullmatch(expected_session_ref):
        raise SupervisorError("claude_desktop_session_ref_invalid")
    run = _binding_run(store, run_id)
    canonical_run_id = run["run_id"]
    profile, digest = _load_profile(store, canonical_run_id)
    if digest != expected_profile_sha256:
        raise SupervisorError("claude_desktop_profile_hash_mismatch")
    if profile["session_ref"] != expected_session_ref:
        raise SupervisorError("claude_desktop_session_ref_mismatch")
    if (
        profile["generation"] != run["generation"]
        or profile["run_id"] != canonical_run_id
    ):
        raise SupervisorError("claude_desktop_profile_stale")

    pinned_build = _build_from_profile(profile["desktop_build"])
    pinned_build.require_supported()
    current_build = probe.inspect()
    current_build.require_supported()
    if current_build != pinned_build:
        raise SupervisorError("claude_desktop_build_drift")

    if not store.reserve_claude_desktop_focus(canonical_run_id, focus_id):
        raise SupervisorError("claude_desktop_focus_not_allowed")
    try:
        _binding_run(store, canonical_run_id)
    except SupervisorError as exc:
        store.finish_claude_desktop_focus(
            canonical_run_id, focus_id, "cancelled_before_dispatch"
        )
        raise SupervisorError("claude_desktop_focus_cancelled") from exc

    # Recheck the package after reserving the one-shot receipt.  A Desktop
    # update between the first probe and dispatch consumes this nudge rather
    # than opening an unreviewed build or being retried automatically.
    try:
        final_build = probe.inspect()
        final_build.validate()
    except Exception as exc:
        store.finish_claude_desktop_focus(
            canonical_run_id, focus_id, "probe_failed_before_dispatch"
        )
        raise SupervisorError("claude_desktop_probe_failed") from exc
    if final_build != pinned_build:
        store.finish_claude_desktop_focus(
            canonical_run_id, focus_id, "build_drift_before_dispatch"
        )
        raise SupervisorError("claude_desktop_build_drift")

    try:
        _binding_run(store, canonical_run_id)
    except SupervisorError as exc:
        store.finish_claude_desktop_focus(
            canonical_run_id, focus_id, "cancelled_before_dispatch"
        )
        raise SupervisorError("claude_desktop_focus_cancelled") from exc

    uri = canonical_session_uri(profile["session_id"])
    try:
        accepted = launcher.dispatch(
            uri,
            expected_progid=pinned_build.protocol_progid,
            expected_app_user_model_id=pinned_build.app_user_model_id,
        )
    except Exception as exc:
        store.finish_claude_desktop_focus(
            canonical_run_id, focus_id, "dispatch_error"
        )
        raise SupervisorError("claude_desktop_focus_dispatch_error") from exc
    if not accepted:
        store.finish_claude_desktop_focus(
            canonical_run_id, focus_id, "dispatch_rejected"
        )
        raise SupervisorError("claude_desktop_focus_dispatch_rejected")
    store.finish_claude_desktop_focus(
        canonical_run_id, focus_id, "focus_requested_unverified"
    )
    return DesktopFocusReceipt(digest, expected_session_ref)


def _binding_run(store: StateStore, run_id: str):
    # Explicit --run-id CLI calls do not pass through active_run_id(), so the
    # capability boundary must also perform any compatible local migration.
    store.initialize()
    run = store.run_row(run_id)
    if run["state"] not in (RunState.ACTIVE.value, RunState.QUIET_WATCH.value):
        raise SupervisorError("run_not_active")
    if store.should_cancel(run_id):
        raise SupervisorError("claude_desktop_focus_cancelled")
    if store.clock() >= run["watch_expires_at"]:
        raise SupervisorError("watch_expired")
    if not run["claude_desktop_focus_enabled"]:
        raise SupervisorError("claude_desktop_focus_policy_disabled")
    return run


def _profile_path(store: StateStore, run_id: str) -> Path:
    # run_id was validated by run_row before this helper is reached.
    return resolve_local_ref(
        store.state_root, f"profiles/claude-desktop/{run_id}.json"
    )


def _create_or_match(path: Path, data: bytes) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        try:
            existing = path.read_bytes()
        except OSError as exc:
            raise SupervisorError("claude_desktop_profile_unreadable") from exc
        if len(existing) > _MAX_PROFILE_BYTES or existing != data:
            raise SupervisorError("claude_desktop_profile_conflict")
        return False
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        path.unlink(missing_ok=True)
        raise
    return True


def _load_profile(store: StateStore, run_id: str) -> tuple[dict[str, object], str]:
    path = _profile_path(store, run_id)
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise SupervisorError("claude_desktop_profile_missing") from exc
    if not data or len(data) > _MAX_PROFILE_BYTES:
        raise SupervisorError("claude_desktop_profile_invalid")
    try:
        profile = json.loads(data.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise SupervisorError("claude_desktop_profile_invalid") from exc
    _validate_profile(profile)
    canonical = canonical_json_bytes(profile)
    if canonical != data:
        raise SupervisorError("claude_desktop_profile_not_canonical")
    return profile, sha256_bytes(data)


def _validate_profile(profile: object) -> None:
    expected_keys = {
        "agent_id",
        "capability",
        "desktop_build",
        "generation",
        "route_contract",
        "run_id",
        "schema",
        "schema_version",
        "session_id",
        "session_ref",
    }
    if not isinstance(profile, dict) or set(profile) != expected_keys:
        raise SupervisorError("claude_desktop_profile_invalid")
    if (
        profile["schema"] != PROFILE_SCHEMA
        or profile["schema_version"] != PROFILE_SCHEMA_VERSION
        or profile["agent_id"] != "claude"
        or profile["capability"] != CAPABILITY
        or profile["route_contract"] != ROUTE_CONTRACT
        or not isinstance(profile["generation"], int)
        or isinstance(profile["generation"], bool)
        or profile["generation"] <= 0
        or not isinstance(profile["run_id"], str)
        or not isinstance(profile["session_id"], str)
        or not isinstance(profile["session_ref"], str)
    ):
        raise SupervisorError("claude_desktop_profile_invalid")
    if session_ref(profile["session_id"], profile["run_id"]) != profile["session_ref"]:
        raise SupervisorError("claude_desktop_profile_invalid")
    _build_from_profile(profile["desktop_build"])


def _build_from_profile(value: object) -> ClaudeDesktopBuild:
    expected_keys = {
        "package_name",
        "package_version",
        "package_family",
        "bundle_sha256",
        "protocol_progid",
        "app_user_model_id",
    }
    if not isinstance(value, dict) or set(value) != expected_keys:
        raise SupervisorError("claude_desktop_profile_invalid")
    if any(not isinstance(value[key], str) for key in expected_keys):
        raise SupervisorError("claude_desktop_profile_invalid")
    build = ClaudeDesktopBuild(**value)
    build.validate()
    return build


def _windows_system_paths() -> tuple[Path, Path]:
    if os.name != "nt":
        raise SupervisorError("claude_desktop_platform_unsupported")
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    def query(name: str) -> Path:
        function = getattr(kernel32, name)
        function.argtypes = [ctypes.c_wchar_p, ctypes.c_uint]
        function.restype = ctypes.c_uint
        buffer = ctypes.create_unicode_buffer(32_768)
        length = function(buffer, len(buffer))
        if length == 0 or length >= len(buffer):
            raise SupervisorError("claude_desktop_system_path_unavailable")
        value = Path(buffer.value)
        if not value.is_absolute():
            raise SupervisorError("claude_desktop_system_path_unavailable")
        return value

    return query("GetWindowsDirectoryW"), query("GetSystemDirectoryW")


def _current_claude_protocol_handler() -> tuple[str, str]:
    if os.name != "nt":
        raise SupervisorError("claude_desktop_platform_unsupported")
    shlwapi = ctypes.WinDLL("shlwapi", use_last_error=True)
    query = shlwapi.AssocQueryStringW
    query.argtypes = [
        ctypes.c_uint,
        ctypes.c_uint,
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.POINTER(ctypes.c_uint),
    ]
    query.restype = ctypes.c_long

    def value(kind: int) -> str:
        buffer = ctypes.create_unicode_buffer(1_024)
        length = ctypes.c_uint(len(buffer))
        result = query(0, kind, "claude", None, buffer, ctypes.byref(length))
        if result != 0 or not buffer.value or not _HANDLER_TOKEN_RE.fullmatch(
            buffer.value
        ):
            raise SupervisorError("claude_desktop_protocol_handler_unavailable")
        return buffer.value

    # ASSOCSTR_PROGID=20 and ASSOCSTR_APPID=21.
    return value(20), value(21)
