# 037 dense BGE-M3 refresh verifier verdict

VERDICT: issues_found

Scope checked: `037_DENSE_REFRESH_DONE.md`, committed note `2298587`, and local artifacts under `G:\corpus_md_export_20260612`.

## Verified OK

- `index/retrieval_units.jsonl`
  - File-iteration row count: 274,953.
  - SHA1: `55522119bdd5767957879420b13563eb7c3109ef`.
  - JSONL parse: no bad records found with `for line in f`.
  - `read_text().splitlines()` count is 274,960 while `\n` count/file iteration is 274,953, reproducing the reported 7-record Unicode line-separator failure mode.
- `index/embeddings_bge_m3.npy`
  - Shape: `(274953, 1024)`.
  - dtype: `float32`.
  - File size: 1,126,207,616 bytes; data nbytes + `.npy` header size align.
  - Sample independent norms are near 1.0; manifest norm range is `[0.9997558, 1.0004992]` with `normalized_pass: true`.
- `index/embeddings_bge_m3.manifest.json`
  - `units_count`, `units_sha1`, `n_done`, `n_newly_embedded`, and `n_reused_from_old=0` match a full rebuild aligned to current units.
  - `device: cuda`, `model: BAAI/bge-m3`, `dim: 1024`, `normalize: true`.
- Build script bugfix is present locally:
  - Current `scripts/build_bge_m3_dense.py` uses file iteration over `UNITS_PATH.open(...)`.
  - Backup script still shows the old `read_text(...).splitlines()` path.
- Corpus metadata:
  - `CORPUS_VERSION.json` now advertises version date `2026-06-16`, chunks `274953`, dense `full_rebuild_20260616`, and matching units SHA1.
  - `README_DEPLOY.md` says `3903 papers / 274953 units` and notes the 2026-06-16 full BM25 + BGE-M3 rebuild.
  - `articles/*.md` count and `index/retrieval_papers.json.paper_count` both verify as 3,903.
- Smoke:
  - With `PYTHONIOENCODING=utf-8`, `dense_search.py "Xu 2024 U Pb geochronology geochemistry Changbaishan Tianchi volcanic field dikes" --top-k 8` returns the Xu 2024 replacement paper as top-1, cos `0.796`, over 274,953 vectors.

## Issues

1. Dense manifest has stale/conflicting `build_mode`.
   - Task note says manifest `build_mode` is `full_rebuild`.
   - `CORPUS_VERSION.json` says dense `build_mode: full_rebuild_20260616`.
   - Actual `embeddings_bge_m3.manifest.json` still says `build_mode: full_export_20260602_hydrogen`.
   - Please update the manifest and the build script default so future validators do not misread this as the old June 2 export mode. No re-embedding needed.

2. `dense_search.py` smoke is not Windows-console-safe by default.
   - Running it in the default PowerShell/cp949 environment performed the search, but exited nonzero with `UnicodeEncodeError` while printing a Unicode heading.
   - Please make the script robust, e.g. reconfigure stdout to UTF-8/errors=replace or otherwise sanitize output. Until then, smoke commands need `PYTHONIOENCODING=utf-8`.

3. Exact smoke claim is not fully reproducible from the note text.
   - The note reports Xu 2024 top-1 cos `0.826`, but the visible query is ellipsized.
   - My title-like query verifies top-1 Xu 2024 at cos `0.796`.
   - Please include the exact smoke query/output if you want the exact score to be part of the verification record.

## Gate

Dense artifact integrity itself looks good: row alignment, units SHA, dtype/shape, and replacement-paper smoke all pass. Treat this as a metadata/script-fix verdict, not a request to rerun BGE-M3. After the manifest `build_mode` and Windows-safe smoke output are fixed, this should be acceptable.
