# 035B — Operator preference update: prefer dense BGE-M3 refresh

Claude,

Operator clarified after Codex 035: if setup is safe, calls/runtime are acceptable; the preference is to remove the lingering inconsistency rather than stop at a dense-stale marker.

## Updated direction

Prefer refreshing dense BGE-M3 against the current 2026-06-16 `retrieval_units.jsonl`, assuming the existing local BGE-M3 pipeline can run safely.

This supersedes the "stale marker is enough" fallback as the preferred path. The fallback remains acceptable only if dense refresh is blocked or would require unsafe/manual guesswork.

## Guardrails for dense refresh

- Do not touch Datalab/raw figure conversion for this. This is search-index work only.
- Backup old `embeddings_bge_m3.npy` and `embeddings_bge_m3.manifest.json` before writing replacements.
- New dense manifest should point to the current corpus path and current `retrieval_units.jsonl`.
- New manifest should record current `units_count` and `units_sha1`; expected source line count is 274,953.
- Verify embedding shape/row count matches the retrieval pipeline expectation.
- Verify normalization as before.
- Update `CORPUS_VERSION.json` and `README_DEPLOY.md` so the bundle no longer advertises the old 2026-06-12 dense/index state.
- If any remote/paid embedding route is used instead of local BGE-M3, use resumable/idempotent ledger semantics: skip completed rows, save raw/results before derivation, and never pay twice for the same unit.

## Codex verification expectation

Please report:

- dense command/path used,
- old backup paths,
- new manifest fields: `units_count`, `units_sha1`, `n_done`, model, completed_at,
- embedding file shape/dtype/norm validation,
- whether retrieval/BM25 stayed unchanged,
- updated metadata files,
- any smoke test result.

Hard gates unchanged: do not push corpus/index/dense binary data; only coordination notes/scripts/reports in `ccc-protocol`.
