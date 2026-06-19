# LEDGER_303_CODEX_TOURNAMENT_BLIND_METADATA_HARDENING

VERDICT: ok

Scope:
- Continued Gemma tournament harness hardening after LEDGER_302.
- No model calls.
- No manuscript/corpus data push.
- No raw model prose, protected source text, or resolved numeric values relayed here.

Change:
- Hardened the tournament runner's blind manifest ingestion before it copies metadata into the response-only scoring manifest.
- Added validation for:
  - tournament id shape, using the prompt-tournament generator contract
  - provider fixed to `ollama_local`
  - model tag shape
  - `model_called == false`
  - `network_used == false`
  - `fgp_mode` in the known local modes
  - blind scoring disclosure flags and reveal filename
  - scoring axis / hard-gate / selection-rule token shape
  - `minimum_pass_rate` ratio shape
- Added red tests for unsafe blind top-level metadata and unsafe blind-scoring metadata.

Why:
- The scoring manifest is meant to be response-only and blind.
- Previous guards blocked prompt-pack paths, variant labels, blind ids, response leaves, and copied response paths.
- One remaining seam was that several top-level blind metadata fields were copied into scoring output after only a coarse "no prompt_pack_dir" check.
- This patch makes those copied metadata values bounded before the scoring surface is written.

Verification:
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_tournament_runner_synthetic.py -q`
  - 21 passed
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 229 passed
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q`
  - 468 passed
- `git diff --check -- tools\paper-orchestra\local-llm\v0 tools\paper-orchestra\writing-runner\v0`
  - no whitespace errors
  - only existing CRLF normalization warnings

Notes:
- `manuscript-atelier` remains uncommitted by design.
- ccc-protocol unrelated untracked files, including invoice and detangle JSON files, were not touched.
