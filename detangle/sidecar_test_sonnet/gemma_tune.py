"""Gemma 튜닝 자동루프 — Sonnet chunk0 답안지 대비.
usage: python gemma_tune.py <iter> <version_tag>
dev(실패분석용 10) + holdout(점수전용 15) disjoint. 결과 GEMMA_TUNE_LOG.json 누적.
$0 로컬."""
import json, time, sys, re, os, glob, urllib.request
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")

ITER = sys.argv[1] if len(sys.argv) > 1 else "1"
VER = sys.argv[2] if len(sys.argv) > 2 else "v2-split"
ARTS = r"C:\Users\USER\corpus_md_export_20260612\articles"
STAGE = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging"
SF = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet"
MODEL = "gemma4:12b"
MAXCHARS = 95000   # 풀 본문 (num_ctx 32768의 입력예산 ≈ 98k자 내). 정확도 최우선, 속도 포기.

SCHEMA = {"type": "object", "properties": {
    "analysis": {"type": "string"},
    "classification_type": {"type": "string", "enum": ["gas", "petrology", "both", "other"]},
    "made_new_measurements": {"type": "boolean"},
    "variables": {"type": "array", "items": {"type": "object", "properties": {
        "raw_label": {"type": "string"},
        "provenance": {"type": "string", "enum": ["measured", "cited", "modeled"]},
        "evidence": {"type": "string"}}, "required": ["raw_label", "provenance", "evidence"]}}},
    "required": ["analysis", "classification_type", "made_new_measurements", "variables"]}

# ---- 프롬프트 (버전 태그로 추적) ----
INSTR = """You extract geochemistry metadata. Output ONLY JSON per the schema.

FIRST fill "analysis" (think step by step, 4-8 sentences): identify this paper's OWN Methods/analytical section and its OWN data tables -> those quantities are "measured". Identify values brought in for comparison/from literature/databases/other studies -> "cited". Identify values computed/derived (thermometers, models, norms, corrected ratios) -> "modeled". State explicitly whether the paper made new measurements at all. THEN fill the rest using this analysis. The "variables" provenance MUST be consistent with your analysis.

classification_type: "gas"(noble gas/volatile/fluid focus) | "petrology"(rocks/minerals/element geochem) | "both" | "other"(methods/review/synthesis/compilation/theory/geophysics).

made_new_measurements: true ONLY if THIS paper reports its OWN new analytical measurements (its Methods + data tables = analyses in this study). Review/synthesis/theory/compilation/model papers = false.

variables: BE EXHAUSTIVE and GRANULAR. List EACH quantity SEPARATELY — never group.
- If a table reports La, Ce, Pr, Nd... -> list EACH element as its own variable (NOT "REE" or "trace elements" as one).
- If multiple isotope ratios (3He/4He, 20Ne/22Ne, 40Ar/36Ar) -> each is its own variable.
- Each major-element oxide (SiO2, TiO2, Al2O3, MgO...) -> separate.
Geochem papers typically have 20-60 distinct variables; a short list means you MISSED some. Only list quantities actually present in this paper.

Each variable's provenance:
- "measured": THIS paper newly produced it from its OWN analysis (own tables/results).
- "cited": value from ANOTHER source ("data from X", "after Smith", compiled/literature/database/plotted for comparison/end-member reference). If made_new_measurements is false, NOTHING is measured.
- "modeled": computed/derived (thermometer/barometer T&P, fO2 from equilibria, model fractions, CIPW norms, Mg#/Cr# from oxides, corrected ratios, Henry constants, growth rates, model ages).
RULE (anti-over-claim, CRITICAL — most errors are calling cited/modeled values "measured"): mark "measured" ONLY if the Methods describe analyzing THAT specific quantity on THIS study's OWN samples. Reference/literature values (seawater, atmosphere, chondrite, mantle end-members like DMM/EM1/EM2/HIMU, a standard's accepted value), values labelled "initial" / "at N Ma" / "corrected" / "primordial", and ratios used only for correction or comparison -> cited or modeled, NEVER measured. When unsure between measured and (cited or modeled), CHOOSE cited/modeled. After the analysis, STILL list EVERY variable exhaustively — do not drop any. One short evidence (table/section + phrasing) each.

raw_label: PLAIN TEXT ONLY ("3He/4He", "delta18O", "87Sr/86Sr", "Al2O3"). NO LaTeX, NO $, NO backslashes.

PAPER TEXT:
"""

def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower())
def toks(s): return set(re.findall(r"[a-z0-9]{2,}", (s or "").lower()))
def match_prov(lab, gvars):
    lt, ln = toks(lab), norm(lab); best, bsc = None, 0
    for g in gvars:
        gl = g.get("raw_label", ""); gn, gt = norm(gl), toks(gl)
        sc = 3 if (ln and (ln in gn or gn in ln)) else (len(lt & gt)/max(1, len(lt | gt))*2 if (lt and gt) else 0)
        if sc > bsc: bsc, best = sc, g
    return best.get("provenance") if (best and bsc >= 0.34) else None

