"""전수 Gemma 인벤토리 추출 (production). $0 로컬, idempotent, 동시요청(Ollama 병렬).
usage: python gemma_production.py [workers=2]
- 미staged 논문만 처리(400 Sonnet + 기완료 skip)
- Gemma: classification + made_new + variables_reported(provenance 없음)
- 머지: 기존 Haiku sidecar에서 그 필드만 교체, verbatim(abstract/refs/figures/geo/labs/instruments) 유지
- v2.2, key=variables_reported. 출력→staging.
"""
import json, sys, re, os, glob, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.stdout.reconfigure(encoding="utf-8")

WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
SIDE = os.environ.get("GEMMA_SIDE", r"C:\Users\USER\corpus_md_export_20260612\sidecars")  # 117 base는 GEMMA_SIDE로 override
ARTS = os.environ.get("GEMMA_ARTS", r"G:\corpus_20260624\articles")          # 정본 0624 우선 (helium 런은 GEMMA_ARTS로 override)
ARTS_FB = r"C:\Users\USER\corpus_md_export_20260612\articles"  # 0624에 없는 ~87편 fallback
STAGE = os.environ.get("GEMMA_STAGE", r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_canonical")  # 캐노니컬 staging (helium은 GEMMA_STAGE로 override)
SF = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet"
os.makedirs(STAGE, exist_ok=True)
MODEL = "gemma4:12b"
MAXCHARS = 95000   # (미사용·보존) 청킹 구현완료 = extract_chunked()가 긴 MD를 컷 없이 분할추출+머지

SCHEMA = {"type": "object", "properties": {
    "classification_type": {"type": "string", "enum": ["gas", "petrology", "both", "other"]},
    "made_new_measurements": {"type": "boolean"},
    "variables_reported": {"type": "array", "items": {"type": "object", "properties": {
        "raw_label": {"type": "string"}, "id": {"type": "string"},
        "unit": {"type": ["string", "null"]}, "phase": {"type": ["string", "null"]},
        "kind": {"type": ["string", "null"]}},
        "required": ["raw_label"]}}},
    "required": ["classification_type", "made_new_measurements", "variables_reported"]}

# 지구물리 라우팅: GEOPHYS_SUBSET이면 geophys 프롬프트
try:
    GEO = set(json.load(open(os.path.join(SF, "GEOPHYS_SUBSET.json"), encoding="utf-8")))
except Exception:
    GEO = set()

INSTR = """You build a DATA INVENTORY for a geochemistry paper. Output ONLY JSON per the schema.
Inventory = WHICH quantities/data the paper contains. Do NOT judge measured vs cited (decided later by reading). List everything present.

classification_type: "gas"(noble gas/volatile/fluid) | "petrology"(rocks/minerals/elements) | "both" | "other"(methods/review/synthesis/compilation/theory/geophysics).
made_new_measurements: true if the paper reports its own new analytical measurements; false for review/synthesis/theory/compilation/model.

variables_reported: BE EXHAUSTIVE and GRANULAR — list EACH quantity SEPARATELY (each element La,Ce,Nd; each isotope ratio 3He/4He,87Sr/86Sr; each oxide SiO2,Al2O3). Never group ("REE"/"trace elements" as one = WRONG). Only quantities ACTUALLY present. id: canonical (3He/4He->He3_He4_RRa, 87Sr/86Sr->Sr87_Sr86, d18O->delta_18O, d13C->delta_13C) else "raw_label_only". raw_label: PLAIN TEXT (no LaTeX/$/backslash).

PAPER TEXT:
"""

GEO_INSTR = """This is a GEOPHYSICS / geodynamics / seismology / geodesy paper. Build a DATA INVENTORY of the GEOPHYSICAL quantities it reports. Output ONLY JSON per the schema. List which quantities are present; do NOT judge measured vs derived.

classification_type: almost always "other" for pure geophysics (use gas/petrology/both only if it genuinely centers on volatile or rock geochemistry).
made_new_measurements: true if the paper produces its own new observations/inversions; false for pure review/compilation.

variables_reported: BE EXHAUSTIVE and GRANULAR - list EACH geophysical quantity SEPARATELY (only those actually present):
- Seismic velocities: Vp, Vs, Vp/Vs, velocity anomaly dVp(%), dVs(%), phase/group velocity
- Anisotropy: SKS delay time, fast-axis direction, Pn anisotropy, radial/azimuthal anisotropy
- Structure depths: Moho depth, LAB depth, slab depth, 410/660 discontinuity, crustal/lithospheric thickness, sediment thickness
- Attenuation: Qp, Qs, Q
- Earthquake source: moment magnitude Mw, focal mechanism, hypocenter depth, slip distribution, stress drop, b-value
- Geodesy: GPS velocity, slip rate, strain rate, coseismic displacement/uplift, InSAR LOS, subsidence
- Potential fields: Bouguer/free-air gravity anomaly, magnetic anomaly, heat flow, electrical resistivity/conductivity
- Other: receiver-function amplitude, rotation rate, plate velocity, temperature/rheology profile
Add a "kind" hint per variable (seismic_velocity, anisotropy, depth, attenuation, source, geodetic, potential_field, other). raw_label PLAIN TEXT (no LaTeX).

PAPER TEXT:
"""

def call(prompt):
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                       "stream": False, "think": False, "format": SCHEMA,
                       "options": {"temperature": 0, "num_ctx": 49152, "num_predict": 16384}}).encode("utf-8")
    req = urllib.request.Request("http://localhost:11434/api/chat", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode("utf-8")).get("message", {}).get("content", "")

