"""인벤토리 모드 확정 테스트 — provenance 제거, variables_reported.
측정: 완전성(recall) + precision(환각) + classification + made_new + instruments/geo.
Sonnet chunk0 답안지 대비. $0 로컬."""
import json, time, sys, re, os, glob, urllib.request
sys.stdout.reconfigure(encoding="utf-8")

ARTS = r"C:\Users\USER\corpus_md_export_20260612\articles"
STAGE = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging"
SF = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet"
MODEL = "gemma4:12b"
MAXCHARS = 95000

SCHEMA = {"type": "object", "properties": {
    "classification_type": {"type": "string", "enum": ["gas", "petrology", "both", "other"]},
    "made_new_measurements": {"type": "boolean"},
    "variables_reported": {"type": "array", "items": {"type": "object", "properties": {
        "raw_label": {"type": "string"}, "id": {"type": "string"},
        "unit": {"type": ["string", "null"]}, "phase": {"type": ["string", "null"]}},
        "required": ["raw_label"]}},
    "instruments": {"type": "array", "items": {"type": "object", "properties": {
        "category": {"type": "string"}, "raw_verbatim": {"type": "string"}},
        "required": ["category", "raw_verbatim"]}},
    "geography": {"type": "object", "properties": {
        "region": {"type": ["string", "null"]}, "country": {"type": ["string", "null"]},
        "tectonic_setting": {"type": ["string", "null"]}}}},
    "required": ["classification_type", "made_new_measurements", "variables_reported"]}

INSTR = """You build a DATA INVENTORY for a geochemistry paper. Output ONLY JSON per the schema.
This is an inventory of WHICH quantities/data the paper contains — do NOT judge whether measured vs cited (that is decided later by reading the text). Just list everything present.

classification_type: "gas"(noble gas/volatile/fluid) | "petrology"(rocks/minerals/elements) | "both" | "other"(methods/review/synthesis/compilation/theory/geophysics).
made_new_measurements: true if the paper reports its own new analytical measurements; false for review/synthesis/theory/compilation/model papers.

variables_reported: BE EXHAUSTIVE and GRANULAR — list EACH quantity SEPARATELY (each element La, Ce, Nd...; each isotope ratio 3He/4He, 87Sr/86Sr...; each oxide SiO2, Al2O3...). Never group ("REE", "trace elements" as one = WRONG). Only quantities ACTUALLY present in this paper (do not invent). id: canonical (3He/4He->He3_He4_RRa, 87Sr/86Sr->Sr87_Sr86, d18O->delta_18O...) else "raw_label_only". raw_label: PLAIN TEXT (no LaTeX/$/backslash).

instruments: each analytical instrument named, category from {irms,sims,qms,gc,icp_ms,noble_gas_ms,ic,xrd,epma,laser_ablation,crds,ftir,inaa,sem,software,aas,xrf,icp_aes,icp_oes,ams,raman,other} (TIMS->other, no tims category). raw_verbatim = exact string.
geography: region, country(ISO2), tectonic_setting (or null).

PAPER TEXT:
"""

_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
_SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
def _canon(s):  # δ/Δ/∆/delta 통일 + 위·아래첨자 ascii화
    s = (s or "").translate(_SUP).translate(_SUB).lower()
    s = s.replace("δ", "d").replace("∆", "d").replace("delta", "d")
    return s
def norm(s): return re.sub(r"[^a-z0-9]", "", _canon(s))
def toks(s): return set(re.findall(r"[a-z0-9]{2,}", _canon(s)))
def matches(lab, others):
    lt, ln = toks(lab), norm(lab)
    for o in others:
        on, ot = norm(o), toks(o)
        if ln and (ln in on or on in ln): return True
        if lt and ot and len(lt & ot)/max(1, len(lt | ot)) >= 0.34: return True
    return False

def call(prompt):
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                       "stream": False, "think": False, "format": SCHEMA,
                       "options": {"temperature": 0, "num_ctx": 32768, "num_predict": 8192}}).encode("utf-8")
    req = urllib.request.Request("http://localhost:11434/api/chat", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode("utf-8")).get("message", {}).get("content", "")

pool = [f[:-5] for f in sorted(os.listdir(STAGE)) if f.endswith(".json")
        and glob.glob(os.path.join(ARTS, f[:-5] + ".md"))]
dev = pool[0::max(1, len(pool)//12)][:10]
rem = [p for p in pool if p not in set(dev)]
hold = rem[0::max(1, len(rem)//18)][:15]

SAVED = []
def run(pids):
    a = {"cls": 0, "mnm": 0, "recall_m": 0, "recall_t": 0, "prec_m": 0, "prec_t": 0,
         "gv": 0, "sv": 0, "instr": 0, "geo": 0, "latex": 0, "n": 0, "fail": 0}
    for pid in pids:
        son = json.load(open(os.path.join(STAGE, pid + ".json"), encoding="utf-8"))
        md = open(glob.glob(os.path.join(ARTS, pid + ".md"))[0], encoding="utf-8", errors="replace").read()[:MAXCHARS]
        out = None
        for _ in range(2):
            try:
                c = call(INSTR + md)
                if c.strip(): out = json.loads(c); break
            except Exception: pass
        if not out: a["fail"] += 1; continue
        gvars = [v.get("raw_label", "") for v in out.get("variables_reported", [])]
        svars = [v.get("raw_label", "") for v in (son.get("variables_measured") or [])]
        SAVED.append({"pid": pid, "g": gvars, "s": svars,
                      "cls": out.get("classification_type"), "mnm": out.get("made_new_measurements"),
                      "instr": out.get("instruments") or [], "geo": out.get("geography") or {}})
        # recall: sonnet 변수 중 gemma가 잡은 비율
        for s in svars:
            a["recall_t"] += 1; a["recall_m"] += matches(s, gvars)
        # precision: gemma 변수 중 sonnet에 있는 비율 (낮으면 환각 의심)
        for g in gvars:
            a["prec_t"] += 1; a["prec_m"] += matches(g, svars)
        a["cls"] += (out.get("classification_type") == (son.get("classification") or {}).get("type"))
        a["mnm"] += (out.get("made_new_measurements") == son.get("made_new_measurements"))
        a["gv"] += len(gvars); a["sv"] += len(svars)
        a["instr"] += len(out.get("instruments") or [])
        a["geo"] += 1 if (out.get("geography") or {}).get("region") else 0
        a["latex"] += sum(1 for g in gvars if "\\" in g or "$" in g)
        a["n"] += 1
    return a

def P(x, y): return round(x/max(1, y)*100)
print(f"=== 인벤토리 확정 테스트 (provenance 제거) | dev {len(dev)} / hold {len(hold)} ===")
t0 = time.time()
for tag, pids in [("dev", dev), ("hold", hold)]:
    a = run(pids)
    print(f"  [{tag:4}] n={a['n']} fail={a['fail']} | recall(완전성) {P(a['recall_m'],a['recall_t'])}% | "
          f"precision(환각역) {P(a['prec_m'],a['prec_t'])}% | cls {P(a['cls'],a['n'])}% | "
          f"mnm {P(a['mnm'],a['n'])}% | latex {a['latex']} | instr/편 {a['instr']//max(1,a['n'])} | geo {a['geo']}/{a['n']}")
print(f"⏱ {time.time()-t0:.0f}s")
json.dump(SAVED, open(os.path.join(SF, "GEMMA_INV_OUTPUTS.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"출력 {len(SAVED)}편 저장 → GEMMA_INV_OUTPUTS.json (이후 재측정은 Gemma 재호출 불요)")
