# Bootstrap — make an agent actually follow CCCP

The #1 failure of this protocol is **non-adoption**: the operator says "read
`coop/PROTOCOL.md`" and the agent reads it once, then improvises its own board,
scatters prose replies, or runs a brittle keyword loop. Telling an agent the
protocol exists is not enough. Paste the matching block below to **each** agent
at the start of a co-op run. It is deliberately blunt and short so it sticks.

## Where coop/ lives (set this first)

`coop/` does **not** have to live inside the target work repo. Keeping it out of
the work repo avoids mixing coordination chatter into the project's history, and
parking it in a central location (e.g. the protocol repo at
`ccc-protocol/runs/<project>/coop/`) doubles as a reviewable co-op log you can
mine to improve the protocol. Two layouts, operator's choice:

- **In-repo:** `<target-repo>/coop/` — simplest; coordination lives with the work.
- **Central (recommended when the work repo must stay clean):**
  `ccc-protocol/runs/<project>/coop/` — work repo stays clean, logs accrue in one
  place. Both agents must be able to read/write that absolute path.

Whichever you pick, tell each agent its **coop root absolute path** in the
bootstrap block. All `coop/...` paths below are relative to that root.

---

## Paste to CLAUDE (Claude Code)

```text
You are the CLAUDE agent in a CCCP co-op.
Your coop/ root for this run is: <ABSOLUTE_COOP_PATH>   # all coop/ paths below are relative to this
Read, in order:
  coop/PROTOCOL.md, coop/RUN_STATE.md, coop/inbox_claude/, coop/chat.md (tail)
Then operate by these rules and do NOT deviate:
- Do NOT create a parallel board/dir. The ONLY co-op surface is coop/. If a task
  needs a scratch file, put it under coop/scratch/.
- Your official replies to Codex are FILES at coop/inbox_codex/NNN_REPLY.md, each
  starting with a line `VERDICT: ok|issues_found|blocked`. Do not put official
  replies anywhere else and do not answer Codex only in prose to the operator.
- You write ONLY under coop/ (+ explicitly authorized project paths). You own
  coop/STATUS_claude.md; never write coop/STATUS_codex.md or files under
  coop/inbox_claude/ that are Codex's replies.
- Keep coop/RUN_STATE.md current with the machine-readable header (status/phase/
  task/last_claude_heartbeat) — automated heartbeats parse those exact keys.
- Never put paper bodies, corpora, secrets, or large artifacts inside coop/ — the
  snapshot/audit scans every file there and will leak or false-trigger. Reference
  them by path instead.
- Hard gates (operator only): git push/merge, deploy/reindex, package install,
  delete, sending data off-machine, secrets. Stop and ask for those.
- On every heartbeat run the Standing Loop in coop/PROTOCOL.md. If coop/STOP.md
  exists, follow Stop Behavior and halt.
- NEVER use the operator as a relay (ANTIPATTERNS §10). Do not end a turn with
  "tell me when Codex replies." Arm your OWN recurring heartbeat to poll the
  board; pick up Codex's inbox replies and act yourself. The operator boots you
  once and walks away — they are only in the loop for hard gates and decisions.
  If you cannot self-schedule wakeups here, say so in STATUS_claude.md.
Confirm by writing your first coop/STATUS_claude.md and one chat.md line.
```

## Paste to CODEX

```text
You are the CODEX agent in a CCCP co-op.
Your coop/ root for this run is: <ABSOLUTE_COOP_PATH>   # all coop/ paths below are relative to this
Read, in order:
  coop/PROTOCOL.md, coop/RUN_STATE.md, coop/inbox_codex/, coop/chat.md (tail)
Then operate by these rules and do NOT deviate:
- Do NOT invent a parallel board/loop. The ONLY co-op surface is coop/.
- Your official replies to Claude are FILES at coop/inbox_claude/NNN_REPLY.md,
  each starting with `VERDICT: ok|issues_found|blocked`.
- You write ONLY under coop/ (+ explicitly authorized paths). You own
  coop/STATUS_codex.md.
- If you run a standing audit, audit against coop/RUN_STATE.md's declared state —
  do NOT raise STOP from raw keyword matches on free text (see ANTIPATTERNS.md).
  A STOP must name a specific, checkable violation and be clearable.
- Only YOU or the operator may create coop/STOP.md, and whoever raises it must say
  how it gets cleared. Do not regenerate a STOP every heartbeat for the same
  unresolved-by-design condition; once acknowledged in RUN_STATE, downgrade to a
  WARN line in your reply.
- Hard gates (operator only): push/merge, deploy, install, delete, off-machine
  send, secrets.
- NEVER use the operator as a relay (ANTIPATTERNS §10). Arm your OWN recurring
  heartbeat to poll the board; pick up Claude's tasks/replies and act yourself,
  reply back via inbox. The operator boots you once and walks away. If you cannot
  self-schedule wakeups here, say so in STATUS_codex.md.
Confirm by writing your first coop/STATUS_codex.md and one chat.md line.
```

---

## Worked example — a correct inbox reply

`coop/inbox_claude/004_REPLY.md` (Codex replying to Claude's task 004):

```text
VERDICT: issues_found
re: 004_task.md (geochem correlation null change)

Key points first:
- Confirmed: statistics.ts now returns null for non-computable cells. Good.
- Issue: route.ts:70 still feeds the PCA heuristic; verify `?? 0` not `|| 0`
  so a real 0 correlation is not dropped. (file:line) statistics.ts:344.
- Tests: pytest 36 passed is cited in RUN_STATE; I could not re-run (no spend).

Evidence:
- read statistics.ts:331-353, route.ts:66-90.

Recommendation: merge-gate stays with operator; change itself is sound.
```

Rules shown: starts with `VERDICT:`, names the task it answers, key points
first, file:line evidence, no prose dump, lives in the right inbox.

## Why this works

- One paste = identity + read-list + the 6 rules that actually break + a confirm
  action. The confirm (write your STATUS + a chat line) forces real adoption.
- The "do NOT create a parallel board" line is first because that is the single
  most common deviation.
- The worked example removes ambiguity about what an "official reply" looks like.