CHUNK = 88000   # char/청크 (ctx49152 여유). 긴 MD는 잘라버리지 않고 청킹+머지(꼬리 변수 보존)
def parse_resp(c):
    if not c or not c.strip(): return None
    try: return json.loads(c)
    except json.JSONDecodeError:
        try: return json.JSONDecoder().raw_decode(c.strip())[0]
        except Exception: return None
def chunk_md(md):
    if len(md) <= CHUNK: return [md]
    out = []; i = 0
    while i < len(md):
        end = min(i + CHUNK, len(md))
        if end < len(md):
            nl = md.rfind("\n", i + CHUNK // 2, end)
            if nl > i: end = nl
        out.append(md[i:end]); i = end
    return out
def _nrm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower())
def extract_chunked(md, instr):
    """긴 MD를 청킹 추출 후 variables_reported union+dedup. classification/made_new=첫 유효청크."""
    merged = {}; cls = None; made = None; got = False
    for ch in chunk_md(md):
        out = None
        for _ in range(2):
            out = parse_resp(call(instr + ch))
            if out is not None: break
        if out is None: continue
        got = True
        if cls is None: cls = out.get("classification_type"); made = out.get("made_new_measurements")
        for v in (out.get("variables_reported") or []):
            k = (v.get("id") or "") + "|" + _nrm(v.get("raw_label"))
            merged.setdefault(k, v)
    if not got: return None
    return {"classification_type": cls, "made_new_measurements": made, "variables_reported": list(merged.values())}

def process(pid):
    try:
        mds = glob.glob(os.path.join(ARTS, pid + ".md")) or glob.glob(os.path.join(ARTS_FB, pid + ".md"))
        if not mds:
            return (pid, "no_md")
        md = open(mds[0], encoding="utf-8", errors="replace").read()   # 전문(컷 제거) — 긴 건 청킹+머지
        instr = GEO_INSTR if pid in GEO else INSTR
        out = extract_chunked(md, instr)
        if not out:
            return (pid, "empty")
        sc = json.loads(open(os.path.join(SIDE, pid + ".json"), encoding="utf-8").read())
        if not isinstance(sc.get("classification"), dict): sc["classification"] = {}  # 기존이 str이면 dict로(머지 크래시 방지)
        sc["classification"]["type"] = out.get("classification_type")
        sc["made_new_measurements"] = out.get("made_new_measurements")
        sc["variables_reported"] = out.get("variables_reported") or []
        sc.pop("variables_measured", None)  # 레거시 키 제거(=reported로 이관)
        sc["schema_version"] = "v2.2"
        if not isinstance(sc.get("extraction_meta"), dict): sc["extraction_meta"] = {}
        sc["extraction_meta"]["inventory_reextract"] = {
            "model": "gemma4:12b", "prompt": ("geophys" if pid in GEO else "geochem"),
            "fields": ["classification.type", "variables_reported", "made_new_measurements"],
            "kept_from_haiku": ["abstract", "conclusions", "references", "figures", "geography", "labs", "instruments"]}
        json.dump(sc, open(os.path.join(STAGE, pid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return (pid, "ok")
    except Exception as e:
        return (pid, f"err:{str(e)[:40]}")

if __name__ == "__main__":
    done = {f[:-5] for f in os.listdir(STAGE) if f.endswith(".json")}
    todo = [f[:-5] for f in sorted(os.listdir(SIDE)) if f.endswith(".json") and f[:-5] not in done]
    print(f"전체 sidecar {len(os.listdir(SIDE))} | 기완료(staging) {len(done)} | 이번 처리대상 {len(todo)} | workers {WORKERS}")
    t0 = time.time(); n_ok = n_fail = 0; fails = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(process, pid): pid for pid in todo}
        for i, fut in enumerate(as_completed(futs), 1):
            pid, status = fut.result()
            if status == "ok": n_ok += 1
            else: n_fail += 1; fails.append((pid, status))
            if i % 25 == 0 or i == len(todo):
                el = time.time() - t0
                rate = el / max(1, i)
                eta_h = rate * (len(todo) - i) / 3600
                print(f"  {i}/{len(todo)} | ok {n_ok} fail {n_fail} | {rate:.0f}s/편 | ETA {eta_h:.1f}h", flush=True)
                json.dump({"done": n_ok, "fail": n_fail, "total": len(todo), "fails": fails[:50]},
                          open(os.path.join(SF, "PROD_PROGRESS.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"완료: ok {n_ok} / fail {n_fail} / staging 누적 {len(os.listdir(STAGE))}")
