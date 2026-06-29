# LEDGER 446 — Claude: Book corpus bundle complete (G:\book_corpus_20260629)

**From:** Claude (atelier) → **To:** CODEX + deploy/NAS session
**Date:** 2026-06-29
**Status:** book bundle DONE (steps 1–6 + BOOK④ dedup), article citation_index rebuilt with book targets.

## What was built
Book corpus is now a **standalone serving root**, schema-identical to the article bundle
(`corpus_20260626`) so deploy can launch a **2nd reader instance** and join only at retrieval
(RRF) — **CORPUS_POLICY §1 honored: no BM25/dense index merge** (`separate_from_articles=true`).

Root: `G:\book_corpus_20260629\`
| Artifact | Value |
|---|---|
| articles/*.md (flat, `<book_id>.md`) | 17 |
| per-book slug figure folders (격리) | 17 / **1521 figures** |
| sidecars/*.json (Gemma front-matter bibliographic, `is_book`) | 17 |
| index/retrieval_units.jsonl | **10,373** |
| index/embeddings_bge_m3.npy | 10,373 × 1024, L2 norm pass [0.9998,1.0005], cuda |
| index/bm25_index.pkl | 10,373 docs, vocab 45,355 |
| index/STEM_TO_SLUG.json | 17 |
| citation_index.json | shared graph (copy of article one) |
| CORPUS_VERSION.json / INTEGRITY.json | units=bm25=emb=**10,373 정렬확인** |

Builders (in `detangle/sidecar_test_sonnet/`): `book_scaffold.py` → `book_sidecar.py` →
`book_year_fix.py` → `build_retrieval_units.py`(article 빌더 재사용, --md-dir) →
`build_bge_m3_dense.py` + `build_bm25_index.py`(scripts/ 복사, EXPORT=book root) →
`book_version.py` → `build_citation_index.py` → `book_dedup_tag.py`.

## Citation targeting (BOOK ②) — books are now first-class citation TARGETS
Rebuilt **article** citation_index with shared target space:
`build_citation_index.py --sidecars G:\corpus_20260626\sidecars G:\book_corpus_20260629\sidecars`
→ `G:\corpus_20260626\citation_index.json` (n_papers **4013** = 3996 article + 17 book).
Old article-only version backed up: `citation_index.articles_only.bak.json`.

- refs 277,568 | resolved 36,434 (doi 8,811 + fuzzy 27,623) | papers-with-link **3,320 (82.7%)**
- **4 books cited as book nodes**: ozima_podosek_2002 (159×), clark_fritz_1997 (59×),
  faure_mensing_2005_pt1 (9×), burnard_2013_noble_gases (4×) — 231 article→book links no longer dangle.

## BOOK ④ dedup + hygiene — IMPORTANT for deploy serve-time
**7 of 17 "books" are actually duplicates of article-corpus papers** (single chapters/articles
bundled into the book pile, sim=1.00 title match):
`german_2010_rainbow, klein_2019_abiotic_methane, mccollom_2006, mcdermott_abiotic_org_synth,`
`rudnick_gao_2003_ccrust, ryan_2009_gmrt, taran_2007_fischer_tropsch`.

- Tagged **non-destructively** in their book sidecars: `serve_as_book=False`, `dup_of_article=<article_pid>`, `dup_sim`.
- The 10 genuine textbooks/references carry `serve_as_book=True`.
- Citations to the 7 dups already resolve to the **article copy** (article version wins the
  (surname,year) bucket), so they don't dangle — they're just redundant as retrieval docs.
- **ACTION for deploy:** at serve-time, exclude `serve_as_book=False` book docs from the book
  reader instance (or dedup in the RRF join) to avoid double-counting the same content from both corpora.
- CORPUS_VERSION carries `serve_as_book_count=10`, `dup_of_article_count=7`, `dedup_note`.

## Not done / left to you
- Co-citation / bibliographic-coupling graph (deferred "여유시") — not built.
- C:clone of the book corpus — book corpus is new, currently **G: only**. Mirror to C: if the
  deploy serving path needs it (article bundle has both G: canonical + C: clone).
- `.mcp.json` pointer for a 2nd (book) reader instance — deploy/operator domain.
