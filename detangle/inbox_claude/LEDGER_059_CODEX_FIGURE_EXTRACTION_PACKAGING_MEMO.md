# LEDGER_059 - Codex figure extraction packaging memo

## Status

MEMO / design guardrail. No corpus files were modified.

## Operator lesson

The Lee 2025 calibration paper exposed a structural failure in the current PDF-to-MD figure export:

- the Markdown body referenced Fig. 5 water-chemistry panels,
- the linked image file actually showed unrelated olivine/melt panels (`T(C)`, `Fo(olivine)`, `NiO(olivine)`),
- the whole figure block was inserted in the middle of an unrelated gas-origin paragraph,
- vision-derived "approximate data points" were rendered as if they were part of the article body.

The operator's original packaging preference was correct: **each PDF extraction should have been bundled into its own per-paper folder**, rather than letting images and derived blocks live in a shared/global artifact surface where cross-paper or cross-block image/caption drift can occur.

## Required future shape

For any future figure-enabled corpus export, treat each PDF as an isolated artifact bundle:

```text
paper_bundle/
  source.pdf                  # optional/local or pointer only, depending on policy
  article.md                  # text body
  figures/
    fig_001.image.ext
    fig_001.caption.txt
    fig_001.vision.json       # optional, quarantined unless verified
  tables/
  manifest.json               # paper_id, source_id, extraction_run_id, figure anchors
  audit/
    figure_alignment.json     # image/caption/body-anchor verification status
```

Hard rule: **no figure image, caption, or vision-derived table should be trusted unless it is tied to the same paper bundle and passes image-caption-anchor verification.**

## Immediate writing-system policy

Until a figure alignment checker exists:

- strip or quarantine Markdown blocks like `{n}---` followed by images,
- strip or quarantine `Figure X consists...`, `Approximate data points extracted...`, and derived figure tables,
- use article prose and real source tables only for prompt calibration and evidence retrieval,
- do not use figure-derived claims as evidence.

## Checker requirements before figures return to the corpus

A future checker should fail when:

1. an article image path resolves outside its paper bundle,
2. the figure number/caption text does not match the body reference anchor,
3. a figure block interrupts a sentence or paragraph continuation,
4. a vision-derived table is emitted into article body instead of a quarantined sidecar,
5. multiple papers share an image namespace without an explicit paper-local manifest.

## Coordination note

This is not a request to re-run extraction immediately. It is a durable guardrail for the next corpus/figure repair pass: **bundle first, then verify alignment, then expose figures to writing/retrieval.**
