# LEDGER_309_CODEX_OLLAMA_CONDUCTOR_OUTPUT_SELF_CHECK

VERDICT: ok

Scope:
- Continued local Gemma harness hardening after LEDGER_308.
- No model calls.
- No manuscript/corpus data push.
- No raw model prose, protected source text, or resolved numeric values relayed here.

Change:
- Added output self-checking to `ollama_conductor_runner` before it writes `LOCAL_OLLAMA_CONDUCTOR_RUN.safe.json`.
- The self-check verifies:
  - run schema
  - compact UTC `created_at`
  - prompt-pack run id shape
  - quartet run schema
  - provider/model/provenance bits
  - FGP mode and phrase guard metadata
  - conductor prompt file name, prompt hash, and prompt line count
  - conductor response file name, response hash, response counts, paragraph counts, and id counts
  - warning code token shape
  - required tripwire metadata
  - required semantic review metadata
  - response_count fixed at 1
- Added red tests for response_count drift, response hash drift, and tripwire metadata drift.

Why:
- The Conductor runner is the final stitch surface for the B/M/T local writing path.
- Its output manifest is used downstream to decide whether Conductor output is usable and review-gated.
- This patch makes response and review/tripwire metadata fail closed if future edits drift count/hash/gate fields.

Verification:
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests\test_ollama_conductor_runner_synthetic.py -q`
  - 14 passed
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 253 passed
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q`
  - 468 passed
- `git diff --check -- tools\paper-orchestra\local-llm\v0 tools\paper-orchestra\writing-runner\v0`
  - no whitespace errors
  - only existing CRLF normalization warnings

Notes:
- `manuscript-atelier` remains uncommitted by design.
- ccc-protocol unrelated untracked files, including invoice and detangle JSON files, were not touched.
