# LEDGER_277 — Codex scorecard repair semantic-review closure

VERDICT: ok

Scope:
- Target repo: `C:\Users\USER\Documents\manuscript-atelier`
- Local changes only; no manuscript-atelier commit/push.
- No model calls, no raw draft prose, no protected article text, no resolved numeric values, no caption relay.

Implemented:
1. Addressed Claude `CLAUDECODE_REPAIR_SEMANTIC_REVIEW_RUNNER_BREAKIT` finding.
   - The semantic-review runner now rejects Markdown-fenced model responses before the shared Ollama stdout cleaner can unwrap them.
   - Added an end-to-end fenced-response test so the integration path, not only the inner validator, is covered.
   - Intent is now explicit: semantic-review responses must be bare JSON.

2. Extended `gemma_quartet_scorecard.py` to read optional semantic-review run manifests.
   - Adds `repair_semantic_review_run_schema`.
   - Adds top-level `repair_semantic_review` summary:
     - `status`: `not_needed`, `pending`, `passed`, `issues_found`, or `blocked`
     - `required_count`
     - `reviewed_count`
     - `issue_count`
     - `blocked_count`
     - drift-count totals
   - Validates schema, run id, local-only / non-relay flags, item identity, source kind/label, relative prompt/response paths, response hashes, status enums, drift-flag shape, issue-count totals, and drift-count totals.
   - Does not copy reviewer notes, before/after draft prose, local paths, or repaired text into the scorecard.

3. Updated local docs.
   - Word-count ranges are documented as task/journal/section contracts.
   - Near-bound misses with an explicit repair margin are treated as paraphrase/tighten/expand candidates, not scientific failures.
   - The scorecard now records whether the post-repair semantic-review loop is still pending or closed.

Tests:
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_repair_semantic_review_runner_synthetic.py tools\paper-orchestra\local-llm\v0\tests\test_gemma_quartet_scorecard_synthetic.py -q`
  - 29 passed
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 157 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `py -3.11 -m py_compile tools\paper-orchestra\local-llm\v0\gemma_repair_semantic_review_runner.py tools\paper-orchestra\local-llm\v0\gemma_quartet_scorecard.py`
  - passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; Windows LF/CRLF warnings only.

Design note:
- This keeps length as an operational contract while avoiding fake-red behavior for small misses.
- Mechanical repair still cannot prove semantic identity; accepted repairs therefore require a before/after semantic-review pass.
- The scorecard now exposes that review status without making local prose relayable.

Open / next:
- Claude may re-break the new scorecard semantic-review closure surface.
- manuscript-atelier changes remain local until operator explicitly approves commit/push.
