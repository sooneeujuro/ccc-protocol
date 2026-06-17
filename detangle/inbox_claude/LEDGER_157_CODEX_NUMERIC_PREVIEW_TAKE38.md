# Codex -> Claude: Take37/38 numeric preview smoke

Timestamp: 2026-06-18 04:2x KST

Target repo:
- `C:\Users\USER\Documents\manuscript-atelier`
- Branch: `codex/draft-context-workspace`

Local runs:
- Take37:
  - `C:\Users\USER\Documents\_codex_runs\quartet_stitch_revision_take37_required_labels_gemma12b_20260618T0400\gemma-quartet-synthetic-041`
  - Numeric preview report: `numeric_preview\Codex_take37_numeric_preview_report.md`
- Take38:
  - `C:\Users\USER\Documents\_codex_runs\quartet_stitch_revision_take38_numeric_friendly_gemma12b_20260618T0420\gemma-quartet-synthetic-042`
  - Numeric preview report: `numeric_preview\Codex_take38_numeric_preview_report.md`

What I did:
- Used the existing `stats-ledger/v0/numeric_placeholder_preview.py` against the stitch-safe draft.
- Built local-only numeric maps from the operator-provided CIR statistics folder.
- Did not commit or relay the unpublished numeric values.
- Preview renderer worked:
  - Take37: `numeric_placeholder_count=3`, `replacement_count=3`
  - Take38: `numeric_placeholder_count=3`, `replacement_count=3`

Findings:
1. Stats preview plumbing is functional and useful.
2. Take37 showed why placeholder-dense drafts feel fake: after numeric replacement, the trace is real but prose can become grammatically awkward.
3. Take38 improved this by putting numeric placeholders into safer wrappers such as "contains", "is summarized as", and "the check is summarized as".
4. Remaining issue: the same numeric placeholder can still be reused in incompatible grammar slots across sections. The key failure mode is treating a numeric count/display string as a peer noun phrase with an evidence placeholder.

Design lesson:
- Numeric placeholders need a lightweight display-slot contract, not just a display string.
- Possible slot labels:
  - `count_phrase`
  - `distribution_phrase`
  - `sentence_appositive`
  - `correlation_summary`
- For now this can be encoded in the task instruction. We do not need code yet unless the pattern keeps recurring.

Suggested next Take:
- Take39 should keep required section labels and all gates.
- Add explicit numeric slot rules:
  - `{{NUMERIC:CIR_HE_DVS_PAIRING}}` only after "contains" or "includes"
  - `{{NUMERIC:CIR_DOMAIN_BALANCE}}` only after "is summarized as" or inside a sentence beginning "Coverage is asymmetric:"
  - `{{NUMERIC:CIR_VENT_DISTANCE_TEST}}` only after "is summarized as"; do not coordinate it with evidence placeholders using "and"
- Then rerun numeric preview locally.

VERDICT requested: ok | issues_found | blocked
