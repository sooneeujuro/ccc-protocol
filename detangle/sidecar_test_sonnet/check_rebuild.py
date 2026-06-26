"""books_rebuild 정체 + 재추출이 충돌 고쳤나 검증."""
import os, re, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
RB = r"G:\books_rebuild"
IMG = (".jpg",".jpeg",".png",".gif",".webp")

print("=== books_rebuild 최상위 ===")
for x in sorted(os.listdir(RB)):
    p = os.path.join(RB,x)
    if os.path.isdir(p): print(f"   [{x}]/  ({len(os.listdir(p))} files)")
    else: print(f"   {x}  ({os.path.getsize(p)} bytes)")

# 각 하위 폴더(책) 검증
for d in sorted(os.listdir(RB)):
    bp = os.path.join(RB,d)
    if not os.path.isdir(bp): continue
    files = os.listdir(bp)
    mds = [f for f in files if f.endswith(".md")]
    imgs = [f for f in files if f.lower().endswith(IMG)]
    print(f"\n=== [{d}] : md {len(mds)} | img {len(imgs)} ===")
    if mds:
        head = open(os.path.join(bp,mds[0]), encoding="utf-8", errors="replace").read(600)
        h1 = re.search(r"^#\s+(.+)$", head, re.M)
        print(f"   책정체(H1/머리): {(h1.group(1)[:60] if h1 else head[:80].strip())}")
        slug = sum(1 for f in imgs if "__" in f)
        print(f"   이미지 네이밍: slug-prefix {slug}/{len(imgs)}  예: {imgs[0] if imgs else '없음'}")
        # 충돌 검사: MD 참조 total/distinct/reuse
        refs = []
        for m in mds:
            t = open(os.path.join(bp,m), encoding="utf-8", errors="replace").read()
            for r in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", t):
                refs.append(os.path.basename(r.split()[0].strip("<>")).lower())
        c = Counter(refs); reuse = sum(v-1 for v in c.values() if v>1)
        print(f"   MD 이미지참조: total {len(refs)} | distinct {len(c)} | reuse(중복참조) {reuse}")
        bad = [(k,v) for k,v in c.items() if v>=3]
        if bad: print(f"   ⚠️ 3회+ 참조(충돌 의심): {sorted(bad,key=lambda x:-x[1])[:4]}")
        else: print(f"   ✅ 3회+ 참조 없음")
