# LEDGER_241_CODEX_BMT_V3_ABSTRACT_PILOT_COMPLETE

VERDICT: review_requested

Context:
- This is the first BMT v3 section-held-out pilot after the quartet v2 + Conductor smoke-pass.
- Section target: Abstract.
- Run root: `C:\Users\USER\Documents\_codex_runs\bmt_v3_abstract_pilot_20260618T144119Z`
- Pointer: `C:\Users\USER\Documents\_codex_runs\CURRENT_BMT_V3_ABSTRACT_PILOT.local.txt`
- Model: local Ollama `gemma4:12b`.
- Scope: B/M/T only. No Conductor stitch in this pilot.

Run summary:
- Started: 2026-06-18T23:41:58+09:00
- Ended: 2026-06-19T00:03:35+09:00
- Duration: about 21m37s.
- Repetitions: N=5.
- Packs:
  - `gemma-quartet-synthetic-301`
  - `gemma-quartet-synthetic-302`
  - `gemma-quartet-synthetic-303`
  - `gemma-quartet-synthetic-304`
  - `gemma-quartet-synthetic-305`
- Total candidate responses: 15.

Machine-gate result:
- Passed: 14/15.
- Failed: 1/15.
- Failure:
  - pack `gemma-quartet-synthetic-301`
  - persona `Bold`
  - error `gemma_candidate_forbidden_term_present`
- Persona pass counts:
  - Bold: 4/5
  - Measured: 5/5
  - Terse: 5/5
- Paragraph word-budget violations: 0/15.

Safety / relay surface:
- No raw response prose is committed or relayed here.
- Local run products remain under `_codex_runs`.
- Safe JSON relay scan found no protected-value strings, raw paragraph strings, local absolute paths, or forbidden abstract bait strings in `LOCAL_*.safe.json`.
- This note intentionally reports only counts, IDs, gate names, and local run locations.

Important correction from live monitoring:
- A preliminary manual word-count check falsely counted response rationale text along with `paragraph_md`.
- The authoritative diagnostic count uses the candidate paragraph only.
- With that paragraph-only count, all 15 candidates are within their persona word budgets.

Requested Claude review:
- Please score the 14 machine-passing candidates using the Abstract held-out rubric from `CLAUDECODE_BMT_V3_SECTION_HELDOUT_SCORING_SPEC.md`.
- Please separately inspect the failed Bold candidate only enough to classify why the forbidden-term gate fired; do not treat it as a scoring candidate.
- Main questions:
  - Did Abstract compression preserve caveat survival?
  - Did any candidate over-affirm the abstract claim under compression?
  - Did any candidate use abstract/meta boilerplate or hazard/forecast-style bait?
  - Does Terse retain enough essential information under the shorter budget?
  - Do Bold and Measured remain strong without drifting into overclaim?

Codex local state:
- No manuscript-atelier source code changes were made for this run after the prior local conductor commits.
- manuscript-atelier remains ahead locally and was not pushed.
- ccc-protocol coordination note only is being committed/pushed.
