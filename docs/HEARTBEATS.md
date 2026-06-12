# Heartbeats

Heartbeats are recurring wakeups that keep an agent from silently going idle.

## Recommended Intervals

- 5 minutes: active production run, high uncertainty, operator away.
- 10 minutes: normal co-op work.
- 15 minutes: low-risk monitoring.
- 30 minutes: long background jobs where only status checks matter.

## Heartbeat Prompt Template

```text
CCC heartbeat for <project>. Worktree: <absolute path>.

Every turn:
1. Check coop/STOP.md.
2. Read coop/chat.md tail.
3. Check coop/inbox_<this_agent>/ for unhandled tasks.
4. Check coop/operator/commands.md.
5. If there is new work, handle it within the current write constraints.
6. If there is no new work, perform the agreed standing audit or report idle.

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

