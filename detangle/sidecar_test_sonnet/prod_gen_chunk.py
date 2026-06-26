"""생산 청크 생성: 다음 N편(미처리, idempotent) → Workflow .js 생성.
usage: python prod_gen_chunk.py <chunk_no> [size=400]
판단필드(classification/made_new_measurements/variables+provenance)만 Sonnet 재추출."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

SIDE = Path(r"C:\Users\USER\corpus_md_export_20260612\sidecars")
ARTS = Path(r"C:\Users\USER\corpus_md_export_20260612\articles")
STAGE = Path(r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging")
STAGE.mkdir(exist_ok=True)
SF = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet")

chunk_no = int(sys.argv[1]) if len(sys.argv) > 1 else 0
size = int(sys.argv[2]) if len(sys.argv) > 2 else 400

done = {p.stem for p in STAGE.glob("*.json")}
allsc = sorted(SIDE.glob("*.json"), key=lambda p: p.name)

pick = []
for jf in allsc:
    if jf.stem in done:
        continue
    try:
        sc = json.loads(jf.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        continue
    mf = (sc.get("provenance") or {}).get("md_file") or (jf.stem + ".md")
    mp = ARTS / mf
    if not mp.exists():
        mp = ARTS / (jf.stem + ".md")
    if not mp.exists():
        continue
    pick.append({"paper_id": jf.stem, "md_path": str(mp)})
    if len(pick) >= size:
        break

print(f"전체 {len(allsc)} | 처리완료 {len(done)} | 이번 청크 {len(pick)}편")
if not pick:
    print("남은 미처리 없음 — 전수 완료.")
    sys.exit(0)

TEMPLATE = r'''export const meta = {
  name: 'sidecar-v22-prod-chunk__CHUNKNO__',
  description: 'v2.2 production re-extract (classification + provenance variables) chunk __CHUNKNO__, isolated staging',
  phases: [{ title: 'Extract' }],
}
const PICK = __PICK__;
const SCHEMA = {
  type: 'object',
  properties: {
    classification: {
      type: 'object',
      properties: {
        type: { type: 'string', enum: ['gas', 'petrology', 'both', 'other'] },
        confidence: { type: 'number' },
        evidence: { type: 'array', items: { type: 'string' } }
      },
      required: ['type', 'confidence']
    },
    made_new_measurements: { type: 'boolean' },
    variables: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string', description: 'canonical id or raw_label_only' },
          raw_label: { type: 'string' },
          unit: { type: ['string', 'null'] },
          phase: { type: ['string', 'null'] },
          provenance: { type: 'string', enum: ['measured', 'cited', 'modeled'] },
          evidence: { type: 'string' }
        },
        required: ['raw_label', 'provenance', 'evidence']
      }
    }
  },
  required: ['classification', 'made_new_measurements', 'variables']
}
function prompt(p) {
  return [
    'You are a geochemistry metadata extractor. First use the Read tool to read this markdown file IN FULL:',
    p.md_path, '',
    'Return ONLY the structured output for THIS single paper.', '',
    '(1) classification.type - exactly one: "gas"(noble gas/volatile/fluid), "petrology"(rocks/minerals/element geochem), "both", "other"(methods/reviews/geophysics/theory/compilations/syntheses). Give confidence 0-1 and brief evidence strings.', '',
    '(2) made_new_measurements: true ONLY if this paper reports its OWN new analytical measurements (Methods + data tables describe analyses done in THIS study). For review/synthesis/theory/compilation/model papers reporting no new analysis: false.', '',
    '(3) variables - every distinct quantity reported or discussed, each with PROVENANCE (THE CRITICAL FIELD):',
    '  - "measured": THIS paper newly produced it from its OWN analysis (its own tables/results).',
    '  - "cited": value from ANOTHER source ("data from X 2015", "after Smith", compiled/database/synthesis/review/literature values for comparison). If made_new_measurements is false, NOTHING is measured - all cited or modeled.',
    '  - "modeled": computed/derived - thermometer/barometer T&P, fO2 from equilibria, model fractions/contributions, CIPW norms, atmospherically/nucleogenic-corrected ratios, growth rates, model ages.',
    '  RULE: when in doubt it is NOT measured. Do not over-assert; preserve the source own hedges. One-line evidence (section/table + phrasing) each.',
    '  id: canonical vocabulary id when it matches, else "raw_label_only". Common ids: 3He/4He->He3_He4_RRa, 87Sr/86Sr->Sr87_Sr86, 143Nd/144Nd->Nd143_Nd144, 206Pb/204Pb->Pb206_Pb204, 207Pb/204Pb->Pb207_Pb204, 208Pb/204Pb->Pb208_Pb204, d13C->delta_13C, d18O->delta_18O, dD/d2H->delta_D. unit/phase as written or null.'
  ].join('\n')
}
phase('Extract')
const out = await parallel(PICK.map(p => () =>
  agent(prompt(p), { label: 'x:' + p.paper_id.slice(0, 20), phase: 'Extract', schema: SCHEMA, model: 'sonnet' })
    .then(r => ({ paper_id: p.paper_id, extraction: r }))
))
return { chunk: __CHUNKNO__, n: out.length, results: out.filter(Boolean) }
'''
js = (TEMPLATE.replace("__PICK__", json.dumps(pick, ensure_ascii=False))
              .replace("__CHUNKNO__", str(chunk_no)))
outp = SF / f"prod_chunk_{chunk_no}.js"
outp.write_text(js, encoding="utf-8")
print(f"생성: {outp.name} ({len(js)} bytes)")
