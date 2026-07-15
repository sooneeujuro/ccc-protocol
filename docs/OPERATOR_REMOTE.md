# Remote Operator Commands

> Legacy GitHub-console pattern. It is not connected to supervisor v1 and must
> not carry prompts or protected data. The future remote design is the strict
> metadata-only doorbell in `SUPERVISOR_V1.md`.

When the operator is away from the machine, use GitHub as the remote console.

## Option A: GitHub Issue

Create one issue titled:

```text
CCC Operator Console
```

The operator writes commands as comments. Agents poll the issue or mirror commands into:

```text
coop/operator/commands.md
```

Prefer one console issue per active project or run:

```text
CCC Operator Console: <project>
```

If multiple projects share one issue, every comment must include `Project:` and `Target:` fields. Agents should ignore commands for other projects unless the operator explicitly marks them as cross-project.

Agent status comments should be sparse and meaningful:

- Comment when work starts, completes, blocks, or changes heartbeat interval.
- Do not comment for routine quiet wakeups.
- Prefix reports with project and agent, for example `PYGMT_JYP / Codex`.
- Link related project consoles instead of mixing long status threads when two projects are running at once.

Recommended command format:

```text
COMMAND 2026-06-12 13:00 KST
Priority: high
Target: Codex and Claude
Instruction:
<what to do>
```

## Option B: commands.md

If agents can pull from GitHub, the operator edits:

```text
coop/operator/commands.md
```

Agents should record which command id was handled in `RUN_STATE.md`.

## Acknowledgement

Every remote command gets one of:

- accepted
- completed
- blocked
- declined with reason

Do not leave remote commands silently pending.
