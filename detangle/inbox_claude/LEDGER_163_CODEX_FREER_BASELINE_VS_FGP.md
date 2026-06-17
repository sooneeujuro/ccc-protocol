# LEDGER_163_CODEX_FREER_BASELINE_VS_FGP

## VERDICT: progress

Codex compared a freer baseline quartet run against the same freer task with FGP narrow routing.

Target branch/worktree:

- manuscript-atelier branch: `codex/draft-context-workspace`
- Take44 baseline run id: `gemma-quartet-synthetic-048`
- Take45 FGP narrow run id: `gemma-quartet-synthetic-049`

## Safety/gate status

Both runs passed:

- prompt pack prepare
- Ollama/Gemma trio run
- candidate gate
- quartet scorecard
- stitch shape
- numeric preview
- evidence/caveat preview

Take45 also passed local FGP source loading and forbidden phrase guarding.

Real FGP phrases and unpublished numeric values remain local-only and are not relayed here.

## Interpretation

The freer task made the model rewrite more than Take42/Take43. This exposed a useful distinction:

- FGP narrow is safe and gives a small register benefit, especially in Discussion calibration;
- FGP is not the main prose bottleneck once the task is still placeholder-heavy;
- the current candidate gate preserves placeholder presence but does not enforce the exact grammar context of numeric placeholders.

In Take44/Take45, candidates could pass while slightly distorting numeric slot wording or reattaching a long numeric display to interpretation with a `while` clause. The model obeys the instruction often, but this is currently not a hard gate.

## Next recommended implementation

Promote numeric slot frames from free-text instructions into an optional structured constraint, e.g. `constraints.numeric_placeholder_slots`, so `gemma_candidate_gate.py` can reject context drift directly.

After that:

1. rerun freer baseline/FGP comparison;
2. full-preview the best candidate;
3. hand it to conductor/frontier polish.
