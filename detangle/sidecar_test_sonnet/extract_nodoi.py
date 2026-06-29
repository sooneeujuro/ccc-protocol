# -*- coding: utf-8 -*-
"""⑦ doi 비어있는 sidecar 추출 → 메타 (JAKO/한국 특화 재scout 입력). year는 ①로 이미 채워짐."""
import os, json, sys
sys.stdout.reconfigure(encoding="utf-8")
SIDE = sys.argv[1] if len(sys.argv) > 1 else r"G:\corpus_20260626\sidecars"
OUT = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\MISSING_NODOI.json"
def hangul(s): return any(0xAC00 <= ord(c) <= 0xD7A3 for c in str(s or ""))
out = []
for fn in os.listdir(SIDE):
    if not fn.endswith(".json"): continue
    try: d = json.load(open(os.path.join(SIDE, fn), encoding="utf-8"))
    except Exception: continue
    doi = d.get("doi")
    if doi and str(doi).strip() and str(doi).lower() != "null": continue
    b = d.get("bibliographic") if isinstance(d.get("bibliographic"), dict) else {}
    out.append({"pid": d.get("id") or fn[:-5],
                "title": (b.get("title") or "")[:200],
                "year": b.get("year") or b.get("year_print") or b.get("year_online"),
                "authors": [a for a in (b.get("authors_full") or []) if isinstance(a, str)][:3],
                "journal": b.get("journal") or ""})
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
kor = sum(1 for m in out if hangul(m["title"]) or hangul(m["journal"]))
print(f"no-DOI sidecar {len(out)} | 한글 제목/저널(국내지 추정) {kor} | 비한글(구논문/책/기타) {len(out)-kor}")
print("저장:", OUT)
for m in out[:6]:
    print(f"  {m['pid'][:36]}  [{m.get('journal','')[:20]}]")
