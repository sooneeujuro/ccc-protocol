VERDICT: issues_found

# Codex verdict on TASK 027 B-prime pilot 1a

Reviewed `G:\fig_rebuild_v20260616\d0d849cec9de\` for Lee & Walker 2006.

## What checks out

- Staging folder exists and contains 4 extracted figure JPGs, `manifest.csv`, and `contact_sheet.png`.
- Contact sheet visually shows 4 real scientific figures, not publisher logo/banner material.
- Old references in the article markdown exist in order:
  - fig01 maps to old Fig. 1 ref at line 43.
  - fig02 maps to old Fig. 2 ref at line 105.
  - fig03 maps to old Fig. 3 ref at line 133.
  - fig04 maps to old Fig. 4 ref at line 185.
- Source PDF SHA-256 matches manifest:
  `c903dcf481b33d44b218da0611ffa1b1bae191115f905370fba7f46f7fb8d764`.
- Manifest dimensions match the saved JPG dimensions.
- No live `articles/` edit was detected from this artifact set.

For this specific paper, the caption-page filter did the right thing: raw 6 embedded images became 4 figure candidates, matching the 4 missing markdown refs, and the contact sheet supports the mapping.

## Issues to fix before Seton / batch

1. `img_sha256` and filename sha12 do not identify the saved JPG bytes.
   The manifest stores the SHA-256 of the extracted PDF image bytes, but the script saves a re-encoded JPEG. Recomputed saved-file hashes differ for all 4 files:
   - fig01 manifest `448ca9c51315`, saved file `bf9f70f931ce`
   - fig02 manifest `1f26c5b23497`, saved file `3c768fc4e631`
   - fig03 manifest `1e4669d9cf76`, saved file `1768da04d032`
   - fig04 manifest `d5e4346174ff`, saved file `8c376291b889`

   Please either:
   - make the filename suffix and `img_sha256` refer to the final saved file bytes, or
   - keep both fields explicitly as `source_image_sha256` and `output_file_sha256`, with the filename using `output_file_sha256[:12]`.

2. `staged_md.diff.txt` is promised by the script docstring / B-prime plan but absent from the pilot folder.
   Add a staged diff that changes only the four image targets and leaves live `articles/` untouched.

3. Manifest evidence is too thin for later audit.
   Add `article_md`, `article_line`, full `old_alt` or sidecar JSON, `pdf_caption_text`, `pdf_caption_fig_no`, `xref`, `candidate_index_on_page`, `raw_candidate_count`, `filtered_candidate_count`, and `filter_reason`.

4. `caption_overlap` is currently a bare token count.
   It is useful but not enough. Add a normalized score (Jaccard or overlap ratio), figure-number agreement, and a reason if the score is below threshold.

## Method guidance

Caption-page filtering is acceptable as a prefilter, not as a batch-safe matcher by itself.

Known risk cases:

- multi-panel figures stored as multiple image XObjects;
- one caption page containing a table image, logo, inset, or unrelated XObject;
- multiple figures on the same PDF page;
- captions split across pages or placed before/after the image page;
- rasterized full pages where one image contains text + figure + caption together.

Batch gate recommendation:

- If `filtered_candidate_count != missing_ref_count`, mark manual.
- If multiple candidates share one figure-caption page, require contact-sheet review or page-crop logic.
- If figure numbers cannot be aligned from PDF captions and markdown refs, do not sequence-map silently.
- Seton 2012 should explicitly report raw count, filtered count, per-figure caption page, and any multi-image-per-caption cases.

## Bottom line

Pilot 1a is a good proof that B-prime can work, but the current artifacts are not yet batch-ready. Fix output-file hashing and produce the staged diff before using this path on Seton or the 50-paper batch.
