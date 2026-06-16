VERDICT: ok

# Codex verdict on TASK 032 hygiene/promote gate

Read: `detangle/inbox_codex/032_ACK_031_HYGIENE_PROMOTE_GATE.md`

Checked local artifacts under `G:\fig_rebuild_v20260616\` after the orphan cleanup:

- The 5 promote-candidate folders now contain exactly the manifest-referenced staged JPGs:
  - `2a6fa59f9765`: 14 matched, 14 JPGs, 0 extra, 0 missing.
  - `a418032b2ea6`: 7 matched, 7 JPGs, 0 extra, 0 missing.
  - `bc21a8a7c2f8`: 7 matched, 7 JPGs, 0 extra, 0 missing.
  - `6c3a91bb631f`: 5 matched, 5 JPGs, 0 extra, 0 missing.
  - `42846efb5369`: 2 matched, 2 JPGs, 0 extra, 0 missing.
- All matched rows are still `match_method=by_number`.
- Output SHA-256 values still match the staged JPG files, and filename hash12 prefixes still match.
- `BATCH_SUMMARY.csv` remains 51 rows: 5 `auto-ok`, 46 `MANUAL`, 0 `NO_PDF`.
- No Datalab run folder was present at `G:\datalab_runs_v20260616`; no paid/raw output detected in this check.

Promote gate status:

- I agree with the revised status: these 5 are `PROMOTE_CANDIDATE_BY_NUMBER`, not immediate live promote.
- Required gates remain: operator visual sign-off, copy only manifest `new_name` files, no folder globbing, and no live article edits before explicit promote approval.

Nonblocking note:

- `BATCH_SUMMARY.csv` still labels Kiyosugi (`6c3a91bb631f`) as `mode=embedded`, while its current `_summary.json` and `manifest.csv` say `mode=region`. Counts and matching are OK, so this is not a promote blocker, but please sync the mode metadata in the next report to avoid audit confusion.

Seton/Datalab:

- The adopted 10-metric Datalab accurate pilot plan matches Codex 031.
- Keep raw-first/ledger/resume as a hard precondition before any paid call.
