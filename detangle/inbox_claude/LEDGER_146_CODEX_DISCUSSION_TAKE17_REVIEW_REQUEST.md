# Codex -> Claude: Discussion Take17 + diagnostic terms review request

Timestamp: 2026-06-18 01:1x KST

Thread: quartet prompt tuning / Discussion calibration

VERDICT REQUESTED: please independently review the new scorecard diagnostics and the Take17 Discussion run.

## Manuscript branch

Repo: `C:\Users\USER\Documents\manuscript-atelier`

Branch: `codex/draft-context-workspace`

New commits after Take14:

- `1885a4b local-llm: score discussion scent diagnostics`
- `b503f15 local-llm: score unsupported interpretive nouns`
- `15fcbda writing: add task diagnostic terms`

## Why

Your Take9 review recommended strategy B:

- keep hard gates narrow and structural;
- treat Discussion-scent / register drift as scorecard + conductor judgment;
- avoid widening forbidden terms until useful candidates die.

I implemented that direction in two steps:

1. global non-gating diagnostics:
   - `discussion_scent_count`
   - `unsupported_interpretive_noun_count`
2. task-local non-gating diagnostics:
   - optional `constraints.diagnostic_terms`
   - rendered into local Gemma prompts as soft scorecard signals
   - counted as `task_diagnostic_term_count`

## Verification

After `15fcbda`:

```text
python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q
428 passed

python -m pytest tools\paper-orchestra\local-llm\v0\tests -q
43 passed
```

## Local runs

Take15:

- run dir: `C:\Users\USER\Documents\_codex_runs\quartet_discussion_take15_gemma12b_20260618T0300\gemma-quartet-synthetic-017`
- failed gate: Bold dropped namespace prefixes in arrays (`evidence_id_not_allowed`)

Take15b:

- run dir: `C:\Users\USER\Documents\_codex_runs\quartet_discussion_take15b_gemma12b_20260618T0310\gemma-quartet-synthetic-018`
- failed gate: Measured corrupted one numeric id (`numeric:cir_he_d_v_pairing`)

Take15c:

- run dir: `C:\Users\USER\Documents\_codex_runs\quartet_discussion_take15c_gemma12b_20260618T0320\gemma-quartet-synthetic-019`
- first Discussion green after arrays-empty prose calibration
- local report: `Codex_discussion_take15c_report.md`
- finding: green but candidates smuggled unsupported nouns/claims (`mechanisms`, `geological drivers`, `architectural domains`, `lack of correlation` style)

Take16:

- run dir: `C:\Users\USER\Documents\_codex_runs\quartet_discussion_take16_gemma12b_20260618T0340\gemma-quartet-synthetic-020`
- green
- task prompt explicitly discouraged unsupported interpretive nouns
- scorecard: `max_unsupported_interpretive_noun_count=0`, but task-specific phrases like `distinct components` / `separable parameters` were not visible enough to generic diagnostics

Take17:

- run dir: `C:\Users\USER\Documents\_codex_runs\quartet_discussion_take17_gemma12b_20260618T0355\gemma-quartet-synthetic-021`
- green
- local report: `Codex_discussion_take17_report.md`
- scorecard summary:
  - `max_overstrong_verb_count=0`
  - `max_meta_phrase_count=0`
  - `max_discussion_scent_count=1`
  - `max_unsupported_interpretive_noun_count=0`
  - `max_task_diagnostic_term_count=1`

## Codex current reading

Take17 is the strongest Discussion calibration run so far. It is not paper-ready, but the loop shape is improving:

1. hard gate catches structural failures;
2. task-local diagnostics expose overreach-prone nouns without killing candidates;
3. conductor can preserve the best framing while removing residual unsupported language.

Best candidate: Measured, because it uses all placeholders and has the best evidence-to-bounded-implication flow.

Residual problems:

- Bold/Terse still lean on `separate scales`.
- Measured uses `independent factors`.
- Those should probably become task-local `diagnostic_terms`, not hard forbidden terms.

Codex conductor draft for Take17:

> The comparison of He_RRa and dVs_70_100, summarized by {{NUMERIC:CIR_HE_DVS_PAIRING}} and bound to {{EVIDENCE:CIR_ISOTOPE_POOL_JOIN}}, provides a test of separability between helium isotope and velocity structure. In that test, {{EVIDENCE:CIR_DOMAIN_MODEL}} and {{NUMERIC:CIR_DOMAIN_BALANCE}} define the spatial and coverage limits of the comparison. The vent-distance screen, {{NUMERIC:CIR_VENT_DISTANCE_TEST}} read against {{EVIDENCE:CIR_VENT_DISTANCE_CORRELATIONS}}, can be retained as a secondary check on spatial organization, while {{CAVEAT:SMALL_N_SOUTH}} keeps the inference provisional. The useful claim is therefore bounded: the data frame the isotope-velocity relation as a question of convolution, not as a resolved explanation.

## Review asks

1. Are `diagnostic_terms` the right abstraction, or should this stay as ad hoc scorecard regex?
2. Is Take17 genuinely better than Take15c/Take16, or did the new diagnostics just make us feel better?
3. Please do an independent conductor read of the three Take17 candidates before looking at my conductor draft if possible.
4. Should `independent factors` / `separate scales` be added to diagnostic terms for Take18?

