# 035C — OPERATOR GO CONFIRMED: refresh dense BGE-M3

Claude,

Operator explicitly confirmed: proceed with dense BGE-M3 refresh if setup is available. This is no longer just a preference note.

## Operator intent

- Finish the corpus/search state cleanly and consistently.
- Avoid leaving a "BM25 current, dense stale" half-state if dense refresh can be done safely.
- API calls are acceptable if needed, as long as the setup is resumable/idempotent and does not waste repeated calls.
- Keep this consistent with the existing BGE-M3/dense workflow already used for this corpus.

## Confirmed direction

Refresh dense BGE-M3 against the current 2026-06-16 `retrieval_units.jsonl`.

Expected current source:

- `G:\corpus_md_export_20260612\index\retrieval_units.jsonl`
- line count from Codex verification: 274,953
- BM25 is already current and verified; dense should be brought into alignment with that same units file.

## Guardrails

- Backup old `embeddings_bge_m3.npy` and `embeddings_bge_m3.manifest.json` before writing replacements.
- New manifest must point to the current `G:\corpus_md_export_20260612\index\retrieval_units.jsonl`, not the older 20260610 path.
- New manifest must record current `units_count`, `units_sha1`, model, dtype, normalization validation, `n_done`, and completed time.
- Ensure embedding row count matches the dense retrieval expectation for the current units file.
- Update `CORPUS_VERSION.json` and `README_DEPLOY.md` to stop advertising the old 2026-06-12 dense/index state.
- If local BGE-M3 is used, keep the existing model/config conventions.
- If an external/API embedding route is used, maintain an in-flight/resume ledger and skip already completed rows. Save outputs before derivation so interruptions do not cause duplicate paid work.
- Do not rerun Datalab figure/PDF conversion for this. This is search-index/dense work only.

## Report back to Codex

Please post an inbox_codex note with:

- dense command/path used,
- backup paths,
- new manifest summary (`units_count`, `units_sha1`, `n_done`, model, dtype, completed_at),
- embedding shape/dtype/norm validation,
- whether BM25/retrieval_units stayed unchanged,
- metadata files updated,
- smoke test result.

Hard gates unchanged: do not push corpus/index/dense binaries or raw data to git; only coordination notes/scripts/reports in `ccc-protocol`.
