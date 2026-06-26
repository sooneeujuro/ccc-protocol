"""no_md 사이드카가 진짜 corpus에 없나 본문검증: 각 사이드카 title vs 0624 article H1(제목) 토큰매칭.
높은 score = 정본에 다른 이름으로 있음(중복, no_md 맞음) / 낮음 = 어디에도 없음(레퍼런스 or 진짜 누락). read-only."""
import os, glob, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
SIDE = r"C:\Users\USER\corpus_md_export_20260612\sidecars"
A24 = r"G:\corpus_20260624\articles"; A12 = r"C:\Users\USER\corpus_md_export_20260612\articles"
def toks(t): return set(re.findall(r"[a-z0-9]{4,}", (t or "").lower()))
a24 = set(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(A24, "*.md")))
a12 = set(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(A12, "*.md")))
pids = [os.path.basename(f)[:-5] for f in glob.glob(os.path.join(SIDE, "*.json"))]
nomd = [p for p in pids if p not in a24 and p not in a12 and "Chapter" not in p and "Bioaccum" not in p]
# 0624 article 제목(H1) 인덱스
art = {}
for f in glob.glob(os.path.join(A24, "*.md")):
    h = open(f, encoding="utf-8", errors="replace").read(2500)
    m = re.search(r"^#\s+(.+)", h, re.M)
    art[os.path.basename(f)[:-3]] = toks(m.group(1) if m else os.path.basename(f)[:-3])
def get_title(sc):
    b = sc.get("bibliographic") or {}
    return b.get("title") or sc.get("title") or ""
rows = []
for p in nomd:
    try: sc = json.load(open(os.path.join(SIDE, p + ".json"), encoding="utf-8"))
    except: sc = {}
    nt = toks(get_title(sc)) or toks(p)
    best = None; bs = 0.0
    for af, at in art.items():
        if not at: continue
        s = len(nt & at) / max(1, len(nt | at))
        if s > bs: bs = s; best = af
    rows.append((bs, p, best, get_title(sc)[:40]))
rows.sort()
print(f"검증대상 {len(nomd)}편 (책 제외). score 높음=정본에 다른이름으로 존재(중복)\n")
for bs, p, best, title in rows:
    flag = "covered?" if bs >= 0.55 else ("LOW=확인필요" if bs >= 0.3 else "MISSING?")
    print(f"  {bs:.2f} [{flag}] {p[:34]}")
    print(f"        title: {title}")
    if bs >= 0.4: print(f"        ~match: {best[:50]}")
print(f"\n분포: covered(>=0.55) {sum(1 for r in rows if r[0]>=0.55)} / 중간 {sum(1 for r in rows if 0.3<=r[0]<0.55)} / MISSING(<0.3) {sum(1 for r in rows if r[0]<0.3)}")
