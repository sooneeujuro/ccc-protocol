# LEDGER_281 — Codex repair semantic-review blocked-status coverage

VERDICT: ok

Scope:
- Target repo: `C:\Users\USER\Documents\manuscript-atelier`
- Local changes only; no manuscript-atelier commit/push.
- No model calls, no raw draft prose, no protected article text, no resolved numeric values, no caption relay.

Implemented:
- Added synthetic coverage for semantic-review responses with `review_status=blocked`.
- Scorecard now has an explicit test proving that blocked review rows surface as top-level `repair_semantic_review.status=blocked`, with separate `blocked_count`.

Why:
- `issues_found` and `blocked` are operationally different.
- `issues_found` means the repair appears semantically wrong.
- `blocked` means the review could not safely decide and should remain a human/stronger-review handoff rather than being collapsed into an ordinary issue bucket.

Tests:
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_quartet_scorecard_synthetic.py -q`
  - 26 passed
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 163 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `py -3.11 -m py_compile tools\paper-orchestra\local-llm\v0\gemma_quartet_scorecard.py`
  - passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; Windows LF/CRLF warnings only.

Open / next:
- Claude can re-break the semantic-review closure path.
- manuscript-atelier changes remain local until operator explicitly approves commit/push.
