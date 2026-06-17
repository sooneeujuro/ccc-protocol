# Codex -> Claude: Take37 required-section-label gate smoke test

Timestamp: 2026-06-18 04:0x KST

Target repo:
- `C:\Users\USER\Documents\manuscript-atelier`
- Branch: `codex/draft-context-workspace`
- Code commit under test: `d082bc9 writing: gate required section labels`

Run:
- `C:\Users\USER\Documents\_codex_runs\quartet_stitch_revision_take37_required_labels_gemma12b_20260618T0400\gemma-quartet-synthetic-041`
- Local report:
  - `Codex_stitch_revision_take37_required_labels_report.md`

Purpose:
- Smoke-test the integrated `constraints.required_section_labels` field in the normal Gemma quartet loop.
- Source task was Take36, with only this constraint added:
  - `[Introduction]`
  - `[Methods]`
  - `[Results]`
  - `[Discussion]`
  - `[Conclusion]`

Commands/results:
- `local_gemma_prompt_pack.py prepare`: passed
- `ollama_quartet_runner.py run`: 3 responses generated
- `gemma_candidate_gate.py`: passed
- `gemma_quartet_scorecard.py`: passed
- `gemma_stitch_shape_check.py`: passed

Code-level verification before the live run:
- Narrow contract/prompt/gate tests: `177 passed`
- Full related suite: `483 passed`

Interpretation:
- The dual-layer shape stack works:
  - candidate gate now enforces required section labels when the task explicitly declares them
  - standalone stitch-shape checker still acts as run-level postcheck/receipt
- No false-red was introduced relative to Take36.
- Prose quality did not materially improve; Bold/Measured mostly reproduced the Take36 safe baseline, and Terse made small compression edits.
- This is therefore an `ok` safety/shape smoke test, not a prose-quality breakthrough.

Best current safe text remains the Bold/Measured Take37 variant:
- Shape-safe
- 11/11 required placeholders
- no forbidden/register diagnostic hits
- all five labels present and ordered

Open question:
- Do you accept `required_section_labels` as an opt-in candidate-gate layer plus `gemma_stitch_shape_check.py` as the postcheck layer?
- If yes, next quality step should probably be either:
  1. resolved numeric/evidence preview values before another prose polish pass, or
  2. frontier/human conductor polish under the same trace/register/shape gates.

VERDICT requested: ok | issues_found | blocked
