# LEDGER_280 — Codex repair semantic-review queue/run binding

VERDICT: ok

Scope:
- Target repo: `C:\Users\USER\Documents\manuscript-atelier`
- Local changes only; no manuscript-atelier commit/push.
- No model calls, no raw draft prose, no protected article text, no resolved numeric values, no caption relay.

Implemented:
- Extended scorecard semantic-review closure to bind the run manifest back to the semantic-review queue manifest.
- If `LOCAL_GEMMA_REPAIR_SEMANTIC_REVIEW_RUN.safe.json` is present, scorecard now requires and validates `LOCAL_GEMMA_REPAIR_SEMANTIC_REVIEW_QUEUE.safe.json`.
- The scorecard verifies:
  - queue schema, run id, scorecard schema, local-only and non-relay flags
  - queue `model_called=false` and `network_used=false`
  - queue status/count consistency
  - queue item identity/source labels match expected accepted repairs
  - queue prompt file/hash is still current
  - semantic-review run item set matches queue item set
  - semantic-review run prompt file/hash matches queue prompt file/hash

Added red-path tests:
- semantic-review run without its queue manifest is rejected.
- semantic-review run whose prompt reference is not the queue-produced prompt is rejected.

Tests:
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_quartet_scorecard_synthetic.py -q`
  - 25 passed
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 162 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `py -3.11 -m py_compile tools\paper-orchestra\local-llm\v0\gemma_quartet_scorecard.py`
  - passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; Windows LF/CRLF warnings only.

Design note:
- This closes the remaining fake-green class where a semantic-review run manifest could point to a plausible local prompt/result pair that was not produced by the canonical before/after repair-review queue.
- Local before/after prose remains local-only; scorecard relays only status/count/hash-derived closure.

Open / next:
- Claude can re-break the queue/run binding.
- manuscript-atelier changes remain local until operator explicitly approves commit/push.
