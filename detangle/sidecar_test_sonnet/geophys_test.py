"""지구물리 전용 프롬프트 테스트 — GEOPHYS_SUBSET 상위 3편에 적용, 변수 eyeball.
geochem 프롬프트는 이런 논문서 암석명만 뽑았음 → geophys 변수(Vp/Vs·이방성·깊이·focal) 잡나 확인."""
import json, sys, re, os, glob, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
ARTS = r"C:\Users\USER\corpus_md_export_20260612\articles"
SF = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet"
subset = json.load(open(os.path.join(SF, "GEOPHYS_SUBSET.json"), encoding="utf-8"))
PICK = subset[:3]

SCHEMA = {"type": "object", "properties": {
    "classification_type": {"type": "string", "enum": ["gas", "petrology", "both", "other"]},
    "made_new_measurements": {"type": "boolean"},
    "variables_reported": {"type": "array", "items": {"type": "object", "properties": {
        "raw_label": {"type": "string"}, "id": {"type": "string"}, "kind": {"type": "string"}},
        "required": ["raw_label"]}}},
    "required": ["classification_type", "made_new_measurements", "variables_reported"]}

INSTR = """This is a GEOPHYSICS / geodynamics / seismology / geodesy paper. Build a DATA INVENTORY of the GEOPHYSICAL quantities it reports. Output ONLY JSON per the schema. List which quantities are present; do NOT judge measured vs derived here.

classification_type: almost always "other" for pure geophysics (use gas/petrology/both only if it genuinely centers on volatile or rock geochemistry).
made_new_measurements: true if the paper produces its own new observations/inversions; false for pure review/compilation.

variables_reported: BE EXHAUSTIVE and GRANULAR — list EACH geophysical quantity SEPARATELY. Typical types (only those actually present):
- Seismic velocities: Vp, Vs, Vp/Vs ratio, velocity anomaly dVp(%), dVs(%)
- Anisotropy: SKS delay time, fast-axis direction, Pn anisotropy, radial/azimuthal anisotropy
- Structure depths: Moho depth, LAB depth, slab depth, 410/660 discontinuity depth, sediment thickness
- Attenuation: Qp, Qs, Q
- Earthquake source: moment magnitude Mw, focal mechanism, hypocenter depth, slip distribution, stress drop, b-value
- Geodesy: GPS velocity, slip rate, strain rate, coseismic displacement, InSAR LOS, subsidence rate
- Potential fields: Bouguer/free-air gravity anomaly, magnetic anomaly, heat flow, electrical resistivity/conductivity
- Other: receiver-function amplitude, rotation rate, plate velocity, temperature/rheology profiles
Use a "kind" hint per variable (e.g. seismic_velocity, anisotropy, depth, source, geodetic, potential_field). raw_label PLAIN TEXT (no LaTeX).

PAPER TEXT:
"""

def call(prompt):
    body = json.dumps({"model": "gemma4:12b", "messages": [{"role": "user", "content": prompt}],
                       "stream": False, "format": SCHEMA,
                       "options": {"temperature": 0, "num_ctx": 32768, "num_predict": 8192}}).encode("utf-8")
    req = urllib.request.Request("http://localhost:11434/api/chat", data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode("utf-8"))["message"]["content"]

for pid in PICK:
    mds = glob.glob(os.path.join(ARTS, pid + ".md"))
    if not mds:
        print(f"[{pid[:40]}] MD없음"); continue
    md = open(mds[0], encoding="utf-8", errors="replace").read()[:95000]
    try:
        out = json.loads(call(INSTR + md))
    except Exception as e:
        print(f"[{pid[:40]}] 실패 {e}"); continue
    vs = out.get("variables_reported", [])
    print(f"\n=== {pid[:50]} | class={out.get('classification_type')} new={out.get('made_new_measurements')} | {len(vs)}변수 ===")
    for v in vs[:18]:
        print(f"   [{str(v.get('kind',''))[:16]:16}] {str(v.get('raw_label'))[:50]}")
