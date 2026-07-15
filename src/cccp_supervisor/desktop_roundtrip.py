from __future__ import annotations

import hmac
import json
import os
import re
import stat
import time
import uuid
from collections.abc import Callable
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Protocol

from .errors import SupervisorError
from .files import atomic_write_bytes, canonical_json_bytes, resolve_local_ref, sha256_bytes
from .claude_desktop_uia import restricted_wake_text


RECEIPT_SCHEMA = "ccc.desktop_roundtrip_receipt.v1"
COMPLETION_SCHEMA = "ccc.desktop_completion.v1"
WAKE_INTENT_SCHEMA = "ccc.desktop_codex_wake_intent.v1"

_TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]{16,128}$")
_REF_RE = re.compile(r"^(?:drt|msg|cmp|non|wake)_[0-9a-f]{24}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_FAILURE_RE = re.compile(r"^[a-z][a-z0-9_]{0,95}$")
_MAX_MESSAGE_BYTES = 512
_MAX_REF_BYTES = 512
_MAX_RECEIPT_BYTES = 8_192

_TERMINAL_STATES = {
    "stopped_before_send",
    "stopped_after_send",
    "stopped_before_codex_wake",
    "completion_rejected",
    "codex_wake_requested",
    "codex_wake_ambiguous",
}
_VALID_STATES = _TERMINAL_STATES | {
    "send_intent_recorded",
    "send_requested_unverified",
    "send_ambiguous",
    "awaiting_completion",
    "completion_observed",
    "codex_wake_intent_recorded",
}


class DesktopSendPort(Protocol):
    """A pre-bound exact-session transport. It must never choose a session."""

    def send_message(
        self,
        *,
        message: str,
        message_id: str,
        cancel_requested: Callable[[], bool],
    ) -> bool: ...


class CodexWakePort(Protocol):
    """A pre-bound exact-task wake transport carrying no prompt text."""

    def request_wake(
        self,
        *,
        wake_id: str,
        roundtrip_ref: str,
        cancel_requested: Callable[[], bool],
    ) -> bool: ...


class CompletionObserver(Protocol):
    def observe(
        self,
        path: Path,
        *,
        expected_nonce: str,
        stop_requested: Callable[[], bool],
    ) -> "CompletionObservation": ...


@dataclass(frozen=True)
class CompletionObservation:
    state: str
    content_sha256: str | None = None
    content_bytes: int = 0

    def __post_init__(self) -> None:
        if self.state not in {"observed", "timeout", "stopped"}:
            raise ValueError("completion observation state invalid")
        if self.state == "observed":
            if not self.content_sha256 or not _SHA256_RE.fullmatch(
                self.content_sha256
            ):
                raise ValueError("completion observation digest invalid")
            if self.content_bytes <= 0:
                raise ValueError("completion observation size invalid")
        elif self.content_sha256 is not None or self.content_bytes != 0:
            raise ValueError("non-observed completion cannot carry content")


@dataclass(frozen=True)
class DesktopRoundTripRequest:
    roundtrip_id: str
    message_id: str
    wake_id: str
    message: str
    completion_ref: str
    completion_nonce: str


@dataclass(frozen=True)
class DesktopRoundTripReceipt:
    schema: str
    schema_version: int
    roundtrip_ref: str
    request_sha256: str
    message_ref: str
    message_sha256: str
    message_bytes: int
    completion_ref: str
    completion_nonce_sha256: str
    wake_ref: str
    state: str
    send_intent_recorded: bool
    send_requested: bool
    completion_observed: bool
    codex_wake_intent_recorded: bool
    codex_wake_requested: bool
    completion_sha256: str | None
    completion_bytes: int
    failure_code: str | None
    revision: int

    @property
    def terminal(self) -> bool:
        return self.state in _TERMINAL_STATES


class BoundedCompletionFileObserver:
    """Observe one exact local completion file without consuming prose."""

    def __init__(
        self,
        *,
        timeout_seconds: float = 30.0,
        max_bytes: int = 4_096,
        stability_samples: int = 2,
        stability_interval_seconds: float = 0.05,
        clock: Callable[[], float] = time.monotonic,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        if not (0 < timeout_seconds <= 300):
            raise ValueError("completion timeout outside hard bounds")
        if not (0 < max_bytes <= 65_536):
            raise ValueError("completion size outside hard bounds")
        if not (2 <= stability_samples <= 10):
            raise ValueError("completion stability samples outside hard bounds")
        if not (0 < stability_interval_seconds <= 5):
            raise ValueError("completion stability interval outside hard bounds")
        self.timeout_seconds = float(timeout_seconds)
        self.max_bytes = max_bytes
        self.stability_samples = stability_samples
        self.stability_interval_seconds = float(stability_interval_seconds)
        self.clock = clock
        self.sleeper = sleeper

    def observe(
        self,
        path: Path,
        *,
        expected_nonce: str,
        stop_requested: Callable[[], bool],
    ) -> CompletionObservation:
        _validated_nonce(expected_nonce)
        deadline = self.clock() + self.timeout_seconds
        previous: tuple[int, int, int, int] | None = None
        stable_count = 0

        while True:
            if stop_requested():
                return CompletionObservation("stopped")
            now = self.clock()
            if now >= deadline:
                return CompletionObservation("timeout")

            try:
                current = _completion_signature(path, self.max_bytes)
            except FileNotFoundError:
                previous = None
                stable_count = 0
            else:
                if current == previous:
                    stable_count += 1
                else:
                    previous = current
                    stable_count = 1
                if stable_count >= self.stability_samples:
                    data = _read_stable_completion(path, current, self.max_bytes)
                    value = _parse_completion(data, expected_nonce)
                    if value:
                        return CompletionObservation(
                            "observed", sha256_bytes(data), len(data)
                        )

            remaining = deadline - self.clock()
            if remaining <= 0:
                return CompletionObservation("timeout")
            self.sleeper(min(self.stability_interval_seconds, remaining))


class DesktopRoundTrip:
    """One Claude Desktop send followed by one completion-gated Codex wake.

    The first O_EXCL receipt is also the send intent. Any later invocation is
    reconciliation-only and can never call the Desktop send port again.
    """

    def __init__(
        self,
        coop_root: Path,
        *,
        completion_root: Path,
        sender: DesktopSendPort,
        observer: CompletionObserver,
        codex_waker: CodexWakePort,
    ) -> None:
        self.coop_root = Path(coop_root).resolve()
        self.state_root = self.coop_root / ".ccc" / "desktop-roundtrip"
        self.receipt_root = self.state_root / "receipts"
        self.intent_root = self.state_root / "wake-intents"
        self.completion_root = Path(completion_root).resolve()
        self.stop_path = self.coop_root / "STOP.md"
        self.sender = sender
        self.observer = observer
        self.codex_waker = codex_waker

    def run(self, request: DesktopRoundTripRequest) -> DesktopRoundTripReceipt:
        validated = self._validate_request(request)
        receipt, created = self._create_or_load(validated)
        immutable = {
            "roundtrip_ref": validated["roundtrip_ref"],
            "request_sha256": validated["request_sha256"],
            "message_ref": validated["message_ref"],
            "message_sha256": validated["message_sha256"],
            "message_bytes": validated["message_bytes"],
            "completion_ref": validated["completion_ref"],
            "completion_nonce_sha256": validated["completion_nonce_sha256"],
            "wake_ref": validated["wake_ref"],
        }
        if any(getattr(receipt, key) != value for key, value in immutable.items()):
            raise SupervisorError("desktop_roundtrip_idempotency_conflict")
        if receipt.terminal or receipt.codex_wake_intent_recorded:
            return receipt

        if created:
            if self._stopped():
                return self._transition(
                    receipt,
                    state="stopped_before_send",
                    failure_code="desktop_roundtrip_stopped",
                )
            try:
                accepted = self.sender.send_message(
                    message=request.message,
                    message_id=request.message_id,
                    cancel_requested=self._stopped,
                )
                if not isinstance(accepted, bool):
                    raise TypeError("send result must be boolean")
            except Exception:
                receipt = self._transition(
                    receipt,
                    state="send_ambiguous",
                    failure_code="desktop_send_ambiguous",
                )
            else:
                receipt = self._transition(
                    receipt,
                    state=(
                        "send_requested_unverified" if accepted else "send_ambiguous"
                    ),
                    send_requested=accepted,
                    failure_code=None if accepted else "desktop_send_ambiguous",
                )
        elif receipt.state == "send_intent_recorded":
            # The process may have crashed immediately before or after sending.
            # Reconciliation is allowed; replay is permanently forbidden.
            receipt = self._transition(
                receipt,
                state="send_ambiguous",
                failure_code="desktop_send_reconcile_required",
            )

        if self._stopped():
            return self._transition(
                receipt,
                state="stopped_after_send",
                failure_code="desktop_roundtrip_stopped",
            )

        if not receipt.completion_observed:
            try:
                observation = self.observer.observe(
                    validated["completion_path"],
                    expected_nonce=request.completion_nonce,
                    stop_requested=self._stopped,
                )
            except SupervisorError as exc:
                return self._transition(
                    receipt,
                    state="completion_rejected",
                    failure_code=exc.code,
                )
            except Exception:
                return self._transition(
                    receipt,
                    state="completion_rejected",
                    failure_code="completion_observer_failed",
                )

            if observation.state == "stopped":
                return self._transition(
                    receipt,
                    state="stopped_after_send",
                    failure_code="desktop_roundtrip_stopped",
                )
            if observation.state == "timeout":
                # Preserve an ambiguous send as the primary diagnostic.  The
                # watcher may be resumed, but a missing completion must never
                # make an unconfirmed Desktop send look merely slow.
                if not receipt.send_requested:
                    return self._transition(
                        receipt,
                        state="send_ambiguous",
                        failure_code=(
                            receipt.failure_code or "desktop_send_ambiguous"
                        ),
                    )
                return self._transition(
                    receipt,
                    state="awaiting_completion",
                    failure_code="completion_timeout",
                )
            receipt = self._transition(
                receipt,
                state="completion_observed",
                completion_observed=True,
                completion_sha256=observation.content_sha256,
                completion_bytes=observation.content_bytes,
                failure_code=None,
            )

        if self._stopped():
            return self._transition(
                receipt,
                state="stopped_before_codex_wake",
                failure_code="desktop_roundtrip_stopped",
            )

        intent_created = self._reserve_wake_intent(receipt)
        receipt = self._transition(
            receipt,
            state="codex_wake_intent_recorded",
            codex_wake_intent_recorded=True,
            failure_code=None,
        )
        if not intent_created:
            return receipt
        if self._stopped():
            return self._transition(
                receipt,
                state="stopped_before_codex_wake",
                failure_code="desktop_roundtrip_stopped",
            )

        try:
            accepted = self.codex_waker.request_wake(
                wake_id=request.wake_id,
                roundtrip_ref=receipt.roundtrip_ref,
                cancel_requested=self._stopped,
            )
            if not isinstance(accepted, bool):
                raise TypeError("wake result must be boolean")
        except Exception:
            return self._transition(
                receipt,
                state="codex_wake_ambiguous",
                failure_code="codex_wake_ambiguous",
            )
        return self._transition(
            receipt,
            state="codex_wake_requested" if accepted else "codex_wake_ambiguous",
            codex_wake_requested=accepted,
            failure_code=None if accepted else "codex_wake_ambiguous",
        )

    def _validate_request(self, request: DesktopRoundTripRequest) -> dict[str, object]:
        if not isinstance(request, DesktopRoundTripRequest):
            raise SupervisorError("desktop_roundtrip_request_invalid")
        roundtrip_id = _validated_uuid(request.roundtrip_id, "roundtrip_id_invalid")
        message_id = _validated_uuid(request.message_id, "message_id_invalid")
        wake_id = _validated_uuid(request.wake_id, "wake_id_invalid")
        if not isinstance(request.message, str):
            raise SupervisorError("desktop_message_invalid")
        try:
            expected_message = restricted_wake_text(message_id)
        except SupervisorError as exc:
            raise SupervisorError("desktop_message_invalid") from exc
        if request.message != expected_message:
            raise SupervisorError("desktop_message_invalid")
        message_data = request.message.encode("utf-8")
        if len(message_data) > _MAX_MESSAGE_BYTES:
            raise SupervisorError("desktop_message_invalid")
        nonce = _validated_nonce(request.completion_nonce)
        if not isinstance(request.completion_ref, str):
            raise SupervisorError("completion_ref_invalid")
        if (
            not request.completion_ref
            or len(request.completion_ref.encode("utf-8")) > _MAX_REF_BYTES
        ):
            raise SupervisorError("completion_ref_invalid")
        try:
            completion_path = resolve_local_ref(
                self.completion_root, request.completion_ref
            )
        except SupervisorError as exc:
            raise SupervisorError("completion_ref_invalid") from exc

        roundtrip_ref = _opaque_ref("drt", roundtrip_id)
        descriptor = {
            "schema": "ccc.desktop_roundtrip_request_descriptor.v1",
            "roundtrip_ref": roundtrip_ref,
            "message_ref": _opaque_ref("msg", message_id),
            "message_sha256": sha256_bytes(message_data),
            "message_bytes": len(message_data),
            "completion_ref": _opaque_ref(
                "cmp", str(completion_path).encode("utf-8").hex()
            ),
            "completion_nonce_sha256": sha256_bytes(nonce.encode("ascii")),
            "wake_ref": _opaque_ref("wake", wake_id),
        }
        return {
            **descriptor,
            "request_sha256": sha256_bytes(canonical_json_bytes(descriptor)),
            "completion_path": completion_path,
        }

    def _create_or_load(
        self, validated: dict[str, object]
    ) -> tuple[DesktopRoundTripReceipt, bool]:
        receipt = DesktopRoundTripReceipt(
            schema=RECEIPT_SCHEMA,
            schema_version=1,
            roundtrip_ref=str(validated["roundtrip_ref"]),
            request_sha256=str(validated["request_sha256"]),
            message_ref=str(validated["message_ref"]),
            message_sha256=str(validated["message_sha256"]),
            message_bytes=int(validated["message_bytes"]),
            completion_ref=str(validated["completion_ref"]),
            completion_nonce_sha256=str(validated["completion_nonce_sha256"]),
            wake_ref=str(validated["wake_ref"]),
            state="send_intent_recorded",
            send_intent_recorded=True,
            send_requested=False,
            completion_observed=False,
            codex_wake_intent_recorded=False,
            codex_wake_requested=False,
            completion_sha256=None,
            completion_bytes=0,
            failure_code=None,
            revision=1,
        )
        path = self._receipt_path(receipt.roundtrip_ref)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = canonical_json_bytes(asdict(receipt))
        try:
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            return self._load_receipt(path), False
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
        except Exception:
            path.unlink(missing_ok=True)
            raise
        return receipt, True

    def _transition(self, receipt: DesktopRoundTripReceipt, **changes: object) -> DesktopRoundTripReceipt:
        updated = replace(receipt, revision=receipt.revision + 1, **changes)
        _validate_receipt(updated)
        atomic_write_bytes(
            self._receipt_path(updated.roundtrip_ref),
            canonical_json_bytes(asdict(updated)),
        )
        return updated

    def _reserve_wake_intent(self, receipt: DesktopRoundTripReceipt) -> bool:
        path = self.intent_root / f"{receipt.roundtrip_ref}.json"
        value = {
            "schema": WAKE_INTENT_SCHEMA,
            "roundtrip_ref": receipt.roundtrip_ref,
            "request_sha256": receipt.request_sha256,
            "wake_ref": receipt.wake_ref,
        }
        data = canonical_json_bytes(value)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            try:
                existing = path.read_bytes()
            except OSError as exc:
                raise SupervisorError("codex_wake_intent_ambiguous") from exc
            if existing != data:
                raise SupervisorError("codex_wake_intent_conflict")
            return False
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        return True

    def _load_receipt(self, path: Path) -> DesktopRoundTripReceipt:
        try:
            data = path.read_bytes()
        except OSError as exc:
            raise SupervisorError("desktop_roundtrip_receipt_unreadable") from exc
        if not data or len(data) > _MAX_RECEIPT_BYTES:
            raise SupervisorError("desktop_roundtrip_receipt_invalid")
        try:
            value = json.loads(data.decode("utf-8"))
            receipt = DesktopRoundTripReceipt(**value)
        except (UnicodeError, json.JSONDecodeError, TypeError) as exc:
            raise SupervisorError("desktop_roundtrip_receipt_invalid") from exc
        if canonical_json_bytes(asdict(receipt)) != data:
            raise SupervisorError("desktop_roundtrip_receipt_not_canonical")
        _validate_receipt(receipt)
        return receipt

    def _receipt_path(self, roundtrip_ref: str) -> Path:
        if not _REF_RE.fullmatch(roundtrip_ref) or not roundtrip_ref.startswith("drt_"):
            raise SupervisorError("roundtrip_ref_invalid")
        return self.receipt_root / f"{roundtrip_ref}.json"

    def _stopped(self) -> bool:
        return self.stop_path.exists()


def _opaque_ref(prefix: str, value: str) -> str:
    digest = sha256_bytes(prefix.encode("ascii") + b"\x00" + value.encode("utf-8"))
    return f"{prefix}_{digest[:24]}"


def _validated_uuid(value: str, code: str) -> str:
    if not isinstance(value, str):
        raise SupervisorError(code)
    try:
        canonical = str(uuid.UUID(value))
    except (ValueError, AttributeError) as exc:
        raise SupervisorError(code) from exc
    if canonical != value:
        raise SupervisorError(code)
    return canonical


def _validated_nonce(value: str) -> str:
    if not isinstance(value, str) or not _TOKEN_RE.fullmatch(value):
        raise SupervisorError("completion_nonce_invalid")
    return value


def _completion_signature(path: Path, max_bytes: int) -> tuple[int, int, int, int]:
    details = path.lstat()
    if stat.S_ISLNK(details.st_mode) or not stat.S_ISREG(details.st_mode):
        raise SupervisorError("completion_file_type_invalid")
    if details.st_size <= 0:
        raise SupervisorError("completion_file_empty")
    if details.st_size > max_bytes:
        raise SupervisorError("completion_file_too_large")
    return (details.st_dev, details.st_ino, details.st_size, details.st_mtime_ns)


def _read_stable_completion(
    path: Path, expected: tuple[int, int, int, int], max_bytes: int
) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise SupervisorError("completion_file_unreadable") from exc
    try:
        before = os.fstat(descriptor)
        before_signature = (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
        )
        if before_signature != expected or not stat.S_ISREG(before.st_mode):
            raise SupervisorError("completion_file_unstable")
        data = os.read(descriptor, max_bytes + 1)
        after = os.fstat(descriptor)
        after_signature = (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        )
    finally:
        os.close(descriptor)
    if len(data) > max_bytes:
        raise SupervisorError("completion_file_too_large")
    if before_signature != after_signature:
        raise SupervisorError("completion_file_unstable")
    return data


def _parse_completion(data: bytes, expected_nonce: str) -> bool:
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise SupervisorError("completion_file_invalid") from exc
    if (
        not isinstance(value, dict)
        or set(value) != {"schema", "state", "nonce"}
        or value.get("schema") != COMPLETION_SCHEMA
        or value.get("state") != "completed"
        or not isinstance(value.get("nonce"), str)
        or canonical_json_bytes(value) != data
    ):
        raise SupervisorError("completion_file_invalid")
    if not hmac.compare_digest(value["nonce"], expected_nonce):
        raise SupervisorError("completion_nonce_mismatch")
    return True


def _validate_receipt(receipt: DesktopRoundTripReceipt) -> None:
    if receipt.schema != RECEIPT_SCHEMA or receipt.schema_version != 1:
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    for prefix, value in (
        ("drt_", receipt.roundtrip_ref),
        ("msg_", receipt.message_ref),
        ("cmp_", receipt.completion_ref),
        ("wake_", receipt.wake_ref),
    ):
        if (
            not isinstance(value, str)
            or not value.startswith(prefix)
            or not _REF_RE.fullmatch(value)
        ):
            raise SupervisorError("desktop_roundtrip_receipt_invalid")
    for value in (
        receipt.request_sha256,
        receipt.message_sha256,
        receipt.completion_nonce_sha256,
    ):
        if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
            raise SupervisorError("desktop_roundtrip_receipt_invalid")
    if receipt.state not in _VALID_STATES:
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    if not isinstance(receipt.message_bytes, int) or not (
        0 < receipt.message_bytes <= _MAX_MESSAGE_BYTES
    ):
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    if receipt.failure_code is not None and (
        not isinstance(receipt.failure_code, str)
        or not _FAILURE_RE.fullmatch(receipt.failure_code)
    ):
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    if receipt.completion_sha256 is not None and (
        not isinstance(receipt.completion_sha256, str)
        or not _SHA256_RE.fullmatch(receipt.completion_sha256)
    ):
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    if not isinstance(receipt.completion_bytes, int) or not (
        0 <= receipt.completion_bytes <= 65_536
    ):
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    if not isinstance(receipt.revision, int) or receipt.revision <= 0:
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    flags = (
        receipt.send_intent_recorded,
        receipt.send_requested,
        receipt.completion_observed,
        receipt.codex_wake_intent_recorded,
        receipt.codex_wake_requested,
    )
    if any(not isinstance(value, bool) for value in flags):
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    if not receipt.send_intent_recorded:
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    if receipt.completion_observed != (receipt.completion_sha256 is not None):
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    if receipt.completion_observed != (receipt.completion_bytes > 0):
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    if receipt.codex_wake_requested and not receipt.codex_wake_intent_recorded:
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    if receipt.state in {
        "completion_observed",
        "codex_wake_intent_recorded",
        "codex_wake_requested",
        "codex_wake_ambiguous",
        "stopped_before_codex_wake",
    } and not receipt.completion_observed:
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    if receipt.state in {
        "codex_wake_intent_recorded",
        "codex_wake_requested",
        "codex_wake_ambiguous",
    } and not receipt.codex_wake_intent_recorded:
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
    if receipt.codex_wake_requested != (receipt.state == "codex_wake_requested"):
        raise SupervisorError("desktop_roundtrip_receipt_invalid")
