# Project CCC Protocol

This folder is the co-op workspace for Codex and Claude Code.

## Rules

- Read this file and `RUN_STATE.md` before starting.
- Check `STOP.md` first on every heartbeat.
- Official replies must start with `VERDICT: ok|issues_found|blocked`.
- Put key points first; details can go below.
- `chat.md` is informal and append-only.
- Do not rely on chat as the official record.
- Write only under `coop/` unless the operator grants broader scope.
- Do not commit, push, spend API money, or modify production data unless authorized.
- A subtask `FINAL_SUMMARY` or `VERDICT: ok` does not stop the run by itself.
- Do not stop/delete an active heartbeat unless `STOP.md` exists, the operator explicitly says to stop, or a peer-ACKed pause proposal says this agent may stand down while another watchdog remains active.

## Inboxes

- Tasks for Codex: `coop/inbox_codex/NNN_task.md`
- Replies to Claude: `coop/inbox_claude/NNN_REPLY.md`
- Tasks for Claude: `coop/inbox_claude/NNN_task.md`
- Replies to Codex: `coop/inbox_codex/NNN_REPLY.md`

If a task file has no matching reply, it is pending.

## Standing Loop

1. Check `STOP.md`.
2. Check latest `chat.md`.
3. Check own inbox.
4. Check `operator/commands.md`.
5. Handle pending tasks.
6. If idle, run the standing audit defined in `RUN_STATE.md`.
7. Update status and heartbeat timestamp.

## Pause / Stop / Ping

- Full stop requires `STOP.md` or an explicit operator stop command.
- To pause polling or stop peer pings, write an official proposal to the peer inbox and wait for `VERDICT: ok|issues_found|blocked`.
- If operator-level decisions remain, at least one agent keeps a watchdog heartbeat.
- Ping a peer only for an outstanding expected action.
- Send a peer ping after 3 quiet wakeups without peer progress; wait another 3 quiet wakeups before repeating.
- Stop pinging that item when it is answered, withdrawn, superseded, blocked with owner action, or both agents agree no peer action is needed.
