# LEDGER_308_CODEX_OLLAMA_QUARTET_OUTPUT_SELF_CHECK

VERDICT: ok

Scope:
- Continued local Gemma harness hardening after LEDGER_307.
- No model calls.
- No manuscript/corpus data push.
- No raw model prose, protected source text, or resolved numeric values relayed here.

Change:
- Added output self-checking to `ollama_quartet_runner` before it writes `LOCAL_OLLAMA_QUARTET_RUN.safe.json`.
- The self-check verifies:
  - run schema
  - compact UTC `created_at`
  - prompt-pack run id shape
  - provider/model/provenance bits
  - FGP mode and phrase guard metadata
  - response_count matching actual response rows
  - persona order and uniqueness
  - safe response leaf filenames
  - prompt/response SHA-256 hex shape
  - positive response char/line counts
- Added red tests for response_count drift, unsafe response file drift, and response hash drift.

Why:
- Tournament runner copies response files based on the Ollama quartet run manifest.
- The prompt-pack input surface was already checked, but the output manifest did not yet prove its own response count/file/hash metadata before disk write.
- This patch makes the immediate model-output manifest fail closed if future edits drift count/path/hash fields.

Verification:
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests\test_ollama_quartet_runner_synthetic.py -q`
  - 15 passed
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 250 passed
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q`
  - 468 passed
- `git diff --check -- tools\paper-orchestra\local-llm\v0 tools\paper-orchestra\writing-runner\v0`
  - no whitespace errors
  - only existing CRLF normalization warnings

Notes:
- `manuscript-atelier` remains uncommitted by design.
- ccc-protocol unrelated untracked files, including invoice and detangle JSON files, were not touched.
