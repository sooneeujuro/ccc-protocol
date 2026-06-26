"""최종 정합성: 한글 살린 토큰(+difflib). 격리 전 풀 vs 정본.
노이즈 H1 제외하고 진짜 갭만. 결정론적 $0."""
import os, re, glob, json, sys
from difflib import SequenceMatcher
sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"G:\corpus_20260624\articles"
POOLS = {
 "Q_duplicates(20260602)": r"G:\corpus_md_export_20260602\articles\_duplicates_quarantine",
 "Q_newdup(20260609)": r"G:\corpus_md_export_20260602\_renewal_20260609\_new_dup_quarantine",
 "Q_20260612": r"G:\corpus_md_export_20260612\quarantine",
}
# H1이 진짜 제목이 아닌 노이즈 패턴
NOISE = re.compile(r"^(article|articles|volcanology|geochemistry|chemical geodynamics|earth sciences|"
   r"index|preface|references|acknowledg|abstract|introduction|chapter\s*\d*$|epsl|scientific reports|"
   r"technical reports|unknown|references and notes|geochemical perspectives|nature|science|"
   r"\d+$|\W*$)", re.I)
TOK = re.compile(r"[가-힣a-z0-9]{2,}")
STOP = set("the of and in a to for on with from by an at as is are this".split())
def get_title(path):
    try: t = open(path, encoding="utf-8", errors="replace").read(1800)
    except: return None
    m = re.search(r"^#\s+(.+)$", t, re.M)
    return (m.group(1) if m else "").strip()
def toks(s): return frozenset(x for x in TOK.findall(s.lower()) if x not in STOP)
def norm(s): return " ".join(TOK.findall(s.lower()))

print("정본 인덱스(한글 포함)...", flush=True)
ct = []; inv = {}
for f in glob.glob(os.path.join(CORPUS, "*.md")):
    ti = get_title(f)
    if not ti: ti = os.path.basename(f)[:-3]   # H1없으면 파일명(최후수단)
    tk = toks(ti)
    if len(tk) < 2: continue
    i = len(ct); ct.append((ti, norm(ti), tk))
    for t in tk: inv.setdefault(t, []).append(i)
print(f"  정본 {len(ct)}편\n", flush=True)

def best(ti):
    tk = toks(ti); nq = norm(ti); cand = {}
    for t in tk:
        for i in inv.get(t, []): cand[i] = cand.get(i,0)+1
    b = (0.0, None)
    for i,_ in sorted(cand.items(), key=lambda x:-x[1])[:50]:
        r = SequenceMatcher(None, nq, ct[i][1]).ratio()
        if r > b[0]: b = (r, ct[i][0])
    return b

real_gaps = []
for name, d in POOLS.items():
    if not os.path.isdir(d): continue
    incorp = noise = gap = 0
    for f in glob.glob(os.path.join(d, "*.md")):
        ti = get_title(f)
        if not ti or NOISE.match(ti) or len(toks(ti)) < 3:
            noise += 1; continue          # H1 노이즈 → 판정불가(대개 정본에 있음)
        r, cm = best(ti)
        if r >= 0.82: incorp += 1
        else:
            gap += 1
            real_gaps.append({"pool": name, "title": ti[:75], "best_corpus": (cm[:60] if cm else None), "r": round(r,2)})
    print(f"{name:24} 정본有 {incorp:>4} | 노이즈H1 {noise:>3} | 진짜갭후보 {gap:>3}")

# 진짜갭 중복 제거
seen = set(); uniq = []
for g in real_gaps:
    k = norm(g["title"])[:50]
    if k in seen: continue
    seen.add(k); uniq.append(g)
print(f"\n=== 유니크 진짜갭 후보(노이즈·중복 제외): {len(uniq)} ===")
for g in sorted(uniq, key=lambda x:-x["r"]):
    print(f"  r={g['r']} [{g['pool'][:12]}] {g['title']}")
    print(f"        ↔최근접: {g['best_corpus']}")
json.dump(uniq, open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\FINAL_GAPS.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n→ FINAL_GAPS.json")