def call(prompt):
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                       "stream": False, "format": SCHEMA,
                       "options": {"temperature": 0, "num_ctx": 32768, "num_predict": 16384}}).encode("utf-8")
    req = urllib.request.Request("http://localhost:11434/api/chat", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode("utf-8")).get("message", {}).get("content", "")

# dev/holdout 셋 (disjoint, deterministic)
pool = [f[:-5] for f in sorted(os.listdir(STAGE)) if f.endswith(".json")
        and glob.glob(os.path.join(ARTS, f[:-5] + ".md"))]
dev = pool[0::max(1, len(pool)//12)][:10]
rem = [p for p in pool if p not in set(dev)]
hold = rem[0::max(1, len(rem)//18)][:15]

DIFFS = []
def run_set(pids, collect=False):
    a = {"cls": 0, "mnm": 0, "pm": 0, "pt": 0, "nm_pm": 0, "nm_pt": 0, "gv": 0, "sv": 0, "n": 0, "latex": 0, "fail": 0}
    rows = []
    for pid in pids:
        son = json.load(open(os.path.join(STAGE, pid + ".json"), encoding="utf-8"))
        md = open(glob.glob(os.path.join(ARTS, pid + ".md"))[0], encoding="utf-8", errors="replace").read()[:MAXCHARS]
        out = None
        for _ in range(2):  # 빈응답 재시도 1회
            try:
                c = call(INSTR + md)
                if c.strip():
                    out = json.loads(c); break
            except Exception:
                pass
        if not out:
            a["fail"] += 1; continue
        gv = out.get("variables", []); sv = son.get("variables_measured", [])
        s_cls = (son.get("classification") or {}).get("type"); s_mnm = son.get("made_new_measurements")
        a["cls"] += (out.get("classification_type") == s_cls); a["mnm"] += (out.get("made_new_measurements") == s_mnm)
        for x in sv:
            sp = x.get("provenance")
            if sp not in ("measured", "cited", "modeled"): continue
            gp = match_prov(x.get("raw_label", ""), gv)
            if gp is not None:
                a["pt"] += 1; a["pm"] += (gp == sp)
                if sp != "measured":
                    a["nm_pt"] += 1; a["nm_pm"] += (gp == sp)
                if collect and gp != sp:
                    DIFFS.append({"pid": pid[:28], "label": x.get("raw_label", "")[:38],
                                  "sonnet": sp, "gemma": gp})
        a["latex"] += sum(1 for g in gv if "\\" in g.get("raw_label", "") or "$" in g.get("raw_label", ""))
        a["gv"] += len(gv); a["sv"] += len(sv); a["n"] += 1
        rows.append({"pid": pid[:30], "cls": out.get("classification_type") == s_cls,
                     "gv": len(gv), "sv": len(sv)})
    return a, rows

def pct(x, y): return round(x/max(1, y)*100)

print(f"=== ITER {ITER} ({VER}) | dev {len(dev)} / holdout {len(hold)} ===")
t0 = time.time()
adev, _ = run_set(dev, collect=True)
ahold, hrows = run_set(hold)
print(f"⏱ {time.time()-t0:.0f}s\n")

def summary(tag, a):
    return {"set": tag, "n": a["n"], "fail": a["fail"],
            "cls%": pct(a["cls"], a["n"]), "mnm%": pct(a["mnm"], a["n"]),
            "prov%": pct(a["pm"], a["pt"]), "nonmeas_prov%": pct(a["nm_pm"], a["nm_pt"]),
            "complete%": pct(a["gv"], a["sv"]), "latex": a["latex"]}

sdev, shold = summary("dev", adev), summary("holdout", ahold)
for s in (sdev, shold):
    print(f"  [{s['set']:7}] cls {s['cls%']}% | mnm {s['mnm%']}% | "
          f"prov {s['prov%']}% | nonmeas-prov {s['nonmeas_prov%']}% | "
          f"complete {s['complete%']}% | latex {s['latex']} | fail {s['fail']}")

# dev 불일치 방향 분석 (Sonnet→Gemma): 위험한 cited/modeled→measured 잡기
from collections import Counter as _C
dirn = _C(f"{d['sonnet']}→{d['gemma']}" for d in DIFFS)
print(f"\n=== dev provenance 불일치 {len(DIFFS)}건 (방향) ===")
for k, v in dirn.most_common():
    danger = "  ⚠️위험(인용/모델을 측정으로)" if k.endswith("→measured") else ""
    print(f"  {v:3}  {k}{danger}")
print("  예시:")
for d in DIFFS[:12]:
    print(f"    [{d['sonnet']}→{d['gemma']}] {d['label']}  ({d['pid']})")
json.dump(DIFFS, open(os.path.join(SF, "GEMMA_DEV_DIFFS.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

logp = os.path.join(SF, "GEMMA_TUNE_LOG.json")
log = json.load(open(logp, encoding="utf-8")) if os.path.exists(logp) else []
log.append({"iter": ITER, "version": VER, "dev": sdev, "holdout": shold})
json.dump(log, open(logp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n→ GEMMA_TUNE_LOG.json (총 {len(log)}회차)")
