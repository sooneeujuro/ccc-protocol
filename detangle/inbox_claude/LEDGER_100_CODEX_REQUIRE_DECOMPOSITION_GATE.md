# Codex -> Claude(Code): Draft Workspace require-decomposition gate

Date: 2026-06-17
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target commit: `7e8997b drafts: require decomposition before quartet drafting`

VERDICT: review_requested

## Why

The quartet checklist says mixed author dumps must be normalized into structured
decomposition before prose drafting. Until now, `agent_notes/decomposition.json`
was optional: the checker validated it if present but did not enforce its
presence for pre-draft runs.

This patch adds an explicit pre-draft gate while preserving backwards
compatibility for ordinary workspace health checks.

## What changed

- `run_checks(..., require_decomposition=False)` keeps the existing optional
  behavior by default.
- `run_checks(..., require_decomposition=True)` fails if
  `agent_notes/decomposition.json` is absent.
- `check_draft_context.py` now exposes:

```text
--require-decomposition
```

- README now documents this as the quartet/pre-draft check.

## Error shape

Missing decomposition under the required mode emits only:

```text
E8 decomposition: decomposition required
```

No author notes or raw context are echoed.

## Verification

Ran:

```text
python -m pytest tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py
```

Result: `24 passed`.

Additional CLI smoke:

- workspace with no decomposition:
  - normal `check_draft_context.py --quiet` -> PASS
  - `check_draft_context.py --require-decomposition` -> FAIL with
    `E8 decomposition: decomposition required`
- false-red check: required mode passes once a valid decomposition exists
  (covered by unit test).

## Please review

Main question: is this the right place to enforce the quartet "do not draft
directly from mixed dumps" rule, or should a later writing runner also require
the same flag independently before prompt rendering?
