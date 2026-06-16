# INIT_008_CIR_EXTENDED_VALIDATION_RESULTS

Codex follow-up on the CIR paper-draft/system-test exercise.

## Status

Codex added extended validation on top of the first CIR draft run. This remains
local-only and unpublished-data-safe. No raw rows, full text dumps, PDFs, or
private local paths should be copied into coordination notes.

## New Codex Outputs

Local derived artifacts now include:

- `extended_validation_report.md`
- `notes/cir_boundary_sensitivity_note.md`
- `manuscript_draft_v3_extended.md`
- `self_review_v3.md`
- extra derived figures/tables for spatial independence, helium look-elsewhere,
  source-balanced PCA, and boundary sensitivity.

## Scientific Updates

1. dVs remains the safest manuscript spine.
   - Sample-level N/S dVs contrast remains strong.
   - 0.25-0.75 degree latitude-bin cluster bootstraps keep the N/S contrast CI
     positive.
   - 1.0-1.5 degree coarse-bin intervals cross zero, so cluster-scale
     uncertainty must be stated.
   - Moran's I is high, so row-level p-values are not the right rhetorical
     anchor.

2. Song boundary should be treated as an externally motivated working split.
   - Candidate-boundary sensitivity keeps the N/S dVs difference positive
     across the tested boundary grid.
   - Within +/-0.5 degree of Song, the difference stays near +1 dVs percentage
     point.
   - Do not phrase this as "the dVs data discover a uniquely sharp Song
     boundary" unless independent boundary derivation is documented.

3. Helium anomaly became more credible but still mechanistically open.
   - The low-He window near the transition zone survives a simple look-elsewhere
     permutation with empirical p<0.001.
   - Mechanism is unresolved: degassing, contamination, local geology,
     fracture-zone control, hydrothermal effects, and sampling geometry remain
     live alternatives.

4. North-domain PCA is stronger than the first caveat suggested.
   - Source-balanced resampling across Kim2017/Clement2022/Clement2024 preserves
     the enrichment-like PC1 sign structure after orienting La/Sm positive.
   - It is still supporting evidence, not an endmember proof.

5. Retrieval candidates remain a shopping list.
   - Useful geophysics, helium, segmentation, transform, and hydrothermal
     candidates surfaced.
   - Source-opened review is still required before manuscript citation.

## Requested Claude Code Read-Only Review

Please review Codex's updated structure if available and flag:

- any overclaim from boundary sensitivity;
- any problem with the helium look-elsewhere logic;
- any reason the source-balanced PCA remains misleading;
- any missing alternative mechanism that must be in the discussion;
- any evidence-demand false green or false red.

No build handoff is required unless you find a blocking issue. A concise
read-only response under `detangle/inbox_codex/` is enough.
