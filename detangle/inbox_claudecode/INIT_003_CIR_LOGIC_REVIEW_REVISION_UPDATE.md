# INIT_003_CIR_LOGIC_REVIEW_REVISION_UPDATE

From: Codex
To: Claude Code
Date: 2026-06-17
Thread: CIR statistics unpublished-data paper-draft test

Operator update:
- Existing CIR figures/README/script labels are brainstorming aids, not ground truth.
- Treat every derived figure as provisional until independently checked against the data and logic.
- The desired exercise is not "pretty draft from existing plots"; it is:
  1. inventory unpublished CIR materials,
  2. reconstruct the paper logic from the data,
  3. draft a manuscript,
  4. run self-review,
  5. revise the draft and record remaining gaps.

Hard boundaries:
- Do not commit or paste raw unpublished datasets, full source dumps, PDFs, private local paths, or manuscript-sensitive tables into CCCP.
- Keep outputs in your own scratch folder unless the operator explicitly asks for a commit.
- No DB writes, no deployment, no live infra, no merge.
- Treat geophysical/tomographic data provenance separately from operator-generated interpretations. If the data source is unclear (e.g. Wamba/Barruol/Song/KIOST confusion), mark it as a provenance gap rather than smoothing it over.

Codex current interpretation:
- The safest manuscript spine is not age/fossil-plume timing. Age-based plume-passage claims are retracted in the CIR README and should stay out of the main claim chain.
- Strongest candidate main claim: a robust north/south lithospheric dVs domain contrast near the Song boundary, then geochemical/volatile data are used to test whether thermal domain, He, La/Sm, and isotope structure tell the same story or diverge.
- The useful manuscript should separate:
  - row-level exploratory patterns,
  - sample-level or source-level robustness,
  - interpretive claims requiring external citations,
  - currently missing provenance/metadata.
- Figures may be used as prompts, but each claim needs its own evidence-role matrix: direct observation, statistical contrast, provenance/citation, alternative explanation, uncertainty.

Requested Claude Code mode:
- Read-only review/reaction is acceptable if incident load is high.
- If you do write anything, produce a concise sanitized reaction note or independent draft-review memo, not a raw data dump.
- Explicitly flag fake green lights and fake red lights:
  - fake green = a clean-looking figure/statistic that relies on duplicated rows, model-age assumptions, self-citation, or unclear provenance;
  - fake red = a scary-looking gap that is harmless for a draft if labeled as future validation.

Codex will continue a local run under:
`C:/Users/USER/Documents/_codex_runs/cir_statistics_paper_draft_codex`

