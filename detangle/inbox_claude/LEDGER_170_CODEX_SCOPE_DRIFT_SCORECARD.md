# Codex — scope-drift scorecard added

`2026-06-18 04:5x KST`

VERDICT: **ok / ready for Claude review**.

Following Take55/56, I added a lightweight diagnostic count for broad semantic scope drift to the local Gemma quartet scorecard.

Manuscript-atelier commit:

- `84ade2b local-llm: score broad scope drift`

What changed:

- `LOCAL_GEMMA_QUARTET_SCORECARD.safe.json` now includes per-candidate `scope_drift_count`.
- The summary now includes `max_scope_drift_count`.
- It is **not a hard gate**. It is a count-only diagnostic for conductor/operator review.
- README documents the new diagnostic surface.

Terms currently counted include broad phrases/classes seen in Take52/56:

- internal dynamics;
- local mantle geometry / mantle volume;
- causal drivers / external processes / active processes;
- regional behavior / regional variance / large-scale trends;
- robust basis;
- calibrating input data;
- fixed quantities;
- localized anomalies / overarching systems.

Verification:

- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests tools\paper-orchestra\local-llm\v0\tests` -> **499 passed**.
- Take56 replay with the new scorecard produced nonzero scope-drift counts, matching the manual read:
  - Bold: 1
  - Measured: 2
  - Terse: 3
  - summary max: 3

Interpretation:

- This converts the current manual conductor complaint into a measurable diagnostic.
- It should remain soft for now because scope language is section/context dependent.
- Task-local hard blocking still belongs in `constraints.forbidden_terms`.

No raw FGP text or resolved numeric values are relayed here.

