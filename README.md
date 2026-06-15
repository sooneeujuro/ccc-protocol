# CCC Protocol

Codex-Claude Cowork Protocol, codename CCCP.

This repo stores a reusable file-based co-op protocol for running Codex and Claude Code in the same project without turning the operator's machine into a black box.

The goal is simple:

- predictable inboxes
- heartbeat/wakeup discipline
- append-only chat
- periodic GitHub snapshots
- clear stop/final-summary behavior
- remote operator commands when the operator is away from the machine

## Quick Start

From a target project repo:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\USER\Documents\ccc-protocol\scripts\install-ccc.ps1 -ProjectRoot .
```

Then **bootstrap each agent with the paste-blocks in [`docs/BOOTSTRAP.md`](docs/BOOTSTRAP.md)**
— do not just say "read the protocol". Telling an agent the protocol exists is
the #1 reason co-ops fail (the agent reads it once, then improvises its own
board). The bootstrap block forces adoption with a read-list + the 6 rules that
actually break + a confirm action. Each agent should read:

```text
coop/PROTOCOL.md
coop/RUN_STATE.md
coop/inbox_<agent>/
coop/chat.md (tail)
```

If a run "isn't working", check [`docs/ANTIPATTERNS.md`](docs/ANTIPATTERNS.md) first —
it lists the observed failure modes (parallel-board drift, prose-instead-of-inbox,
brittle keyword-STOP, payload in coop/, ...) with fixes.

Use a heartbeat interval such as 5, 10, or 15 minutes. Short intervals are good for hot operations; longer intervals are better for quiet monitoring. For unattended watch mode, use adaptive quiet backoff: 10 minutes, then 30 minutes, then 90 minutes after 3 consecutive no-op checks at each level.

## Repo Layout

```text
docs/
  HEARTBEATS.md
  OPERATOR_REMOTE.md
  GITHUB_SYNC.md
scripts/
  install-ccc.ps1
  ccc_status.ps1
  ccc_push_snapshot.ps1
templates/
  coop/
    PROTOCOL.md
    RUN_STATE.md
    chat.md
    inbox_codex/
    inbox_claude/
    operator/
    reports/
    scratch/
```

## Design Principles

- Agents write only inside `coop/` unless the operator explicitly grants broader write scope.
- Official findings go through inbox reply files with `VERDICT: ok|issues_found|blocked`.
- `chat.md` is useful but disposable; it is not the official ledger.
- Each agent owns its own reply/status files to avoid merge conflicts.
- Push snapshots are for observability, not for dumping sensitive corpora or giant artifacts.
- Destructive actions require explicit operator approval.

## Suggested Naming

Use `ccc-protocol` for the protocol repo. If you like the bit, call it "CCCP" in chat, but keep the public-facing name boring enough for work.
