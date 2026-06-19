# LEDGER_263_CODEX_LENGTH_REPAIR_DOCS

VERDICT: ok

Follow-up to LEDGER_259-262. Codex documented the uncommitted length-repair warning behavior in the local manuscript-atelier docs.

## Additional Patch

New local changes:

- `tools/paper-orchestra/local-llm/v0/README.md`
- `tools/paper-orchestra/writing-runner/v0/README.md`

Documentation now states:

- `constraints.paragraph_word_count_repair_margin` defaults to `0`.
- When the margin is set, near-bound word-count misses can pass as repairable drafts with warning codes.
- Larger misses still hard-fail with the original word-count error codes.
- Candidate gate, Conductor, and scorecard surfaces keep warning codes count/hash-only and enum-like.
- Word-count diagnostics remain collapse guards, not prose-quality scores.

## Current Edited Files

The manuscript-atelier patch now touches ten files:

- `tools/paper-orchestra/writing-runner/v0/contract.py`
- `tools/paper-orchestra/writing-runner/v0/tests/test_contract_synthetic.py`
- `tools/paper-orchestra/writing-runner/v0/README.md`
- `tools/paper-orchestra/local-llm/v0/gemma_candidate_gate.py`
- `tools/paper-orchestra/local-llm/v0/ollama_conductor_runner.py`
- `tools/paper-orchestra/local-llm/v0/gemma_quartet_scorecard.py`
- `tools/paper-orchestra/local-llm/v0/README.md`
- `tools/paper-orchestra/local-llm/v0/tests/test_gemma_candidate_gate_synthetic.py`
- `tools/paper-orchestra/local-llm/v0/tests/test_ollama_conductor_runner_synthetic.py`
- `tools/paper-orchestra/local-llm/v0/tests/test_gemma_quartet_scorecard_synthetic.py`

## Verification

Commands run with system Python 3.11:

- `py -3.11 -m pytest tools/paper-orchestra/local-llm/v0/tests -q`
  - Result: 117 passed.
- `py -3.11 -m pytest tools/paper-orchestra/writing-runner/v0/tests/test_contract_synthetic.py -q`
  - Result: 157 passed.
- `git diff --check` on the ten edited files
  - Result: no whitespace errors.

Only the pre-existing `requests` dependency warning appeared during pytest startup.

## Recommendation

This patch is review-ready. It should be committed to manuscript-atelier only after operator/Codex accepts the scope or Claude completes code review.
