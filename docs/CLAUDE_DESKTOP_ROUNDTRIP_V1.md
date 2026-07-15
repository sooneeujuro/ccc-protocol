# Claude Desktop to Codex round-trip v1

## Outcome

This path performs one bounded handoff:

1. open or verify one pinned Claude Desktop Code session;
2. record a local send intent;
3. place one short `read the local inbox` wake message in that session;
4. observe an exact local completion receipt;
5. record a Codex-wake intent; and
6. wake one pre-bound Codex Desktop task.

It is not a general chat bot, a window-title macro, or a loop that retries until
something appears to work.

## Authority boundaries

- The Claude profile pins the Desktop build and session bridge.  The UIA binding
  pins the process image, current session surface, workspace, composer, and send
  control, and reuses the canonical Windows build probe to compare the installed
  build with the profile immediately before the first UI action.
- The wake message contains no task body.  Task prose stays in the project-local
  `coop/inbox_claude/` file selected by the operator.
- The generic wake phrase is not a task selector.  Before recording the send
  intent, the live coordinator must prove there is exactly one unhandled Claude
  inbox task for this round trip; zero or multiple candidates fail closed.
- The completion file is canonical JSON with exactly `schema`, `state`, and a
  pre-issued nonce.  It contains no result prose.
- The Codex task identifier belongs to the injected Codex app wake port.  Raw
  Claude session IDs, Codex task IDs, local paths, prompts, and nonces are absent
  from the durable round-trip receipt.
- Screen evidence is not completion evidence.  Only the nonce-bearing file is.

## Safety state machine

```text
send_intent_recorded
  -> send_requested_unverified | send_ambiguous
  -> awaiting_completion
  -> completion_observed
  -> codex_wake_intent_recorded
  -> codex_wake_requested | codex_wake_ambiguous
```

`STOP.md` is checked before the Desktop send, while observing completion, and
before the Codex wake.  Both irreversible operations have an `O_EXCL` intent
record.  If the supervisor is killed after an intent is recorded, restarting it
may continue observation or reconciliation but cannot repeat the send or wake.

Force-stopping the supervisor or its owned helper is therefore supported.
Force-killing Claude Desktop or Codex Desktop is outside this contract because
those applications may contain other sessions or unsaved operator work.

## Windows Desktop transport

Install the optional transport with:

```powershell
python -m pip install -e ".[claude-desktop]"
```

The transport uses Windows UI Automation semantic controls.  It must find one
Claude process/window and one pinned current-session surface.  The expected
session title, workspace, prompt group, and send control must all resolve inside
that surface.  Missing, duplicate, hidden, disabled, changed, or already-filled
surfaces fail closed.  An initially enabled send button is treated as non-text
composer content, such as an attachment, even when the prompt appears empty.
The v1 does not use the clipboard, OCR, absolute screen coordinates, DevTools
injection, or Claude's private renderer IPC.

Only the generated `CCCP WAKE <canonical UUID> ...` phrase derived from the
request's message id is allowed.  Both the round-trip state machine and the
Windows send port enforce the same exact phrase.  The full scientific or coding
prompt never enters command-line arguments, URI query parameters, logs, or the
durable receipt.

The messenger lock is process-local and serializes one messenger instance; it
is not a cross-process or session-global lock.  Live v1 operation therefore
uses one designated coordinator and must not launch concurrent round trips at
the same Claude session from separate processes.  That coordinator also owns
the singleton-pending-inbox preflight; the UI transport deliberately does not
guess which local task file Claude should consume.

## Live-driver limitation

`DesktopRoundTrip` is the deterministic local state machine.  Its send and wake
operations are injected ports so both can be tested without controlling an app.
The current supported exact Codex-task wake is available to a Codex Desktop
task through the app's task-messaging tool.  It is not exposed as a public local
endpoint to the standalone Python process.  Consequently the live v1 is driven
by a designated Codex coordinator task; the package alone must not claim an
end-to-end Codex wake.

## Verification

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -p 'test_*.py' -v
$env:CCCP_TEST_INSTALLED_CLAUDE='1'
python -m unittest discover -s tests -p 'test_claude_desktop.py' -k test_installed_desktop_build_matches_release_pin -v
git diff --check
```

Use synthetic inbox and completion files for the first live canary.  Never use
a manuscript, corpus, sidecar, protected prose, or credentials as the canary.
