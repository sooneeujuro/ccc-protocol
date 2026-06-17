# LEDGER_162_CODEX_TAKE43_FGP_NARROW

## VERDICT: progress

Codex ran the Take42 slot-aware task with FGP narrow routing enabled.

Target branch/worktree:

- manuscript-atelier branch: `codex/draft-context-workspace`
- run id: `gemma-quartet-synthetic-047`
- local run folder: `C:\Users\USER\Documents\_codex_runs\quartet_stitch_revision_take43_fgp_narrow_slot_aware_gemma12b_20260618T0610\gemma-quartet-synthetic-047`

## Safety checks

- FGP source readiness check: passed, count-only output
- prompt pack prepare with `fgp_mode=narrow`: passed
- Ollama/Gemma run with forbidden phrase guard: passed
- candidate gate: passed
- quartet scorecard: passed
- stitch shape: passed
- numeric preview: passed
- evidence/caveat preview: passed

Real FGP phrases and unpublished numeric values remain local-only and are not relayed here.

## Interpretation

The FGP safety chain worked end to end: local phrase corpus was loaded, prompt/output guards ran, and no FGP phrase-overlap failure occurred.

Writing effect was small. Bold and Measured converged to the same paragraph as Take42. Terse produced a slightly more compact variant but lost some visual breathing between sections. For this constrained stitch/numeric/preview task, Take42/Take43 Measured remains the best current candidate.

## Next

The Take42 task is now too constrained to expose much FGP signal. Next experiment should increase writing freedom while keeping safety gates:

- keep section labels and placeholder preservation;
- keep numeric/evidence/caveat slot rules;
- loosen exact sentence-template copying;
- ask personas to rewrite Introduction and Discussion frames rather than preserve the base text;
- compare baseline vs FGP narrow/wide after full local preview.
