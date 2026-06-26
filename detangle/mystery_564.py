import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

ART = Path(r"G:\corpus_md_export_20260612\articles")
idx = Path(r"C:\Users\USER\Documents\manuscript-atelier\tools\paper-orchestra\corpus\index")
d = json.load(open(idx / "retrieval_papers.json", encoding="utf-8"))
papers = d["papers"]

def norm(s):
    return re.sub(r"[^a-z0-9가-힣]", "", str(s).lower())

idx_md = {norm(re.sub(r"\.md$", "", p.get("source_md_name", "") or "")) for p in papers}

IMG = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
NS = re.compile(r"^[0-9a-f]{12}__[0-9a-f]{32}_img", re.I)
BARE = re.compile(r"^[0-9a-f]{32}_img", re.I)

missing = []
for md in ART.glob("*.md"):
    if norm(md.stem) in idx_md:
        continue
    # prefix 매칭도 시도
    ng = norm(md.stem)
    if any(k and k[:30] == ng[:30] for k in idx_md if len(k) >= 20):
        continue
    missing.append(md)

print(f"articles {len(list(ART.glob('*.md')))} - index {len(papers)} = index에 없는 article: {len(missing)}")

# 특성 분석
kor = eng = 0
fmt = {"bare": 0, "ns": 0, "nofig": 0}
years = {}
for md in missing:
    if re.search(r"[가-힣]", md.stem):
        kor += 1
    else:
        eng += 1
    t = md.read_text(encoding="utf-8", errors="replace")
    fns = [m.group(1).rsplit("/", 1)[-1] for m in IMG.finditer(t)]
    if not fns:
        fmt["nofig"] += 1
    elif any(BARE.match(f) for f in fns):
        fmt["bare"] += 1
    elif any(NS.match(f) for f in fns):
        fmt["ns"] += 1
    ym = re.search(r"(19|20)\d{2}", md.stem)
    if ym:
        y = ym.group(0)
        years[y] = years.get(y, 0) + 1

print(f"언어: 한글 {kor} | 영어 {eng}")
print(f"그림형식: {fmt}")
print("연도 분포(많은 순):", sorted(years.items(), key=lambda x: -x[1])[:8])
print("--- 샘플 20 ---")
for md in missing[:20]:
    print("  ", md.stem[:60])
