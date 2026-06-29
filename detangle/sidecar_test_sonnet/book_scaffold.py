# -*- coding: utf-8 -*-
"""책 번들화 1단계: book corpus_root 스캐폴딩 (article 번들과 동일 스키마).
books_v5_out\<12hexslug>\<book_id>.md → DST\articles\<book_id>.md(flat) + DST\<slug>\(그림격리) + index\STEM_TO_SLUG.json."""
import os, json, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
SRC = r"G:\books_v5_out"
DST = r"G:\book_corpus_20260629"
for sub in ("articles", "index", "sidecars"):
    os.makedirs(os.path.join(DST, sub), exist_ok=True)

s2s = {}; nbook = nimg = 0; books = []
for slug in os.listdir(SRC):
    sd = os.path.join(SRC, slug)
    if slug == "_seg_dryrun" or not os.path.isdir(sd): continue
    mds = [f for f in os.listdir(sd) if f.endswith(".md")]
    if not mds: continue
    bookid = mds[0][:-3]
    shutil.copy2(os.path.join(sd, mds[0]), os.path.join(DST, "articles", bookid + ".md"))
    figdst = os.path.join(DST, slug); os.makedirs(figdst, exist_ok=True)
    for f in os.listdir(sd):
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            shutil.copy2(os.path.join(sd, f), os.path.join(figdst, f)); nimg += 1
    s2s[bookid] = slug; nbook += 1; books.append(bookid)

json.dump(s2s, open(os.path.join(DST, "index", "STEM_TO_SLUG.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"book corpus_root 스캐폴딩 → {DST}")
print(f"  {nbook}권 articles(flat) + 그림 {nimg}장(slug 격리) + STEM_TO_SLUG")
for b in sorted(books): print("  " + b[:52])
