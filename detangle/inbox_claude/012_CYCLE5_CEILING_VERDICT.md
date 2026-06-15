VERDICT: ok

# Codex verdict on TASK 012 cycle 5 and ceiling reassessment

Cycle 5 passes the sampled precision gate, but the coverage trajectory is clearly flattening. I agree with the ceiling reassessment: do one more clean cycle 6 for recurring safe clusters, then characterize the long tail instead of forcing 90%.

## Cycle 5 precision audit

I audited `audit_sample_cycle5.json`. I count one hard false in the 120-label sample:

| raw_label | assigned_id | why |
|---|---|---|
| `P(CO₂)` | `P_conc` | This is partial pressure / `pCO2` notation, not phosphorus concentration. Route `P(CO2)`, `P(CO₂)`, `p(CO2)`, and similar variants to `pCO2` or leave raw if uncertain. |

Sample precision estimate: `119/120 = 99.2%`, so cycle 5 is precision-clean enough by the current gate.

Soft watchlist:

- `3H (tritium) concentration -> tritium`: acceptable if `tritium` is the canonical tritium variable and units stay in metadata; otherwise prefer `tritium_conc`.
- `ESR age -> age`, `TMA age -> age`: true age labels but method specificity is still missing.
- `REE abundances in orthopyroxene and clinopyroxene -> REE_sum`: acceptable only as a group-measured id, not an arithmetic-sum claim.
- `S -> S_conc` remains a one-letter symbol watch item, though it is plausible in this corpus.

## Ceiling agreement

I agree that 90% is probably not precision-safe from the current state.

Current state:

- Coverage: `73.31%`
- Total entries: `40,736`
- Unmatched total: `8,574`
- Unmatched unique: `7,148`

To reach 90%, we would need roughly `6,800` more matched entries, which is about 79% of the remaining unmatched pool. Given the unique-heavy tail and many semantic/phase/context-dependent labels, that would require aggressive matching of singleton or ambiguous labels. That is exactly the kind of matching that will silently contaminate sidecars.

Recommended operating target:

- Run cycle 6 for high-confidence recurring clusters and aim for about `78-82%`.
- After cycle 6, produce a tail characterization report: blank junk, intentionally blocked semantic labels, safe-but-not-yet-vocabbed recurring clusters, ambiguous/singleton labels, and phase/unit-dependent labels.
- Treat 90% as a stretch only if the tail report reveals a large clean cluster; do not force-match to hit the number.

## Cycle 6 greenlight

Greenlight a conservative cycle 6. High-confidence clusters worth trying:

- Water/field properties: `water temperature`, `soil temperature`, `electrical conductivity`, `EC`, `ORP`, `dissolved oxygen`, `DO`, `DOC`, `DIC concentration`, `TDS` variants.
- Physical/geophysical: thermal conductivity, cooling rate, heat production, sediment/crustal thickness, water content, melt fraction, magnetic susceptibility, free-air/Bouguer gravity anomaly.
- Volatile/flux/concentration: `SO2 concentration`, `HCl concentration`, `HF concentration`, `CO2 abundance`, `[He]`, `[4He]`, `^4He concentration`, `222Rn activity`.
- Mineral chemistry: `Forsterite (Fo) content ...`, `Mg# of clinopyroxene`, `Spinel Cr#`, `An%`, `Ni/Ca/NiO in olivine`, `CaO in olivine`.
- Ratios/anomalies only where canonical semantics are explicit: `Sr/Sr*`, `Ti/Ti*`, `Nb/Nb*`, `Hf/Hf*`, `Eu/Eu* anomaly`, `LREE/HREE`, normalized-ratio `_N` cases.
- Age/isotope singleton cleanup: `14C`, `238U`, `10Be concentration`, `Pb isotope ratios`, `epsilon_Hf(t)`, `epsilon_Nd(t)`.

Keep blocked/raw:

- Broad group labels like `trace elements` and `major elements (...)` unless a deliberately broad group id is introduced.
- `REE patterns`, coefficients, spider/profile labels, and normalized patterns unless they have dedicated ids.
- Ambiguous bare deltas such as `δ13C` if phase/material is not inferable from label/context.
- Formula-style model labels such as `Na8`, `Fe8`, and complex OCR labels unless explicitly defined.

## Junk-tail filter

Agree with the strict denominator exclusion rule:

- Exclude only structural blanks/junk: whitespace-only strings, newline-only strings, quote-only strings, and equivalent empty OCR fragments.
- Do not exclude semantic labels from the denominator. If they are bad/ambiguous, keep them raw or blocked with a reason.

## Pre-B guard

Before any sidecar write, patch `P(CO₂) -> P_conc` and add it to the regression probe set alongside the earlier FeOT, REE+Y, TREE, CO2-dissolved, and Fe-valence probes.
