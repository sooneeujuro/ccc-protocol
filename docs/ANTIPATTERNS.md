# Supervisor anti-patterns

These patterns are prohibited in CCCP supervisor v1. They either make the
lifecycle nondeterministic or expand the data and authority boundary without an
operator decision.

## Treating cooperative files as a scheduler

`chat.md`, status files, inbox files, and heartbeat prose are useful human
surfaces. They do not provide atomic claims, fencing, idempotency, cancellation,
or bounded retries. Do not infer that a task is exclusively owned because an
agent wrote “working on it.”

Use the local supervisor store for lifecycle state and the Markdown files for
human explanation.

## Reusing a vague “current session”

Never resume whichever Claude or Codex conversation happens to be most recent.
Bind an explicit adapter session/thread id to a run participant only after a
confirmed terminal result. A killed or partially observed session is ambiguous
and requires reconciliation.

## PID-only cleanup

Windows reuses process IDs. A PID recorded minutes earlier may now belong to an
unrelated process. Never terminate by PID alone. Require the expected creation
time, executable identity, and membership in the supervisor-owned Job Object.

Do not attach to or terminate the Codex app server that Codex Desktop already
owns.

## Retrying an effect because the error looks transient

A timeout after a Git push, message send, file mutation, or external API call
does not prove the effect did not happen. Automatic retry is reserved for
read-only or proven-reversible work, under a finite attempt budget. Mutating and
external tasks stop for operator reconciliation.

`retryable=true` is not permission to ignore the task effect class.

## Unbounded polling or “quiet watch forever”

Every run needs a watch TTL, wake budget, retry budget, and handoff-depth cap.
Adaptive backoff saves resources but does not create a termination condition.
When a budget is exhausted, enter `waiting_operator` instead of silently
renewing it.

## Checking STOP only between large tasks

STOP must be checked before accepting a wake, acquiring/renewing work, claiming,
starting, retrying, and handing off. Active adapters need bounded cancellation.
Deleting STOP must not resurrect an old generation.

## Success by exit code or friendly prose

Exit code zero without a valid terminal protocol event is not success. Neither
is an assistant sentence saying the work is finished. Validate the expected
session/thread and turn, the terminal state, output bounds, and the fenced task
receipt.

## Shell strings assembled from task content

Do not place prompts or task payloads in command-line arguments, PowerShell
command strings, or environment variables. Use stdin or a typed protocol. Pass
executable arguments as an argument list and validate every path and enum.

## Auto-approving permission requests

An unattended supervisor must not turn an unexpected approval dialog into an
automatic “yes.” Deny it, record `approval_required`, and return control to the
operator. Dangerous permission-bypass flags are outside v1.

## Capturing unlimited stdout “for debugging”

Agent output can contain private prose, paths, credentials, or very large
streams. Drain pipes continuously, enforce line/event/byte caps, keep only the
minimum local result, and export counts, hashes, and stable enums. Never put raw
stdout in `chat.md`, a Git snapshot, or cloud status.

## Committing `.ccc/`

`coop/.ccc/` contains local database files and may contain raw payload and
result envelopes. A repository-wide add, snapshot script, or backup that picks
it up violates the trust boundary. Keep a nested ignore rule and verify it with
Git before every rollout.

## Using UI automation as the primary adapter

Window titles, visible button labels, screen coordinates, OCR, and keyboard
shortcuts are not stable selectors. UIA must remain disabled until a signed,
version-pinned application exposes an exact unique selector. It may not steal
focus, type, paste, dismiss modals, or retry an ambiguous click.

A UI nudge is never evidence that a turn started.

## Falling back from a structured failure to UI silently

If Claude or Codex probing fails, report the failure. Do not secretly switch to
UI automation. The operator must enable the fallback profile explicitly, and
the one-shot/cooldown ledger still applies.

## Turning the cloud doorbell into a prompt relay

The future sooneeujuro.com/Vercel/Supabase surface may carry an opaque wake,
stop, or status-probe command. It must not carry prompts, prose, URLs, local
paths, file content, results, corpus excerpts, sidecars, manuscript text, or an
arbitrary command field.

The local supervisor polls outward. Do not expose a workstation listener or a
generic webhook that executes supplied content.

## Trusting frontend validation

Vercel form validation is not an authorization boundary. Supabase constraints,
row-level policy, and the local supervisor must independently enforce the same
strict schema, project binding, generation, expiry, replay id, and capability.
Unknown keys fail closed.

## Running the v1 database from several hosts

SQLite under a NAS share, synced folder, or two active machines is not a
distributed queue. Same-host v1 requires a local filesystem and one supervisor
authority. Multi-host execution needs a later protocol with explicit consensus,
leases, and split-brain recovery.

## Letting handoffs expand authority

A child task does not inherit permission to write, deploy, spend money, call an
external service, or exceed the original workspace. Handoffs inherit the
correlation chain but remain subject to their own effect class, policy, depth,
payload, and attempt bounds.

## Editing historical detangle evidence to fit v1

Historical detangle reports describe earlier behavior and should remain
immutable evidence. Supersede them with a current canonical document and a
clear link; do not rewrite the past to make the new supervisor appear older or
more complete than it is.
