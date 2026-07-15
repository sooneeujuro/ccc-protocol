from __future__ import annotations

import json
import tempfile
import unittest
import uuid
from dataclasses import replace
from pathlib import Path

from cccp_supervisor.desktop_roundtrip import (
    COMPLETION_SCHEMA,
    BoundedCompletionFileObserver,
    CompletionObservation,
    DesktopRoundTrip,
    DesktopRoundTripRequest,
)
from cccp_supervisor.claude_desktop_uia import restricted_wake_text
from cccp_supervisor.errors import SupervisorError
from cccp_supervisor.files import canonical_json_bytes


NONCE = "nonce_1234567890abcdef"
MESSAGE_ID = "11111111-1111-4111-8111-111111111111"


class FakeSender:
    def __init__(self, result: bool = True, error: BaseException | None = None) -> None:
        self.result = result
        self.error = error
        self.calls: list[dict[str, object]] = []

    def send_message(self, **kwargs):
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return self.result


class FakeWaker:
    def __init__(self, result: bool = True, error: BaseException | None = None) -> None:
        self.result = result
        self.error = error
        self.calls: list[dict[str, object]] = []

    def request_wake(self, **kwargs):
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return self.result


class FakeObserver:
    def __init__(self, *observations: CompletionObservation) -> None:
        self.observations = list(observations) or [CompletionObservation("timeout")]
        self.calls: list[dict[str, object]] = []

    def observe(self, path, **kwargs):
        self.calls.append({"path": path, **kwargs})
        return self.observations.pop(0) if len(self.observations) > 1 else self.observations[0]


class AdvancingClock:
    def __init__(self) -> None:
        self.value = 0.0

    def __call__(self) -> float:
        return self.value

    def sleep(self, seconds: float) -> None:
        self.value += seconds


class DesktopRoundTripTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.coop = self.root / "coop"
        self.completions = self.root / "completion-root"
        self.coop.mkdir()
        self.completions.mkdir()
        message_id = MESSAGE_ID
        self.request = DesktopRoundTripRequest(
            roundtrip_id=str(uuid.uuid4()),
            message_id=message_id,
            wake_id=str(uuid.uuid4()),
            message=restricted_wake_text(message_id),
            completion_ref="claude-done.json",
            completion_nonce=NONCE,
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def runner(self, sender, observer, waker) -> DesktopRoundTrip:
        return DesktopRoundTrip(
            self.coop,
            completion_root=self.completions,
            sender=sender,
            observer=observer,
            codex_waker=waker,
        )

    def test_happy_path_is_one_shot_and_receipt_is_scrubbed(self) -> None:
        sender = FakeSender()
        observer = FakeObserver(
            CompletionObservation("observed", "a" * 64, 71)
        )
        waker = FakeWaker()
        runner = self.runner(sender, observer, waker)

        first = runner.run(self.request)
        second = runner.run(self.request)

        self.assertEqual("codex_wake_requested", first.state)
        self.assertEqual(first, second)
        self.assertEqual(1, len(sender.calls))
        self.assertEqual(1, len(observer.calls))
        self.assertEqual(1, len(waker.calls))
        self.assertEqual(self.request.message, sender.calls[0]["message"])
        self.assertEqual(self.request.message_id, sender.calls[0]["message_id"])
        self.assertEqual(self.request.wake_id, waker.calls[0]["wake_id"])

        receipt_path = next(
            (self.coop / ".ccc" / "desktop-roundtrip" / "receipts").glob("*.json")
        )
        raw = receipt_path.read_text(encoding="utf-8")
        self.assertNotIn(self.request.message, raw)
        self.assertNotIn(self.request.message_id, raw)
        self.assertNotIn(self.request.wake_id, raw)
        self.assertNotIn(self.request.completion_ref, raw)
        self.assertNotIn(self.request.completion_nonce, raw)
        self.assertNotIn(str(self.completions), raw)
        self.assertTrue(first.send_intent_recorded)
        self.assertTrue(first.send_requested)
        self.assertTrue(first.completion_observed)
        self.assertTrue(first.codex_wake_intent_recorded)
        self.assertTrue(first.codex_wake_requested)

    def test_crash_during_send_resumes_without_resending(self) -> None:
        crashing_sender = FakeSender(error=KeyboardInterrupt())
        first_observer = FakeObserver(CompletionObservation("timeout"))
        waker = FakeWaker()
        runner = self.runner(crashing_sender, first_observer, waker)

        with self.assertRaises(KeyboardInterrupt):
            runner.run(self.request)
        self.assertEqual(1, len(crashing_sender.calls))

        replacement_sender = FakeSender()
        replacement_observer = FakeObserver(
            CompletionObservation("observed", "b" * 64, 69)
        )
        resumed = self.runner(replacement_sender, replacement_observer, waker).run(
            self.request
        )

        self.assertEqual("codex_wake_requested", resumed.state)
        self.assertEqual([], replacement_sender.calls)
        self.assertEqual(1, len(replacement_observer.calls))
        self.assertEqual(1, len(waker.calls))

    def test_crash_during_codex_wake_never_rewakes(self) -> None:
        sender = FakeSender()
        observer = FakeObserver(
            CompletionObservation("observed", "c" * 64, 68)
        )
        crashing_waker = FakeWaker(error=KeyboardInterrupt())
        runner = self.runner(sender, observer, crashing_waker)

        with self.assertRaises(KeyboardInterrupt):
            runner.run(self.request)
        self.assertEqual(1, len(crashing_waker.calls))

        replacement_waker = FakeWaker()
        resumed = self.runner(FakeSender(), observer, replacement_waker).run(
            self.request
        )
        self.assertEqual("codex_wake_intent_recorded", resumed.state)
        self.assertEqual([], replacement_waker.calls)

    def test_timeout_can_resume_observation_but_not_send(self) -> None:
        sender = FakeSender()
        first = self.runner(
            sender, FakeObserver(CompletionObservation("timeout")), FakeWaker()
        ).run(self.request)
        self.assertEqual("awaiting_completion", first.state)

        replacement_sender = FakeSender()
        waker = FakeWaker()
        resumed = self.runner(
            replacement_sender,
            FakeObserver(CompletionObservation("observed", "d" * 64, 67)),
            waker,
        ).run(self.request)
        self.assertEqual("codex_wake_requested", resumed.state)
        self.assertEqual([], replacement_sender.calls)
        self.assertEqual(1, len(waker.calls))

    def test_stop_before_send_consumes_intent_and_blocks_replay(self) -> None:
        (self.coop / "STOP.md").write_text("stop", encoding="utf-8")
        sender = FakeSender()
        observer = FakeObserver()
        waker = FakeWaker()
        runner = self.runner(sender, observer, waker)

        stopped = runner.run(self.request)
        (self.coop / "STOP.md").unlink()
        replay = runner.run(self.request)

        self.assertEqual("stopped_before_send", stopped.state)
        self.assertEqual(stopped, replay)
        self.assertEqual([], sender.calls)
        self.assertEqual([], observer.calls)
        self.assertEqual([], waker.calls)

    def test_stop_reported_by_observer_blocks_codex_wake(self) -> None:
        result = self.runner(
            FakeSender(),
            FakeObserver(CompletionObservation("stopped")),
            FakeWaker(),
        ).run(self.request)
        self.assertEqual("stopped_after_send", result.state)
        self.assertFalse(result.codex_wake_intent_recorded)

    def test_same_roundtrip_id_with_changed_request_is_conflict(self) -> None:
        runner = self.runner(
            FakeSender(), FakeObserver(CompletionObservation("timeout")), FakeWaker()
        )
        runner.run(self.request)
        changed_message_id = str(uuid.uuid4())
        with self.assertRaisesRegex(
            SupervisorError, "desktop_roundtrip_idempotency_conflict"
        ):
            runner.run(
                replace(
                    self.request,
                    message_id=changed_message_id,
                    message=restricted_wake_text(changed_message_id),
                )
            )

    def test_canonical_receipt_cannot_substitute_opaque_wake_binding(self) -> None:
        runner = self.runner(
            FakeSender(), FakeObserver(CompletionObservation("timeout")), FakeWaker()
        )
        runner.run(self.request)
        receipt_path = next(
            (self.coop / ".ccc" / "desktop-roundtrip" / "receipts").glob("*.json")
        )
        value = json.loads(receipt_path.read_text(encoding="utf-8"))
        value["wake_ref"] = "wake_" + "0" * 24
        receipt_path.write_bytes(canonical_json_bytes(value))
        with self.assertRaisesRegex(
            SupervisorError, "desktop_roundtrip_idempotency_conflict"
        ):
            runner.run(self.request)

    def test_completion_path_cannot_escape_configured_root(self) -> None:
        with self.assertRaisesRegex(SupervisorError, "completion_ref_invalid"):
            self.runner(FakeSender(), FakeObserver(), FakeWaker()).run(
                replace(self.request, completion_ref="../outside.json")
            )

    def test_desktop_message_must_match_message_id_derived_wake(self) -> None:
        runner = self.runner(FakeSender(), FakeObserver(), FakeWaker())
        for message in (
            "raw task body\nsecond line",
            "run {arbitrary-code}",
            "본문 전체를 전달",
            "x" * 513,
            restricted_wake_text("22222222-2222-4222-8222-222222222222"),
        ):
            with self.subTest(message=message[:20]), self.assertRaisesRegex(
                SupervisorError, "desktop_message_invalid"
            ):
                runner.run(replace(self.request, message=message))

    def test_unexpected_port_result_is_ambiguous_not_success(self) -> None:
        sender = FakeSender(result=True)
        sender.result = "yes"  # type: ignore[assignment]
        receipt = self.runner(
            sender, FakeObserver(CompletionObservation("timeout")), FakeWaker()
        ).run(self.request)
        self.assertEqual("send_ambiguous", receipt.state)
        self.assertEqual("desktop_send_ambiguous", receipt.failure_code)
        self.assertFalse(receipt.send_requested)


class CompletionFileObserverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.path = self.root / "done.json"
        self.clock = AdvancingClock()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def observer(self, *, max_bytes: int = 4096) -> BoundedCompletionFileObserver:
        return BoundedCompletionFileObserver(
            timeout_seconds=1,
            max_bytes=max_bytes,
            stability_samples=2,
            stability_interval_seconds=0.1,
            clock=self.clock,
            sleeper=self.clock.sleep,
        )

    def write_completion(self, nonce: str = NONCE, **extra) -> bytes:
        value = {
            "schema": COMPLETION_SCHEMA,
            "state": "completed",
            "nonce": nonce,
            **extra,
        }
        data = canonical_json_bytes(value)
        self.path.write_bytes(data)
        return data

    def test_exact_stable_canonical_file_is_observed(self) -> None:
        data = self.write_completion()
        result = self.observer().observe(
            self.path, expected_nonce=NONCE, stop_requested=lambda: False
        )
        self.assertEqual("observed", result.state)
        self.assertEqual(len(data), result.content_bytes)

    def test_missing_file_times_out_with_finite_clock(self) -> None:
        result = self.observer().observe(
            self.path, expected_nonce=NONCE, stop_requested=lambda: False
        )
        self.assertEqual(CompletionObservation("timeout"), result)
        self.assertGreaterEqual(self.clock.value, 1)

    def test_stop_interrupts_observation(self) -> None:
        result = self.observer().observe(
            self.path, expected_nonce=NONCE, stop_requested=lambda: True
        )
        self.assertEqual(CompletionObservation("stopped"), result)
        self.assertEqual(0, self.clock.value)

    def test_wrong_nonce_extra_keys_and_noncanonical_json_fail_closed(self) -> None:
        cases = []
        cases.append(canonical_json_bytes({
            "schema": COMPLETION_SCHEMA,
            "state": "completed",
            "nonce": "nonce_ffffffffffffffff",
        }))
        cases.append(canonical_json_bytes({
            "schema": COMPLETION_SCHEMA,
            "state": "completed",
            "nonce": NONCE,
            "result": "prose is forbidden",
        }))
        cases.append(json.dumps({
            "schema": COMPLETION_SCHEMA,
            "state": "completed",
            "nonce": NONCE,
        }, indent=2).encode("utf-8"))
        for data in cases:
            with self.subTest(data=data):
                self.clock.value = 0
                self.path.write_bytes(data)
                with self.assertRaises(SupervisorError):
                    self.observer().observe(
                        self.path,
                        expected_nonce=NONCE,
                        stop_requested=lambda: False,
                    )

    def test_size_bound_and_symlink_fail_closed(self) -> None:
        self.path.write_bytes(b"x" * 65)
        with self.assertRaisesRegex(SupervisorError, "completion_file_too_large"):
            self.observer(max_bytes=64).observe(
                self.path, expected_nonce=NONCE, stop_requested=lambda: False
            )

        self.path.unlink()
        target = self.root / "target.json"
        target.write_bytes(canonical_json_bytes({
            "schema": COMPLETION_SCHEMA,
            "state": "completed",
            "nonce": NONCE,
        }))
        try:
            self.path.symlink_to(target)
        except OSError:
            self.skipTest("symlink creation unavailable")
        with self.assertRaisesRegex(SupervisorError, "completion_file_type_invalid"):
            self.observer().observe(
                self.path, expected_nonce=NONCE, stop_requested=lambda: False
            )


if __name__ == "__main__":
    unittest.main()
