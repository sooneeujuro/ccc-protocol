# LEDGER_278 — Codex repair semantic-review fake-green hardening

VERDICT: ok

Scope:
- Target repo: `C:\Users\USER\Documents\manuscript-atelier`
- Local changes only; no manuscript-atelier commit/push.
- No model calls, no raw draft prose, no protected article text, no resolved numeric values, no caption relay.

Follow-up to Claude review:
- Read `CLAUDECODE_REPAIR_SEMANTIC_REVIEW_RUNNER_BREAKIT.md`.
- Confirmed the fenced-response finding was valid: the shared Ollama cleaner could unwrap Markdown-fenced JSON before the semantic-review runner's validator saw it.

Implemented:
1. Semantic-review runner fenced-response integration fix.
   - The runner now rejects Markdown-fenced model responses before stdout cleaning.
   - Added an end-to-end test so the actual runner path rejects fenced responses, not only the inner payload validator.

2. Scorecard semantic-review fake-green hardening.
   - Scorecard already checked semantic-review response file hashes.
   - It now also parses each local review response JSON and verifies that the manifest row's `review_status` and drift flags match the response payload.
   - Added a red-path test where the manifest row and response hash are updated to look safe while the local response payload reports drift; scorecard rejects it with a stable error.

Tests:
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_quartet_scorecard_synthetic.py -q`
  - 21 passed
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_repair_semantic_review_runner_synthetic.py tools\paper-orchestra\local-llm\v0\tests\test_gemma_quartet_scorecard_synthetic.py -q`
  - 29 passed
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 158 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `py -3.11 -m py_compile tools\paper-orchestra\local-llm\v0\gemma_repair_semantic_review_runner.py tools\paper-orchestra\local-llm\v0\gemma_quartet_scorecard.py`
  - passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; Windows LF/CRLF warnings only.

Design note:
- This keeps the safe manifest from becoming the sole source of truth for semantic-review pass/fail status.
- The local response payload remains local-only; scorecard records only status/count/hash-derived closure.

Open / next:
- Claude can re-break the scorecard closure surface, especially queue/run/response drift combinations.
- manuscript-atelier changes remain local until operator explicitly approves commit/push.
