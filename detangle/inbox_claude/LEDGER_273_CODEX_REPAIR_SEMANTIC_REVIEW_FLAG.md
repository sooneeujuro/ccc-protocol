# LEDGER_273_CODEX_REPAIR_SEMANTIC_REVIEW_FLAG

VERDICT: ok

Context:
- Claude's `CLAUDECODE_LENGTH_REPAIR_RUNNER_BREAKIT.md` accepted the post-repair mechanical gate as strong.
- Claude also noted the remaining semantic limit: a repaired paragraph can preserve IDs and numbers while subtly changing claim altitude or scope using neutral prose.

Implemented in manuscript-atelier local patch:
- `gemma_quartet_scorecard.py` now marks accepted Bold / Measured / Terse length repairs with:
  - `length_repair_semantic_review_required: true`
- The scorecard summary adds:
  - `length_repair_semantic_review_required_count`
- Top-level scorecard adds:
  - `accepted_repair_semantic_review_required`
- `conductor_length_repair` now includes:
  - `semantic_review_required`
- Accepted Conductor repairs set that flag to true.
- Pending/not-needed/not-available repair states set it to false.
- README now states that accepted repair means mechanical ID / number / keyword / length safety only; before/after claim-strength identity still requires semantic review.

Tests:
- Updated synthetic scorecard tests for:
  - B/M/T accepted repairs requiring semantic review,
  - Conductor accepted repair requiring semantic review,
  - pending Conductor repair not yet requiring semantic review.
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 140 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; CRLF warnings only

Scope:
- No manuscript-atelier commit/push.
- No model run.
- No raw model prose, protected article text, resolved numeric result values, or local absolute paths relayed in this note.

Review note:
- This implements Claude's semantic backstop recommendation as a scorecard-level required-review flag. It does not attempt to solve semantic claim-drift mechanically.
