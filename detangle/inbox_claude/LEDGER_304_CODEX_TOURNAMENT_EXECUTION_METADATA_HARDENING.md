# LEDGER_304_CODEX_TOURNAMENT_EXECUTION_METADATA_HARDENING

VERDICT: ok

Scope:
- Continued Gemma tournament harness hardening after LEDGER_303.
- No model calls.
- No manuscript/corpus data push.
- No raw model prose, protected source text, or resolved numeric values relayed here.

Change:
- Hardened prompt-tournament execution manifest ingestion in the tournament runner.
- Added validation for:
  - execution tournament id shape
  - `contains_prompt_pack_dirs == true`
  - `blind_scoring_surface == false`
  - `local_only == true`
  - `commit_or_relay_safe == false`
  - blind/execution tournament id equality
  - blind expected model-call count matching execution entries
  - blind persona count matching the runner persona set
  - blind variant/repetition counts matching execution entry count
- Added red tests for unsafe execution scope metadata, blind/execution id mismatch, and blind count drift.

Why:
- LEDGER_303 bounded the metadata copied into the response-only scoring manifest.
- The execution manifest remains local-only, but it still drives model execution and run-manifest provenance.
- This patch makes the local execution surface fail closed if scope/provenance bits or count metadata drift before execution starts.

Verification:
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_tournament_runner_synthetic.py -q`
  - 30 passed
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 238 passed
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q`
  - 468 passed
- `git diff --check -- tools\paper-orchestra\local-llm\v0 tools\paper-orchestra\writing-runner\v0`
  - no whitespace errors
  - only existing CRLF normalization warnings

Notes:
- `manuscript-atelier` remains uncommitted by design.
- ccc-protocol unrelated untracked files, including invoice and detangle JSON files, were not touched.
