# LEDGER_095 - Codex Draft Decomposition Checker Built

Status: review_requested

Target repo: `C:\Users\USER\Documents\manuscript-atelier`

Branch: `codex/draft-context-workspace`

Target commit: `44997b4` (`drafts: validate structured decomposition notes`)

## Build Summary

Codex implemented the first code bridge from quartet Takes 26-28 into Draft Workspace MVP A:

- optional `agent_notes/decomposition.json`;
- schema constant `draft_decomposition_v1`;
- fail-closed validation when present;
- checks for `verb_level`, `source_roles`, `unsupported_components[].missing_evidence`, source id binding, blocked provenance channel shape, and draft id mismatch;
- no effect on existing workspaces when the optional file is absent.

## Tests

Ran:

```text
python -m pytest tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py
```

Result:

```text
19 passed
```

## Review Request

Please review:

1. whether the schema is too broad or too narrow for MVP B;
2. whether optional validation is the right first step or whether `decomposition.json` should become required later;
3. whether the checker errors are stable and non-leaky enough;
4. whether source-role enums need additional values before wider use.

No live infra, corpus rebuild, or external model calls were performed.
