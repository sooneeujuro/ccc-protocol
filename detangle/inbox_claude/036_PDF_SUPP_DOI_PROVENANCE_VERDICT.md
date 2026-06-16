# 036 PDF/Supp + DOI provenance verifier verdict

VERDICT: issues_found

Scope checked: `036_PDF_SUPP_GATHER_DOI_PROVENANCE.md`, committed reports/scripts through `890a445`, plus local copy targets `G:\corpus_pdfs` and `G:\corpus_supplementary`.

## OK

- WS2 copy counts verify independently:
  - `G:\corpus_pdfs`: 3,665 PDFs, 13,746,644,205 bytes, exactly the matched corpus stems; no extra/missing matched stems found.
  - Corpus markdown stems: 3,852; matched PDFs: 3,665; corpus without PDF: 187.
  - `G:\corpus_supplementary`: 41 matched folders, 162 files, 221,513,037 bytes. Ambiguous 9 and nomatch 13 were not silently copied into corpus-named destinations.
- DOI-first provenance is the right direction and much better than filename-only fuzzy matching.
- The 660 candidate PDF basenames used by `DOI_PROVENANCE_MATCH.json` reproduce from `CORPUS_GAP_REPORT.json`, and the reported headline counts reproduce: DOI duplicate 209, title duplicate 255, genuinely_new 187, undetermined_no_text 9.

## Issues to fix before using the 187 as a final action list

1. Denominator drift is confusing and should be made explicit.
   - `PDF_CORPUS_MAP.stats.pdf_without_corpus = 741`, but `CORPUS_GAP_REPORT.n741_pdf_no_corpus` contains 660 basenames.
   - This appears explainable: 741 is raw unmatched unique-normalized PDF keys, while 660 is after duplicate/prefix collapse for candidate provenance. Please rename the key or add both denominators with definitions so later agents do not treat them as contradictory.

2. `dup_by_title = 255` is not sufficiently auditable yet.
   - Current JSON does not record the matched corpus md/title/sidecar DOI/evidence for each title duplicate, so false positives cannot be reviewed without rerunning enrichment.
   - At least one real false-positive pattern exists: Baker & Haggerty Part II can match the corpus Part I title prefix because the first 50 normalized title characters are shared.
   - Please emit for every title match: orphan basename, extracted DOI if any, matched corpus md, matched corpus title, corpus DOI, similarity score, and whether multiple corpus prefixes matched.

3. Title fallback should be demoted or tightened when PDF DOI is present but absent from corpus DOI set.
   - Many title matches are likely valid duplicates with blank corpus sidecar DOI, but a DOI-present/title-prefix-only match should be `probable_duplicate_title`, not hard duplicate, unless full-title similarity is high and no series/part/chapter ambiguity is detected.
   - Please add guardrails for `part`, roman numerals, chapter/series subtitles, and ambiguous prefix collisions.

4. The 187 `genuinely_new` list needs subtype splitting before any Datalab/corpus decision.
   - Samples include journal articles, books, book chapters, theses, reports, and reference schemes.
   - Please split at minimum: `journal_article`, `book`, `chapter`, `thesis`, `report`, `unknown`, and keep relevance/source evidence. Do not send the whole 187 to paid conversion as one homogeneous paper batch.

5. `PDF_ORPHAN_CLASSIFY.json` conflicts with DOI provenance and should not be treated as canonical.
   - It reports `new_relevant = 475` and includes several items that DOI/title provenance treats as duplicates.
   - Please label it exploratory/superseded or reconcile it with `DOI_PROVENANCE_MATCH.json`.

## Gate

No objection to the copied PDF/supp layout as a local non-git working library. Do not proceed from the 187/255 provenance buckets to paid Datalab conversion or corpus promotion until the above evidence fields and subtype split are added.
