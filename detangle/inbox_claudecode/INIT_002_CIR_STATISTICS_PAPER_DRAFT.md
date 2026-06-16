# INIT_002 — Codex → Claude Code: CIR Statistics Paper Draft Independent Pass

Date: 2026-06-17

Operator request: use the unpublished/local materials in `G:\260518_CIR_Statistics` to explore whether we can draft a manuscript from the data. Codex is starting one independent pass; Claude Code should run a separate pass in its own scratch and leave reactions/review notes.

Primary local data root:

- `G:\260518_CIR_Statistics`

Suggested scratch/output root:

- Claude Code: `C:\Users\USER\Documents\_claudecode_runs\cir_statistics_paper_draft`
- Codex will use its own run folder and must not overwrite yours.

Hard gates:

- Do not commit or push unpublished raw data, derived data tables, private figures, PDFs, local paths, or full source dumps.
- Do not push corpus/paper/sidecar/index/wiki/figure data.
- No live infra changes, DB writes, deployments, or irreversible actions.
- No merge.
- Treat Wamba/geophysical-source material as requiring attribution and source separation. If a claim depends on Wamba data or a Wamba paper, mark it explicitly as source-dependent rather than laundering it as new operator data.

Requested Claude Code role:

1. Independently inventory the folder structure and identify data types.
2. Do not start by writing prose. First derive:
   - possible research question(s),
   - available variables,
   - provenance/rights/attribution boundaries,
   - reproducible figures/tables,
   - missing metadata.
3. Then attempt a paper skeleton/draft only from what is supportable.
4. Record fake-green/fake-red risks:
   - figures that look plausible but lack metadata,
   - correlations without units/coordinate reference/time range,
   - source mixing between operator data and Wamba-derived data,
   - private paths or unpublished material leaking into committed notes.
5. Leave a concise review/reaction note in coordination, not a raw draft dump.

Codex intended output:

- Local-only run artifacts under a private run folder.
- A committed high-level report may be added to the target repo only if it contains no raw unpublished data, no local paths, and no full paper text.
- If a manuscript draft is generated, keep it local-only unless the operator asks to commit it.

Goal:

Assess whether the current paper-orchestra/evidence-demand/retrieval discipline can support a new manuscript from local unpublished data without the Kim-2024 self-source trap, and identify the next engineering/data-cleanup steps needed to make the draft reproducible.
