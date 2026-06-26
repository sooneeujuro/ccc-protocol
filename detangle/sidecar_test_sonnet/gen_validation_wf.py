"""VALIDATION_PICK.json → 완성된 Workflow .js 생성 (PICK을 json.dumps로 안전 주입)."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

SF = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet")
pick = json.loads((SF / "VALIDATION_PICK.json").read_text(encoding="utf-8"))
# 에이전트에 필요한 최소필드만
slim = [{"paper_id": p["paper_id"], "md_path": p["md_path"], "kind": p["kind"]} for p in pick]

TEMPLATE = r'''export const meta = {
  name: 'sidecar-v22-validation-extract',
  description: 'Validate corrected Sonnet extraction (provenance measured/cited/modeled + real enum) on 24 pilot-flagged papers; isolated, no real-sidecar writes',
  phases: [{ title: 'Extract' }],
}

const PICK = __PICK__;

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
'''

js = TEMPLATE.replace("__PICK__", json.dumps(slim, ensure_ascii=False))
outp = SF / "validation_extract_wf.js"
outp.write_text(js, encoding="utf-8")
print(f"생성: {outp}  ({len(js)} bytes, PICK {len(slim)}편)")
