# LEDGER_306_CODEX_TOURNAMENT_TIMESTAMP_HARDENING

VERDICT: ok

Scope:
- Continued Gemma tournament harness hardening after LEDGER_305.
- No model calls.
- No manuscript/corpus data push.
- No raw model prose, protected source text, or resolved numeric values relayed here.

Change:
- Added UTC timestamp validation to prompt tournament manifest production and consumption.
- Generator-side self-check now requires blind/execution/reveal `created_at` to be a compact UTC timestamp and to match across all three manifests.
- Runner-side ingestion now rejects:
  - invalid blind `created_at`
  - invalid execution `created_at`
  - valid-but-mismatched blind/execution `created_at`
- Added red tests for all three drift classes.

Why:
- LEDGER_305 ensured the three generated manifest surfaces are internally consistent.
- Timestamp shape and equality were a remaining provenance seam: malformed or mismatched time metadata could survive even when entry/count metadata matched.
- This patch aligns the tournament path with the broader manifest timestamp hardening already applied elsewhere in the local Gemma harness.

Verification:
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_prompt_tournament_synthetic.py -q`
  - 17 passed
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_tournament_runner_synthetic.py -q`
  - 33 passed
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 245 passed
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q`
  - 468 passed
- `git diff --check -- tools\paper-orchestra\local-llm\v0 tools\paper-orchestra\writing-runner\v0`
  - no whitespace errors
  - only existing CRLF normalization warnings

Notes:
- `manuscript-atelier` remains uncommitted by design.
- ccc-protocol unrelated untracked files, including invoice and detangle JSON files, were not touched.
