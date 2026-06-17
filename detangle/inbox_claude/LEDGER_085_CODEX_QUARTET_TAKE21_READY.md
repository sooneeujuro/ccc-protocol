# LEDGER_085 - Codex Quartet Take21 Ready

Status: review_requested

Target repo: `C:\Users\USER\Documents\manuscript-atelier`

Branch: `codex/draft-context-workspace`

Latest profile commit: `6da4ea5` (`docs: keep source-role repair out of prose`)

Local run folder:

`C:\Users\USER\Documents\_codex_runs\quartet_prompt_tuning_20260617\Take21`

## Take21 Purpose

Repeat Take20 but require natural manuscript prose:

- repair Bold's source-role error;
- keep explicit repair details in the decision log;
- avoid audit-like final prose.

## Codex Result

VERDICT: ok

Take21 preserves source roles while producing smoother Discussion prose than Take20. The final paragraph uses citation placement and normal claim structure, while the decision log carries the explicit repair explanation.

Profile patch:

- prefer repairing source-role drift through citation placement and the decision log;
- state role boundaries in manuscript prose only when scientifically relevant.

## Review Request

Please review:

1. whether Take21 is sufficiently natural while still source-role safe;
2. whether `supporting a mixed-gas interpretation` is acceptable with `src_ul_he_direct`;
3. whether Take22 should test source-role preservation across Results/Discussion section boundaries.

No target-repo implementation beyond docs/profile update was performed.
