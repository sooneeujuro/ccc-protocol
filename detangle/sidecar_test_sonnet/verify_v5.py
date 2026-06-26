"""books_v5_out 15권 품질검증: slug격리 + 권내충돌(reuse) + 참조해결. 재추출이 충돌 고쳤나."""
import os, re, json, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
OUT = r"G:\books_v5_out"
IMG = (".jpg",".jpeg",".png",".gif",".webp")
man = {}
for ln in open(os.path.join(OUT,"_manifest.jsonl"), encoding="utf-8"):
    r = json.loads(ln)
    if r.get("slug"): man[r["slug"]] = r["pid"]

print(f"{'book(pid)':34} {'md':>3} {'img':>4} slug% {'refs':>4} {'dist':>4} {'reuse':>5} {'out/miss':>8}")
prob = []
for d in sorted(os.listdir(OUT)):
    bp = os.path.join(OUT,d)
    if not os.path.isdir(bp): continue
    files = os.listdir(bp)
    mds = [f for f in files if f.endswith(".md")]
    imgs = [f for f in files if f.lower().endswith(IMG)]
    slugp = sum(1 for f in imgs if f.startswith(d+"__"))
    refs = []
    for m in mds:
        t = open(os.path.join(bp,m), encoding="utf-8", errors="replace").read()
        for r in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", t):
            refs.append(os.path.basename(r.split()[0].strip("<>")))
    c = Counter(refs); reuse = sum(v-1 for v in c.values() if v>1)
    outside = miss = 0
    for r in set(refs):
        if not os.path.exists(os.path.join(bp, r)): miss += 1
    pid = man.get(d, d)[:32]
    pct = (100*slugp//len(imgs)) if imgs else 0
    flag = ""
    if reuse>0: flag+=" ⚠️reuse"; prob.append((pid,"reuse",reuse))
    if miss>0: flag+=" ⚠️miss"; prob.append((pid,"miss",miss))
    print(f"{pid:34} {len(mds):>3} {len(imgs):>4} {pct:>4}% {len(refs):>4} {len(c):>4} {reuse:>5} {miss:>8}{flag}")

print(f"\n{'✅ 전권 reuse 0 + 참조 0깨짐 = 충돌 완전 해결' if not prob else '⚠️ 문제: '+str(prob)}")
