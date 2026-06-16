VERDICT: issues_found

# Codex verdict on TASK 031 tightened 5/51 batch

Read: `detangle/inbox_codex/031_TIGHTENED_BATCH_5_OF_51.md`

Checked local artifacts under `G:\fig_rebuild_v20260616\`:

- `BATCH_SUMMARY.csv` has 51 rows: 5 `auto-ok`, 46 `MANUAL`, 0 `NO_PDF`.
- Auto-ok set matches Claude's report: Pang2015, Woo2014, Landais2007, Kiyosugi2010, Hart1984.
- For the 5 auto-ok folders, `_summary.json` reports `paper_ok: true`.
- All matched manifest rows use `match_method=by_number`; no matched `by_order` rows found.
- Manifest output SHA-256 values match the staged JPG files, and the filename hash12 prefixes match.
- `staged_md.diff.txt` replacement counts match manifest matched counts: 14, 7, 7, 5, 2.

Issue 1: do not direct-promote the 5 yet.

The 5 are reasonable promote candidates for mapping precision, but not approved for immediate live promotion. Visual contact-sheet review still shows quality/crop risks:

- Woo2014 and Hart1984 include broad page/body text around some figures.
- Landais2007 includes figure crops with surrounding article text for some subfigures.
- Pang2015/Woo2014/Hart1984 folders contain unmanifested extra JPGs even though the contact-sheet summary says `extra_unused=0`:
  - Pang2015: 2 extra JPGs
  - Woo2014: 7 extra JPGs
  - Hart1984: 2 extra JPGs

This is not a mapping failure, but it is a staging hygiene and image-quality gate. Treat these 5 as `PROMOTE_CANDIDATE_BY_NUMBER`, not `PROMOTE_NOW`.

Required before any local promote:

- Remove or segregate unmanifested extra JPGs from the staged promote package.
- Operator visual sign-off on the contact sheets, especially Woo2014, Landais2007, and Hart1984.
- Promote only the manifest-listed `new_name` files; never glob every JPG in the folder.
- Keep live `articles/` untouched until the explicit promote gate.

Seton Datalab accurate pilot metrics proposal:

1. Raw/resume gate: save complete raw JSON first; ledger must include `paper_id`, `pdf_sha256`, Datalab options/model, `request_id`, `check_url`, state, raw path, page count, and estimated cost.
2. Figure identity coverage: matched true figure refs / expected figure refs, excluding logo/cover/junk.
3. Figure-number agreement: body/ref number to extracted caption number, with Seton treated as non-count-only because its current MD has 28 image refs, 2 non-figure refs, 26 figure refs, and body mentions Figure 1..29.
4. Caption overlap: lexical Jaccard plus manual review for low-overlap but plausible geoscience captions.
5. Visual crop quality: full figure present, no clipped panels, no excessive body text, readable labels/colorbars.
6. Contact-sheet audit: side-by-side local region vs Datalab accurate for each figure number.
7. Staged diff safety: only image target lines change unless separately approved.
8. Render audit: staged markdown renders all new images and no broken refs.
9. Idempotency: rerun derivation from raw with zero API calls and identical output manifest.
10. Cost ledger sanity: no resubmit when `raw/<paper_id>.json` or in-flight request exists.

Recommendation:

- Proceed with Datalab accurate harness/pilot first, quality-first not cheap-first.
- Keep the 5 local auto-ok papers as candidates, but do not promote them directly until the staging hygiene and visual gates above pass.
