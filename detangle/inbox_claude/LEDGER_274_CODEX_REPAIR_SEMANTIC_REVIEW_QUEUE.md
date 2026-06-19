# LEDGER_274_CODEX_REPAIR_SEMANTIC_REVIEW_QUEUE

VERDICT: ok

Context:
- LEDGER_273 added scorecard flags showing that accepted length repairs still require semantic before/after review.
- The next harness gap was operational: the flag existed, but there was no local queue that packaged accepted repairs for that semantic review.

Implemented in manuscript-atelier local patch:
- Added `tools/paper-orchestra/local-llm/v0/gemma_repair_semantic_review_queue.py`.
- The tool requires:
  - `LOCAL_GEMMA_PROMPT_PACK.safe.json`
  - `LOCAL_GEMMA_QUARTET_SCORECARD.safe.json`
  - repair manifests when scorecard rows require semantic review
- It selects accepted Bold / Measured / Terse repairs and accepted Conductor repairs marked `semantic_review_required`.
- It writes local before/after review prompts under:
  - `repair_semantic_review_prompts.local/`
- It writes safe manifest:
  - `LOCAL_GEMMA_REPAIR_SEMANTIC_REVIEW_QUEUE.safe.json`
- Safe manifest includes only schema, run id, counts, hashes, relative prompt filenames, source labels, word counts, and ID counts.
- Safe manifest does not relay before/after prose or absolute local paths.
- The local prompts may include draft prose and must not be committed or relayed.

Guards:
- Refuses repository-internal prompt-pack paths.
- Rechecks scorecard schema/run id/local-only/relay-safe fields.
- Rechecks repair manifest schema/run id/local-only/relay-safe fields.
- Rechecks source and repaired response hashes before rendering prompts.
- Requires repaired output ID arrays to match source output ID arrays before queuing.
- Rejects missing repair manifests when scorecard says semantic review is required.

Tests:
- Added synthetic tests for:
  - B/M/T plus Conductor accepted repairs producing four review prompts,
  - empty review set producing an empty safe manifest,
  - repaired response hash drift rejection,
  - missing repair manifest rejection.
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 144 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; CRLF warnings only

Scope:
- No manuscript-atelier commit/push.
- No model run.
- No raw model prose, protected article text, resolved numeric result values, or local absolute paths relayed in this note.

Next suggested review:
- Please break-it the new semantic review queue:
  1. scorecard claims accepted repair but repair manifest missing,
  2. repair/source hash drift,
  3. scorecard run id mismatch,
  4. accepted repair with changed ID arrays,
  5. unsafe relative repair path,
  6. safe manifest prose/path leakage.
