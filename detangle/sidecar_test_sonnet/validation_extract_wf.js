export const meta = {
  name: 'sidecar-v22-validation-extract',
  description: 'Validate corrected Sonnet extraction (provenance measured/cited/modeled + real enum) on 24 pilot-flagged papers; isolated, no real-sidecar writes',
  phases: [{ title: 'Extract' }],
}

const PICK = [{"paper_id": "Hofmann_and_White,_1982,_Mantle_plumes_from_ancient_oceanic_crust", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Hofmann_and_White,_1982,_Mantle_plumes_from_ancient_oceanic_crust.md", "kind": "dispute"}, {"paper_id": "Wilhelm,_1977,_Low-pressure_solubility_of_gases_in_liquid_water", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Wilhelm,_1977,_Low-pressure_solubility_of_gases_in_liquid_water.md", "kind": "dispute"}, {"paper_id": "Hancock(2023)_Global_Synthesis_of_Regional_Holocene_Hydroclimate_Variability_Using_Proxy", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Hancock(2023)_Global_Synthesis_of_Regional_Holocene_Hydroclimate_Variability_Using_Proxy.md", "kind": "dispute"}, {"paper_id": "Elliott_et_al._(1999)_Exploring_the_kappa_conundrum;_the_role_of_recycling_in_the_lead_isotope_evolution_of_the_mantle", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Elliott_et_al._(1999)_Exploring_the_kappa_conundrum;_the_role_of_recycling_in_the_lead_isotope_evolution_of_the_mantle.md", "kind": "dispute"}, {"paper_id": "Rodbell(2022)_700,000_years_of_tropical_Andean_glaciation", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Rodbell(2022)_700,000_years_of_tropical_Andean_glaciation.md", "kind": "dispute"}, {"paper_id": "Jackson_et_al._(2017)_primordial_helium_entrained_by_the_hottest_mantle_plumes", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Jackson_et_al._(2017)_primordial_helium_entrained_by_the_hottest_mantle_plumes.md", "kind": "dispute"}, {"paper_id": "Loewen_et_al._(2019)_Hydrogen_isotopes_in_high_3He_4He_submarine_basalts", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Loewen_et_al._(2019)_Hydrogen_isotopes_in_high_3He_4He_submarine_basalts.md", "kind": "dispute"}, {"paper_id": "Marty_&_Tolstikhin_(1998)_CO2_fluxes_from_mid-ocean_ridges,_arcs_and_plumes", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Marty_&_Tolstikhin_(1998)_CO2_fluxes_from_mid-ocean_ridges,_arcs_and_plumes.md", "kind": "dispute"}, {"paper_id": "Woodhead_et_al._(1993)_Oxygen_isotope_evidence_for_recycled_crust_in_the_source_", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Woodhead_et_al._(1993)_Oxygen_isotope_evidence_for_recycled_crust_in_the_source_.md", "kind": "dispute"}, {"paper_id": "Liang_et_al._(2013)_A_REE-in-two-pyroxene_thermometer_for_mafic_and_ultramafic_r", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Liang_et_al._(2013)_A_REE-in-two-pyroxene_thermometer_for_mafic_and_ultramafic_r.md", "kind": "dispute"}, {"paper_id": "Colombier_et_al._(2021)_Degassing_and_gas_percolation_in_basaltic_magmas", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Colombier_et_al._(2021)_Degassing_and_gas_percolation_in_basaltic_magmas.md", "kind": "dispute"}, {"paper_id": "Deegan_et_al._(2016)_Pyroxene_standards_for_SIMS_oxygen_isotope_analysis_and_the", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Deegan_et_al._(2016)_Pyroxene_standards_for_SIMS_oxygen_isotope_analysis_and_the.md", "kind": "dispute"}, {"paper_id": "Giuliani_et_al._(2020)_Evolution_of_textures,_crystal_size_distributions_and_gro", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Giuliani_et_al._(2020)_Evolution_of_textures,_crystal_size_distributions_and_gro.md", "kind": "dispute"}, {"paper_id": "Furi_et_al.,_2010,_Apparent_decoupling_of_the_He_and_Ne_isotope_systematics_of_the_Icelandic_mantle;_The_role_of_He_depletion,_melt_mixing,_degassing_", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Furi_et_al.,_2010,_Apparent_decoupling_of_the_He_and_Ne_isotope_systematics_of_the_Icelandic_mantle;_The_role_of_He_depletion,_melt_mixing,_degassing_.md", "kind": "dispute"}, {"paper_id": "Poreda_&_Craig_(1989)_Helium_isotope_ratios_in_circum-Pacific_volcanic_arcs", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Poreda_&_Craig_(1989)_Helium_isotope_ratios_in_circum-Pacific_volcanic_arcs.md", "kind": "dispute"}, {"paper_id": "Sano_et_al._(1998)_Helium_degassing_related_to_the_Kobe_earthquake_", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Sano_et_al._(1998)_Helium_degassing_related_to_the_Kobe_earthquake_.md", "kind": "dispute"}, {"paper_id": "Nan_et_al._(2024)_Unraveling_abiotic_organic_synthesis_pathways_in_the_mafic_cru", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Nan_et_al._(2024)_Unraveling_abiotic_organic_synthesis_pathways_in_the_mafic_cru.md", "kind": "clean"}, {"paper_id": "1-s2.0-S0012821X12004621-main", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\1-s2.0-S0012821X12004621-main.md", "kind": "clean"}, {"paper_id": "Kim_D._et_al._(2024)_Upper_mantle_scale_enrichment_of_Cenozoic_intraplate_magmat", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Kim_D._et_al._(2024)_Upper_mantle_scale_enrichment_of_Cenozoic_intraplate_magmat.md", "kind": "clean"}, {"paper_id": "Shejwalkar_et_al._(2013)_Experimental_calibration_of_the_roles_of_temperature_and_composition_in_the_Ca-in-olivine_geothermometer_at_0.1_MPa", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Shejwalkar_et_al._(2013)_Experimental_calibration_of_the_roles_of_temperature_and_composition_in_the_Ca-in-olivine_geothermometer_at_0.1_MPa.md", "kind": "clean"}, {"paper_id": "006f3a79-6623-ab35-34a2-35fb003aeb4f", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\006f3a79-6623-ab35-34a2-35fb003aeb4f.md", "kind": "clean"}, {"paper_id": "Seyfried_et_al._(2007)_Redox_evolution_and_mass_transfer_during_serpentinization", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Seyfried_et_al._(2007)_Redox_evolution_and_mass_transfer_during_serpentinization.md", "kind": "clean"}, {"paper_id": "Arai_et_al._(2018)_Abyssal_Peridotite_as_a_Component_of_Forearc_Mantle;_New_Mant", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Arai_et_al._(2018)_Abyssal_Peridotite_as_a_Component_of_Forearc_Mantle;_New_Mant.md", "kind": "clean"}, {"paper_id": "Benko_et_al._(2021)_Combined_petrography,_noble_gas,_stable_isotope_and_fluid_in", "md_path": "C:\\Users\\USER\\corpus_md_export_20260612\\articles\\Benko_et_al._(2021)_Combined_petrography,_noble_gas,_stable_isotope_and_fluid_in.md", "kind": "clean"}];

const SCHEMA = {
  type: 'object',
  properties: {
    classification_type: { type: 'string', enum: ['gas', 'petrology', 'both', 'other'] },
    classification_confidence: { type: 'number' },
    made_new_measurements: { type: 'boolean', description: 'true only if this paper reports its own new analytical measurements' },
    variables: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          raw_label: { type: 'string' },
          provenance: { type: 'string', enum: ['measured', 'cited', 'modeled'] },
          evidence: { type: 'string', description: 'one line: section/table + phrasing that justifies the provenance call' }
        },
        required: ['raw_label', 'provenance', 'evidence']
      }
    },
    instruments: {
      type: 'array',
      items: {
        type: 'object',
        properties: { category: { type: 'string' }, raw_verbatim: { type: 'string' } },
        required: ['category', 'raw_verbatim']
      }
    }
  },
  required: ['classification_type', 'made_new_measurements', 'variables']
}

