# LEDGER_259_CODEX_LENGTH_REPAIR_MARGIN_PATCH

VERDICT: ok

Codex implemented a local manuscript-atelier patch in response to the operator's question about word-count gates. This note is prose-free and count-only.

## Motivation

The CIR subsection pilot showed that near-bound word-count misses can be repairable drafting issues rather than scientific failures. One p2 candidate missed the active word-count floor by only a few words while preserving the intended bounded role. Re-running with a lower floor passed cleanly, but that is an ad hoc workaround.

## Local Patch

Uncommitted manuscript-atelier files changed:

- `tools/paper-orchestra/writing-runner/v0/contract.py`
- `tools/paper-orchestra/local-llm/v0/gemma_candidate_gate.py`
- `tools/paper-orchestra/local-llm/v0/tests/test_gemma_candidate_gate_synthetic.py`

Behavior:

- Default remains strict: `paragraph_word_count_repair_margin` defaults to `0`, so existing tasks still hard-fail short/long paragraphs exactly as before.
- If a task explicitly sets `constraints.paragraph_word_count_repair_margin`, near-bound short/long outputs within that margin pass the candidate gate with a warning code.
- Outputs beyond the margin still hard-fail with the original stable error codes.
- Gate and diagnostic safe manifests now include `warning_codes`; diagnostics also record the active repair margin.

Warning codes:

- `gemma_candidate_paragraph_word_count_repairable_short`
- `gemma_candidate_paragraph_word_count_repairable_long`

## Verification

Pytest was unavailable in the current bundled Python environment, so Codex ran:

- `compileall` on the edited modules.
- A manual end-to-end synthetic smoke: prepare prompt pack -> synthetic quartet executor -> gate -> diagnose.

Smoke result:

- A candidate two words below the configured minimum passed when repair margin was two and emitted the repairable-short warning.
- The same candidate remained a hard failure when the deficit exceeded the repair margin.

## Review Request

Claude should review the design before manuscript-atelier commit:

- Is `paragraph_word_count_repair_margin` the right contract field name?
- Should warning-bearing candidates be allowed into Conductor automatically, or should Conductor receive an explicit length-repair notice?
- Is a symmetric short/long margin acceptable, or should short and long margins be separate?

No manuscript-atelier commit or push has been made for this patch.
