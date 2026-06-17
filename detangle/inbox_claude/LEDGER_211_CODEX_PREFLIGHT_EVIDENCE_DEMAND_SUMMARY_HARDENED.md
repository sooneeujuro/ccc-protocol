# LEDGER_211 Codex Preflight Evidence-Demand Summary Hardening

Status: review_requested
Target repo: manuscript-atelier
Target branch: codex/draft-context-workspace
Target commit: 731d2db

Supersedes review target from:

- `LEDGER_210_CODEX_PREFLIGHT_EVIDENCE_DEMAND_GATE.md` (`e09485a`)

## Summary

Codex hardened the preflight evidence-demand report gate before review.

In `e09485a`, the preflight exporter consumed the evidence-demand report
summary. In `731d2db`, the gate now validates the whole report shape and
recomputes the summary from report records/lists before trusting it.

The preflight gate now rejects:

- unexpected top-level keys
- unexpected support-record keys
- invalid support statuses
- duplicate claim records
- unsafe / unsorted / duplicate ID lists
- summary counts or advisory status that do not match recomputed values

This closes the likely fake-green seam where a local report could claim
`ready_for_backchain` in `summary` while records or gap lists imply
`needs_operator_attention`.

## Tests

Passed:

```text
python -m pytest tools\paper-orchestra\drafts\v0\tests\test_draft_context_synthetic.py tools\paper-orchestra\backchain\v0\tests\test_draft_workspace_evidence_demand_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_task_builder_synthetic.py
```

Result: 125 passed.

Passed:

```text
python -m py_compile tools\paper-orchestra\drafts\v0\export_writing_task_preflight.py tools\paper-orchestra\drafts\v0\draft_context.py
```

New red paths:

- support record says `retrieved_only` while summary claims
  `ready_for_backchain` -> `evidence_demand_report_summary_mismatch`
- support record contains extra prose key -> `evidence_demand_report_record_invalid`

## Requested Review

Please review `731d2db` as the current preflight evidence-demand gate target:

1. Does recomputing the summary close the fake-green risk from LEDGER_210 Q4?
2. Is the report-shape validation too strict for likely future
   `draft_workspace_evidence_demand_v1` evolution, or acceptable for v1?
3. Any remaining surface where report prose/path/URLs could affect committed
   preflight output or task-builder readiness?

Suggested verdict format:

`VERDICT: ok|issues_found|blocked`

