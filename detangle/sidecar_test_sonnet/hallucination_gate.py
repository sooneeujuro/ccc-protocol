"""$0 결정론 hallucination 게이트 v2 (read-only, 토큰 기반 고정밀).
isotope/δ 비율 라벨만 게이트(고신뢰): 라벨의 모든 동위원소 토큰이 본문에 없으면 flag.
서술형 라벨(예: 'Li concentration')은 게이트 불가 → 스킵(과탐 방지).
한 논문의 게이트가능 변수 대부분이 flag되면 = MD 로드/OCR 의심으로 분리(진짜 환각 아님).
출력만 격리폴더; 실 sidecar/corpus 절대 미수정.
"""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

SIDE = Path(r"C:\Users\USER\corpus_md_export_20260612\sidecars")
ARTS = Path(r"C:\Users\USER\corpus_md_export_20260612\articles")
OUT  = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\HALLUCINATION_GATE.json")

SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻", "0123456789+-")
SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")

def norm(s):
    s = s.translate(SUP).translate(SUB).lower()
    s = s.replace("δ", "d").replace("∆", "d").replace("Δ", "d")
    s = re.sub(r"\\[a-z]+", "", s)        # LaTeX 명령 제거 (\text \mathrm \frac ...)
    s = re.sub(r"[{}$^_\\]", "", s)       # 수식 구분자 제거
    return re.sub(r"[^a-z0-9]", "", s)   # 토큰탐지용 영숫자만

# 동위원소 토큰: 질량수+원소 (3he, 40ar, 18o, 87sr, 143nd, 206pb ...)
ISO = re.compile(r"\d{1,3}[a-z]{1,2}")
def iso_tokens(raw):
    raw = re.sub(r"\([^)]*\)", "", raw)          # parenthetical 제거
    n = norm(raw)
    toks = set(ISO.findall(n))
    # 1글자 원소 뒤 단독 케이스 줄이려 길이>=2 토큰만, he/o/c 등 흔한건 그대로
    return {t for t in toks if len(t) >= 2}

md_cache = {}
def md_norm(md_file):
    if md_file in md_cache:
        return md_cache[md_file]
    p = ARTS / md_file
    if not p.exists():
        p = ARTS / (Path(md_file).stem + ".md")
    t = norm(p.read_text(encoding="utf-8", errors="replace")) if p.exists() else None
    md_cache[md_file] = t
    return t

n_side = 0; n_no_md = 0
by_model = {}
total_vars = 0; gateable_vars = 0; flagged_vars = 0
flagged_papers = []      # 진짜 환각 의심
md_suspect_papers = []   # 게이트가능 변수 대부분 flag = MD/OCR 의심

for jf in sorted(SIDE.glob("*.json")):
    try:
        sc = json.loads(jf.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        continue
    n_side += 1
    model = (sc.get("extraction_meta") or {}).get("extraction_model", "?")
    by_model[model] = by_model.get(model, 0) + 1
    vm = sc.get("variables_measured") or []
    if not vm:
        continue
    md_file = (sc.get("provenance") or {}).get("md_file") or (jf.stem + ".md")
    mdn = md_norm(md_file)
    if mdn is None:
        n_no_md += 1
        continue
    miss = []; n_gate = 0
    for v in vm:
        raw = v if isinstance(v, str) else (v.get("raw_label") or v.get("id") or "") if isinstance(v, dict) else ""
        if not raw:
            continue
        total_vars += 1
        toks = iso_tokens(raw)
        if not toks:
            continue                       # 서술형 = 게이트불가, 스킵
        gateable_vars += 1; n_gate += 1
        if not any(t in mdn for t in toks): # 토큰 하나도 본문에 없으면 환각의심
            flagged_vars += 1
            miss.append(raw)
    if miss:
        rec = {"stem": jf.stem, "model": model, "n_missing": len(miss),
               "n_gateable": n_gate, "missing_labels": miss}
        # 게이트가능 변수의 70%+ 가 flag면 MD/OCR 의심으로 분리
        if n_gate >= 3 and len(miss) / n_gate >= 0.7:
            md_suspect_papers.append(rec)
        else:
            flagged_papers.append(rec)

flagged_papers.sort(key=lambda x: -x["n_missing"])
md_suspect_papers.sort(key=lambda x: -x["n_missing"])
fp_by_model = {}
for fp in flagged_papers:
    fp_by_model[fp["model"]] = fp_by_model.get(fp["model"], 0) + 1

summary = {
    "sidecars_scanned": n_side,
    "by_extraction_model": by_model,
    "no_md_found": n_no_md,
    "total_measured_vars": total_vars,
    "gateable_iso_vars": gateable_vars,
    "flagged_iso_vars_absent": flagged_vars,
    "flagged_iso_var_rate": round(flagged_vars / max(1, gateable_vars), 4),
    "REAL_hallucination_suspect_papers": len(flagged_papers),
    "real_suspect_rate": round(len(flagged_papers) / max(1, n_side), 4),
    "real_suspect_by_model": fp_by_model,
    "md_ocr_suspect_papers(separate)": len(md_suspect_papers),
}
OUT.write_text(json.dumps({"summary": summary, "hallucination_suspect": flagged_papers,
                           "md_ocr_suspect": md_suspect_papers},
                          ensure_ascii=False, indent=1), encoding="utf-8")

print("=== $0 HALLUCINATION GATE v2 (토큰기반, read-only) ===")
for k, v in summary.items():
    print(f"  {k}: {v}")
print("\n=== 진짜 환각 의심 상위 15편 ===")
for fp in flagged_papers[:15]:
    print(f"  [{fp['model'][:12]:12}] {fp['n_missing']}/{fp['n_gateable']} iso  {fp['stem'][:40]}")
    print(f"       miss: {', '.join(fp['missing_labels'][:4])}")
print(f"\n출력: {OUT}")
