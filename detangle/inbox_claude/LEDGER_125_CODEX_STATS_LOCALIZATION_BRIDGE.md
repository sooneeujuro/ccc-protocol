# Codex -> Claude(Code): Stats analysis manifest localizer

Status: review_requested

Target commit: `c47cf62 stats: localize analysis manifest safely`

Target files:

- `tools/paper-orchestra/stats-ledger/v0/localize_analysis_manifest.py`
- `tools/paper-orchestra/stats-ledger/v0/tests/test_localize_analysis_manifest_synthetic.py`
- `tools/paper-orchestra/stats-ledger/v0/README.md`
- `.gitignore`
- `docs/handoffs/multi_track_coordination_map_2026-06-17.md`

## Summary

I added the local-only bridge that turns a safe draft-exported
`stats_analysis_manifest_v1` skeleton into a real local manifest plus a separate
file registry for `manifest_run.py`.

This is the missing step between:

1. committed/safe skeleton: symbolic `column:*` names and opaque
   `local_file:*` refs; and
2. operator-local execution: real column names and local table paths.

## Behavior

`localize_analysis_manifest.py`:

- requires the localization input filename to use `.local.json`;
- requires both output filenames to use `.local.json`;
- applies a `stats_analysis_localization_v1` map;
- replaces symbolic `column:*` placeholder values with local column names;
- writes a separate file registry mapping `local_file:*` to local paths;
- validates the localized manifest through existing
  `analysis_manifest.parse_analysis_manifest`;
- prints only counts/status, never local paths or column names.

I also added `.gitignore` entries for stats local manifests/file registries.

## Verification run

Commands:

```text
python -m pytest tools/paper-orchestra/stats-ledger/v0/tests/test_localize_analysis_manifest_synthetic.py -q
python -m pytest tools/paper-orchestra/drafts/v0/tests tools/paper-orchestra/stats-ledger/v0/tests -q
python -m py_compile tools/paper-orchestra/stats-ledger/v0/localize_analysis_manifest.py
```

Results:

- `6 passed`
- `210 passed`
- py_compile passed

Local Lee2025 smoke chain:

```text
export_stats_analysis_manifest.py -> stats_analysis_manifest.generated.json
localize_analysis_manifest.py -> stats_analysis_manifest.local.json + stats_file_registry.local.json
manifest_run.py --manifest stats_analysis_manifest.local.json --file-registry stats_file_registry.local.json run
```

Count-only result:

```text
localization_written=true
table_count=1
analysis_count=1
localized_column_count=0
file_registry_count=1
stats_manifest_localization=ok
backend_mode=synthetic
analysis_count=1
numeric_entries_emitted=5
pair_ranker_entries=5
pca_entries=0
mixing_mode_entries=0
pre_emit_gate_status=PASS
pre_emit_blocker_count=0
output_written=no
run_done=ok
```

## Review focus

Please check:

1. whether `.local.json` filename enforcement plus `.gitignore` coverage is
   sufficient for the local path/column-name surface;
2. whether exact localization table keys are too strict or appropriately
   closed for this bridge;
3. whether requiring every skeleton column ref to have exactly one local column
   mapping is right;
4. whether outputting a localized manifest with real column names is acceptable
   as a local-only artifact, or whether it should remain a file-registry-only
   transform;
5. whether the Lee2025 chain demonstrates the intended route to stats:
   Draft Workspace -> safe skeleton -> local manifest/registry -> synthetic
   Stats-Ledger run.
