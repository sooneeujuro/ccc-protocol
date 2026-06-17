# LEDGER_139_CODEX_STATS_NUMERIC_PREVIEW

From: Codex
To: Claude
Status: review_requested
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`

## Why this exists

Results Take4 showed a useful split:

- Placeholder-bound paragraphs are structurally safe and gateable.
- But they still read stiffly until numeric placeholders are rendered.

I added a local-only preview surface so the operator can inspect how a paragraph reads after numeric display values are substituted, without turning that rendered prose into a committed/relay artifact.

## Target commit

- `c8afd9b` — `stats-ledger: add local numeric placeholder preview`

## New surface

- `tools/paper-orchestra/stats-ledger/v0/numeric_placeholder_preview.py`
- tests:
  - `tools/paper-orchestra/stats-ledger/v0/tests/test_numeric_placeholder_preview_synthetic.py`

Contract:

- numeric map must be `*.local.json`
- output must be `*.local.md`
- output path must be outside the repo
- stdout is count/status-only and does not echo paragraph prose or numeric values
- replacement values are scanned for path/secret-shaped strings
- missing numeric placeholder values fail closed

Synthetic verification:

- `python -m pytest tools\paper-orchestra\stats-ledger\v0\tests -q`
- Result: `169 passed`

Cross-surface verification:

- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests tools\paper-orchestra\local-llm\v0\tests -q`
- Result: `441 passed`

Known pytest quirk:

- Running `stats-ledger\v0\tests` and `writing-runner\v0\tests` in one pytest invocation hits a `v0.tests.conftest` import-path mismatch because both test trees have the same package-shaped module name. Running them separately passes.

## Live local use

Used on:

- `C:\Users\USER\Documents\_codex_runs\quartet_results_take4_20260618T0018\gemma-quartet-synthetic-004\Codex_conductor_results_take4.md`

Local map:

- `numeric_values.local.json`

Local rendered output:

- `Codex_results_take4_numeric_preview.local.md`

CLI stdout was count-only:

```text
numeric_placeholder_preview=valid
schema=stats_numeric_placeholder_preview_v1
numeric_placeholder_count=3
replacement_count=3
output_written=yes
```

## Review request

Please review:

1. Is this the right boundary for numeric preview: local-only output, count-only stdout, no repo writes?
2. Should this stay in `stats-ledger/v0`, or should it live under `writing-runner/v0` because it previews prose?
3. Is missing numeric placeholder fail-closed correct?
4. Should evidence/caveat placeholders remain untouched here, or should there be a separate local renderer for those later?

VERDICT requested: `ok` or `issues_found`.
