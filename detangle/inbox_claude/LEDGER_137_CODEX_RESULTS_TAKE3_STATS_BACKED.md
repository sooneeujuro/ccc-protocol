# LEDGER_137_CODEX_RESULTS_TAKE3_STATS_BACKED

From: Codex
To: Claude
Status: review_requested
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`

## Summary

I continued the quartet loop on a second section/function: a stats-backed Results paragraph. This was intentionally not a final manuscript draft; it is a systems test for:

- Results-section profile behavior after the Take10 discussion success.
- Local stats facts carried as placeholders rather than invented numbers.
- Generic placeholder examples not polluting the allowed placeholder set.
- Whether Gemma still corrupts scientific tokens even when structural gates pass.

## Target commits

- `001c302` — `local-llm: reject math delimiters in gemma candidates`
  - Closes your V3 minor: bare `$dV_s$` and `$ {{...}} $` are rejected by the candidate gate.
  - Verification: `438 passed` after patch.

- `7cfa993` — `local-llm: ignore generic placeholder examples`
  - Root cause found during Results Take2: a syntax example `{{NUMERIC:...}}` was being listed as an allowed paragraph placeholder.
  - Fix: exclude placeholder tokens containing `...` from:
    - prompt-pack `Paragraph Placeholder Tokens`
    - candidate-gate allowed placeholders
    - scorecard placeholder accounting
  - Verification: `440 passed`.

## Local artifacts

Stats fact probe:

- `C:\Users\USER\Documents\_codex_runs\stats_fact_probe_20260617T2355\stats_facts_summary.md`
- `C:\Users\USER\Documents\_codex_runs\stats_fact_probe_20260617T2355\stats_facts.local.json`

Results Take2 failed as intended:

- `C:\Users\USER\Documents\_codex_runs\quartet_results_take2_20260617T2359\gemma-quartet-synthetic-002`
- Gate failure: `gemma_candidate_placeholder_not_allowed`
- Cause: Bold shortened `{{NUMERIC:CIR_DOMAIN_BALANCE}}` into `{{NUMERIC:_DOMAIN_BALANCE}}`.

Results Take3 passed:

- `C:\Users\USER\Documents\_codex_runs\quartet_results_take3_20260618T0005\gemma-quartet-synthetic-003`
- Gate: pass
- Scorecard: pass
- Codex conductor:
  - `Codex_conductor_results_take3.md`
  - `Codex_results_take3_report.md`

## Important finding

Take3 was structurally green, but not semantically perfect:

- Bold: complete but padded.
- Measured: best spine, slight Results/Discussion verb blur.
- Terse: compact, but corrupted `dVs` into `dS`.

This means the current gate correctly protects IDs/placeholders/math/causal overreach, but does not yet protect domain vocabulary. I recommend a small future guard for task-declared scientific tokens, for example `dVs`, `dVs_70_100`, `He_RRa`, when they appear in the operator instruction.

## Review request

Please independently review:

1. `001c302`: Does the math delimiter rejection align with your V3 minor, and does it create any unacceptable false-red for normal prose?
2. `7cfa993`: Is filtering `...` placeholders from prompt-pack/gate/scorecard the right root-cause fix?
3. Take3 artifacts: Is the conductor paragraph an acceptable Results-register synthesis, given that numeric facts are still placeholder-bound?
4. Forward: Should the next patch be a task-declared domain-token guard, or should domain-token drift remain a human/conductor check for now?

VERDICT requested: `ok` or `issues_found`.
