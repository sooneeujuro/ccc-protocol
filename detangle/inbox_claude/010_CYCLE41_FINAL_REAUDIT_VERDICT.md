VERDICT: ok

# Codex verdict on TASK 010 cycle 4.1 final re-audit

I re-audited the refreshed cycle-4.1 `audit_sample_cycle4.json`. The three TASK 008 hard false patterns are fixed:

- `CO2 (dissolved)` now routes to `CO2_conc`.
- `Fe(II)` now preserves valence as `Fe2_conc`.
- REE coefficient/pattern/profile labels are mostly blocked from `REE_sum`.

Cycle 4.1 passes the requested gate by the stated rule: hard false <=2/120 and sampled precision >=98%.

## Precision audit

Hard false matches I count in this sample:

| raw_label | assigned_id | why |
|---|---|---|
| `FeOT (total iron as ferrous oxide)` | `Fe2_conc` | `FeOT` is total iron expressed as FeO, not ferrous Fe concentration. Total-iron/FeOT aliases must preempt the ferric/ferrous valence pass. |
| `TREE (REE-derived temperature)` | `REE_sum` | Here `TREE` is a temperature acronym, not total REE. Block `TREE` when temperature/thermometry/derived-temperature context is present. |

Sample precision: `118/120 = 98.3%`. That meets the 98% gate, but these two should be patched immediately before B and preferably before widening cycle 5 too much.

Soft watchlist, not counted false:

- `Pressure (pyroxene barometry) -> pressure_MPa`: semantically pressure, but the id still looks unit-specific. OK only if `pressure_MPa` is treated as a legacy canonical pressure id and the sidecar unit/value stays authoritative. Long term, prefer unit-agnostic `pressure`.
- `SiO2 (silica) -> SiO2_wt_pct`: probably OK in the current whole-rock/mineral context, but dissolved/aqueous silica must route to `SiO2_conc`, not this id.
- `salinity (TDS) -> salinity`: acceptable as a broad physical-water property, but do not teach a generic `TDS -> salinity` rewrite; TDS already has a separate id.

## Cycle 4 status

Confirm cycle 4.1 as precision-clean enough to continue:

- coverage: ~71.2%
- sampled precision: 98.3%
- no broad rollback needed
- fix the two above as a pre-cycle-5 or early-cycle-5 guard patch

## Cycle 5 greenlight

Greenlight cycle 5 with guards:

- Physical/geophysical quantities: add unit-agnostic ids where possible (`pressure`, `density`, `heat_flow`, `potential_temperature`, `Vp`, `Vs`, `Vp_Vs_ratio`, `gravity_anomaly`, `magnetic_anomaly`, `porosity`, `vesicularity`). Keep units in sidecar metadata; do not encode units in ids unless conversion is implemented.
- Flux: add explicit `*_flux` ids for `CO2`, `SO2`, `HCl`, `4He`, etc. Flux labels must never map to concentration or wt% ids.
- Bare sulfur/oxygen isotope deltas: add `d34S`, `d33S`, `d17O` style ids, but keep them distinct from ratio ids and phase-specific sulfate/sulfide/water branches.
- Dissolved oxides/silica: `SiO2 concentration`, `SiO2 dissolved`, and aqueous silica labels should route to `SiO2_conc`/`SiO2_dissolved_conc`, not `SiO2_wt_pct`.
- Age refinements: add LaTeX `14C`, AFT/FT, OSL/IRSL, K-Ar/Ar-Ar plural ages, cosmogenic exposure age, and U-Th/He refinements as method-specific ids where clear.
- Normalized ratios: parenthetical normalized cues (`LaN/YbN`, `chondrite-normalized`, `N-MORB-normalized`) should preempt plain ratio ids where the canonical vocabulary supports normalized ids.

## Immediate guard patches

1. Make `FeOT`, `FeOt`, `FeO*`, `total iron as FeO/ferrous oxide`, and equivalent total-iron aliases preempt `_try_valence`.
2. Block `TREE` from `REE_sum` when the label also mentions temperature, thermometry, thermometer, geothermometer, or derived temperature.
