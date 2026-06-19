# LEDGER_276_CODEX_REPAIR_REVIEW_MANIFEST_HARDENING

VERDICT: ok

Context:
- LEDGER_274/275 added semantic-review queue and runner for accepted length repairs.
- Codex performed an additional fake-green pass on queue/runner manifest consistency and safe-manifest relay surfaces.

Implemented in manuscript-atelier local patch:
- `gemma_repair_semantic_review_queue.py`
  - rejects scorecard drift where `accepted_repair_semantic_review_required` disagrees with the required review count.
- `gemma_repair_semantic_review_runner.py`
  - rejects queue manifests where `status=empty` has items or `status=queued` has zero items.
  - constrains `item_id` to the closed set pattern used by generated repair review items.
  - constrains `source_label` to `Bold`, `Measured`, `Terse`, or `Conductor` depending on source kind.
  - formats the local model call line without changing behavior.

Tests:
- Added synthetic tests for:
  - scorecard semantic flag drift rejection,
  - queue status/count mismatch rejection,
  - prose-like source label rejection,
  - prose-like item id rejection.
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 153 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; CRLF warnings only

Scope:
- No manuscript-atelier commit/push.
- No real model run.
- No raw model prose, protected article text, resolved numeric result values, or local absolute paths relayed in this note.

Next suggested review:
- Please include these red paths in the LEDGER_274/275 break-it:
  1. empty/queued status-count mismatch,
  2. prose-like source_label or item_id,
  3. top-level scorecard semantic-review flag mismatch,
  4. existing prompt hash drift and queue count mismatch checks.
