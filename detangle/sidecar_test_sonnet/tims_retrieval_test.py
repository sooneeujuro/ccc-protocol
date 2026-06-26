"""실측: "TIMS 분석기기 쓴 논문 찾아줘" — full-text vs sidecar 어느 쪽이 맞게 집나.
$0 (deterministic, no LLM). 20260612 (articles+sidecars 같은 vintage)."""
import json, re, os, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

ARTS = Path(r"C:\Users\USER\corpus_md_export_20260612\articles")
SIDE = Path(r"C:\Users\USER\corpus_md_export_20260612\sidecars")

TIMS_PAT = re.compile(r"\bTIMS\b|thermal[\s-]*ionniz|thermal[\s-]*ioniz", re.I)
# TIMS 기기 모델명(본문엔 모델명만 쓰는 경우 많음 — full-text 'TIMS'로는 누락)
MODEL_PAT = re.compile(r"\bTriton\b|\bVG\s?354\b|\bMAT\s?26[0-2]\b|\bPhoenix\b|\bIsoprobe-T\b|\bSector\s?54\b", re.I)

ft_hits = {}        # stem -> {tims_word, model_only}
for md in ARTS.glob("*.md"):
    t = md.read_text(encoding="utf-8", errors="replace")
    has_tims = bool(TIMS_PAT.search(t))
    has_model = bool(MODEL_PAT.search(t))
    if has_tims or has_model:
        ft_hits[md.stem] = {"tims_word": has_tims, "model_only": (has_model and not has_tims)}

sc_hits = {}        # stem -> {category_tims, raw_verbatim_tims}
sc_total = 0
for jf in SIDE.glob("*.json"):
    sc_total += 1
    try:
        sc = json.loads(jf.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        continue
    an = sc.get("analytical")
    an = an if isinstance(an, dict) else {}
    instrs = an.get("instruments") or []
    cat_tims = any((i.get("category") == "tims") for i in instrs if isinstance(i, dict))
    rv_tims = any(TIMS_PAT.search(str(i.get("raw_verbatim", ""))) for i in instrs if isinstance(i, dict))
    cat_other_with_tims = any(
        (i.get("category") == "other" and TIMS_PAT.search(str(i.get("raw_verbatim", ""))))
        for i in instrs if isinstance(i, dict))
    if cat_tims or rv_tims:
        sc_hits[jf.stem] = {"cat_tims": cat_tims, "rv_tims": rv_tims,
                            "as_other": cat_other_with_tims}

ftset, scset = set(ft_hits), set(sc_hits)
print(f"=== '기기로 TIMS 쓴 논문 찾기' — {sc_total}편 코퍼스, $0 ===\n")
print(f"[full-text]  'TIMS'나 thermal ionization 등장: {len(ftset)}편")
print(f"    그중 모델명만(Triton/VG354등, 'TIMS' 없이): {sum(1 for v in ft_hits.values() if v['model_only'])}편")
print(f"[sidecar]    instruments에 TIMS: {len(scset)}편")
print(f"    그중 category=='tims': {sum(1 for v in sc_hits.values() if v['cat_tims'])}편  ← 열거 설계(TIMS→other)")
print(f"    category=='other'인데 raw_verbatim에 TIMS: {sum(1 for v in sc_hits.values() if v['as_other'])}편")
print(f"\n[집합 비교]")
print(f"    양쪽 다 잡음: {len(ftset & scset)}")
print(f"    full-text만(sidecar 놓침): {len(ftset - scset)}")
print(f"    sidecar만(full-text 놓침): {len(scset - ftset)}")

print(f"\n[full-text가 잡고 sidecar가 놓친 예 5편] — 세 가지 이유(모델명·언급·Haiku누락) 섮임")
for s in list(ftset - scset)[:5]:
    print(f"    · {s[:56]}  (모델명만={ft_hits[s]['model_only']})")
print(f"\n[sidecar가 잡고 full-text가 놓친 예 5편]")
for s in list(scset - ftset)[:5]:
    print(f"    · {s[:56]}")
