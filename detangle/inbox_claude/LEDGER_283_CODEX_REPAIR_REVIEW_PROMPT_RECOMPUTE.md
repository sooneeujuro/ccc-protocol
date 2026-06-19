# LEDGER_283 — Codex repair semantic-review prompt recompute

VERDICT: ok

Scope:
- Target repo: `C:\Users\USER\Documents\manuscript-atelier`
- Local changes only; no manuscript-atelier commit/push.
- No model calls, no raw draft prose, no protected article text, no resolved numeric values, no caption relay.

Implemented:
- Extended scorecard validation of the semantic-review queue.
- Scorecard now reloads each queue item's source response and repair response, verifies their hashes, validates ID arrays are unchanged, and deterministically re-renders the before/after semantic-review prompt.
- The queue prompt file must exactly match the recomputed prompt.
- This prevents a forged queue manifest plus forged prompt file from being accepted merely because their hashes agree with each other.

Added red-path tests:
- A tampered queue repair hash is rejected.
- A forged semantic-review prompt whose queue/run hashes are updated to match the forged prompt is rejected by deterministic prompt recomputation.

Tests:
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_quartet_scorecard_synthetic.py -q`
  - 28 passed
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 165 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `py -3.11 -m py_compile tools\paper-orchestra\local-llm\v0\gemma_quartet_scorecard.py`
  - passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; Windows LF/CRLF warnings only.

Design note:
- The scorecard still does not relay before/after prose.
- It reads local-only source/repair prose only to prove that the semantic-review prompt was generated from the accepted repair pair.

Open / next:
- Claude can re-break prompt recomputation, especially template drift between queue builder and scorecard.
- manuscript-atelier changes remain local until operator explicitly approves commit/push.
