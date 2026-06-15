VERDICT: ok

# Codex verdict on TASK 013 ceiling and FINAL proposal

I agree with the ceiling call. Cycle 6 is precision-clean enough, and the coverage curve has flattened enough that forcing 90% would likely damage sidecar quality.

## Cycle 6 audit

I audited `audit_sample_cycle6.json`. I count one hard false in the sample:

| raw_label | assigned_id | why |
|---|---|---|
| `FeO_total` | `Fe_total_conc` | This is total Fe expressed as FeO / an oxide-form total, so it should stay with the total-iron oxide family (`Fe_total_oxide_wt_pct`) unless context proves elemental total Fe. |

Sample precision estimate: `119/120 = 99.2%`, so cycle 6 passes the precision gate.

Soft watchlist:

- `CO2 (carbon dioxide) -> CO2_wt` is acceptable only under the established "bare CO2 defaults to volatile wt%" rule. Keep CO2 phase/unit probes in the regression set.
- `Re depletion model age -> age` is semantically true but should become method-specific where possible.
- `δ17O(O2/H2O) -> d17O` is a true isotope variable but phase/material detail is not represented.

## Ceiling agreement

Approve `74.8%` as the honest precision-safe ceiling for this night run.

Rationale:

- Coverage trajectory has flattened: `12.9 -> 47.3 -> 56.1 -> 62.1 -> 71.2 -> 72.6 -> 73.3 -> 74.3 -> 74.8%`.
- Cycle 6 added less than 1 percentage point despite targeted cleanup.
- Remaining unmatched is mostly high-unique tail, blocked semantic groups, phase-ambiguous labels, formula/model labels, and OCR/singleton material.
- Reaching 90% would require matching most of the remaining tail, which would violate the precision-first rule.

I agree with reporting both:

- raw all-entry coverage: `74.8%`
- adjusted normalizable-denominator coverage: about `79.1%`, if junk and intentionally blocked groups are excluded as documented

## FINAL_SUMMARY approval

Approve Claude writing `FINAL_SUMMARY` and stopping the 5-minute loop after it is posted, with B/sidecar write, PR merge, and ceiling acceptance left to the operator.

Please include these in FINAL:

- Full trajectory and layer counts through cycle 6.
- Sample precision history and the final `119/120` audit result.
- Regression probe set:
  - FeOT / FeO_total / total iron as FeO
  - REE+Y explicit lists
  - TREE as temperature acronym
  - CO2 dissolved / mmol-mol / phase variants
  - F(ppm) / F- / F as fraction collision
  - Fe-valence and Fe-valence ratios
  - 3H/3He age
  - Age-grid misfit
  - P(CO2) / P(CO₂) partial pressure
  - Pressure(GPa) unit-agnostic handling
  - LaN/YbN and normalized-ratio cues
- Tail characterization table and strict junk filter rule.
- A note that corpus/sidecars were not written, pushed, or modified.
- A pre-B sanity check: explain why `Nd` and `Na` appear in cycle-6 `top_unmatched` despite simple element rules. If it is a report artifact, document it; if it is a real matcher miss, patch it before B. It is not a path to 90%, but it is visible enough that the operator will notice.

## Junk-tail rule

Final agreement:

- Exclude only structural blank/junk labels from the denominator (`" "`, newline-only, quote-only, `not measured`, `n.d.`, etc.).
- Keep semantic-but-bad labels in the denominator as raw/blocked with reasons.
- Do not force-match singleton/OCR/phase-ambiguous labels to chase the original 90% target.
