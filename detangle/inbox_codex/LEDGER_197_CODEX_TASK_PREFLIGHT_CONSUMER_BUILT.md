# Codex — task preflight consumer built

`2026-06-18 07:4x KST`

Review requested.

Target repo:
- `C:\Users\USER\Documents\manuscript-atelier`
- branch `codex/draft-context-workspace`
- commit `16921e3` (`writing: consume draft task preflight`)

Why:
- Follow-up to the fe9cb68 forward item: Draft Workspace can emit an
  evidence-aware `writing_task_preflight.generated.json`, but writing-task
  builders needed a consumer gate so preflight warnings cannot remain only
  advisory.

What changed:
1. `writing-runner/v0/task_builder.py`
   - `TaskBuilderInput` now accepts optional `writing_task_preflight`.
   - When supplied, builder refuses:
     - non-`draft_writing_task_preflight_v1` schema
     - missing/unreadable decomposition
     - `ready_for_task_builder != true`
     - `task_builder_status != ready`
     - `evidence_grounding_status == needs_evidence_grounding`
     - allowed evidence/numeric/claim ids that do not exactly match the
       task-builder input ids
   - The preflight is consumed as an input-side gate and is not copied into
     `writing_task_v1`.
   - Summary output exposes only booleans/enums/counts.

2. `writing-runner/v0/cli.py`
   - `build-task` accepts `--writing-task-preflight`.
   - `build-revision-task` also accepts `--writing-task-preflight` and passes it
     through the action-queue bridge.

3. `writing-runner/v0/action_queue_task_bridge.py`
   - Optional preflight is passed into the shared `build_writing_task` gate.

4. Tests and README updated.

Verification:
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_task_builder_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_action_queue_task_bridge_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_cli_synthetic.py`
  - 75 passed
- `python -m pytest tools\paper-orchestra\drafts\v0\tests\test_draft_context_synthetic.py`
  - 47 passed
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_staged_loop_synthetic.py`
  - 13 passed
- `python -m pytest tools\paper-orchestra\draft-driver\v0\tests\test_driver_prepare_synthetic.py`
  - 8 passed
- A mixed pytest invocation across draft-driver and writing-runner hit the known
  `v0.tests.conftest` import-path collision, so those suites were run in
  separate pytest processes.

Known scope boundary:
- This does not make every legacy/direct task construction path require a Draft
  Workspace preflight. It makes the shared writing-runner builder and action
  queue bridge consume and enforce the preflight whenever one is supplied.
- Draft-driver prepare still constructs outline-slot draft tasks directly from
  its own retrieval hits and remains a separate draft-driver path; its existing
  prepare tests stayed green.

Questions for review:
1. Is exact allowed-id match between preflight and builder input the right
   default, or should subset semantics ever be allowed?
2. Should `evidence_grounding_status=not_checked` remain allowed when the
   preflight has no assembly report, or should some future operator mode require
   `grounded` only?
3. Do you want this optional gate wired into any additional higher-level runner
   before we call the fe9cb68 forward item closed?
