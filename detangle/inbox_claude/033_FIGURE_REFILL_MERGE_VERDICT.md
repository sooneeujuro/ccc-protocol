VERDICT: issues_found

# Codex verifier response to TASK 033

Merge/render result is functionally strong, but I found one live-corpus hygiene issue that should be fixed before calling this complete.

## Verified OK

- STOP.md absent; branch was at origin/e0d8c216 before this verdict.
- `FIGURES_RENDER_AUDIT.json` currently reports:
  - papers: 3903
  - papers_renderable: 3903
  - papers_with_hard_missing: 0
  - refs_total: 42469
  - refs_resolved: 42468
  - refs_allowlisted_missing: 1
  - refs_hard_missing: 0
- `FIGURES_MISSING_ALLOWLIST.txt` has exactly 1 entry: `2d59d5e2b795e07431153b9e2bd77faf_img.jpg`.
- Backup folder exists with 10 MDs; all 10 have live counterparts whose bytes differ from backup, consistent with 10 same-name MD replacements.
- Ledger has 641 lines and op counts A=189, B=452.
- For valid `slug__hash_img.jpg` ledger rows, source/live byte checks matched:
  - A rows resolved from `G:\fig_refix_out\<slug>\<slug>__<hash>_img.jpg`
  - B rows resolved from `G:\datalab_runs_v20260616\derived\<slug>\images\<hash>_img.jpg`
- No hard-missing refs remain; keeping the RG/cruft images is consistent with operator direction to preserve Datalab MD-image pairing.

Minor correction: the audit total is `refs_total=42469`; `42468` is the resolved count.

## Issue 1 - unreferenced `_check.png` copied into live articles

Ledger line 189 is:

`A	_check.png	424148`

and the file exists at:

`G:\corpus_md_export_20260612\articles\_check.png`

It matches `G:\fig_refix_out\ff724e5a79c6\_check.png`, but it is not referenced by any markdown file (`rg --fixed-strings "_check.png" articles` returned no refs). This appears to be a diagnostic/contact-check artifact, not a corpus figure. It does not affect render audit because it is unreferenced, but it pollutes live `articles` and the merge ledger/counts.

Requested fix:

- Remove `G:\corpus_md_export_20260612\articles\_check.png`.
- Remove or mark the `_check.png` row in `FIGURES_MERGE_LEDGER_20260616.txt`.
- Re-run the render audit and allowlist regen.
- Report revised counts. Expected: refs should stay `resolved=42468`, `allowlisted_missing=1`, `hard_missing=0`; image-present delta will likely be +640 rather than +641 unless another legitimate A image was missed.

Do not rerun paid Datalab for this.

## Reindex direction

Reindex is required before retrieval/search is considered current, because 10 MDs changed.

Recommended:

1. Run full retrieval-unit rebuild with `build_retrieval_units.py --all`.
2. Then run full BM25 rebuild with `build_bm25_index.py --build`.

Important guard:

- Do not use `build_retrieval_units.py --id ...` with default outputs unless you first add a safe merge/update wrapper. Current CLI writes only the selected IDs to `--out`, so using `--id` against the default full `retrieval_units.jsonl` can replace the full corpus JSONL with a subset.
- `build_bm25_index.py` has no incremental build mode; it rebuilds the pickle from a complete `retrieval_units.jsonl`.

Dense `embeddings_bge_m3`:

- Strict correctness requires regenerating dense embeddings/manifest too.
- If the operator wants to stop the time sink now, BM25-only can be an explicit temporary state, but mark dense retrieval stale for these 10 changed papers and avoid relying on dense search until refreshed.

## Stray allowlist 1

Keep `2d59d5e2b795e07431153b9e2bd77faf_img.jpg` in allowlist for now. It is out of the 51-paper refill scope and should be tracked as a separate small cleanup, not a blocker for this merge after `_check.png` is removed and audit is rerun.
