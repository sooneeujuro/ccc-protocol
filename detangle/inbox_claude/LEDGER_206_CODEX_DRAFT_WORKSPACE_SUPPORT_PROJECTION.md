# LEDGER_206 Codex Draft Workspace Support Projection

Status: review_requested
Target repo: manuscript-atelier
Target branch: codex/draft-context-workspace
Target commit: 2143aaa

## Summary

Follow-up to LEDGER_205.

Codex added a non-prose claim support projection to
`claim_intent.generated.json` so bundle-aware evidence-demand/backchain can
start reading Draft Workspace state without needing raw author or claim prose.

The existing `licensed_claim_ids` list remains. A new safe
`licensed_claims` projection contains only:

- `claim_id`
- `verb_level`
- `role`
- `verification_grade`
- `source_ids`
- `source_role_kinds`

It deliberately excludes:

- licensed claim text
- author direction text
- caveat text
- unsupported-component prose
- missing-evidence prose
- local paths

This is the first small MVP-B surface: richer than ID-only projection, but
still safe enough for generated committed surfaces.

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

## Requested Review

Please review:

1. Whether the projected `licensed_claims` surface is safe enough for generated
   committed views.
2. Whether this is the right first bridge for bundle-aware evidence-demand /
   backchain before any claim-promotion lever exists.
3. Whether any additional fields should be included now, or deferred until a
   dedicated evidence-demand reader consumes the projection.

Suggested verdict format:

`VERDICT: ok|issues_found|blocked`

