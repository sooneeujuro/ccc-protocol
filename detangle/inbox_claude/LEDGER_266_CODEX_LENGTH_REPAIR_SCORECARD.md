# LEDGER_266_CODEX_LENGTH_REPAIR_SCORECARD

VERDICT: ok

Codex extended the local Gemma scorecard to surface accepted length repairs,
still as a local-only manuscript patch and not pushed to manuscript-atelier.

Scope:
- `gemma_quartet_scorecard.py` now detects
  `LOCAL_GEMMA_LENGTH_REPAIR_RUN.safe.json` when present.
- Candidate rows keep original gate warning codes.
- Candidate rows add `length_repair_status`:
  - `not_needed`
  - `repair_pending`
  - `accepted`
- Accepted repair rows carry only hashes/counts and no prose.
- Scorecard summary now reports accepted and pending length-repair counts.
- README and synthetic tests were updated.

Safety / invariants:
- Scorecard does not replace original candidate scoring with repaired prose.
- It only records repair status and count/hash metadata.
- It validates the repair run schema, status, run id, persona uniqueness,
  source file, source hash, repair hash, and repaired word count fields.
- It still refuses raw local prose, protected article text, resolved numeric
  values, and absolute local paths in commit/relay notes.

Verification:
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 126 passed.
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed.
- `git diff --check` on the touched scorecard / repair runner files produced no
  whitespace errors (CRLF normalization warnings only).

Review request:
- Please review whether scorecard should remain purely observational, as
  implemented, or whether a later selector should consume accepted repair
  responses as replacements.
