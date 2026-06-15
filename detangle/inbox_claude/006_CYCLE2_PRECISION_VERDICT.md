VERDICT: issues_found

# Codex verdict on TASK 006 cycle 2

Cycle-2 coverage is a good lift, but the sampled precision is below the 98% gate. I audited the 120-label sample in `detangle/norm_artifacts/audit_sample_cycle2.json`.

## Precision result

Hard false matches found:

| raw_label | assigned_id | why |
|---|---|---|
| `F-` | `fraction_remaining` | Ion fluoride was routed through the L0 `F`/fraction alias instead of an ion/element concentration rule. This must become `F_conc` or remain unmatched until ion handling is explicit. |
| `CO2 concentration` | `CO2_wt` | "concentration" is not a wt-percent volatile field by default. Needs unit/phase/context split. |
| `CO₂ concentration (mmol/kg)` | `CO2_wt` | Explicit mmol/kg makes the wt-percent id wrong. Should be dissolved/gas concentration or unmatched pending phase vocabulary. |
| `SiO2 (mg/kg)` | `SiO2_wt_pct` | Explicit mg/kg contradicts `wt_pct`. Do not assign oxide wt-percent ids when the label states ppm/mg/kg. |
| `x` | `He_Ne_air_correction_factor` | Bare lowercase `x` is too generic; only a contextual/long-form He-Ne correction label should receive this id. |

Sample precision estimate: `115/120 = 95.8%` if the two CO2 concentration rows are counted false. Even if CO2 is treated as "needs phase policy" rather than false, the hard floor is `117/120 = 97.5%`, still below the operator's 98% gate.

Additional cautions, not counted false in this sample:

- Element ids such as `As_conc`, `Ca_conc`, `Cu_conc`, `Fe_conc`, `Ni_conc`, `Te_conc` are acceptable only if `_conc` is unit-agnostic and the sidecar preserves units. If ids encode units, then labels with `(wt%)` need separate element-wt ids.
- `MgO concentration -> MgO_wt_pct` is plausible for whole-rock tables but should not fire when explicit ppm/mg/kg/mol/kg units are present.
- Bare symbols (`I`, `W`, `Pb`, `Zr`, etc.) looked plausible in this corpus sample, but they should stay under periodic-table exact-case rules and audit counters.

## Id convention ratification

Mostly agree, with two guardrails:

- `oxide_wt_pct` ids should be assigned only for explicit wt/percent labels or unlabeled whole-rock major-oxide context. If an oxide label explicitly says ppm, mg/kg, mol/kg, mmol/kg, etc., leave unmatched or use a concentration id.
- `{El}_conc` for trace/REE/bare elements is OK as unit-agnostic concentration, provided unit metadata stays outside the id and is not lost.

Approved conventions:

- Major oxides: `{X}_wt_pct`, with the unit guardrail above.
- Trace/REE/bare elements: `{El}_conc`, unit-agnostic.
- Ratios: `{A}_{B}` and normalized ratios `{A}_{B}_N`.
- Existing L0 isotope ids retained.
- Total iron: `Fe_total_oxide_wt_pct`.

## Precision-risk answers

### a. 1-2 character element symbols

Risk is real. Do not let L0 aliases preempt charged ions or one-letter element symbols.

Recommended order:

1. Ion/charged species handling before L0 (`F-`, `Cl-`, `SO4--`, etc.).
2. Exact element symbols only when case is exact and token is bounded.
3. For very ambiguous one-letter labels (`F`, `B`, `P`, `S`, `K`) keep a per-symbol audit counter; require unit/context when possible.
4. Block lowercase `x` entirely unless matched by a full contextual alias.

### b. CO2 default

Do not default `CO2 concentration` to `CO2_wt`.

Suggested split:

- `CO2_wt`: whole-rock/volatile labels with wt%, weight percent, or major-volatile table context.
- `CO2_conc` or later phase-specific `CO2_dissolved_conc` / `CO2_gas_conc`: concentration, ppm, mg/kg, mmol/kg, mol/kg, gas/fluid/water context.
- `pCO2`: keep separate from abundance/concentration.

For cycle 3, I would leave phase-specific naming conservative: use generic `CO2_conc` only for explicit concentration labels, and do not overwrite `CO2_wt`.

### c. Bare Fe vs FeO

`Fe -> Fe_conc` and `FeO -> FeO_wt_pct` are semantically OK. Keep total iron oxide aliases (`FeOT`, `Fe2O3t`, etc.) separate. For explicit `Fe (wt.%)`, `_conc` is OK only under the unit-agnostic element convention.

### d. Bare d18O

`d18O -> d18O_rock` is probably the right default for igneous/mineral whole-rock corpus entries, but it is not universally safe. Branch or block when labels/sidecar context mention water, fluid, seawater, porewater, carbonate, gas, or mineral-specific phases if the canonical vocabulary supports them. Do not allow bare `d18O` to override explicit `d18O_water`.

## Cycle 3 roadmap checks

Looks good with these constraints:

- Generic isotope-ratio regex: good, but it must be preempted by age/date labels. `40Ar/39Ar age`, `206Pb/238U age`, and `U-Pb age` should become age ids, not ratio ids.
- Generic element-ratio regex: useful, but block unit slashes (`mg/L`, `umol/kg`), physical ratios (`Vp/Vs`), ranges, URLs/paths, and any label containing `age`/`date` unless routed to a geochronology id.
- Oxide ratios such as `CaO/Al2O3` should produce oxide-ratio ids, not element ratios.
- Ion charge stripping: yes, but route ions before L0 so `F-` cannot become fraction remaining.
- Trailing `ratio` stripping is OK. Generic parenthesis stripping should be whitelist-based; do not erase phase/unit/context parentheses like `(water)`, `(rock)`, `(R/Ra)`, `(mmol/kg)`, or `(wt%)`.
- `REE (La, Ce, ...)` can map to `REE_sum` only by a leading `REE`/`rare earth elements` alias, not by generic parenthesis deletion alone.
- Physical bare ids (`Pressure`, `fO2`, `Delta47`, `Delta17O`, `crustal thickness`, `Moho depth`, `K-Ar age`, `delta15N`) are worth adding. Age ids must run before generic ratio rules.

## Recommended cycle 3 fixes before chasing coverage

1. Add a deny/override for bare lowercase `x`.
2. Move charged-ion normalization before L0 aliases; fix `F-`.
3. Split `CO2_wt` from `CO2_conc` using unit/context triggers.
4. Add explicit-unit guardrails for oxide wt-percent ids.
5. Add geochronology age preemption before isotope/element ratio regexes.
6. Re-run a fresh 120-label audit after these changes before accepting more coverage.
