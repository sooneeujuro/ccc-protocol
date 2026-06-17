# LEDGER_161_CODEX_TAKE42_SLOT_AWARE_PREVIEW

## VERDICT: progress

Codex ran Take42 after the new draft placeholder preview layer showed that plain evidence/caveat noun-phrase replacement can still break grammar.

Target branch/worktree:

- manuscript-atelier branch: `codex/draft-context-workspace`
- run id: `gemma-quartet-synthetic-046`
- local run folder: `C:\Users\USER\Documents\_codex_runs\quartet_stitch_revision_take42_slot_aware_preview_gemma12b_20260618T0545\gemma-quartet-synthetic-046`

## Take42 change

Take42 kept the Take41 numeric sentence-boundary rule and added slot-aware preview rules:

- evidence placeholders should sit in noun-phrase slots;
- evidence placeholders should not start sentences unless the frame still works with a lower-case local display value;
- `{{CAVEAT:SMALL_N_SOUTH}}` should not be the actor of verbs like marks/defines/shows;
- caveats should be placed in bounded-inference frames such as `remains bounded by {{CAVEAT:SMALL_N_SOUTH}}`;
- vent-distance numeric summary and evidence trace remain separate sentences.

## Results

- prompt pack prepare: passed
- Ollama/Gemma trio run: passed
- candidate gate: passed
- quartet scorecard: passed
- stitch shape: passed
- numeric preview: passed
- evidence/caveat draft preview: passed

Exact unpublished numeric values remain local-only and are not relayed here.

## Interpretation

All three Gemma personas converged to the same paragraph body. Take42 is now the best current stitch/numeric/preview candidate because placeholder substitution no longer collapses the grammar.

Remaining weakness: the Introduction still feels dense due to stacked `via / using / within` framing. That is acceptable for scaffold evaluation, but a later conductor/frontier polish should smooth it after placeholders are previewed.

## Next

Recommended next experiment: run the same Take42 task shape with FGP routing enabled and compare baseline Take42 vs FGP-routed Take42 after local preview. This should test FGP effect after placeholder mechanics stop dominating the prose.
