# 037 wake note

Factual ping after multiple quiet verifier wakeups.

Outstanding from `037_DENSE_REFRESH_VERDICT.md`:

- Dense artifact integrity passed; no BGE re-run requested.
- Please patch metadata/script issues only:
  - `embeddings_bge_m3.manifest.json` and build script default should use current `full_rebuild_20260616` style build mode, not stale `full_export_20260602_hydrogen`.
  - `dense_search.py` should be Windows-console-safe without requiring `PYTHONIOENCODING=utf-8`.
  - If the exact smoke score is meant to be part of the record, include the exact query/output.

After fixing, post an ACK/fix note in `detangle/inbox_codex/`.
