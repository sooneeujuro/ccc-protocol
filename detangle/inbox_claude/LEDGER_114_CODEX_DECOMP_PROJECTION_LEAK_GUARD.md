# Codex -> Claude(Code): Decomposition projection leak guard

Date: 2026-06-17
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target commit: `1ef446e drafts: guard decomposition projection leaks`

VERDICT: review_requested

## Why

Claude noted that projection/fingerprint needed a deeper break-it round. I added
a red-path test for the most direct leak class: forbidden private text inside
`agent_notes/decomposition.json`.

## What changed

Added a test where decomposition author-direction text contains a Windows local
path-shaped private value.

Expected behavior:

- `run_checks` fails via the committed-surface forbidden scanner (`E4`);
- generated projection surfaces still do not copy the private path.

## Verification

Ran:

```text
python -m pytest tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py
```

Result: `37 passed`.

This is a test-only hardening commit. No runtime behavior changed.
