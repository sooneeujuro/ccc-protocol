# LEDGER_279 — Codex repair semantic-review execution metadata hardening

VERDICT: ok

Scope:
- Target repo: `C:\Users\USER\Documents\manuscript-atelier`
- Local changes only; no manuscript-atelier commit/push.
- No model calls, no raw draft prose, no protected article text, no resolved numeric values, no caption relay.

Implemented:
- Extended scorecard validation of optional `LOCAL_GEMMA_REPAIR_SEMANTIC_REVIEW_RUN.safe.json`.
- The scorecard now rejects semantic-review run manifests unless execution metadata matches the expected local-only shape:
  - queue schema matches the semantic-review queue schema
  - provider is `ollama_local`
  - sampler control is the known Ollama CLI default
  - `network_used` is false
  - `model_called` matches run status (`false` only for `empty`, `true` for non-empty runs)
  - timeout is a positive integer
  - model tag is a bounded single-line string

Added red-path tests:
- semantic-review run with `network_used=true` is rejected.
- non-empty semantic-review run with `model_called=false` is rejected.

Tests:
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_quartet_scorecard_synthetic.py -q`
  - 23 passed
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 160 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `py -3.11 -m py_compile tools\paper-orchestra\local-llm\v0\gemma_quartet_scorecard.py`
  - passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; Windows LF/CRLF warnings only.

Design note:
- This closes another fake-green class where a safe manifest could claim to be a completed local semantic-review run while its execution metadata says otherwise.
- Local review prose and notes remain out of scorecard and ccc relay.

Open / next:
- Claude can re-break the scorecard closure surface.
- manuscript-atelier changes remain local until operator explicitly approves commit/push.
