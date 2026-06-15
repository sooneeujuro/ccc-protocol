# Anti-patterns — how CCCP co-ops actually break

These are observed failure modes from real Codex↔Claude runs, with the fix.
If a run "isn't working," it is almost always one of these.

## 1. Parallel-board drift (most common)
**Symptom:** an agent ignores `coop/` and improvises its own board (e.g.
`some_run_2026xxxx/` with a custom `verdicts/` dir and ad-hoc filenames). The
two agents end up on different surfaces and never actually meet.
**Fix:** the bootstrap block forbids this explicitly. The ONLY co-op surface is
`coop/`. Scratch goes under `coop/scratch/`. If you already drifted, move the
state into `coop/` and delete the parallel board.

## 2. Prose-instead-of-inbox
**Symptom:** an agent "replies" by writing prose to the operator, or drops
free-form `.md` notes outside the inboxes. The other agent never sees an official
reply; nothing is parseable.
**Fix:** official replies are files at `coop/inbox_<other>/NNN_REPLY.md` starting
with `VERDICT:`. See the worked example in `BOOTSTRAP.md`. Chat is disposable.

## 3. Non-machine-readable RUN_STATE
**Symptom:** an automated heartbeat/audit reports `status: unknown` because
`RUN_STATE.md` is all prose. The watcher cannot tell what phase the run is in.
**Fix:** keep the machine-readable header at the top of `RUN_STATE.md` —
`key: value` at line start for `status`, `phase`, `task`, `last_<agent>_heartbeat`.
Prose can follow, but those keys must be parseable.

## 4. Brittle keyword-STOP (false-positive halts)
**Symptom:** a watcher raises STOP from a raw keyword match on free text
(e.g. STOP whenever the board contains both "Fischer" and "AGU Centennial"). A
*diagnosis that correctly documents a problem* trips the same keyword, so the
STOP fires every heartbeat and never clears — halting the whole run on a
non-issue.
**Fix:** a STOP must name a **specific, checkable violation**, not a keyword
co-occurrence. Audit against `RUN_STATE.md`'s *declared* state, not raw prose.
Once a flagged condition is acknowledged in `RUN_STATE.md`, downgrade it to a
`WARN` line in the reply instead of re-raising STOP. Prefer evidence the watcher
can verify (a sha1, a file diff, a count) over text matching.

## 5. STOP with no owner / no clear path
**Symptom:** a STOP file appears and the run halts, but nobody knows who may
clear it or how, so it lingers. Worse, an auto-writer regenerates it each tick.
**Fix:** whoever raises a STOP states (in the STOP file) the exact condition and
how it clears. Auto-generated STOPs must not regenerate for a
resolved-or-by-design condition. The operator can always clear a STOP; an agent
may clear a STOP it raised once the named condition is resolved, leaving a note.

## 6. Polluting coop/ with payload (leaks + false triggers)
**Symptom:** an agent stages paper bodies, corpora, or large outputs **inside**
`coop/`. The snapshot then commits sensitive/huge data, and the audit scans those
bytes — e.g. a number in a paper gets read as a "cost" value and raises a budget
WARN.
**Fix:** `coop/` holds coordination state only (status, inboxes, small ledgers).
Real data lives outside (NAS/project paths); reference it by path. Snapshot
policy in `PROTOCOL.md` lists what may be committed.

## 7. "I am polling" without real automation
**Symptom:** an agent claims it will check every N minutes, but no heartbeat
exists, so it silently goes idle.
**Fix:** if the platform does not guarantee recurring wakeups, say so plainly in
`STATUS_<agent>.md`. Re-arm the heartbeat each turn if manual re-arming is needed.

## 8. Shared-file write conflicts
**Symptom:** both agents write the same status file and clobber each other.
**Fix:** each agent owns `STATUS_<agent>.md` and writes replies only into the
*other* agent's inbox. Never edit the peer's status or reply files.

## 9. Stale-context big action
**Symptom:** an agent wakes and does a large action without re-reading
`chat.md`/inbox, acting on outdated assumptions.
**Fix:** the Standing Loop reads STOP → chat tail → inbox → operator commands
*before* doing work. Always.
