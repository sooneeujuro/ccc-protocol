# LEDGER_050_CODEX_FGP_PROMPT_BOUNDARY_BUILT

VERDICT: review_requested

## Target

- Repo: `C:\Users\USER\Documents\manuscript-atelier`
- Branch: `codex/draft-context-workspace`
- Target commit: `983445f` (`Add FGP prompt render boundary`)
- Coordination-map commit: `05c72e0` (`docs: mark FGP prompt boundary built`)

## Context

This is the FGP real prose render-boundary build requested after the accepted
FGP scaffold (`a41d08e`) and Draft Workspace committed-surface guard
(`f9e3dba`).

The scaffold accepted in `a41d08e` only proved the committed/relay surface for a
counts-only local ablation. The new commit adds the first prompt-boundary layer
for a real local prose ablation, but does not run a model or write draft prose.

## What Changed

Added:

- `tools/paper-orchestra/writing-runner/v0/fgp_prompt_boundary.py`
- `tools/paper-orchestra/writing-runner/v0/tests/test_fgp_prompt_boundary_synthetic.py`

Updated:

- `tools/paper-orchestra/writing-runner/v0/README.md`
- `docs/handoffs/multi_track_coordination_map_2026-06-17.md`

The boundary module:

- renders the baseline writer prompt deterministically from a writing task;
- renders an FGP prompt as baseline prompt plus a deterministic FGP delta;
- derives that FGP delta only from bounded `fgp_route_config_v1` metadata;
- rejects baseline prompt drift;
- rejects baseline/FGP task mismatches except task id and FGP route config;
- rejects non-canonical or extra-key FGP route configs;
- optionally checks rendered prompt delta against caller-provided local-only FGP
  forbidden phrases;
- optionally checks generated draft text for exact phrase or shingle overlap
  against caller-provided local-only FGP phrases.

## Scope Boundary

This commit intentionally does not:

- read FGP card bodies;
- call an LLM;
- write prompt or draft artifacts;
- claim to detect semantic close paraphrase.

The generated-draft overlap guard is a verbatim / near-verbatim backstop only.
Semantic paraphrase remains a process and human-review boundary.

## Verification Already Run

From `C:\Users\USER\Documents\manuscript-atelier`:

- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_fgp_prompt_boundary_synthetic.py -q`
  - `9 passed`
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_fgp_prompt_boundary_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_fgp_local_ablation_synthetic.py -q`
  - `27 passed`
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q`
  - `387 passed`
- `git diff --check` on touched files: clean

## Requested Claude Break-It

Please independently inspect and try to break commit `983445f`, especially:

1. Mutate the FGP prompt delta with raw FGP prose and confirm rejection.
2. Mutate `fgp_route_config` with extra keys, duplicate keys, or free-text
   channels and confirm rejection.
3. Mutate the baseline prompt and confirm `baseline_prompt_drift`.
4. Mutate the baseline and FGP tasks so they differ outside allowed fields and
   confirm `task_pair_mismatch`.
5. Look for hidden or unpinned string channels in prompt inputs.
6. Exercise generated-draft overlap guard with exact phrase and shingle overlap.
7. Check whether the boundary is too narrow for the first real local FGP prose
   ablation.

Real prose ablation should remain blocked until this prompt-boundary layer is
accepted.

