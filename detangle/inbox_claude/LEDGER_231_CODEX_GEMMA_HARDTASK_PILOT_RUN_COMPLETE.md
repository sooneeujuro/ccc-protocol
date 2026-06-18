# LEDGER_231 - Codex Gemma hard-task pilot run complete

Timestamp: 2026-06-18 16:58 KST

Scope: Gemma prompt tournament hard-task pilot after the operator chose path (b): harder task plus 0-3 discriminating rubric. This note contains only local paths, counts, timing, and gate error codes. It intentionally does not echo task prose, resolved scientific values, or model responses.

## Run

- Tournament id: `gemma-tournament-20260618T064019Z`
- Local run directory: `C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T064019Z`
- Run manifest: `C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T064019Z\LOCAL_GEMMA_TOURNAMENT_RUN.local.json`
- Blind scoring manifest: `C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T064019Z\LOCAL_GEMMA_TOURNAMENT_SCORING_BLIND.local.json`
- Prepare/blind contract manifest: `C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T064019Z\LOCAL_GEMMA_PROMPT_TOURNAMENT_BLIND.safe.json`
- Variant preset: `round1`
- Scoring rubric: `discriminating_v2`
- Score scale: `0-3`
- Score axes: `claim_altitude_two_sided`, `bound_tightness`, `caveat_survival`, `register_fit`, `protected_preservation`, `conciseness_vs_completeness`
- Repetitions: `5`
- Expected model calls: `45`

## Result

- Entries: `45`
- Passed: `43`
- Failed: `2`
- Runner stderr: `0` bytes
- Started: `2026-06-18T06:41:44Z` / `2026-06-18 15:41:44 KST`
- Completed: `2026-06-18T07:54:10Z` / `2026-06-18 16:54:10 KST`
- Total elapsed: `4,347,000 ms` (`72m 27s`)
- Median entry elapsed: `91,422 ms`
- P90 entry elapsed: `133,156 ms`

Per persona:

| Persona | Passed | Failed |
|---|---:|---:|
| Bold | 14 | 1 |
| Measured | 14 | 1 |
| Terse | 15 | 0 |

Failed entries:

| Persona | Blind id | Attempts | Error codes |
|---|---|---:|---|
| Measured | `blind_7e6f37c5563fe767` | 2 | `gemma_candidate_protected_term_missing`; `gemma_candidate_forbidden_term_present` |
| Bold | `blind_9167875968577d5b` | 2 | `gemma_candidate_forbidden_term_present`; `gemma_candidate_forbidden_term_present` |

## Claude handoff

The 43 passed responses are ready for blind scoring with the `discriminating_v2` 0-3 rubric. Please use the blind scoring manifest and keep the reveal closed until scoring is complete. This is an N=5 hard-task pilot run, not the N=8/two-run reproducibility phase yet.

Notes:

- The scoring manifest is response-only and withholds execution paths and variant mapping.
- The full rubric id is present in the prepare/blind contract manifest. The scoring manifest carries the axes and selection rule.
- No response prose or resolved task values were committed or relayed in this note.
