"""지구물리/지구조 논문 detector — 전용 프롬프트 재패스 대상 식별. CPU $0, GPU 무관.
geochem(원소·동위원소) 신호 낮고 geophysics(탄성파·이방성·측지·단층) 신호 높은 논문 flag."""
import re, os, sys, glob, json
sys.stdout.reconfigure(encoding="utf-8")
ARTS = r"C:\Users\USER\corpus_md_export_20260612\articles"

# 지구물리 신호 (정량변수가 탄성파/측지/지진/구조류)
GEO = [r"\btomograph", r"\bseismic", r"anisotrop", r"receiver function", r"shear[- ]wave",
       r"\bP[- ]?wave", r"\bS[- ]?wave", r"\bVp\b", r"\bVs\b", r"velocity (model|structure)",
       r"\bSKS\b", r"shear[- ]wave splitting", r"geodet", r"\bGPS\b", r"InSAR",
       r"fault slip", r"slip rate", r"focal mechanism", r"\bearthquake", r"seismicity",
       r"moment magnitude", r"crustal (structure|thickness)", r"lithospher.{0,12}thickness",
       r"\bLAB depth", r"\bMoho\b", r"heat flow", r"gravity anomal", r"magnetotellur",
       r"strain rate", r"co-?seismic", r"rupture", r"subsidence", r"deformation field"]
# geochem 신호 (이게 강하면 geochem이지 geophysics 아님)
CHEM = [r"\bisotop", r"\b\d+[A-Z][a-z]?/\d+[A-Z]", r"δ\d", r"trace element", r"major element",
        r"\bREE\b", r"\bppm\b", r"whole[- ]rock", r"\bmelt\b", r"partition coefficient",
        r"\bxenolith", r"\bbasalt", r"noble gas", r"\bhelium\b", r"\bppb\b"]

geo_re = [re.compile(p, re.I) for p in GEO]
chem_re = [re.compile(p, re.I) for p in CHEM]

rows = []
for md in glob.glob(os.path.join(ARTS, "*.md")):
    stem = os.path.basename(md)[:-3]
    t = open(md, encoding="utf-8", errors="replace").read()
    head = t[:5000]  # 제목+초록+서론 가중
    g = sum(1 for r in geo_re if r.search(head)) * 2 + sum(1 for r in geo_re if r.search(t))
    c = sum(1 for r in chem_re if r.search(head)) * 2 + sum(1 for r in chem_re if r.search(t))
    rows.append((stem, g, c))

# 지구물리 우세: geo 신호 충분 + chem보다 우세
geophys = [(s, g, c) for s, g, c in rows if g >= 6 and g > c]
geophys.sort(key=lambda x: -(x[1] - x[2]))
print(f"전체 {len(rows)}편 | 지구물리 우세 후보: {len(geophys)}편 (geo>=6 & geo>chem)")
print("\n=== 상위 25편 (geo / chem 점수) ===")
for s, g, c in geophys[:25]:
    print(f"  geo{g:3} chem{c:3}  {s[:58]}")
out = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\GEOPHYS_SUBSET.json"
json.dump([s for s, g, c in geophys], open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n→ {len(geophys)}편 stem 저장: GEOPHYS_SUBSET.json")
