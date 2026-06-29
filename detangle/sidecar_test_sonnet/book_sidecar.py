# -*- coding: utf-8 -*-
"""책 번들화 2단계: 책 sidecar (Gemma bibliographic, ollama). md 앞부분(front matter) → bibliographic.
배포 book② 인용 타겟화용: title/authors/editors/year/publisher/isbn/doi + book/chapter flag."""
import os, json, urllib.request, sys
sys.stdout.reconfigure(encoding="utf-8")
DST = r"G:\book_corpus_20260629"
ART = os.path.join(DST, "articles"); OUT = os.path.join(DST, "sidecars")
os.makedirs(OUT, exist_ok=True)
MODEL = "gemma4:12b"
SCHEMA = {"type": "object", "properties": {
    "title": {"type": "string"},
    "authors_full": {"type": "array", "items": {"type": "string"}},
    "editors": {"type": "array", "items": {"type": "string"}},
    "year": {"type": ["integer", "null"]},
    "publisher": {"type": ["string", "null"]},
    "isbn": {"type": ["string", "null"]},
    "doi": {"type": ["string", "null"]},
    "kind": {"type": "string", "enum": ["book", "book_lite", "chapter"]}},
    "required": ["title", "year", "kind"]}
INSTR = """Extract bibliographic metadata for this geochemistry BOOK / book-chapter from its title page / front matter. Output ONLY JSON per schema.
title: full title (plain text). authors_full: ["Surname, I."] (authors). editors: editors if edited volume else []. year: publication year int. publisher. isbn. doi if present.
kind: "book" (full textbook/monograph) | "chapter" (a chapter/section of a larger work) | "book_lite" (short standalone reference).
FRONT MATTER:
"""
def call(prompt):
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                       "stream": False, "think": False, "format": SCHEMA,
                       "options": {"temperature": 0, "num_ctx": 8192, "num_predict": 2048}}).encode("utf-8")
    req = urllib.request.Request("http://localhost:11434/api/chat", data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read().decode("utf-8")).get("message", {}).get("content", "")

n = ok = 0
for fn in sorted(os.listdir(ART)):
    if not fn.endswith(".md"): continue
    n += 1; bookid = fn[:-3]
    text = open(os.path.join(ART, fn), encoding="utf-8", errors="replace").read()[:5000]
    try:
        b = json.loads(call(INSTR + text))
    except Exception as e:
        print(f"  FAIL {bookid[:40]}: {str(e)[:50]}"); continue
    sc = {"id": bookid, "doi": b.get("doi"),
          "bibliographic": {"title": b.get("title"), "authors_full": b.get("authors_full") or [],
                            "editors": b.get("editors") or [], "year": b.get("year"),
                            "year_print": b.get("year"), "publisher": b.get("publisher"), "isbn": b.get("isbn")},
          "kind": b.get("kind"), "is_book": True,
          "extraction_meta": {"extraction_model": "gemma4:12b", "source": "book_corpus_20260629", "via": "front_matter"}}
    json.dump(sc, open(os.path.join(OUT, bookid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ok += 1
    au = (b.get("authors_full") or b.get("editors") or [""])[0]
    print(f"  {bookid[:34]} -> {(b.get('title') or '')[:32]} ({b.get('year')}, {b.get('kind')}, {au[:18]})")
print(f"책 sidecar: {ok}/{n}")
