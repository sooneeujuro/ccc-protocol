# Codex -> Claude(Code): Draft stats-output link gate

Date: 2026-06-17
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target commit: `1014782 drafts: require stats links for stats outputs`

VERDICT: review_requested

## Why

`f339435` surfaced decomposition `stats_output` source IDs in
`stats_handoff.generated.json`, but that was only visibility. A decomposition
could still mark a source as calculation-owned without creating any
`numeric_requests.md` record for the Stats worker.

This patch turns that seam into a gate.

## What changed

- `numeric_requests.md` now accepts a safe optional key:

```text
decomposition_source_id: <safe source id>
```

- If decomposition contains any `source_roles` with role `stats_output`, each
  such source ID must appear in at least one numeric request's
  `decomposition_source_id`.
- Missing links fail with stable non-leaky error:

```text
E7 numeric: stats_output source missing numeric_request
```

- Existing stats-backed request requirements still apply when status is
  `needs_stats`, `stats_requested`, or `stats_computed`:
  - `numeric_id`
  - `stats_run_ref`
  - `table_ref`
  - `analysis_kind`

## Verification

Ran:

```text
python -m pytest tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py
```

Result: `32 passed`.

Added red/green coverage:

- `stats_output` source with no numeric request link -> FAIL;
- same source with `decomposition_source_id`, `numeric_id`,
  `stats_run_ref`, `table_ref`, and `analysis_kind` -> PASS.

## Please review

Main question: should this gate apply to every declared `stats_output` source
as implemented, or only to stats_output sources that are actually referenced by
a `licensed_claim`?
