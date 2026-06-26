"""로컬 Gemma 4 12B (Ollama)로 sidecar 판단필드 추출 테스트.
파일럿 정답 아는 4편으로 — JSON 유효성 + classification + provenance 품질 평가. $0."""
import json, time, sys, urllib.request, glob, os
sys.stdout.reconfigure(encoding="utf-8")

ARTS = r"C:\Users\USER\corpus_md_export_20260612\articles"
MODEL = "gemma4:12b"
MAXCHARS = 35000

# 테스트 4편 + 파일럿 기대값
TESTS = [
    ("Hofmann_and_White,_1982", "other/false; Sr·Nd·Pb=cited, 모델값=modeled (개념논문, 측정 없음)"),
    ("Wilhelm,_1977", "gas/false; 용해도=cited, Henry/엔탈피=modeled (컴파일/열역학)"),
    ("Arai_et_al._(2018)", "petrology/true; 전암·광물=measured, CIPW/2px-T=modeled, lit=cited"),
    ("Stroncik_et_al._(2007)", "gas/true; He·Ne·Ar 동위원소=measured (신규 측정)"),
]

SCHEMA = {
    "type": "object",
    "properties": {
        "classification_type": {"type": "string", "enum": ["gas", "petrology", "both", "other"]},
        "made_new_measurements": {"type": "boolean"},
        "variables": {"type": "array", "items": {"type": "object", "properties": {
            "raw_label": {"type": "string"},
            "provenance": {"type": "string", "enum": ["measured", "cited", "modeled"]},
            "evidence": {"type": "string"}
        }, "required": ["raw_label", "provenance", "evidence"]}}
    },
    "required": ["classification_type", "made_new_measurements", "variables"]
}

INSTR = """You extract geochemistry metadata. Output ONLY JSON matching the schema.

classification_type: "gas"(noble gas/volatile/fluid focus) | "petrology"(rocks/minerals/elements) | "both" | "other"(method/review/theory/compilation/synthesis).

made_new_measurements: true ONLY if THIS paper reports its OWN new analytical measurements (its Methods + data tables describe analyses done in this study). Review/synthesis/theory/compilation/model papers = false.

variables: each quantity the paper reports or discusses, with provenance:
- "measured": THIS paper newly produced it from its OWN analysis (own tables/results).
- "cited": value from ANOTHER source ("data from X", "after Smith", compiled/literature/database/for comparison). If made_new_measurements is false, NOTHING is measured.
- "modeled": computed/derived (thermometer/barometer T&P, fO2 from equilibria, model fractions, CIPW norms, corrected ratios, Henry's constants, growth rates, model ages).
RULE: when in doubt, NOT measured. Short evidence (section/phrasing) each.

PAPER TEXT:
"""

def resolve(stem):
    g = glob.glob(os.path.join(ARTS, stem + "*.md"))
    return g[0] if g else None

def call(prompt):
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "format": SCHEMA,
        "options": {"temperature": 0, "num_ctx": 16384}
    }).encode("utf-8")
    req = urllib.request.Request("http://localhost:11434/api/chat", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read().decode("utf-8"))

for stem, exp in TESTS:
    p = resolve(stem)
    print("\n" + "=" * 70)
    print(f"[{stem}]  기대: {exp}")
    if not p:
        print("  MD 못찾음"); continue
    md = open(p, encoding="utf-8", errors="replace").read()[:MAXCHARS]
    t0 = time.time()
    try:
        resp = call(INSTR + md)
        dt = time.time() - t0
        content = resp.get("message", {}).get("content", "")
        out = json.loads(content)
    except Exception as e:
        print(f"  실패: {e}"); continue
    vs = out.get("variables", [])
    from collections import Counter
    pc = Counter(v.get("provenance") for v in vs)
    print(f"  ⏱{dt:.0f}s | JSON OK | class={out.get('classification_type')} "
          f"new_meas={out.get('made_new_measurements')} | vars={len(vs)} {dict(pc)}")
    for v in vs[:10]:
        print(f"      [{str(v.get('provenance')):8}] {str(v.get('raw_label'))[:42]:42} | {str(v.get('evidence'))[:50]}")
