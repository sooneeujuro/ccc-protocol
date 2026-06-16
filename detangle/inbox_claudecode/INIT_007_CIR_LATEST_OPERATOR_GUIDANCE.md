# INIT_007_CIR_LATEST_OPERATOR_GUIDANCE

Operator update for the CIR statistics paper-draft exercise.

## Context

Codex is continuing the CIR paper-draft/system-test work from the operator's
local unpublished CIR project.

- Source project: local unpublished CIR statistics folder supplied by operator.
- Codex run folder: local Codex CIR paper-draft run folder.
- Target repo worktree used for system tools: Codex evidence-demand worktree.

Do not copy raw unpublished tables, PDFs, figure source data, or local/private paths into CCCP notes. Coordination notes should stay sanitized.

## Latest Operator Guidance

1. Treat the existing figures as brainstorming-grade, not as proof.
   - Rebuild logic from data, statistics, provenance, and literature context.
   - It is acceptable if exploratory tests are imperfect, as long as false-green and false-red risks are explicitly recorded.

2. Run review-revision loops, not just one-pass drafting.
   - Decompose draft claims into evidence demands.
   - Check whether the current system gives a true structural signal or a misleading green/red.
   - Revise the draft toward safer claims after each critique.

3. Local LLM use is allowed for experimentation only.
   - `C:/Users/USER/Documents/LocalLLM` has Ollama/Gemma available.
   - Use local Gemma as a cheap auxiliary reviewer or style/logic critic, not as the source of scientific truth.
   - Frontier/primary reasoning should remain responsible for final judgment on methods, provenance, and claims.

4. Prioritize getting to a manuscript-writing-capable state.
   - Evidence-demand, reverse retrieval, claim-gap detection, and corpus sufficiency checks are more important than polishing dashboards or adding broad new infrastructure.
   - New corpus/source-discovery ideas should stay in additive, reversible ledgers unless explicitly promoted.

## Current Codex Findings To Compare Against

Codex has already produced a local CIR run with:

- `manuscript_draft_v2_revised.md`
- `claim_evidence_matrix.md`
- `CODEX_CIR_DRAFT_REPORT.md`
- `notes/cir_evidence_demand_v0.normalized.json`
- `notes/cir_retrieval_gap_probe_summary.md`
- second-pass figures/tables under the same run folder

Current scientific spine from Codex:

- Strongest support: north/south dVs contrast near the Song boundary, robust at sample and latitude-bin levels.
- Safer interpretation: thermal/geophysical structure, helium behavior, and enrichment/isotope signals are partly decoupled rather than one simple fossil-plume timeline.
- Keep as caveated: helium low window near `-18.4` to `-18.0` S, domain-dependent La/Sm meaning, and north-domain PCA.
- Avoid as main claims unless independently rescued: age-based fossil-plume timing, all-pool La/Sm-dVs partial correlations, and overconfident vent-fluid mismatch narrative.

## Suggested Claude Code Role

If you review this while Codex is running:

- Compare Codex's draft claims against the same local data and retrieved literature context.
- Flag any claim that depends mainly on a brainstorming figure or merged-table artifact.
- Look specifically for:
  - spatial autocorrelation / duplicated sample / source-dominance artifacts,
  - circular use of the target project as its own evidence,
  - claims needing external OA literature before manuscript use,
  - places where the evidence-demand system gives a false green or false red.

Please write a concise response under `detangle/inbox_codex/` if you find a blocking critique or a useful alternate structure. Otherwise a short read-only ACK is enough.
