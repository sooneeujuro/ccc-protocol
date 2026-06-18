# LEDGER_244_CODEX_BMT_V3_INTRO_PILOT_COMPLETE

Timestamp: 2026-06-19 01:4x KST

VERDICT: review_requested

Scope:
- BMT v3 section-held-out suite, Introduction result-leak pilot.
- Local-only run root: `C:\Users\USER\Documents\_codex_runs\bmt_v3_intro_profile_v3_20260619T012344`
- Task: `writing_task_lee_intro_take01.local.json`
- Profile: `lee2025_discussion_register_v3`
- Model: `gemma4:12b`
- FGP mode: `narrow`
- Runs: `gemma-quartet-synthetic-501` through `gemma-quartet-synthetic-505`
- This note commits counts/flags only. It does not relay response prose, result values, or protected article text.

Run status:
- Started: 2026-06-19 01:24:08 KST
- Ended: 2026-06-19 01:40:40 KST
- Duration: about 16m33s
- Prompt prepare: 5/5 ok
- Ollama B/M/T responses: 15/15 produced
- Candidate diagnostics: 11 passed / 4 failed

Per-persona diagnostics:

| Persona | Pass | Word counts | Diagnostic issue |
|---|---:|---|---|
| Bold | 5/5 | 129, 148, 129, 129, 139 | none |
| Measured | 5/5 | 142, 135, 143, 153, 132 | none |
| Terse | 1/5 | 112, 126, 104, 130, 123 | 4x `gemma_candidate_protected_term_missing` |

Failure detail:
- All 4 failures are Terse.
- All 4 failures are the same protected-term omission: `spring gases`.
- A local prose scan found 0 forbidden-term hits, 0 diagnostic-term hits, and 0 numeric-token hits across all 15 candidates, including the 4 diagnostic failures.

Interpretation before Claude scoring:
- The machine gate did not see result leakage, forbidden result/conclusion terms, or new numbers.
- The first visible section-heldout signal is Terse information loss under Introduction framing: it often compresses away one required study-object term while still staying in budget.
- This may be either a real Terse info-loss failure or an over-strict task constraint. Please score all 15 candidates, including the 4 failed Terse outputs, so we can distinguish "bad prose" from "strict protected-term gate artifact."

Requested Claude review:
1. Score with the section-heldout Introduction rubric from `CLAUDECODE_BMT_V3_SECTION_HELDOUT_SCORING_SPEC.md`.
2. Focus axes:
   - `result_leak`: does the Introduction state findings/conclusions prematurely?
   - `framing_fit`: context -> gap -> objective, without Results/Discussion leakage.
   - `claim_altitude_two_sided`: not timid, not overclaiming.
   - `protected_preservation`: is the missing Terse term a substantive information loss?
   - `register_fit`: Lee-style intro register without meta text or generic framework language.
3. Track persona-specific watch items:
   - Bold: result-leak or mechanism overreach while trying to be strong.
   - Measured: causal/eruption-bait recurrence.
   - Terse: essential information loss under compression.

Next proposed branch:
- If Claude confirms Intro is result-leak clean and only Terse drops the protected term, patch Terse section guidance or task protected-term handling, then move to Results-adjacent held-out pilot.
- If Claude finds real result leakage, patch Intro-specific task/profile guidance before Results-adjacent.

