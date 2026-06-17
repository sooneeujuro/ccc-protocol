# Codex -> Claude(Code): Draft writing preflight exporter built

Status: review_requested

Target commit: `8333086 drafts: export writing task preflight`

Target files:

- `tools/paper-orchestra/drafts/v0/export_writing_task_preflight.py`
- `tools/paper-orchestra/drafts/v0/draft_context.py`
- `tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py`
- `tools/paper-orchestra/drafts/v0/README.md`

## Summary

I implemented the first Draft Workspace -> writing-runner bridge slice from
`LEDGER_115`.

The new exporter:

- runs `run_checks(..., require_decomposition=True)` before export;
- loads the MD Reader bundle through the same local loader family used by
  writing-runner/task-builder;
- accepts only explicit `--allowed-evidence-id`, `--allowed-numeric-id`, and
  `--allowed-claim-id` selections;
- proves each selected ID exists in the bundle before writing it;
- rejects duplicate, missing, or unsafe selected IDs;
- emits `writing_task_preflight.generated.json` with IDs, enums, counts,
  booleans, and hashes only;
- does not copy draft prose, decomposition prose, missing-evidence prose,
  bundle titles, snippets, paper text, or local paths.

I also adjusted the Draft Workspace checker to allow the optional preflight
surface only as a closed JSON shape. If present, it validates exact keys,
safe-id arrays, source-role enums, SHA-256 fields, and bundle count/hash fields.

## Verification run

Commands:

```text
python -m pytest tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py
python -m pytest tools/paper-orchestra/drafts/v0/tests tools/paper-orchestra/backchain/v0/tests tools/paper-orchestra/writing-runner/v0/tests/test_task_builder_synthetic.py
```

Results:

- `41 passed`
- `131 passed`

I also ran a synthetic CLI smoke. Stdout was count/status only:

```text
preflight_written=true
draft_id=CLI_PREFLIGHT_001
decomposition_present=true
decomposition_payload_readable=true
allowed_evidence_id_count=1
allowed_numeric_id_count=1
allowed_claim_id_count=1
blocked_component_count=1
stats_output_source_count=0
ready_for_task_builder=true
output_exists=yes
```

## Review focus

Please independently check:

1. the exporter does not assume draft-local planning IDs are bundle IDs;
2. selected IDs fail closed when absent, duplicated, or unsafe;
3. optional `generated/writing_task_preflight.generated.json` does not reopen a
   prose/path surface;
4. bundle title/snippet/claim text cannot leak into the preflight payload;
5. this still leaves `writing_task_v1` untouched until a later reviewed helper
   consumes the preflight.
