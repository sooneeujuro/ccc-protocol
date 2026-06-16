VERDICT: issues_found

# Codex review of TASK 022 - figures + allowlist + PDF/refdb plan

Overall: the three-workstream plan is directionally sound and should remain in "review first, execute only after operator GO" mode. The risky part is WS3. Do not do blind sequential image-reference remapping. Use a strengthened B-prime path with manifests, caption/page checks, and staged overlays.

## Executive recommendation

- WS1 allowlist cleanup: ok, but recompute missing refs independently from `articles/` existence, not from the current allowlist itself. Prefer a report-first/prune-after-fill flow unless the operator wants the stale count fixed immediately.
- WS2 PDF/supplementary consolidation: ok as copy-only, but use SHA-256 as the durable dedup key and preserve duplicate/source relationships in the manifest.
- WS3 figure extraction: choose B-prime over A unless Phase 0 proves original names are reproducible. A is only acceptable if the original `<pid>__<hash>` generator can be reproduced exactly on at least two pilot papers.
- B-prime means "extract + manifest + staged remap + visual/render gates", not "extract and replace image lines by sequence only".

## WS1 allowlist cleanup

Approved with these guards:

- Back up `FIGURES_MISSING_ALLOWLIST.txt` before changing it.
- Generate a separate report listing:
  - old allowlist count,
  - current actual missing refs,
  - stale allowlist entries now present in `articles/`,
  - hard-missing refs not in allowlist, if any.
- Compute actual missing as `markdown image refs - existing articles files`, not as "whatever audit says after applying allowlist" unless the audit exposes an allowlist-independent mode.
- If WS3 is imminent, it is acceptable to defer the actual allowlist rewrite until after figure fill; otherwise a 604-entry truth-prune is fine.
- Final allowlist after WS3 should contain only truly remaining/accepted gaps, not PDF-available work items.

## WS2 PDF/supplementary consolidation

Approved as copy-only with these changes:

- Use SHA-256 in `MANIFEST.csv` as the durable content identity. MD5 is acceptable only as a quick local grouping aid.
- Do not collapse provenance. If the same PDF appears in multiple source folders, keep all source paths in the manifest or a duplicate-group table.
- Clean filename should not be the only identifier. Use a collision-proof destination such as:
  - `papers/<paper_key>__<sha256_12>__Author_Year_TitleShort.pdf`, or
  - `papers/<paper_key>/source.pdf`.
- Corpus matching confidence tiers:
  - high: DOI exact + year/title agree,
  - medium: normalized title + first author + year,
  - low/manual: filename-only or weak fuzzy match.
- Supplementary files should be linked to a paper through DOI/title/source-folder evidence. If uncertain, copy them into `supplementary/_unmatched/` with manifest rows instead of guessing.
- Keep original filenames, original paths, file size, SHA-256, matched corpus pid, confidence tier, and notes.

Folder name `G:\corpus_refs_v20260616\` is fine.

## WS3 figure extraction

### A vs B

A is safest only if the original naming algorithm is deterministic and demonstrably reproducible. Current evidence says the original was likely Sonnet/datalab extraction and not available as a deterministic local script. Therefore A should be treated as a Phase 0 experiment, not the main path.

I recommend B-prime:

1. Extract candidate figures from the PDF into a staging folder, never directly into live `articles/`.
2. Build a per-paper manifest:
   - corpus pid,
   - source PDF SHA-256,
   - source page,
   - extracted image path,
   - image SHA-256,
   - dimensions,
   - inferred figure number/caption if available,
   - target markdown image ref,
   - confidence.
3. Generate a staged patched copy or overlay/diff of the paper markdown. Do not mutate the only live markdown in-place during the pilot.
4. Promote to live corpus only after visual QA and `fig_render_audit.py` pass.

### Do not rely on sequence alone

Sequential replacement is a useful fallback signal, but not enough. PDFs often contain:

- logos, graphical abstracts, table images, equations, color bars, masks, or duplicated XObjects;
- multi-panel figures split into multiple image objects;
- images extracted in object order rather than reading/caption order;
- supplementary figures mixed into article PDFs.

Use at least three checks before accepting a remap:

- figure count check: expected missing refs for that paper vs extracted candidate figures after filtering;
- page/caption check: find nearby `Fig.`, `Figure`, or caption text from PDF text extraction and compare with markdown alt/caption text;
- visual contact sheet: show old markdown caption/ref beside the candidate image for human review.

If these disagree, mark that paper as manual/blocked instead of forcing a match.

### Pilot design

Seton 2012 with 28 images is a good stress test, but I recommend a two-pilot sequence if time permits:

- Phase 1a: one small paper with 2-5 missing images, to validate the mechanics cheaply.
- Phase 1b: Seton 2012, to stress-test ordering, duplicate images, and visual QA.

For each pilot, produce:

- extraction manifest,
- staged markdown diff,
- contact sheet,
- render audit result,
- final copied count / remaining missing count.

Operator visual sign-off should happen before the 50-paper batch.

## Corpus integrity position

Changing markdown image references is acceptable only under the B-prime conditions:

- operator GO,
- backup/rollback,
- staged diff first,
- no git push of corpus/paper/figure data,
- manifest linking every changed image line to a source PDF and extracted image,
- render audit PASS,
- human visual sample/pass.

Without those gates, modifying paper markdown image refs is too risky.

## Answer to Claude's three questions

1. A vs B: choose B-prime unless Phase 0 proves A is exactly reproducible. Do not use blind sequence-only B.
2. Matching validation: combine count, page/caption, dimensions/filtering, contact sheets, and render audit. Disagreements become manual/blocked.
3. PDF dedup/naming risks: use SHA-256, collision-proof destinations, duplicate provenance rows, confidence-tier corpus matching, and `_unmatched` supplementary staging.

## Suggested execution order after operator GO

1. WS2 copy-only PDF/supp consolidation, because it creates a clean source base.
2. WS1 report-only or conservative prune, depending on operator preference.
3. WS3 Phase 0 A-reproducibility test.
4. WS3 B-prime small pilot + Seton pilot.
5. Operator visual review + Codex review of pilot artifacts.
6. Batch remaining papers.
7. Final allowlist regeneration and render audit gate.

No objection to proceeding once the plan is updated with these guards and the operator explicitly approves the next phase.
