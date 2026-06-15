VERDICT: blocked

# TASK 017 - Figure re-extraction status clarification

Operator asked: "이어간다는게 무슨소리요... 그림안뽑았어 아직??"

Codex checked the repo-side state on 2026-06-16:

- `detangle/norm_artifacts/FINAL_SUMMARY.md` says the figure track is separate and environment-blocked: about 830 figures need the datalab machine + NAS.
- `detangle/inbox_codex/015_CLAUDE_LOOP_ACK.md` says there is no dedicated figure re-extraction progress artifact in this repo beyond reminders.
- Local `manuscript-atelier` has no obvious new figure re-extraction output in the repo tree; only the older figure tooling / bridge code is visible.
- Earlier `fig_refill_20260613/out*` material appears to be old/quarantined/NAS-integration residue, not evidence of the current 830-figure re-extraction being freshly completed.

Please confirm on your side whether any off-repo or remote-machine figure extraction actually ran. If not, report plainly that the VP-NORM-1 normalization finished but the pending figure re-extraction/refill did not run and remains blocked/waiting on datalab + NAS/operator environment.

Do not push figure data, corpus data, paper text, sidecars, or indexes. Do not run irreversible extraction without explicit operator instruction.
