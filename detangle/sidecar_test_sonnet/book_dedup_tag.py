# -*- coding: utf-8 -*-
"""책 번들화 6b단계 (BOOK ④ dedup+hygiene): article corpus와 중복인 '책'을 비파괴 태깅.
일부 book_id는 실제 교과서가 아니라 단일 논문/챕터가 article corpus에도 독립 논문으로 존재.
serve-time RRF 이중카운트 방지용 serve_as_book 플래그 + dup_of_article 포인터를 sidecar에 추가(삭제 X)."""
import sys, os, json
sys.path.insert(0, r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet")
sys.stdout.reconfigure(encoding="utf-8")
import build_citation_index as B
from collections import defaultdict

ART = r"G:\corpus_20260626\sidecars"
BOOK = r"G:\book_corpus_20260629\sidecars"
TH = 0.50  # 책 dedup은 article보다 보수적(제목 거의 동일해야 dup 판정)

arts = B.load_sidecars([ART])
books = B.load_sidecars([BOOK])
ay = defaultdict(list)
for pid, d in arts.items():
    sn, y = B.surname(B.first_author(d)), B.byear(d)
    if sn and y: ay[(sn, y)].append((pid, B.title_of(d)))

dup = keep = 0
for pid, d in sorted(books.items()):
    sn, y = B.surname(B.first_author(d)), B.byear(d)
    bt = B.title_of(d)
    best, bs = None, 0.0
    for apid, at in ay.get((sn, y), []):
        s = B.sim(bt, at)
        if s > bs: bs, best = s, apid
    p = os.path.join(BOOK, pid + ".json")
    sc = json.load(open(p, encoding="utf-8"))
    if best and bs >= TH:
        sc["dup_of_article"] = best
        sc["dup_sim"] = round(bs, 3)
        sc["serve_as_book"] = False
        dup += 1
        print(f"  DUP  {pid[:34]:36} ~{bs:.2f}~ {best[:42]}")
    else:
        sc.pop("dup_of_article", None); sc.pop("dup_sim", None)
        sc["serve_as_book"] = True
        keep += 1
    json.dump(sc, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"\nBOOK ④ dedup 태깅: serve_as_book=True {keep}권 / dup_of_article {dup}권 (비파괴, 삭제 X)")
print(f"  → deploy serve-time에 serve_as_book=False 제외하면 RRF 이중카운트 방지")
