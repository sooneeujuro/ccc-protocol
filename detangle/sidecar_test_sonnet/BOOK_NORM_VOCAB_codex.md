# BOOK_NORM_VOCAB_codex.md

author: Codex
date_kst: 2026-06-25
purpose: Minimal book-sidecar normalization map aligned to existing paper variable aliases without creating a new vocabulary project.
status: draft_for_claude_round2_review

## Policy

This is not a new controlled vocabulary. It is a thin book-sidecar view over the existing paper normalizer/alias layer.

Rules:

- Keep raw fields as the recall surface: `topics_raw`, `methods_raw`, `isotope_systems_raw`.
- Normalize only exact or alias matches already covered by the paper-side normalizer family.
- Do not force unmatched book concepts into a nearby id.
- Do not add fuzzy matches in v0.
- If the normalizer is unsure, emit raw only and leave the corresponding `*_norm` array empty.
- Use `normalization_confidence=exact|alias` only.
- Do not normalize values. Constants, equations, and tables are typed locator flags, not values.

## Field Map

| Book field | Source behavior | v0 output |
|---|---|---|
| `topics_raw` | model phrase extraction | raw phrases |
| `topics_norm` | exact/alias only, curated subset | ids with confidence |
| `methods_raw` | model phrase extraction | raw phrases |
| `methods_norm` | exact/alias only, curated subset | ids with confidence |
| `isotope_systems_raw` | model phrase extraction | raw phrases |
| `isotope_systems_norm` | exact/alias only, paper normalizer ids or family ids | ids with confidence |
| `reference_data.reference_kind` | closed enum | enum only |
| `reference_data.label_norm` | optional exact/alias id | empty string allowed |

## Core Isotope-System Families

Use these as family-level topic/isotope ids when the segment is about the system rather than a single measured variable.

| norm_id | aliases/examples for matching | notes |
|---|---|---|
| `system_rb_sr` | Rb-Sr, rubidium-strontium, Sr isotope system, isochron Sr | family id; individual ratios can still map to paper ids |
| `system_sm_nd` | Sm-Nd, samarium-neodymium, Nd isotope system, epsilon Nd | family id |
| `system_u_pb` | U-Pb, uranium-lead, Pb-Pb, zircon geochronology | family id |
| `system_lu_hf` | Lu-Hf, hafnium isotope system | family id |
| `system_re_os` | Re-Os, rhenium-osmium, Os isotope system | family id |
| `system_k_ar_ar` | K-Ar, Ar-Ar, 40Ar/39Ar | family id |
| `system_he_ne_ar` | He-Ne-Ar, noble gas, helium-neon-argon | family id |
| `system_kr_xe` | Kr-Xe, krypton-xenon, xenon isotope system | family id |
| `system_c_isotopes` | carbon isotopes, d13C, carbonate carbon, methane carbon | family id |
| `system_o_h_isotopes` | oxygen and hydrogen isotopes, d18O, dD, water isotopes | family id |
| `system_s_isotopes` | sulfur isotopes, d34S, sulfate sulfur | family id |
| `system_n_isotopes` | nitrogen isotopes, d15N | family id |
| `system_b_li_isotopes` | boron/lithium isotopes, d11B, d7Li | family id |
| `system_clumped_isotopes` | clumped isotopes, Delta47, carbonate clumped | family id |

Implementation note: if a phrase maps cleanly to an existing paper variable id such as an isotope ratio or delta notation, the runner may emit both the specific paper id and the family id only when both are exact/alias matches. Otherwise emit the family id only.

## Core Method Families

Use method ids sparingly. They are retrieval facets, not method validation.

| norm_id | aliases/examples for matching | notes |
|---|---|---|
| `method_tims` | TIMS, thermal ionization mass spectrometry | instrument/method |
| `method_sims` | SIMS, ion microprobe | instrument/method |
| `method_mc_icp_ms` | MC-ICP-MS, multi-collector ICP-MS | instrument/method |
| `method_icp_ms` | ICP-MS, quadrupole ICP-MS | instrument/method |
| `method_irms` | IRMS, isotope ratio mass spectrometry | instrument/method |
| `method_noble_gas_ms` | noble gas mass spectrometry, static noble gas MS | instrument/method |
| `method_laser_ablation` | LA-ICP-MS, laser ablation | instrument/method |
| `method_fluorination` | laser fluorination, BrF5 fluorination | procedure |
| `method_step_heating` | step heating, incremental heating | procedure |
| `method_crushing_extraction` | crushing, vacuum crushing, fluid-inclusion crushing | procedure |
| `method_ion_exchange` | ion exchange chromatography, column chemistry | preparation |
| `method_isochron` | isochron, isochron regression | data reduction |
| `method_mixing_model` | binary mixing, endmember mixing, isotope mixing | interpretation |
| `method_fractionation_model` | equilibrium fractionation, kinetic fractionation | interpretation |
| `method_solubility_model` | solubility model, Henry-law style locator, gas solubility | reference/model |
| `method_thermodynamic_model` | equation of state, Gibbs, TEOS, thermodynamic relation | reference/model |

## Topic Families

These are allowed only when the segment clearly teaches or organizes the topic.

| norm_id | aliases/examples for matching |
|---|---|
| `topic_isotope_fractionation` | isotope fractionation, equilibrium fractionation, kinetic isotope effect |
| `topic_radiogenic_decay` | radioactive decay, decay constant, parent-daughter system |
| `topic_geochronology` | age dating, geochronology, chronometer |
| `topic_noble_gas_solubility` | noble gas solubility, gas-water solubility |
| `topic_hydrothermal_fluids` | hydrothermal fluid, vent fluid, geothermal fluid |
| `topic_groundwater_isotopes` | groundwater isotope hydrology, stable isotopes in groundwater |
| `topic_mantle_isotopes` | mantle source isotope, mantle reservoir, MORB/OIB isotope |
| `topic_crustal_contamination` | assimilation, contamination, crustal input |
| `topic_seawater_isotope_reference` | seawater isotope reference, marine Sr isotope, ocean reference curve |
| `topic_standardization_calibration` | standards, calibration, normalization standard |
| `topic_equation_of_state` | equation of state, thermodynamic formulation |
| `topic_reference_table_lookup` | handbook table, property table, compiled reference data |

## Reference Kind Enum

Closed enum for `reference_data.reference_kind`:

- `constant`
- `reference_table`
- `solubility_table`
- `isotope_ratio_reference`
- `equation`
- `conversion`
- `calibration`
- `standard`
- `thermodynamic_relation`
- `property_table`
- `classification_table`
- `unknown_reference`

## Source Role Map

For retrieval/index metadata, use one source role per segment:

| source_role | use when |
|---|---|
| `textbook_explanation` | segment primarily explains a concept |
| `reference_data_locator` | segment primarily points to tables/constants/equations without extracting values |
| `method_background` | segment explains method principles or workflow |
| `review_context` | segment synthesizes literature/background |
| `primary_evidence` | only for original-research-like short documents routed through paper schema |

## Rejection Examples

- A reference table with many constants: emit `reference_kind=constant` or `reference_table`, locator only, `value_extracted=false`.
- A topic phrase that is educational but has no exact/alias id: keep it in `topics_raw`; emit no `topics_norm`.
- A method phrase that names a workflow loosely: keep raw unless it maps to a listed method id exactly or by known alias.
- A table/equation id that is not visible in the segment: do not invent it; use page/section locator if deterministic.

## Version

- normalizer_version: `book_norm_vocab_codex_v0`
- compatible_schema: `book_sidecar_chapter_v0`
- compatible_prompt: `book_gemma_prompt_codex_v0`
