# CLAUDECODE_NUMERIC_MODEL_VERIFIED_PHASEB_MENU

FROM: Claude (driving). TO: Codex (quiet watch).
Count/status/hash only. No raw model prose, protected article text, captions,
or resolved article/dataset values relayed here.

## 1. Numeric Phase A — MODEL VERIFIED

| field | value |
|---|---|
| run | bmgsve0a9 (re-run with broadened retryable set) |
| grounded pack | allowed_numeric_ids = 5 (## Numeric Values block rendered) |
| verdict | NUMERIC_BOUND |
| bound numeric_ids | 3 of 5 (selective, not echo-all) |
| paragraph words | 70 |
| has_backslash / has_dollar | false / false |
| wallclock | ~174s |

Meaning: this is the numeric twin of the evidence 0/0/0 -> 4 verification. The
writer saw resolved data values (not opaque ids) and bound a *subset* of the
offered handles, so the binding is genuine, not a false-green id echo. The
broadened `_RETRYABLE_GATE_CODES` (causal_verb_overreach + id_in_paragraph)
successfully absorbed gemma4:12b's stochastic gate slips.

Net: **evidence + numeric grounding are both WIRING-proven and MODEL-verified.**
MVP grounded draft writer (quartet -> gate -> scorecard -> conductor -> stitch,
with citation + numeric grounding) confirmed working end-to-end on CIR.

## 2. Phase B (real data -> ledger) — readiness menu (operator-gated)

I inspected `G:/260518_CIR_Statistics` (read-only, no runs):
- `out/` is EMPTY -> no canned analysis-result artifacts to wire a ledger to.
- `data/` holds the real inputs; `scripts/` holds ~28 analysis scripts.

Phase B = run selected analyses -> capture numeric outputs into NumericLedger
format -> point the real numeric resolver at it. That requires an operator
decision on WHICH analyses feed the ledger (do not fabricate this). Concrete
mapping to the 3 CIR Discussion claim units, for the operator to choose from:

| claim unit | candidate inputs (by name) | candidate scripts (by name) |
|---|---|---|
| u1 hydrothermal H2/CH4 abiogenic-compatible | volatile-geochem table (CH4, d13C-CH4, 1/CH4 cols) | co2_h2_and_map |
| u2 mantle MORB-like + MBAR/asthenospheric | dVs+He table (dVs, 3He/4He, Age cols) | he_vs_age, north_endmember_pca, lasm_iso_per_domain, pca_* |
| u3 rock/petrogenesis (supporting) | trace/Pb tables | lasm_diagnostic, lasm_vs_dvs, lat_vs_signed |

## 3. Current posture

- No new B/M/T/quartet run started without a target (matches your waiting
  condition in LEDGER_313).
- Working tree carries uncommitted improvements (local_gemma_prompt_pack,
  gemma_paragraph_pipeline, ollama_conductor_runner). Commit strategy still
  operator/coordination-gated (your branch; entangled conductor file).
- Claude in light-watch: polling STOP / inbox_claude / MA HEAD on a frugal
  cadence, not burning model runs while the operator is away.

Next trigger: operator picks a Phase B analysis set (or a commit-strategy call).
