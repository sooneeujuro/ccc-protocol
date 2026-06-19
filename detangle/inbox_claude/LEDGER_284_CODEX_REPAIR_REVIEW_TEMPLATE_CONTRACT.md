# LEDGER_284 — Codex repair semantic-review template contract

VERDICT: ok

Scope:
- Target repo: `C:\Users\USER\Documents\manuscript-atelier`
- Local changes only; no manuscript-atelier commit/push.
- No model calls, no raw draft prose, no protected article text, no resolved numeric values, no caption relay.

Implemented:
- Added a shared local contract helper for rendering repair semantic-review prompts.
- `gemma_repair_semantic_review_queue.py` and `gemma_quartet_scorecard.py` now use the same renderer.
- This removes duplicated prompt-template strings between queue generation and scorecard recomputation.

Why:
- LEDGER_283 made scorecard recompute queue prompts to prevent forged prompt acceptance.
- Duplicating the template in two modules would create a future false-red/template-drift risk if one side changed.
- The shared renderer keeps deterministic prompt recomputation while reducing maintenance drift.

Tests:
- `py -3.11 -m py_compile tools\paper-orchestra\local-llm\v0\gemma_repair_semantic_review_contract.py tools\paper-orchestra\local-llm\v0\gemma_repair_semantic_review_queue.py tools\paper-orchestra\local-llm\v0\gemma_quartet_scorecard.py`
  - passed
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_repair_semantic_review_queue_synthetic.py tools\paper-orchestra\local-llm\v0\tests\test_gemma_quartet_scorecard_synthetic.py -q`
  - 33 passed
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 165 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; Windows LF/CRLF warnings only.

Open / next:
- Claude can re-break the shared renderer / prompt recomputation path.
- manuscript-atelier changes remain local until operator explicitly approves commit/push.
