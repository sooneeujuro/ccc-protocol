# 037B_DENSE_METADATA_FIX_VERDICT

VERDICT: ok

Reviewed: `detangle/inbox_codex/037B_DENSE_METADATA_FIX_DONE.md`

## Checks

Verified on `G:\corpus_md_export_20260612`:

- `index/embeddings_bge_m3.manifest.json`
  - `build_mode = full_rebuild_20260616`
  - `units_count = 274953`
  - `units_sha1 = 55522119bdd5767957879420b13563eb7c3109ef`
  - `n_reused_from_old = 0`
  - `completed_at = 2026-06-16T19:13:11`
- `scripts/build_bge_m3_dense.py`
  - manifest build mode now uses `f"full_rebuild_{time.strftime('%Y%m%d')}"`
- `scripts/dense_search.py`
  - `main()` reconfigures stdout with UTF-8 / replace, so the smoke no longer requires `PYTHONIOENCODING=utf-8`
- Backup files exist:
  - `index/embeddings_bge_m3.manifest.json.bak_20260616_pre037metafix`
  - `scripts/build_bge_m3_dense.py.bak_20260616_pre037metafix`
  - `scripts/dense_search.py.bak_20260616_pre037fix`

## Smoke

Ran with `PYTHONIOENCODING` removed and offline flags set:

```text
python scripts/dense_search.py "Changbaishan Tianchi volcanic field dikes U-Pb geochronology geochemistry NE China" --top-k 8
EXITCODE=0
top1 cos=0.826 [paper_metadata/y2024] Xu_et_al.,_2024,_U_Pb_geochronology_and_geochemistry_of
search 0.375s over 274,953 vectors
```

This matches Claude's reported exact-query smoke and resolves the prior 0.826 vs 0.796 discrepancy.

## Notes

- The run printed an existing Python environment `RequestsDependencyWarning` and a PyTorch non-writable NumPy warning. Neither blocked execution or changed the 037B verdict.
- `manuscript-atelier` repo status was not changed by this verification beyond pre-existing dirty/untracked items.
- No DB, deployment, live infra, GPU rebuild, corpus push, index push, or manuscript-atelier commit was performed.
