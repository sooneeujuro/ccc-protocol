VERDICT: issues_found

# Codex verifier response to TASK 035

The full `retrieval_units` + BM25 rebuild is verified OK. The remaining issue is metadata/stale-marker hygiene: dense BGE-M3 is intentionally not refreshed, but the corpus metadata still presents the old dense/index state as current.

## Verified OK

- `retrieval_units.report.json` has `ok: true`, `errors: []`, `warnings: []`.
- `retrieval_units.jsonl` line count: 274,953.
- `retrieval_papers.json`: `paper_count=3903`, `papers` list length 3903.
- Rebuilt backups exist:
  - `retrieval_units.jsonl.bak_20260616`
  - `retrieval_papers.json.bak_20260616`
- Current file mtimes are consistent with the 17:38-17:41 rebuild window:
  - `retrieval_units.jsonl`: 2026-06-16 17:39:32
  - `retrieval_papers.json`: 2026-06-16 17:39:32
  - `bm25_index.pkl`: 2026-06-16 17:40:56
- BM25 stats:
  - `n_docs=274705`
  - `vocab_size=386343`
  - `avgdl=175.91`
  - `built_at=2026-06-16T17:40:32`
  - `units_path=G:\corpus_md_export_20260612\index\retrieval_units.jsonl`
  - `md_dir=G:\corpus_md_export_20260612\articles`
- The apparent `274953` units vs `274705` BM25 docs difference is explained: independent cold-load/tokenize check found `bad_offset_or_empty=0` and `ok_but_no_tokens=248`, so BM25 excludes 248 tokenless chunks by design.
- The 10 replaced MDs are represented in `retrieval_units.jsonl` with 844 chunks total, and all 10 have matching `retrieval_papers.json` records whose `source_md_sha1` matches the live article bytes.
- Query smoke with UTF-8 output confirms new text is searchable: `Changbaishan Tianchi volcanic field dikes U-Pb geochronology` returns Xu 2024 as ranks 1-4.
- `fig_md_textdiff.py` supports the need for reindex: text-only similarities range from 0.888 to 0.986.

## Issue 1 - Dense stale state is not durably marked in corpus metadata

I agree with deferring dense refresh as a temporary operator-approved state, but the stale state must be visible where future tooling/operators will look.

Current `embeddings_bge_m3.manifest.json` still says:

- `completed_at=2026-06-12T11:14:08`
- `units_count=274957`
- old `units_sha1=210df4e02dd3978a4fcb927161c555ab3b52a9c8`
- old `units_path=C:\Users\USER\corpus_md_export_20260610\index\retrieval_units.jsonl`

There is no corpus-local stale marker under `index/`, and `CORPUS_VERSION.json` / `README_DEPLOY.md` still describe the 2026-06-12 index state (`3902 papers / 274957 units`, dense current). This can mislead a future reader/deploy step into treating dense as compatible with the new 2026-06-16 retrieval units.

Requested fix, no expensive work:

- Add a durable marker or metadata update saying dense BGE-M3 is stale relative to the 2026-06-16 `retrieval_units.jsonl`.
- Include the 10 stale paper names or at least the stale scope: "10 figure-refill reconverted MDs; BM25 current; dense not refreshed".
- Update `CORPUS_VERSION.json` and/or `README_DEPLOY.md` so the bundle does not claim the old 3902/274957 all-current state.
- If a retrieval config exists that enables/weights dense search, either mark dense disabled for this temporary bundle or document "do not rely on dense-only results until refresh".

Dense regeneration is not required for this verdict if the stale state is clearly marked.

## Nonblocking Note

On the default Windows CP949 console, `build_bm25_index.py --query` can crash while printing Unicode snippets. Setting `PYTHONIOENCODING=utf-8` avoids it. This does not affect index integrity, but it is worth remembering for operator smoke tests.
