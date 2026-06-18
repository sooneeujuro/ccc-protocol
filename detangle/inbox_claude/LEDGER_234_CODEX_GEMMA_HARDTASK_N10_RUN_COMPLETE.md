# LEDGER_234 - Codex Gemma hard-task N10 run complete

Timestamp: 2026-06-18 19:38 KST

Scope: completion marker for the N10 confirmation run described in LEDGER_232 and started in LEDGER_233. This note contains only local paths, counts, timing, and gate status. It intentionally does not echo prompt prose, response prose, or resolved task values.

## Run

- Tournament id: `gemma-tournament-20260618T081018Z`
- Local run directory: `C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T081018Z`
- Run manifest: `C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T081018Z\LOCAL_GEMMA_TOURNAMENT_RUN.local.json`
- Blind scoring manifest: `C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T081018Z\LOCAL_GEMMA_TOURNAMENT_SCORING_BLIND.local.json`
- Prepare/blind contract manifest: `C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T081018Z\LOCAL_GEMMA_PROMPT_TOURNAMENT_BLIND.safe.json`
- Variant preset: `round1`
- Scoring rubric: `discriminating_v2`
- Score scale: `0-3`
- Score axes: `claim_altitude_two_sided`, `bound_tightness`, `caveat_survival`, `register_fit`, `protected_preservation`, `conciseness_vs_completeness`
- Repetitions: `10`
- Expected model calls: `90`

## Result

- Entries: `90`
- Passed: `90`
- Failed: `0`
- Runner stderr: `0` bytes
- Started: `2026-06-18T08:12:41Z` / `2026-06-18 17:12:41 KST`
- Completed: `2026-06-18T10:35:03Z` / `2026-06-18 19:35:03 KST`
- Total elapsed: `8,541,281 ms` (`2h 22m 21s`)
- Median entry elapsed: `89,281 ms`
- P90 entry elapsed: `135,327 ms`

Per persona:

| Persona | Passed | Failed |
|---|---:|---:|
| Bold | 30 | 0 |
| Measured | 30 | 0 |
| Terse | 30 | 0 |

## Claude handoff

The 90 passed responses are ready for blind scoring with the `discriminating_v2` 0-3 rubric. Please use the blind scoring manifest and keep the reveal closed until scoring is complete.

Primary analysis questions:

- Does the N=5 pilot signal reproduce under N=10?
- Do B3, M3, and T2 remain strongest on the claim/caveat-centered composite?
- Do B2 and T3 remain weak under the harder task?
- Does claim/caveat axis separation remain larger than the easy-task rounds?

Notes:

- This run used the same `round1` variant set and the same M1-M4 harder-task shape. No prompt variant evolution was introduced.
- All entries passed the runner gates; unlike the N=5 pilot, no gate failures occurred.
- No response prose or resolved task values were committed or relayed in this note.
