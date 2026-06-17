# Codex -> Claude(Code): Lee 2025 draft workspace preflight smoke

Status: info

Related target commit: `8333086 drafts: export writing task preflight`

Local run:

- `C:\Users\USER\Documents\_codex_runs\draft_workspace_lee2025_smoke`

## Summary

After building the Draft Workspace -> writing-runner preflight exporter, I ran
it against the existing Lee 2025 draft workspace smoke.

The first run failed closed because the local smoke workspace had a stale
`stats_handoff.generated.json` after the newer decomposition fingerprint rules.
After regenerating with:

```text
python tools/paper-orchestra/drafts/v0/check_draft_context.py --workspace <LEE workspace> --write --require-decomposition
```

the preflight exporter passed against the synthetic
`sample-packets/local_bundle_demo` bundle.

## Result

```text
draft_context_check=PASS
preflight_written=true
draft_id=LEE2025_ULLEUNGDO_DISCUSSION_SMOKE
decomposition_present=true
decomposition_payload_readable=true
allowed_evidence_id_count=0
allowed_numeric_id_count=0
allowed_claim_id_count=0
blocked_component_count=1
stats_output_source_count=1
ready_for_task_builder=true
```

The allowed ID lists were intentionally empty because this smoke did not have a
real Lee-specific MD Reader bundle mapping. The important check here is that
the workspace planning state projects to a safe preflight surface while blocked
component IDs and stats-output source IDs survive as IDs/enums/counts only.

The local run README now records the smoke, and the generated local output is:

- `C:\Users\USER\Documents\_codex_runs\draft_workspace_lee2025_smoke\writing_task_preflight.generated.json`
