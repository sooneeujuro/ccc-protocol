VERDICT: issues_found

# Codex verdict on TASK 009 cycle 4 re-audit

I re-audited the refreshed `audit_sample_cycle4.json` after the 007 fixes. Several 007 issues are fixed, and the 71.2% coverage gain looks mostly real, but the sample still misses the 98% precision gate.

Do not roll back all of cycle 4. Do a targeted cycle 4.1 precision patch before cycle 5.

## Precision audit

Hard false matches in the 120-label sample:

| raw_label | assigned_id | why |
|---|---|---|
| `CO2 (dissolved)` | `CO2_wt` | Parenthetical phase/context is being stripped before CO2 classification. Dissolved CO2 is concentration/phase data, not whole-rock wt%. |
| `Fe(II)` | `Fe_conc` | Roman-valence Fe is ferrous/speciation, not bulk Fe concentration. Needs `Fe2_conc`/`Fe2_plus_conc` or unmatched. |
| `La/Yb ratio (LaN/YbN)` | `La_Yb` | The parenthetical states normalized LaN/YbN; should route to `La_Yb_N` or stay raw if normalization basis is uncertain. |
| `Pressure (GPa)` | `pressure_MPa` | Unit-specific id says MPa but label says GPa. Either use a unit-agnostic `pressure` id or only assign `pressure_MPa` with conversion/unit handling. |
| `REE/La ratio profiles` | `REE_sum` | A REE/La ratio profile is not a REE sum. The leading REE rule is still too broad for ratio/profile labels. |

Sample precision with these counted false: `115/120 = 95.8%`.

If `Pressure (GPa)` is treated as unit-preserved-but-id-imperfect rather than false, the floor is still `116/120 = 96.7%`, below 98%.

Soft specificity misses, not counted as false:

- `$^{14}C$ age -> age`, `OSL age -> age`, `^40K-^40Ar gas retention age -> age`, and `U,Th-^4He gas retention age -> age` are true age labels but should become method-specific ids where feasible.
- `Au (gold fineness) -> Au_conc` is probably acceptable under unit-agnostic concentration ids, but fineness is a purity metric and should stay on the watchlist.
- `REE in clinopyroxene -> REE_sum` may be a useful group-level id, but the name `REE_sum` is lossy if it means actual arithmetic sum rather than "REE group measured".

## What is fixed from 007

Confirmed improved:

- `F (ppm)` class now has an override path.
- `Age grid misfit` is no longer in the fresh sample; age-tail hardening is the right direction.
- `3H/3He age` path is now dedicated as `age_3H3He`.
- `Fe3+`/`REE-Y`/`total Fe concentration` fixes are visible in the code/artifacts.
- Gloss is much safer than the initial cycle-4 self-audit version.

Still needs patch:

- `_try_co2` strips all parentheses before deciding phase. It must inspect/block phase words like `dissolved`, `aqueous`, `gas`, `soil gas`, `fluid`, `water` before falling back to `CO2_wt`.
- Ion/redox handling preserves `Fe2+`/`Fe3+`, but not Roman forms like `Fe(II)`, `Fe(III)`, ferric, ferrous.
- The leading `REE` rule needs a blocker for `ratio`, `profile`, `pattern`, `coefficient`, `partition`, `D_`, `Kd`, `normalized`, and `anomaly` unless a dedicated id exists.
- Normalized-ratio cues in parentheses (`LaN/YbN`, `(La/Yb)N`, `chondrite-normalized`) should preempt plain ratio ids.
- Unit-specific physical ids need a policy before cycle 5. `pressure_MPa` is not safe for explicit GPa labels unless value conversion is part of the pipeline.

## Cycle 5 greenlight

Conditional greenlight only after the 4.1 fixes above pass a fresh sample.

Cycle 5 feature directions are good with these guards:

- Physical quantities: use unit-agnostic ids unless conversion is implemented (`pressure`, `density`, `heat_flow`, `potential_temperature`, `Vp`, `Vs`, `Vp_Vs_ratio`, gravity/magnetic anomaly). Keep `Vp/Vs` separate from chemical ratios.
- Flux: add explicit `*_flux` ids for `CO2`, `SO2`, `HCl`, `4He`, etc.; never route flux labels to concentration or wt% ids.
- `δ34S` bare: OK as a sulfur isotope id, but keep it distinct from `34S/32S` ratio and future sulfate/sulfide phase branches.
- Dissolved oxides: use `SiO2_conc`/`SiO2_dissolved_conc` style ids, not `SiO2_wt_pct`.
- Age refinements: yes for LaTeX `14C`, AFT/FT, OSL/IRSL, K-Ar/Ar-Ar, U-Th/He, cosmogenic exposure age where identifiers are clear.

## Junk-tail agreement

Agree: blank/structural labels can be excluded from the normalization denominator after both agents agree on the exact filter. Include whitespace-only strings such as `" "`, `"\n"`, and quote-only strings such as `"\""`.

Do not exclude semantic labels as junk. `Age grid misfit`, `REE patterns`, `trace elements`, ratio profiles, coefficients, and unresolved physical quantities should remain raw/blocklisted with a reason, not removed from the denominator as blank junk.
