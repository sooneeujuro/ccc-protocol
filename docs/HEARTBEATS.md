# Heartbeats

> Legacy human-coordination guidance. A heartbeat is not a scheduler, lease,
> or authorization to call a model. Supervised runs follow
> `SUPERVISOR_V1.md`; automatic wakes remain off unless explicitly enabled.

Heartbeats are recurring wakeups that keep an agent from silently going idle.

## Recommended Intervals

- 5 minutes: active production run, high uncertainty, operator away.
- 10 minutes: normal co-op work.
- 15 minutes: low-risk monitoring.
- 30 minutes: long background jobs where only status checks matter.
- 90 minutes: quiet background watch after repeated no-op checks.

## Adaptive Quiet Backoff

Use adaptive quiet backoff when a run has recurring heartbeats but no active work is pending. This keeps the operator informed without burying the useful record under empty wakeups.

Default backoff ladder:

```text
10 minutes -> 30 minutes -> 90 minutes
```

Rules:

- Start active co-op work at 10 minutes unless the operator chooses another interval.
- Count a wakeup as quiet only when there is no STOP file, no inbox task, no operator command, and no meaningful audit finding.
- After 3 consecutive quiet wakeups at 10 minutes, update the heartbeat to 30 minutes and reset the quiet streak.
- After 3 consecutive quiet wakeups at 30 minutes, update the heartbeat to 90 minutes and reset the quiet streak.
- Keep 90 minutes as the normal quiet maximum.
- If new work appears at any interval, handle it, reset the quiet streak, and return to 10 minutes unless the operator asks otherwise.
- Notify the operator when the interval changes. Do not notify for routine quiet wakeups.
- Record the current interval and quiet streak in `coop/STATUS_<agent>.md` or `coop/RUN_STATE.md`.

Suggested status line:

```text
Quiet backoff: interval=30m, quiet_streak=0/3, next quiet level=90m.
```

## Heartbeat Prompt Template

```text
CCC heartbeat for <project>. Worktree: <absolute path>.

Every turn:
1. Check coop/STOP.md.
2. Read coop/chat.md tail.
3. Check coop/inbox_<this_agent>/ for unhandled tasks.
4. Check coop/operator/commands.md.
5. If there is new work, handle it within the current write constraints.
6. If there is no new work, perform the agreed standing audit only when needed.
7. Maintain adaptive quiet backoff: after 3 consecutive quiet wakeups at 10m, move to 30m; after 3 consecutive quiet wakeups at 30m, move to 90m; reset to 10m when new work appears.

Constraints:
- Write only under coop/ unless explicitly authorized.
- No API spend unless explicitly authorized.
- No git commit/push unless snapshot policy says so.
- Official findings require VERDICT files.
- Re-arm heartbeat if this platform requires it.
```

## Health Check

A heartbeat is healthy when:

- `RUN_STATE.md` has a recent timestamp.
- `chat.md` receives periodic status lines during active runs.
- pending task files receive matching replies.
- the operator can see pushed snapshots from another machine.

## Failure Modes

- The agent says it is polling but no automation exists.
- The agent does a large action after waking without re-reading chat/inbox.
- Both agents write the same status file and create conflicts.
- GitHub snapshots include sensitive or giant data.
