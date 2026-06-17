# LEDGER_183_CODEX_ZERO_CLAIM_PREFLIGHT_PATCH

Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Branch: `codex/draft-context-workspace`
Target commit: `6217cf7` (`drafts: mark zero-claim preflight not ready`)

## Summary

Codex patched a second fake-green surface from the repo-function stress review:

- `export_writing_task_preflight.py` previously emitted
  `ready_for_task_builder=true` unconditionally.
- Now it emits:
  - `task_builder_status=ready`
  - `ready_for_task_builder=true`
  only when `allowed_claim_ids` is non-empty.
- If evidence/numeric IDs are selected but no bundle claim ID is selected, it emits:
  - `task_builder_status=needs_claim_extraction`
  - `ready_for_task_builder=false`

The preflight surface remains ID/enum/count/hash only; no claim prose, paper text,
bundle titles, snippets, paths, or author prose are copied.

## Verification run

Codex ran:

```text
python -m pytest tools\paper-orchestra\drafts\v0\tests
```

Result: `46 passed`.

Added red path:

- Build preflight with real bundle evidence/numeric IDs but no claim IDs.
- Expected: checker accepts the generated surface as fresh and safe, but
  `ready_for_task_builder=false` and `task_builder_status=needs_claim_extraction`.

## Review request

Please independently review/break the patch, especially:

1. Does this close the zero-claim fake-green without blocking valid ready preflights?
2. Is `allowed_claim_ids` the right readiness gate, or should readiness require
   another claim surface as well?
3. Does the added `task_builder_status` enum stay closed and count/status-only?
4. Is there any adjacent path where a task can still be built from a zero-claim
   preflight while appearing ready?

Suggested verdict shape:

`VERDICT: ok | issues_found | blocked`

