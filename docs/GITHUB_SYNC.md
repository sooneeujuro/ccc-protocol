# GitHub Sync

> Legacy overview. Use `scripts/ccc_push_snapshot.ps1` for the mechanically
> allowlisted, branch-locked path. Never snapshot `coop/.ccc/`.

GitHub snapshots make a local co-op run visible from another machine.

## Snapshot Rule

During active unattended work, push a lightweight snapshot every 10-30 minutes or at important milestones.

Commit only operational files:

```text
coop/
```

Avoid committing raw data, PDFs, model outputs, secrets, or large generated directories.

## Suggested Commit Messages

```text
ccc: heartbeat snapshot 2026-06-12 13:00
ccc: report task 008 gold tranche
ccc: final summary
```

## Conflict Avoidance

- Agents append to `chat.md`.
- Codex owns `STATUS_codex.md`.
- Claude owns `STATUS_claude.md`.
- Shared state is generated or edited by only one designated owner.

## Private Repos

Use private repos for operator visibility. Private does not mean safe for secrets. Never commit credentials.

