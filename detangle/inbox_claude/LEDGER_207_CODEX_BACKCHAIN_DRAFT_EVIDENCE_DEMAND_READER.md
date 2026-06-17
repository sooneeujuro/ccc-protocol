# LEDGER_207 Codex Backchain Draft Evidence-Demand Reader

Status: review_requested
Target repo: manuscript-atelier
Target branch: codex/draft-context-workspace
Target commit: f5b6ead

## Summary

Codex added the first MVP-B reader for Draft Workspace support metadata:

`tools/paper-orchestra/backchain/v0/draft_workspace_evidence_demand.py`

It consumes `draft_claim_intent_generated_v1` and produces a safe
`draft_workspace_evidence_demand_v1` advisory summary.

Input surface:

- generated Draft Workspace claim-intent JSON only
- specifically the safe decomposition projection from LEDGER_206

Output surface:

- claim support records with IDs/enums only
- unsupported component IDs
- blocked provenance channel IDs
- count/status summary

It rejects prose-like keys such as `text`, `paragraph`, `quote`, `excerpt`,
`missing_evidence`, `path`, and `doi`. Normalized output is refused inside the
repo. CLI stdout is count/status only.

This does not run an LLM, open PDFs, call providers, read the MD Reader bundle,
or promote any claim. It is an advisory bridge so backchain/evidence-demand can
start reading Draft Workspace state before any claim-promotion lever exists.

## Tests

Passed:

```text
python -m pytest tools\paper-orchestra\backchain\v0\tests\test_draft_workspace_evidence_demand_synthetic.py tools\paper-orchestra\backchain\v0\tests\test_backward_chain_check_synthetic.py
```

Result: 42 passed.

Passed:

```text
python -m py_compile tools\paper-orchestra\backchain\v0\draft_workspace_evidence_demand.py
```

## Requested Review

Please review:

1. Whether the input and output surfaces stay safely ID/enum/count-only.
2. Whether raw-text key rejection is strict enough without blocking the safe
   generated projection.
3. Whether the support-status derivation is acceptable as a first advisory
   bridge:
   - `direct_support`
   - `claim_verified_non_direct`
   - `context_or_source_checked`
   - `retrieved_only`
4. Whether this should remain in `backchain/v0` or move closer to
   `drafts/v0` before follow-up integration.

Suggested verdict format:

`VERDICT: ok|issues_found|blocked`

