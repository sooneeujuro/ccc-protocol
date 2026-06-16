VERDICT: issues_found

# Codex verdict on TASK 028 Seton pilot / region mode

Reviewed `G:\fig_rebuild_v20260616\359cf721d5fa\` for Seton 2012.

## What improved

- The saved-file hash issue from 027 is fixed for the current manifest: `output_file_sha256` matches the actual saved JPG bytes for manifest rows checked.
- `staged_md.diff.txt` and `staged.md` now exist.
- Current manifest has 28 rows and reports `filtered_candidate_count=28`, `missing_ref_count=28`, `count_match=True`.
- Contact sheet shows many real plate-reconstruction figures, and region rendering avoids the embedded-XObject over-extraction failure mode.

## Blocking issues

1. Sequence mapping is wrong for Seton.

   The staged diff maps the first two region-rendered figures onto non-figure old references:

   - line 3 old ref alt: `Elsevier logo featuring a tree...`
   - line 7 old ref alt: `Cover image of Earth-Science Reviews journal...`

   These are being replaced by region-rendered scientific figures. That means `28 == 28` is a false positive: the counts match, but the semantic alignment is shifted.

2. Figure-number agreement fails for nearly all rows.

   Independent manifest check:

   - rows: 28
   - `fig_no_agree=True`: 2
   - `fig_no_agree=False`: 26
   - `caption_jaccard=0.0`: 10 rows
   - all rows currently marked `auto-ok`

   This is not safe for automatic promotion. Rows with figure-number disagreement or near-zero caption overlap must be `MANUAL`, not `auto-ok`.

3. The per-paper staging folder contains stale orphan images.

   Current folder state:

   - JPG files total: 90
   - JPGs referenced by current manifest: 28
   - orphan JPGs: 62

   These appear to be earlier embedded-mode outputs left in place. The staging folder must be cleaned or versioned per run before review, otherwise contact sheets, human inspection, and later promotion can pick up stale artifacts.

4. Region crops include large body-text margins.

   Contact sheet confirms that many region images include surrounding article text, not just figure panels/captions. This may be acceptable as a temporary visual pilot, but not as final corpus image quality without tighter crop rules or a higher-quality conversion path.

## Required fixes before batch

- Exclude non-figure old refs from replacement candidates unless explicitly intended:
  - publisher logos
  - journal cover art
  - headers/banners
  - any old alt without figure/table identity
- Match by figure identity, not sequence alone:
  - parse old markdown alt for `Figure N` / `Fig. N`;
  - parse PDF caption `Fig. N`;
  - require figure-number agreement when both are available;
  - if old alt has no figure number, do not auto-map it to a numbered PDF figure.
- Make `status=MANUAL` when:
  - `fig_no_agree=False`;
  - caption overlap is below threshold;
  - old ref is logo/cover/non-figure;
  - crop includes substantial body text and no tight-crop proof exists.
- Clean the per-paper output directory before each run, or write into run-specific subfolders such as `embedded_YYYYMMDDHHMM` and `region_YYYYMMDDHHMM`.
- Do not run or commit batch automation until this Seton mismatch is fixed.

## Datalab recommendation

Given the operator's quality-first direction, Seton 2012 is a strong candidate for a Datalab `accurate` pilot before scaling. Region mode is useful as a local fallback/baseline, but this paper demonstrates why count-based local automation is not quality-conservative enough by itself.

Recommended next step:

1. Run Datalab accurate on Seton, preserving images/captions/page metadata.
2. Compare Datalab output against the current local region output with a contact sheet and staged diff.
3. Choose the route with fewer semantic alignment errors, not the cheaper route.

Bottom line: region mode is promising for extracting visible figures, but Seton pilot is not safe for auto promotion or 50-paper batch yet.
