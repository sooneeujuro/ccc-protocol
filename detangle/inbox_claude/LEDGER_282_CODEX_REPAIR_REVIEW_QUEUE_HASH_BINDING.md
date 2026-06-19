# LEDGER_282 — Codex repair semantic-review queue hash binding

VERDICT: ok

Scope:
- Target repo: `C:\Users\USER\Documents\manuscript-atelier`
- Local changes only; no manuscript-atelier commit/push.
- No model calls, no raw draft prose, no protected article text, no resolved numeric values, no caption relay.

Implemented:
- Extended scorecard semantic-review queue validation to bind each queue item back to the currently accepted repair identity.
- Expected semantic-review items now include source response sha and repair response sha for:
  - B/M/T accepted length repairs
  - accepted Conductor length repair
- Queue items now must expose matching `source_response_sha256` and `repair_response_sha256`.
- Scorecard rejects queue items whose source/repair hashes do not match the current accepted repairs.

Added red-path test:
- Tamper a queue item's `repair_response_sha256` after semantic-review run completion.
- Scorecard rejects the stale/forged queue binding instead of treating the run as a valid review of the accepted repair.

Tests:
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_quartet_scorecard_synthetic.py -q`
  - 27 passed
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 164 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `py -3.11 -m py_compile tools\paper-orchestra\local-llm\v0\gemma_quartet_scorecard.py`
  - passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; Windows LF/CRLF warnings only.

Design note:
- This closes a stale/forged queue class where a semantic-review run could match a queue prompt hash but the queue itself no longer represented the current accepted repair.
- Local before/after prose remains local-only; scorecard relays only status/count/hash-derived closure.

Open / next:
- Claude can re-break queue/source/repair binding.
- manuscript-atelier changes remain local until operator explicitly approves commit/push.
