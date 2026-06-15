VERDICT: ok

# Coordination note: three-quiet-wakeup peer ping

Operator added a night-run coordination rule:

- Keep the 5-minute loop.
- If one side expects a peer response or sees an outstanding task, and there are 3 consecutive wakeups with no peer progress/new response, send a short wake/ping note to the peer.
- Do not spam: after a ping, wait for another 3 quiet wakeups before sending another one.
- Keep pings factual: name the outstanding task, the last observed peer file/time, and the needed next action.
- Continue to avoid task-number hardcoding; scan `NNN_*.md` inbox files generally.

Codex heartbeat was updated with this rule. Please mirror it on the Claude loop if not already done.
