VERDICT: issues_found

# Codex verdict on TASK 008 cycle 4 retroactive audit

Cycle 4 is a substantial coverage gain (`71.2%`) and the generic ratio/isotope-ratio layers look mostly healthy in the 120-label sample. I would not roll back the whole cycle 4 patch.

However, sampled precision is still below the 98% gate. I found at least 3 hard false matches in `audit_sample_cycle4.json`, so this needs targeted fixes before the next expansion.

## Precision audit

Hard false matches:

| raw_label | assigned_id | why |
|---|---|---|
| `CO2 (dissolved)` | `CO2_wt` | The parenthetical is a phase/context word. Dissolved CO2 is not whole-rock wt% CO2. Route to `CO2_conc` or a future `CO2_dissolved_conc`. |
| `Fe(III) concentration` | `Fe_conc` | Ferric Fe/speciation is not bulk Fe concentration. Needs `Fe3_conc`/`Fe3_plus_conc` or unmatched until the vocabulary supports valence. |
| `REE partition coefficients between orthopyroxene and clinopyroxene` | `REE_sum` | Partition coefficients are not REE abundance/sum. The leading `REE` rule is too broad for coefficient/distribution/partition labels. |

Minimum sampled precision: `117/120 = 97.5%`, below the 98% gate.

Precision risks I did not count as hard false in this sample:

- `Pressure (P) -> pressure_MPa` and `Temperature (T OW79) -> temperature_C` are only safe if units are preserved or normalized elsewhere. If the canonical id encodes units, do not assign `_MPa`/`_C` without unit evidence or conversion.
- `Au (gold fineness) -> Au_conc` is probably usable if `*_conc` is unit-agnostic, but "fineness" is a purity metric and should be tracked as a soft-risk label.
- `Mg# (magnesite number) -> Mg_number` is anchored by `Mg#`, so I would keep it, but the gloss is suspicious and should not teach a generic "magnesite number" alias.
- Gas/isotope ratio ids like `CO2_40Ar`, `N_40Ar`, and `S_3He` appear semantically true, but consider normalizing isotope-token order/names (`Ar40` vs `40Ar`) consistently.

## Cycle-3 self-audit agreement

Agree with the cycle-3 self-audit fixes for:

- `F (ppm) -> F_conc`
- `Age grid misfit -> None`
- `3H/3He age -> age_3H3He`
- `CO2 (mmol/mol) -> CO2_conc`

But please ingest my `007_CYCLE3_REAUDIT_VERDICT.md` fully before cycle 5. It had additional hard false patterns that cycle 4 has not fully fixed:

- Fe valence/speciation (`Fe3+`, `Fe(III)`, ferric/ferrous) must not collapse to bulk `Fe_conc`.
- REE+Y and REE coefficients need distinct handling or blocking.
- `total Fe concentration` should not become `Fe_total_oxide_wt_pct` without oxide/wt context.

## Gloss and cycle 4 rules

The conservative gloss rewrite is much better. The sampled bad gloss examples from Claude's self-audit are not reappearing here.

Remaining gaps:

- The phase/unit parenthetical guard must be shared by `_try_co2`, not only `_try_gloss`. `_try_co2` currently strips `(dissolved)` and turns `CO2 (dissolved)` into bare `CO2`, causing the false `CO2_wt`.
- Apply the `_QUALIFIER_WORDS` block or an equivalent qualifier block to the leading `REE` rule. Terms such as `partition coefficient(s)`, `coefficient`, `distribution coefficient`, `D_`, `Kd`, `pattern`, `normalized`, and `anomaly` should not map to `REE_sum` by default.
- Add a valence/speciation pre-pass for `Fe(III)`, `Fe(II)`, `Fe3+`, `Fe2+`, ferric, ferrous before L1/L2 can route them to bulk `Fe_conc`.

## Recommendation

Proceed with a targeted cycle 4.1 patch, not a broad rollback:

1. `CO2 (dissolved|aqueous|gas|fluid|soil gas)` -> concentration/phase branch, never `CO2_wt`.
2. Block or dedicate ids for Fe valence/speciation labels.
3. Block REE coefficient/pattern/anomaly labels from `REE_sum` unless there is an explicit canonical id for that concept.
4. Re-run a fresh 120-label sample after those patches. If hard false count is <=2/120 and the specific regression probes pass, cycle 4 can continue.
