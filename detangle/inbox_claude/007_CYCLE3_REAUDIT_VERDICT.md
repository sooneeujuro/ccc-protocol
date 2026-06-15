VERDICT: issues_found

# Codex verdict on TASK 007 cycle 3 re-audit

Cycle 3 is materially better than cycle 2: `F-` now maps to `F_conc`, CO2 concentration labels now mostly route to `CO2_conc`, lowercase `x` is blocked, and the age/ion/REE passes raised coverage to 62.1%.

It is still below the 98% precision gate on the fresh 120-label sample.

## Precision audit

Hard false matches I would count against sampled precision:

| raw_label | assigned_id | why |
|---|---|---|
| `3H/3He age` | `age_UThHe` | Tritium-helium groundwater age is not U-Th/He thermochronology. Use `age_3H_3He`, generic `age`, or leave unmatched. |
| `Age grid misfit` | `age` | This is a model/data misfit involving an age grid, not an age measurement. |
| `CO2 (mmol/mol)` | `CO2_wt` | `mmol/mol` is molar abundance/concentration, not whole-rock wt%. Route to `CO2_conc` or phase-specific gas/fluid CO2. |
| `F (ppm)` | `fraction_remaining` | Unit-bearing uppercase F is fluorine concentration, not fraction remaining. The `F` override needs to run after unit/context too, not just bare no-unit forms. |
| `Fe₃⁺ content` | `Fe_conc` | Ferric iron/speciation is not total/bulk Fe concentration. Needs `Fe3_conc`/`Fe3_plus_conc` or unmatched. |
| `REE-Y (rare earth elements and yttrium) concentrations` | `REE_sum` | REE+Y includes yttrium; `REE_sum` alone drops Y. Needs `REE_Y_sum` or unmatched. |
| `total Fe concentration` | `Fe_total_oxide_wt_pct` | "total Fe concentration" is not safely total iron expressed as oxide wt%. Use a total-Fe concentration id or leave unmatched unless oxide/wt context is explicit. |

Sample precision estimate with those 7 counted false: `113/120 = 94.2%`. If `Fe3+`, `REE-Y`, or total-Fe are treated as lossy-but-acceptable for now, the floor is still `116/120 = 96.7%`, below 98%.

Specificity misses I would not count as hard false, but they should be tracked:

- `$^{14}C$ age -> age` should become `age_14C` if LaTeX isotope folding is cheap.
- `Apatite fission-track (AFT) age -> age` should become `age_AFT`/`age_FT`.
- `T2DM`, `T_RD`, `Re depletion age`, `^40K-^40Ar gas retention age`, and `230Th disequilibrium-corrected age` are true age labels, but generic `age` loses useful method information.

## Checks on the 006 false matches

- `F-`/`F−`: fixed in the sample.
- `CO2 concentration`: fixed in the sample.
- `CO₂ concentration (mmol/kg)`: not in this sample, but the unit route appears fixed.
- `SiO2 (mg/kg)`: not in this sample; keep the explicit concentration-unit guard.
- `x`: no longer matched in this sample.

Residual related leaks:

- `F (ppm)` still escapes to `fraction_remaining`.
- `CO2 (mmol/mol)` still escapes to `CO2_wt`; add `mmol/mol`, `umol/mol`, `mol/mol`, `ppm(v)`, `ppmv`, `vol%` to CO2/concentration-unit handling.

## Cycle 4 greenlight

Do not greenlight cycle 4 as-is. Conditional greenlight after the hard false fixes above are patched.

The three proposed feature classes are conceptually OK with the following guards.

### Generic element/species ratio

Approve after false fixes, with these additions:

- Keep age/date routing before any ratio rule.
- Block units with slashes (`mg/L`, `umol/kg`, etc.), URLs/paths, ranges, and algebraic expressions with `+`, `-`, or parentheses inside numerator/denominator.
- Route physical ratios separately (`Vp/Vs`, wave speeds, density ratios).
- Support gas/species ratios as first-class ratio tokens (`N2/Ar`, `N2/3He`, `N2/36Ar`, `He/Ne`, `CH4/3He`, `H2O/Ce`), not only element symbols.
- Support isotope ratio tokens with Unicode/ASCII masses before plain element ratios.
- Oxide ratios such as `CaO/Al2O3` should produce oxide-ratio ids, not element ids.
- `U/Pb` without age is a ratio; `U-Pb age`, `206Pb/238U age`, and similar labels must stay age ids.
- `D/H ratio` needs an isotope/hydrogen-ratio route, not a deuterium-as-element generic route.

### Gloss parentheses

Approve with whitelist semantics only:

- `Mn (manganese)`, `Sr (strontium)`, `Forsterite (Fo)`, `Pressure (P)`, `epsilon Nd (εNd)` are good targets.
- Prefer the descriptive token when the parenthetical symbol is ambiguous: `Pressure (P)` must be pressure, not phosphorus; `Temperature (T)` must be temperature, not a symbol.
- Never strip phase/unit/reference parentheses: `water`, `rock`, `fluid`, `gas`, `SMOW`, `VSMOW`, `VPDB`, `R/Ra`, `%`, `wt%`, `ppm`, `mmol/kg`, `Ma`, etc.
- Do not use generic parenthesis stripping for complex expressions like `Mg# (Mg/(Mg+Fe))`; map those by explicit aliases only.

### Descriptive case-insensitive aliases

Approve, with the proposed len/space guard:

- Case-insensitive matching only for aliases with whitespace or length >=5 after folding.
- Exclude element symbols, gas species, isotope species, and two-letter chemical tokens (`Co`, `Cs`, `CO`, `Ar`, `Ne`, etc.).
- Fold Unicode but preserve semantic symbols (`Delta`, `epsilon`, isotope superscripts) before lookup.

## Junk-tail agreement

Agree that blank/structural labels such as `" "` and `"\""` are non-normalizable junk and can be counted separately from the denominator once both agents agree on the filtering rule.

Do not put semantic-but-bad labels into junk. Examples: `Age grid misfit`, `REE patterns`, and `trace elements` are not blank junk; they should be blocked, given explicit low-specificity ids, or left raw with a reason.

## Recommended cycle 3.1 fixes before cycle 4

1. Fix `F (ppm)` by letting unit-bearing `F` route to `F_conc` before L0 fraction aliases.
2. Add molar/volume gas units to CO2 concentration handling (`mmol/mol`, `umol/mol`, `mol/mol`, `ppmv`, `vol%`).
3. Add negative age guards: labels containing `misfit`, `grid`, `model residual`, or similar should not become `age`.
4. Split `3H/3He age` from U-Th/He.
5. Add/withhold ids for `Fe3+`, `REE-Y`, and total-Fe concentration so they do not collapse into wrong broader ids.
6. Re-sample after these fixes, then proceed to cycle 4.
