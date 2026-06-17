# LEDGER_158_CODEX_TAKE40_NUMERIC_SLOT_SMOKE

## VERDICT: progress

Codex continued the quartet profile loop after the required-section-label gate and numeric preview work.

Target branch/worktree:

- manuscript-atelier branch: `codex/draft-context-workspace`
- run id: `gemma-quartet-synthetic-044`
- local run folder: `C:\Users\USER\Documents\_codex_runs\quartet_stitch_revision_take40_numeric_slots_caveat_pin_gemma12b_20260618T0500\gemma-quartet-synthetic-044`

## What changed in Take40

Take40 kept the Take39 numeric slot constraints and added an explicit caveat-placeholder pin after Take39 failed because one persona misspelled `{{CAVEAT:SMALL_N_SOUTH}}`.

Take40 results:

- `local_gemma_prompt_pack.py prepare`: passed
- `ollama_quartet_runner.py run`: passed
- `gemma_candidate_gate.py`: passed
- `gemma_quartet_scorecard.py`: passed
- `gemma_stitch_shape_check.py`: passed
- numeric placeholder preview: valid, all three numeric placeholders replaced

Exact unpublished numeric values remain local-only and are not relayed here.

## Current interpretation

`Measured_response.local.md` is the best current Take40 candidate. It preserves the required five section labels, keeps all required placeholders exact, and has the most stable section shape.

The numeric-slot framing is improved relative to Take38/Take39: numeric placeholders now sit in safer local wrappers rather than being coordinated with evidence placeholders as peer noun phrases.

Remaining issue: one Results sentence is still too crowded after numeric preview because the long vent-distance numeric display is followed by an evidence-link clause in the same sentence. This is not a gate failure, but it is a manuscript-style issue.

## Next proposed Take41 tweak

Add a `numeric display sentence boundary` instruction:

- long numeric displays may complete a sentence;
- evidence placeholders should start the next sentence;
- numeric displays and evidence placeholders should not share the same predicate unless the numeric display is short;
- for the vent-distance slot specifically, use one sentence for the numeric summary and a separate sentence for the evidence trace/interpretation.

No repository code change is required yet. If the pattern recurs, promote it into an optional numeric display-slot contract.
