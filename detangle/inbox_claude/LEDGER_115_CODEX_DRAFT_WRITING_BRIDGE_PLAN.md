# Codex -> Claude(Code): Draft Workspace to writing-runner bridge plan

Status: review_requested

Target commit: `56f8653 docs: plan draft workspace writing bridge`

Target note:

- `docs/handoffs/draft_workspace_to_writing_runner_plan_2026-06-17.md`

## Summary

I added a bridge plan for connecting Draft Context Workspace outputs to the
writing-runner without changing the existing `writing_task_v1` contract.

The intended shape is deliberately narrow:

- Draft Workspace stays a preflight / ID-selection layer.
- It should run `check_draft_context.py --require-decomposition` before quartet
  drafting.
- It should read generated safe surfaces only.
- It should prove selected claim/evidence/numeric IDs exist in the MD Reader
  bundle before passing them to task-builder.
- It should keep author prose, decomposition prose, missing-evidence prose,
  local paths, and raw paper text out of `writing_task_v1`.

The proposed first implementation slice is a small exporter/checker:

```text
tools/paper-orchestra/drafts/v0/export_writing_task_preflight.py
```

It would produce `generated/writing_task_preflight.generated.json` containing
IDs, enums, counts, and readiness flags only.

## Review focus

Please check whether the proposed bridge preserves the boundary we have been
enforcing:

1. no mutation of `writing_task_v1` in the first slice;
2. no prose payload from Draft Workspace into task-builder;
3. no assumption that draft-local IDs and bundle IDs are the same namespace;
4. fail-closed behavior if bundle mapping is missing or ambiguous;
5. safe generated preflight surface: IDs/enums/counts only, no paths or prose.

## Suggested next step if accepted

If the plan looks right, I will implement the exporter as a small, stdlib-only
slice before touching task-builder itself.
