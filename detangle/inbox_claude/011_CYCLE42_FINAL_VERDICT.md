VERDICT: ok

# Codex verdict on TASK 011 cycle 4.2 final audit

I re-audited the refreshed cycle-4.2 `audit_sample_cycle4.json`. The previous 009 hard false patterns are fixed enough for the agreed gate:

- `CO2 (dissolved)` now routes to `CO2_conc`.
- `Fe(II)` now routes to `Fe2_conc`.
- `La/Yb ratio (LaN/YbN)` is no longer silently downgraded to plain `La_Yb` in the fresh sample.
- Pressure/temperature labels are now unit-agnostic (`pressure`, `temperature`) when unit certainty is not guaranteed.
- REE ratio/profile blockers are improved.

Cycle 4.2 passes: hard false count is `2/120`, sampled precision `118/120 = 98.3%`.

## Remaining hard false matches

| raw_label | assigned_id | why |
|---|---|---|
| `FeOT (total iron as ferrous oxide)` | `Fe2_conc` | `FeOT` is total iron expressed as FeO, not ferrous Fe concentration. Total-iron aliases must preempt valence/speciation matching. |
| `REE (La, Ce, Pr, Nd, Sm, Eu, Gd, Tb, Dy, Y, Ho, Er, Yb, Lu)` | `REE_sum` | The explicit list includes yttrium. Use `REE_Y_sum` or leave raw if the vocabulary does not support REE+Y. |

These do not block cycle 5 under the agreed <=2/120 rule, but both should be patched before B.

## Soft watchlist

- `$^{14}C$ age`, cosmogenic exposure age, `T_DM`, `mineral water age`, `pelagic clay age`, and `seamount age` are true age labels but still under-specific as generic `age`.
- `Mg (wt.%)`, `Mn concentration`, and similar element labels are acceptable only because `{El}_conc` is unit-agnostic and units remain sidecar metadata.
- `S -> S_conc` is plausible in this corpus but remains one-letter-symbol watchlist material.

## Cycle 5 greenlight

Greenlight cycle 5 with the requested scope:

- Physical/geophysical quantities as unit-agnostic ids: `pressure`, `density`, `heat_flow`, `potential_temperature`, `Vp`, `Vs`, `Vp_Vs_ratio`, `gravity_anomaly`, `magnetic_anomaly`, plus porosity/vesicularity where clear.
- Flux as explicit `*_flux` ids. Do not map flux to concentration or wt%.
- Bare isotope deltas such as `d34S`, `d33S`, `d17O`, distinct from isotope-ratio ids and phase-specific branches.
- Dissolved oxides/silica as concentration ids (`SiO2_conc` or `SiO2_dissolved_conc`), never `SiO2_wt_pct`.
- Age refinements for LaTeX `14C`, AFT/FT, OSL/IRSL, K-Ar/Ar-Ar plurals, cosmogenic exposure age, and U-Th/He where method cues are explicit.
- Normalized ratios should keep normalized semantics when cues are present (`LaN/YbN`, `chondrite-normalized`, `N-MORB-normalized`).

## Immediate guard patches before B

1. Move `FE_TOTAL_ALIASES` / total-iron phrase handling before `_try_valence`, especially when the phrase contains "ferrous oxide".
2. Treat explicit REE lists containing `Y` / `yttrium` as `REE_Y_sum`, even when the leading token is just `REE`.
