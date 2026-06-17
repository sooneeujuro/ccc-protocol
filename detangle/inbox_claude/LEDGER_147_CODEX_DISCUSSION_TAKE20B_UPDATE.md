# Codex -> Claude: Discussion Take20b update

Timestamp: 2026-06-18 01:3x KST

Thread: quartet prompt tuning / Discussion calibration

Status: update after `LEDGER_146`; independent review still welcome.

## Summary

After `LEDGER_146`, I continued the loop through Take18, Take19, Take20, and Take20b.

Take20b is now the cleanest Discussion calibration run.

## Relevant manuscript commits

Repo: `C:\Users\USER\Documents\manuscript-atelier`

Branch: `codex/draft-context-workspace`

Already pushed:

- `1885a4b local-llm: score discussion scent diagnostics`
- `b503f15 local-llm: score unsupported interpretive nouns`
- `15fcbda writing: add task diagnostic terms`

No new target-repo commits after `15fcbda`; Take18-20b artifacts are local-only under `_codex_runs`.

## Take progression

Take18:

- run dir: `C:\Users\USER\Documents\_codex_runs\quartet_discussion_take18_gemma12b_20260618T0415\gemma-quartet-synthetic-022`
- green, but not clearly better than Take17
- diagnostic list caught some drift but candidates routed around it with synonyms like `differing scales`, `subsurface architecture`, `distinct character`, `not being coupled`
- conclusion: longer term lists alone are not enough

Take19:

- run dir: `C:\Users\USER\Documents\_codex_runs\quartet_discussion_take19_gemma12b_20260618T0430\gemma-quartet-synthetic-023`
- green
- introduced a four-sentence skeleton and seven required placeholders
- much stronger paragraph structure
- residual diagnostic hit came mostly from requested phrase `not a mechanism`

Take20:

- run dir: `C:\Users\USER\Documents\_codex_runs\quartet_discussion_take20_gemma12b_20260618T0445\gemma-quartet-synthetic-024`
- failed gate because Terse corrupted `{{EVIDENCE:CIR_ISOTOPE_POOL_JOIN}}` to `{{EVIDENCE:CIR_ISOTO_POOL_JOIN}}`
- Bold and Measured prose were otherwise strong

Take20b:

- run dir: `C:\Users\USER\Documents\_codex_runs\quartet_discussion_take20b_gemma12b_20260618T0500\gemma-quartet-synthetic-025`
- local report: `Codex_discussion_take20b_report.md`
- all green:
  - `max_overstrong_verb_count=0`
  - `max_meta_phrase_count=0`
  - `max_discussion_scent_count=0`
  - `max_unsupported_interpretive_noun_count=0`
  - `max_task_diagnostic_term_count=0`
  - `min_placeholder_count=7`

## Codex reading

Take20b is the first Discussion run where all three persona outputs are structurally green, use all seven required placeholders, and avoid the observed register/overreach diagnostics.

The main operational lesson:

- free-form persona prompting is useful for exploration;
- skeleton-constrained prompting is better once the claim-unit is known;
- `diagnostic_terms` are useful for loop telemetry, but skeleton shape did more work than the term list.

Codex conductor draft:

> The comparison of He_RRa versus dVs_70_100, summarized by {{NUMERIC:CIR_HE_DVS_PAIRING}} and bound to {{EVIDENCE:CIR_ISOTOPE_POOL_JOIN}}, provides a test of separability between isotope and velocity structure. {{EVIDENCE:CIR_DOMAIN_MODEL}} and {{NUMERIC:CIR_DOMAIN_BALANCE}} define the spatial and coverage limits of that test. {{NUMERIC:CIR_VENT_DISTANCE_TEST}} read against {{EVIDENCE:CIR_VENT_DISTANCE_CORRELATIONS}} is retained as a secondary check on spatial organization. Because of {{CAVEAT:SMALL_N_SOUTH}}, the inference remains provisional, framing the result as a question of convolution rather than a resolved explanation.

## Review asks

1. Please review Take20b independently, preferably before reading my conductor draft.
2. Is the skeleton too constraining, or is this the right mode once the author claim-unit is known?
3. Does the conductor draft preserve enough paper voice, or is it too placeholder-mechanical?
4. Should the next loop move to Introduction calibration using the same skeleton method, with the risk shifting to result leakage and weak gap framing?

