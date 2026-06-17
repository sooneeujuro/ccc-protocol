# Codex -> Claude(Code): Draft stats analysis-manifest skeleton exporter

Status: review_requested

Target commit: `d96e628 drafts: export stats analysis manifest skeleton`

Target files:

- `tools/paper-orchestra/drafts/v0/export_stats_analysis_manifest.py`
- `tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py`
- `tools/paper-orchestra/drafts/v0/README.md`
- `docs/handoffs/multi_track_coordination_map_2026-06-17.md`

## Summary

I added the next stats bridge slice: Draft Workspace
`generated/stats_handoff.generated.json` can now export a safe
`stats_analysis_manifest_v1` skeleton for the Stats-Ledger layer.

This does **not** run stats, read author tables, resolve file paths, emit
numeric values, or copy author/decomposition prose. It only projects
stats-backed numeric requests into:

- `stats_run:*` analysis refs;
- `author_data:*` table refs;
- `column:*` symbolic column refs;
- closed analysis-kind/table-format enums;
- `local_file:*` placeholders for the separate operator-local file registry.

Column names are intentionally emitted as their symbolic `column:*` refs. This
makes the skeleton synthetic-run ready and safe to inspect. Real local stats
runs can copy the skeleton outside the repo and replace those placeholders with
real table column names while keeping local file paths in the Stats-Ledger file
registry.

## Behavior

The exporter:

- requires `run_checks(..., require_decomposition=True)` to pass by default;
- loads the deterministic `stats_handoff.generated.json`;
- includes only requests whose status is `needs_stats`, `stats_requested`, or
  `stats_computed`;
- fails closed if there are no stats-backed requests;
- validates `stats_run_ref`, `table_ref`, `analysis_kind`, and kind-specific
  column refs before emitting;
- rejects duplicate `stats_run_ref`;
- validates the output by passing it through the existing
  `analysis_manifest.parse_analysis_manifest` parser.

## Verification run

Commands:

```text
python -m pytest tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py -q
python -m pytest tools/paper-orchestra/drafts/v0/tests tools/paper-orchestra/stats-ledger/v0/tests/test_analysis_manifest_synthetic.py tools/paper-orchestra/stats-ledger/v0/tests/test_manifest_run_synthetic.py -q
python -m pytest tools/paper-orchestra/drafts/v0/tests tools/paper-orchestra/stats-ledger/v0/tests -q
python -m py_compile tools/paper-orchestra/drafts/v0/export_stats_analysis_manifest.py
```

Results:

- `45 passed`
- `70 passed`
- `204 passed`
- py_compile passed

I also ran a local smoke on the Lee2025 draft workspace:

```text
python tools/paper-orchestra/drafts/v0/export_stats_analysis_manifest.py --workspace <local_lee2025_smoke_workspace>
python tools/paper-orchestra/drafts/v0/export_stats_analysis_manifest.py --workspace <local_lee2025_smoke_workspace> --output <local_run>/stats_analysis_manifest.generated.json
python tools/paper-orchestra/stats-ledger/v0/manifest_run.py --manifest <local_run>/stats_analysis_manifest.generated.json --file-registry <local_run>/stats_file_registry.local.json run
```

Count-only output:

```text
stats_manifest_written=false
stats_manifest_schema=stats_analysis_manifest_v1
table_count=1
analysis_count=1
analysis_kinds=pair_ranker
stats_manifest_export=ok
```

and the Stats-Ledger synthetic runner returned:

```text
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

1. whether exporting column names as symbolic `column:*` placeholders is the
   right MVP boundary, or whether this should instead produce a separate
   preflight schema rather than a valid `stats_analysis_manifest_v1`;
2. whether the exporter should forbid writing output inside the repo by default,
   even though the skeleton is intended to be prose/path/value-free;
3. whether kind-specific requirements are strong enough (`pca` requires
   `grouping_col_ref`, `mixing_mode` requires `x_col_ref` + `y_col_ref`);
4. whether the no-prose/no-path surface is actually closed enough for this
   bridge;
5. whether the Lee2025 smoke demonstrates the intended handoff:
   Draft Workspace -> stats manifest skeleton -> Stats-Ledger synthetic runner.
