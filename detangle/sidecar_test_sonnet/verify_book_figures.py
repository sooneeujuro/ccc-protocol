"""책 그림격리 진짜 검증: 이미지 네이밍(slug-prefix?) + 권내/권간 해시충돌(같은이름 다른크기) + MD 참조해결.
페이퍼 그림꼬임(854편/해시)이 책에도 있나."""
import os, glob, re, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"G:\corpus_md_export_20260612\books\book4_md"
IMG = (".jpg",".jpeg",".png",".gif",".webp")
books = [d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT,d))]

# 전역: 이미지 basename -> [(book, size)]
gimg = defaultdict(list)
print(f"{'book':40} #md #img  slug%  형식예시")
for b in books:
    bp = os.path.join(ROOT,b)
    files = []
    for dp,dn,fn in os.walk(bp):
        for f in fn: files.append((f, os.path.join(dp,f)))
    mds = [f for f,_ in files if f.endswith(".md")]
    imgs = [(f,p) for f,p in files if f.lower().endswith(IMG)]
    slug = sum(1 for f,_ in imgs if "__" in f)
    pct = (100*slug//len(imgs)) if imgs else 0
    ex = imgs[0][0][:42] if imgs else "(no img)"
    print(f"{b[:40]:40} {len(mds):>3} {len(imgs):>4}  {pct:>3}%  {ex}")
    for f,p in imgs:
        try: sz = os.path.getsize(p)
        except: sz = -1
        gimg[f].append((b, sz))

# 권간 충돌: 같은 파일명이 2권 이상 + 크기 다름 = 진짜 충돌(다른 그림인데 같은 이름)
print("\n=== 권간 이름충돌 분석 ===")
multi = {k:v for k,v in gimg.items() if len(set(b for b,_ in v)) >= 2}
collide = {k:v for k,v in multi.items() if len(set(s for _,s in v)) >= 2}
print(f"2권+ 등장 이미지명: {len(multi)}  | 그중 크기까지 달라 진짜충돌: {len(collide)}")
for k,v in list(collide.items())[:8]:
    print(f"  ⚠️ {k[:40]}  → {[(b[:18],s) for b,s in v][:4]}")

# MD 참조 해결 샘플 (1권)
print("\n=== MD 이미지참조 해결 샘플 (faure_mensing_2005) ===")
bp = os.path.join(ROOT,"faure_mensing_2005")
md_imgs_ref = miss = 0
for dp,dn,fn in os.walk(bp):
    for f in fn:
        if f.endswith(".md"):
            t = open(os.path.join(dp,f),encoding="utf-8",errors="replace").read()
            for ref in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", t):
                md_imgs_ref += 1
                rp = os.path.normpath(os.path.join(dp, ref))
                if not os.path.exists(rp): miss += 1
print(f"  MD내 이미지참조 {md_imgs_ref}개 중 파일 없음(깨진참조): {miss}")
