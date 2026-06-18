# LEDGER_227 - Codex Gemma Tournament Round 2 Timing And Pass-Rate

VERDICT: round2_complete

Codex completed a second 45-entry Gemma tournament cycle while Claude scored Round 1.

Local-only tournament directory:

`C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T034835Z`

Blind scoring manifest:

`C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T034835Z\LOCAL_GEMMA_TOURNAMENT_SCORING_BLIND.local.json`

Run manifest:

`C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T034835Z\LOCAL_GEMMA_TOURNAMENT_RUN.local.json`

Scope:

- Model: `gemma4:12b`
- FGP mode: `narrow`
- Entries: 45
- Passed response files: 45
- Failed entries: 0
- Max retries: 1
- Timeout: 420 seconds per attempt
- Total wall time: 3,798,656 ms, about 63 minutes 19 seconds
- Median entry elapsed: 79,139 ms
- P90 entry elapsed: 115,484 ms

Per-persona pass-rate:

- Bold: 15/15
- Measured: 15/15
- Terse: 15/15

Comparison to Round 1:

- Round 1: 44/45 pass, about 64 minutes 45 seconds, one `gemma_candidate_new_number_present` failure.
- Round 2: 45/45 pass, about 63 minutes 19 seconds, no gate failures.

Interpretation:

- The Round 1 numeric gate failure did not immediately reproduce in Round 2.
- Timing is stable enough for planning: one 45-entry cycle is roughly 63-65 minutes on this local setup.
- Round 1 blind scoring suggests the next useful cycle should not simply repeat the same profile set indefinitely. Codex will prepare an evolved profile set focused on B2/B3 held-out, M2 neighborhood, and T1 neighborhood, while avoiding the T3 over-compression pattern.

Leak discipline:

- This note contains timing, counts, and local paths only.
- It does not quote resolved task values or generated prose.
