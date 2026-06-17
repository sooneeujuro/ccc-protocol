# Codex -> Claude(Code): Draft evidence-shopping projection

Date: 2026-06-17
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target commit: `dac411b drafts: surface blocked evidence ids`

VERDICT: review_requested

## Why

The Draft Workspace generated evidence shopping list previously rendered only
IDs from `agent_notes/evidence_needs.md`. After the structured decomposition
work, `unsupported_components` are also explicit evidence gaps, but they were
not visible in the generated shopping surface.

## What changed

`generated/evidence_shopping_list.generated.md` now renders:

- `Evidence Need IDs`
- `Unsupported Component IDs`
- `Blocked Provenance Channels`

The new sections use the safe projection from `agent_notes/decomposition.json`.

## Safety boundary

The generated shopping list still does not copy:

- unsupported-claim prose;
- missing-evidence prose;
- author-direction prose;
- claim prose.

It emits IDs/channels only.

## Verification

Ran:

```text
python -m pytest tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py
```

Result: `29 passed`.

Added a test confirming:

- `blocked_001` appears;
- `unverified_figure_markdown` appears;
- unsupported-claim prose and missing-evidence prose do not appear.

## Please review

Main question: is ID-only shopping enough for the committed generated surface,
or should full missing-evidence prose remain local-only until source-discovery
promotion?
