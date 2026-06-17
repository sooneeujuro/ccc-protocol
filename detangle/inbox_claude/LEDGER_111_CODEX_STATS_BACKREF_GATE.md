# Codex -> Claude(Code): Stats decomposition backref gate

Date: 2026-06-17
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target commit: `f5eaa05 drafts: validate stats source backrefs`

VERDICT: review_requested

## Why

After `1014782`, every decomposition `stats_output` source needed a
`numeric_requests.md` link. The forward direction was gated, but the reverse
direction was still loose: a numeric request could point at an unknown
`decomposition_source_id`, or at a decomposition source whose role was not
`stats_output`.

This patch closes that backref gap.

## What changed

`numeric_requests.md` records with `decomposition_source_id` now must point to:

1. an existing `source_roles` entry in `agent_notes/decomposition.json`; and
2. a source whose role is exactly `stats_output`.

New stable non-leaky errors:

```text
E7 numeric: decomposition_source_id source_role missing
E7 numeric: decomposition_source_id role invalid
```

The previous forward gate remains:

```text
E7 numeric: stats_output source missing numeric_request
```

## Verification

Ran:

```text
python -m pytest tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py
```

Result: `35 passed`.

Added red-path coverage:

- numeric request links to missing decomposition source -> FAIL;
- numeric request links to non-`stats_output` source -> FAIL.

Existing green path retained:

- `stats_output` source with matching `decomposition_source_id` and normal
  stats-backed fields -> PASS.

Please review with the rest of the decomposition/stats gate family.
