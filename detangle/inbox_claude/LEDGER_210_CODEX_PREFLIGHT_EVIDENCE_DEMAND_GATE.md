# LEDGER_210 Codex Preflight Evidence-Demand Gate

Status: review_requested
Target repo: manuscript-atelier
Target branch: codex/draft-context-workspace
Target commit: e09485a

Builds on:

- `f5b6ead` backchain draft evidence-demand reader
- `c8ea5cb` projection-gap handling

## Summary

Codex connected the Draft Workspace evidence-demand report to the
writing-runner preflight gate.

`export_writing_task_preflight.py` now accepts an optional:

```text
--evidence-demand-report <path>
```

If no report is supplied, compatibility is preserved:

- `evidence_demand_status=not_checked`
- task-builder readiness is decided by existing claim-selection and assembly
  grounding gates.

If a report is supplied:

- it must be outside the repository
- schema must be `draft_workspace_evidence_demand_v1`
- `draft_id` must match the workspace draft
- summary counts must be nonnegative integers
- advisory status must be `ready_for_backchain` or `needs_operator_attention`

When the report has `advisory_status=needs_operator_attention`, preflight emits:

- `task_builder_status=needs_evidence_demand`
- `ready_for_task_builder=false`

The preflight generated surface now includes only count/enum/hash/bool fields:

- `evidence_demand_status`
- `evidence_demand_report_present`
- `evidence_demand_report_sha256`
- evidence-demand claim/support/gap/unsupported/provenance counts
- `evidence_demand_needs_operator_attention_count`

Also fixed while touching the seam: assembly/evidence-demand report inside-repo
checks now use the function's supplied `repo_root` rather than the module global
`REPO_ROOT`, so synthetic and alternate worktrees fail closed correctly.

## Tests

Passed:

```text
python -m pytest tools\paper-orchestra\drafts\v0\tests\test_draft_context_synthetic.py tools\paper-orchestra\backchain\v0\tests\test_draft_workspace_evidence_demand_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_task_builder_synthetic.py
```

Result: 123 passed.

Passed:

```text
python -m py_compile tools\paper-orchestra\drafts\v0\export_writing_task_preflight.py tools\paper-orchestra\drafts\v0\draft_context.py tools\paper-orchestra\backchain\v0\draft_workspace_evidence_demand.py tools\paper-orchestra\writing-runner\v0\task_builder.py
```

New red paths:

- evidence-demand report with `needs_operator_attention` forces
  `task_builder_status=needs_evidence_demand`
- repo-internal evidence-demand report is rejected
- repo-internal assembly report is rejected using the supplied `repo_root`

## Requested Review

Please break-it review the preflight evidence-demand gate:

1. Does the optional evidence-demand report consumption preserve compatibility
   while preventing a known-needs-attention report from becoming task-builder ready?
2. Is the generated preflight surface still count/enum/hash/bool only?
3. Is `needs_evidence_demand` the right status name and gate behavior?
4. Any fake-green risk from trusting the report summary rather than recomputing
   from the report records?

Suggested verdict format:

`VERDICT: ok|issues_found|blocked`

