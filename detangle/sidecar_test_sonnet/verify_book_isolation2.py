"""두 가지 검증:
(1) 폴더격리: 각 권 MD 이미지참조가 '자기 폴더 안'으로만 resolve 되나(밖으로 새거나 깨지면 섞임).
(2) 권내 충돌: 같은 이미지파일을 서로 다른 figure로 여러번 참조 = region-hash 뭉갬 의심."""
import os, re, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"G:\corpus_md_export_20260612\books\book4_md"
IMG = (".jpg",".jpeg",".png",".gif",".webp")
books = sorted(d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT,d)))

print(f"{'book':36} imgfiles refs distinct reuse outside missing")
tot_out = tot_miss = 0
suspect = []
for b in books:
    bp = os.path.abspath(os.path.join(ROOT,b))
    img_files = set(); md_paths = []
    for dp,dn,fn in os.walk(bp):
        for f in fn:
            if f.lower().endswith(IMG): img_files.add(f.lower())
            elif f.endswith(".md"): md_paths.append(os.path.join(dp,f))
    refs = []  # basename of each ref
    outside = missing = 0
    for mp in md_paths:
        t = open(mp, encoding="utf-8", errors="replace").read()
        for ref in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", t):
            ref = ref.split()[0].strip("<>")  # strip title/space
            base = os.path.basename(ref).lower()
            refs.append(base)
            rp = os.path.abspath(os.path.join(os.path.dirname(mp), ref))
            if not rp.startswith(bp): outside += 1
            elif not os.path.exists(rp): missing += 1
    c = Counter(refs)
    distinct = len(c); total = len(refs)
    reuse = sum(v-1 for v in c.values() if v > 1)   # 같은 파일 2회+ 참조된 초과분
    tot_out += outside; tot_miss += missing
    print(f"{b[:36]:36} {len(img_files):>7} {total:>5} {distinct:>7} {reuse:>5} {outside:>6} {missing:>6}")
    # 의심: 한 이미지가 여러번(>=3) 참조 = 다른 figure 뭉갬 가능
    bad = [(k,v) for k,v in c.items() if v >= 3]
    if bad: suspect.append((b, sorted(bad, key=lambda x:-x[1])[:3]))

print(f"\n폴더 밖 참조 합계: {tot_out}  | 깨진 참조 합계: {tot_miss}")
print(f"→ 폴더격리: {'✅ 모든 참조가 자기폴더 안 (밖/깨짐 0)' if tot_out==0 and tot_miss==0 else '⚠️ 새거나 깨진 참조 있음'}")
print("\n=== 권내 다중참조(같은 이미지파일 3회+ = 다른 그림 뭉갬 의심) ===")
if not suspect: print("  없음 (권내 충돌 정황 약함)")
for b, bad in suspect[:12]:
    print(f"  {b[:34]:34} {bad}")
