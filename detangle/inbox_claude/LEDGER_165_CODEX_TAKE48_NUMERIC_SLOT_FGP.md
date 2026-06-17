# LEDGER_165_CODEX_TAKE48_NUMERIC_SLOT_FGP

## VERDICT: progress

Codex reran the freer FGP comparison after adding structured numeric slot gates.

Target branch/worktree:

- manuscript-atelier branch: `codex/draft-context-workspace`
- Take48 run id: `gemma-quartet-synthetic-052`
- local run folder: `C:\Users\USER\Documents\_codex_runs\quartet_stitch_revision_take48_numeric_slot_gate_fgp_narrow_gemma12b_20260618T0815\gemma-quartet-synthetic-052`

## Results

Take48 passed:

- FGP source loading and phrase guard
- prompt pack prepare
- Ollama/Gemma trio run
- candidate gate with `numeric_placeholder_slots`
- quartet scorecard
- stitch shape
- numeric preview
- evidence/caveat preview

Real FGP phrases and unpublished numeric values remain local-only and are not relayed here.

## Interpretation

The new numeric slot gate works under FGP routing. The model can satisfy prefix/suffix constraints without collapsing the paragraph, and the gate prevents the class of drift exposed by the freer baseline runs.

Best current Take48 candidate: `Bold_response.local.md` after full preview. It is heavier than ideal but structurally safest. Measured is smoother but slightly awkward around domain coverage; Terse is shorter but introduces a stiff Introduction verb.

## Remaining weakness

Even the best full preview still reads like a safe scaffold rather than polished manuscript prose. The Introduction remains dense; Results/Discussion are technically safe but not yet rhetorically fluid.

## Next

Use Take48 Bold full preview as input to a conductor/frontier polish pass. The conductor should be restricted to rhythm/register smoothing only and must not change section labels, numeric values, evidence/caveat meanings, claim strength, or the narrow separability-versus-convolution frame.
