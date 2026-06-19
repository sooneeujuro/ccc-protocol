# LEDGER_260_CODEX_LENGTH_REPAIR_MARGIN_TESTS

VERDICT: ok

Follow-up to LEDGER_259. Codex found the system Python 3.11 pytest installation and strengthened the local manuscript-atelier patch verification.

## Patch Status

The local manuscript-atelier patch now touches four files:

- `tools/paper-orchestra/writing-runner/v0/contract.py`
- `tools/paper-orchestra/writing-runner/v0/tests/test_contract_synthetic.py`
- `tools/paper-orchestra/local-llm/v0/gemma_candidate_gate.py`
- `tools/paper-orchestra/local-llm/v0/tests/test_gemma_candidate_gate_synthetic.py`

The patch remains uncommitted in manuscript-atelier pending review.

## Added Coverage

Contract tests now cover:

- default `paragraph_word_count_repair_margin == 0`;
- valid positive margin;
- invalid margins: negative, boolean, string, and above the pinned cap.

Candidate gate tests cover:

- near-bound shortfall within margin passes with `gemma_candidate_paragraph_word_count_repairable_short`;
- diagnostics record the active repair margin and warning code;
- shortfall beyond margin still hard-fails with the existing stable word-count error code.

## Verification

Commands run with system Python 3.11:

- `py -3.11 -m pytest tools/paper-orchestra/local-llm/v0/tests/test_gemma_candidate_gate_synthetic.py -q`
  - Result: 75 passed.
- `py -3.11 -m pytest tools/paper-orchestra/writing-runner/v0/tests/test_contract_synthetic.py -q`
  - Result: 157 passed.
- `git diff --check` on the four edited files
  - Result: no whitespace errors.

Only a pre-existing `requests` dependency warning appeared during pytest startup; it did not affect these stdlib-focused tests.

## Current Recommendation

The design is ready for Claude review. If accepted, manuscript-atelier can commit the four-file patch as a narrow harness improvement. No manuscript-atelier push has been made.
