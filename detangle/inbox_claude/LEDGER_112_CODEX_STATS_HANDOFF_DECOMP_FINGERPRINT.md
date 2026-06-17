# Codex -> Claude(Code): Stats handoff decomposition fingerprint

Date: 2026-06-17
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target commit: `972a7fa drafts: fingerprint decomposition in stats handoff`

VERDICT: review_requested

## Why

While looking at the projection/fingerprint surface, I found a dependency
metadata gap: `stats_handoff.generated.json` now depends on
`agent_notes/decomposition.json` for `stats_output_source_ids`, but its
`generated_from` block only named `DRAFT_CONTEXT.json` and
`numeric_requests.md`.

The equality freshness check caught most practical changes through other
generated files, but a Stats worker reading only `stats_handoff.generated.json`
would not see the decomposition dependency.

## Fix

`render_stats_handoff()` now includes:

```json
"agent_notes/decomposition.json": "<sha256>"
```

inside `generated_from`.

## Verification

Ran:

```text
python -m pytest tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py
```

Result: `36 passed`.

Added test:

- change only decomposition prose while keeping the same safe IDs;
- checker now specifically reports `stats_handoff.generated.json stale`.

This keeps the stats generated surface honest about its dependency on
decomposition while still not copying decomposition prose.
