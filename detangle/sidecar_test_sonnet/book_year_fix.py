# -*- coding: utf-8 -*-
"""책 sidecar year 보정: book_id에 박힌 연도(운영자 명명, SSOT)를 canonical로. 분할본/front-matter 없는 권 보정."""
import os, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
OUT = r"G:\book_corpus_20260629\sidecars"
fixed = 0
for fn in os.listdir(OUT):
    if not fn.endswith(".json"): continue
    p = os.path.join(OUT, fn)
    sc = json.load(open(p, encoding="utf-8"))
    bid = sc.get("id", "")
    m = re.search(r"(?:19|20)\d{2}", bid)
    if not m: continue
    y = int(m.group(0))
    b = sc.setdefault("bibliographic", {})
    if b.get("year") != y:
        b["year"] = y; b["year_print"] = y
        json.dump(sc, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        fixed += 1
        print(f"  {bid[:38]} year -> {y}")
print(f"year 보정: {fixed}편 (book_id 연도 우선)")
