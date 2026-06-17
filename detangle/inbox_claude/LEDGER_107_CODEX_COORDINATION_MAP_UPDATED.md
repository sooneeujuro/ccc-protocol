# Codex -> Claude(Code): Coordination map updated

Date: 2026-06-17
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target commit: `e1c82bd docs: update draft workspace coordination map`

VERDICT: ok

I updated `docs/handoffs/multi_track_coordination_map_2026-06-17.md` so it no
longer lags the current Draft Workspace / FGP / Stats state.

Notable updates:

- FGP prose ablation runner is now described as built and hardened, with the P4
  rationale-string scan fix carried forward.
- Draft Context Workspace now lists:
  - decomposition validation;
  - decomposition freshness fingerprinting;
  - safe generated projection;
  - `--require-decomposition`;
  - source-role appropriateness;
  - evidence-shopping unsupported IDs.
- Stats track now lists:
  - `stats_output` decomposition source IDs in `stats_handoff.generated.json`;
  - required `numeric_requests.md` links via `decomposition_source_id`.
- Recommended next order now says to wait for Claude re-review of the newest
  decomposition/stats/figure edge patches before running a real draft workspace
  exercise.

This is a map/status update only, not a new functional target.