function prompt(p) {
  return [
    'You are a geochemistry metadata extractor. First use the Read tool to read this markdown file in full:',
    p.md_path,
    '',
    'Then extract the following for THIS single paper and return ONLY the structured output.',
    '',
    '(1) classification_type - exactly one of:',
    '  - "gas": primary focus is noble gas / volatile / fluid chemistry',
    '  - "petrology": rocks / minerals / element geochemistry',
    '  - "both": equally both',
    '  - "other": methods, reviews, geophysics, theory, compilations, syntheses',
    '',
    '(2) made_new_measurements: true ONLY if this paper reports its own new analytical measurements (its Methods + data tables describe analyses done in THIS study). For a review / synthesis / theory / compilation / data-model paper that reports no new analysis, set false.',
    '',
    '(3) variables - every distinct quantity the paper reports or discusses, each with a PROVENANCE label. THIS IS THE CRITICAL FIELD:',
    '  - "measured": THIS paper newly produced the value from its OWN analysis (its own tables/results).',
    '  - "cited": value taken from ANOTHER source - "data from X (2015)", "after Smith", compiled/database/synthesis/review of others data, literature values plotted for comparison. If made_new_measurements is false, EVERY value is cited or modeled, never measured.',
    '  - "modeled": value computed/derived - thermometer/barometer T and P, fO2 from equilibria, model fractions/contributions, normative (CIPW) values, atmospherically- or nucleogenic-corrected ratios derived via a model, growth rates from models, ages from decay models.',
    '  RULE: when in doubt it is NOT "measured" - prefer cited/modeled if there is any sign the value was not freshly analyzed in this paper. Do not over-assert; preserve the source own hedges.',
    '  Give one-line evidence (section/table + phrasing) for each provenance call.',
    '',
    '(4) instruments - analytical instrument categories used FOR NEW MEASUREMENTS in this paper, each from this enum (NOTE: TIMS maps to "other"; there is NO tims category):',
    '  irms, sims, qms, gc, icp_ms, noble_gas_ms, ic, xrd, epma, laser_ablation, crds, ftir, inaa, sem, software, aas, xrf, icp_aes, icp_oes, ams, raman, other',
    '  raw_verbatim = exact instrument string. If the paper made no new measurements, return an empty array.'
  ].join('\n')
}

phase('Extract')
const out = await parallel(PICK.map(p => () =>
  agent(prompt(p), { label: 'x:' + p.paper_id.slice(0, 22), phase: 'Extract', schema: SCHEMA, model: 'sonnet' })
    .then(r => ({ paper_id: p.paper_id, kind: p.kind, extraction: r }))
))
return { n: out.length, results: out.filter(Boolean) }
