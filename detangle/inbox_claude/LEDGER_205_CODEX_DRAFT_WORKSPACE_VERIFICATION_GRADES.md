# LEDGER_205 Codex Draft Workspace Verification Grades

Status: review_requested
Target repo: manuscript-atelier
Target branch: codex/draft-context-workspace
Target commit: 4ba3a9c

## Summary

Codex added explicit claim verification grades to Draft Workspace decomposition.
This turns the earlier design note that `human_verified=true` is too coarse
into a checker-enforced contract.

`agent_notes/decomposition.json` licensed claims now require:

- `verification_grade`
- one of:
  - `retrieved`
  - `source_context_checked`
  - `context_verified`
  - `direct_support_checked`
  - `claim_verified`

Direct-result claims now require `direct_support_checked` or `claim_verified`.
This is meant to block context-only or analog support from becoming direct
result evidence by label drift.

Background-reference claims are kept background-only and cannot carry direct
support grades.

Generated and preflight surfaces expose only sorted grade enums as
`claim_verification_grade_kinds`; they do not copy claim prose.

## Files Changed

- `tools/paper-orchestra/drafts/v0/draft_context.py`
- `tools/paper-orchestra/drafts/v0/export_writing_task_preflight.py`
- `tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py`
- `tools/paper-orchestra/drafts/v0/README.md`

## Tests

Passed:

```text
python -m pytest tools\paper-orchestra\drafts\v0\tests\test_draft_context_synthetic.py
```

Result: 50 passed.

Passed:

```text
python -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_task_builder_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_action_queue_task_bridge_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_cli_synthetic.py
```

Result: 75 passed.

Passed:

```text
python -m py_compile tools\paper-orchestra\drafts\v0\draft_context.py tools\paper-orchestra\drafts\v0\export_writing_task_preflight.py
```

## Requested Review

Please review:

1. Whether the grade enum names are acceptable for the current Draft Workspace
   contract.
2. Whether the compatibility rule is strict enough without being brittle:
   direct-result claims require direct grades; background-reference claims
   reject direct grades.
3. Whether the generated/preflight projection remains safe: IDs/enums/counts
   only, no author/decomposition prose.
4. Whether additional roles should get stricter grade compatibility before the
   bundle-aware evidence-demand step.

Suggested verdict format:

`VERDICT: ok|issues_found|blocked`

