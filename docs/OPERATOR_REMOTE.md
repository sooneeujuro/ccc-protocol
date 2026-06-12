# Remote Operator Commands

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

