# LEDGER_275_CODEX_REPAIR_SEMANTIC_REVIEW_RUNNER

VERDICT: ok

Context:
- LEDGER_274 added a local-only queue of before/after prompts for accepted length repairs.
- The next harness gap was ingest/execution: the queue prepared prompts but did not yet run a semantic reviewer and summarize drift flags safely.

Implemented in manuscript-atelier local patch:
- Added `tools/paper-orchestra/local-llm/v0/gemma_repair_semantic_review_runner.py`.
- The runner reads `LOCAL_GEMMA_REPAIR_SEMANTIC_REVIEW_QUEUE.safe.json`.
- If the queue is empty, it writes a no-op run manifest and does not call a model.
- If queued, it runs each local before/after prompt through a local Ollama model.
- Full review responses are written under:
  - `repair_semantic_review_responses.local/`
- Safe manifest is:
  - `LOCAL_GEMMA_REPAIR_SEMANTIC_REVIEW_RUN.safe.json`
- Safe manifest includes only schema, run id, model tag, counts, relative response filenames, response hashes, review status, and drift booleans.
- Safe manifest does not relay reviewer notes, before/after prose, protected article text, resolved values, or absolute local paths.

Review response contract:
- `review_status`: one of `pass`, `issues_found`, `blocked`
- `claim_altitude_drift`: bool
- `scope_drift`: bool
- `caveat_drift`: bool
- `numeric_drift`: bool
- `notes`: local-only string, omitted from safe manifest

Tests:
- Added synthetic tests for:
  - all-pass review run producing a prose-free safe manifest,
  - `issues_found` review run setting drift counts and status,
  - empty queue avoiding model calls,
  - invalid review status rejection,
  - prompt hash drift rejection.
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 149 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; CRLF warnings only

Scope:
- No manuscript-atelier commit/push.
- No real model run.
- No raw model prose, protected article text, resolved numeric result values, or local absolute paths relayed in this note.

Next suggested review:
- Please break-it the semantic review runner:
  1. malformed review JSON,
  2. fenced response,
  3. invalid status or non-bool drift flags,
  4. prompt hash drift,
  5. queue count mismatch,
  6. safe manifest note/prose/path leakage,
  7. empty queue false model call.
