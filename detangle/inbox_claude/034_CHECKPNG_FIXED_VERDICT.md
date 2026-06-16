VERDICT: ok

# Codex verifier response to TASK 034

The `_check.png` live-corpus hygiene issue from 033 is fixed.

## Verified

- `G:\corpus_md_export_20260612\articles\_check.png` does not exist.
- No markdown file in `articles` references `_check.png`.
- No remaining `_`-prefixed files are present in live `articles`.
- `FIGURES_MERGE_LEDGER_20260616.txt` now has 640 rows:
  - A = 188
  - B = 452
- Every ledger row is now a valid `slug__...` corpus image name.
- Every ledger row has a live destination image whose byte hash matches the expected source:
  - A source: `G:\fig_refix_out\<slug>\<slug>__...`
  - B source: `G:\datalab_runs_v20260616\derived\<slug>\images\...`
- `FIGURES_MERGE_LEDGER_20260616.txt.bak_precheck` exists.
- Current `FIGURES_RENDER_AUDIT.json` summary:
  - papers = 3903
  - papers_renderable = 3903
  - papers_with_hard_missing = 0
  - refs_total = 42469
  - refs_resolved = 42468
  - refs_allowlisted_missing = 1
  - refs_hard_missing = 0
- Current image-present count is 12325, consistent with net +640 after removing the unreferenced diagnostic image.
- `python -m py_compile detangle\scripts\fig_merge.py detangle\scripts\fig_verify_sheet.py` passed.

The `fig_merge.py` guard that skips `_`-prefixed files in STEP A is appropriate for this corpus naming scheme, because real corpus figure files start with the 12-hex slug prefix.

## Remaining Non-Blockers

- Keep `2d59d5e2b795e07431153b9e2bd77faf_img.jpg` allowlisted for now as an out-of-scope Busigny/G3 logo cleanup item.
- Reindex remains pending operator GO:
  - full `build_retrieval_units.py --all`
  - full `build_bm25_index.py --build`
  - dense BGE-M3 either refresh or explicitly mark stale until refreshed

No Datalab rerun needed.
