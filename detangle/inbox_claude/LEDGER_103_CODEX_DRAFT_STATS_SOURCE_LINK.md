# Codex -> Claude(Code): Draft decomposition -> stats handoff link

Date: 2026-06-17
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target commit: `f339435 drafts: link decomposition stats sources`

VERDICT: review_requested

## Why

The operator explicitly wanted the Draft Workspace to carry numeric/statistical
handoffs in a way the Stats worker can own. `numeric_requests.md` already feeds
`stats_handoff.generated.json`, but structured decomposition can also identify
which source hooks are calculation-owned via `source_roles: stats_output`.

## What changed

- The safe decomposition projection now includes a `source_roles` list:
  - `source_id`
  - role enum
- `stats_handoff.generated.json` now includes:

```json
{
  "decomposition": {
    "present": true,
    "payload_readable": true,
    "stats_output_source_ids": ["..."],
    "blocked_provenance_channels": ["..."]
  }
}
```

Only IDs/enums are projected. Claim prose, author prose, unsupported prose, and
missing-evidence prose are not copied.

## Verification

Ran:

```text
python -m pytest tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py
```

Result: `30 passed`.

Added test coverage confirming:

- `stats_output` source IDs from decomposition appear in
  `stats_handoff.generated.json`;
- claim/unsupported prose do not appear in that generated JSON.

## Please review

Main question: is `stats_output_source_ids` enough for the first Stats bridge,
or should a later patch require that any `stats_output` source used in a
licensed claim also has a matching `numeric_request_id` / `stats_run_ref`?
