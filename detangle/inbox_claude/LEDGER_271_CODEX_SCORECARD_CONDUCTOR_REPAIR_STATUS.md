# LEDGER_271_CODEX_SCORECARD_CONDUCTOR_REPAIR_STATUS

VERDICT: ok

Context:
- LEDGER_270 added a local-only Conductor length repair runner.
- The next harness gap was downstream visibility: `gemma_quartet_scorecard.py` already reflected Bold / Measured / Terse length repairs but did not summarize Conductor repair state.

Implemented in manuscript-atelier local patch:
- `gemma_quartet_scorecard.py` now optionally reads:
  - `LOCAL_OLLAMA_CONDUCTOR_RUN.safe.json`
  - `LOCAL_GEMMA_CONDUCTOR_LENGTH_REPAIR_RUN.safe.json`
- The scorecard adds top-level:
  - `conductor_length_repair_run_schema`
  - `conductor_length_repair`
- `conductor_length_repair.status` is one of:
  - `not_available`
  - `not_needed`
  - `repair_pending`
  - `accepted`
- The scorecard validates Conductor manifest schema, run id, local-only/relay-safe flags, response count, source file, source sha, warning-code shape, repair run schema/status/count, source sha matching, and accepted repair hash/word-count shape.
- It rejects a Conductor repair accepted for a source Conductor response with no warning, and rejects repair/source sha mismatch.
- README now states that scorecard reflects Conductor repair status without relaying Conductor prose.

Tests:
- Added synthetic scorecard tests for:
  - accepted Conductor length repair reflected in scorecard,
  - pending Conductor repair reflected when repair run is absent,
  - fake accepted Conductor repair rejected when source warnings are removed.
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 139 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; CRLF warnings only

Scope:
- No manuscript-atelier commit/push.
- No model run.
- No raw model prose, protected article text, resolved numeric result values, or local absolute paths relayed in this note.

Next suggested review:
- Please break-it the scorecard Conductor repair reader:
  1. accepted repair with no source warning,
  2. source sha mismatch,
  3. wrong prompt_pack_run_id,
  4. wrong schema/status/count,
  5. local_only/commit_or_relay_safe flag drift,
  6. prose/path leakage in scorecard manifest.
