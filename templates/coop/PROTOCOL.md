# Project CCC Protocol

This folder is the co-op workspace for Codex and Claude Code.

If supervisor v1 is enabled, `coop/.ccc/` is the local-only lifecycle source of
truth. Markdown files remain the human-readable collaboration surface. Read
`SUPERVISOR_POLICY.md` before starting a supervised run.

## Rules

- Read this file and `RUN_STATE.md` before starting.
- Check `STOP.md` first on every heartbeat.
- Official replies must start with `VERDICT: ok|issues_found|blocked`.
- Put key points first; details can go below.
- `chat.md` is informal and append-only.
- Do not rely on chat as the official record.
- Write only under `coop/` unless the operator grants broader scope.
- Do not commit, push, spend API money, or modify production data unless authorized.
- Do not commit or relay `coop/.ccc/`; it may contain raw task and result text.
- A task or wake must have an explicit idempotency key or wake id.
- A handoff cannot expand the original task's authority or write scope.
- Automatic wake, live adapters, UI nudge, and cloud doorbell are disabled until
  the operator enables each one separately.

## Inboxes

- Tasks for Codex: `coop/inbox_codex/NNN_task.md`
- Replies to Claude: `coop/inbox_claude/NNN_REPLY.md`
- Tasks for Claude: `coop/inbox_claude/NNN_task.md`
- Replies to Codex: `coop/inbox_codex/NNN_REPLY.md`

If a task file has no matching reply, it is pending.

## Standing Loop

1. Check `STOP.md`.
2. If supervised, verify the current run generation and fenced lease.
3. Check latest `chat.md`.
4. Check own inbox.
5. Check `operator/commands.md`.
6. Handle one claimed task within its effect, retry, time, and output bounds.
7. If idle, run the standing audit defined in `RUN_STATE.md`.
8. Update status and heartbeat timestamp.

## Deterministic supervisor rules

- Only the local supervisor may claim a supervised task.
- Duplicate wake receipts do not start a second worker.
- Stale leases or fence epochs may not start or finish work.
- Only read-only or proven-reversible tasks may retry automatically, and only
  within the configured attempt budget.
- Mutating or external work stops for operator reconciliation after ambiguity.
- Success requires the enabled adapter's validated completion contract. The
  stock v1 CLI has no live profile binding and must not infer one.
- Raw prompts, output, paths, and protected data stay local. Share only safe
  counts, hashes, booleans, and status/failure enums.

## STOP

`STOP.md` is a state transition, not an informal suggestion. When it exists:

1. start no new wake, claim, retry, or handoff;
2. request bounded cancellation of active supervisor-owned work;
3. write the required final summary without starting new analysis;
4. wait for the run to drain to `stopped`;
5. do not resume merely because someone deletes STOP—start a new generation
   explicitly.

## UI and remote doorbell

UI automation is not a fallback adapter. It stays disabled unless the operator
approves a version-pinned, exact, one-shot selector with focus guards and a
cooldown.

A future remote doorbell may carry only an opaque `wake`, `stop`, or
`status_probe` envelope. It must never carry a prompt, free text, URL, path,
file, corpus content, or result payload.

