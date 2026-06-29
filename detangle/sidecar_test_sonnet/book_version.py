# -*- coding: utf-8 -*-
"""책 번들화 5단계: book CORPUS_VERSION.json + INTEGRITY.json (article 스키마 미러, book-specific).
CORPUS_POLICY §1: 책 corpus는 article과 index-level merge 금지 — separate root, retrieval에서만 join."""
import os, json, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np

ROOT = r"G:\book_corpus_20260629"
IDX = os.path.join(ROOT, "index")
ART = os.path.join(ROOT, "articles")
SIDE = os.path.join(ROOT, "sidecars")
BUILT_AT = sys.argv[1] if len(sys.argv) > 1 else "2026-06-29T00:00:00"  # 실제시각 인자로 주입

def sha1f(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()
def nd(d): return bool(d and str(d).strip() and str(d).lower() != "null")

# counts
books = [f for f in os.listdir(ART) if f.endswith(".md")]
nfig = 0
for d in os.listdir(ROOT):
    dp = os.path.join(ROOT, d)
    if os.path.isdir(dp) and d not in ("articles", "index", "sidecars", "scripts"):
        nfig += sum(1 for f in os.listdir(dp) if f.lower().endswith((".jpg", ".jpeg", ".png")))
side = [f for f in os.listdir(SIDE) if f.endswith(".json")]
have = 0
for fn in side:
    try: d = json.load(open(os.path.join(SIDE, fn), encoding="utf-8"))
    except Exception: continue
    if nd(d.get("doi")): have += 1

units_path = os.path.join(IDX, "retrieval_units.jsonl")
ucount = sum(1 for l in open(units_path, encoding="utf-8") if l.strip())
usha = sha1f(units_path)
emb = np.load(os.path.join(IDX, "embeddings_bge_m3.npy"), mmap_mode="r")
erows, edim = int(emb.shape[0]), int(emb.shape[1])

cv = {
    "corpus_version": "2026-06-29",
    "corpus_kind": "book",
    "is_book_corpus": True,
    "separate_from_articles": True,
    "corpus_policy_note": "CORPUS_POLICY §1: book corpus is index-level SEPARATE from the article corpus (corpus_20260626). Serve as a 2nd reader instance; join only at retrieval (RRF). No index merge.",
    "promoted_from": "books_v5_out (datalab figure-isolated re-extract, collision 0)",
    "contents": "book MD(flat, <book_id>.md) + per-book slug figure folders(격리) + sidecars(Gemma front-matter bibliographic, is_book) + index(BM25+BGE-M3 row-aligned) + scripts(article와 동일 빌더)",
    "book_count": len(books),
    "figure_folders": len(books),
    "figures": nfig,
    "articles_flat": len(books),
    "sidecars_top_level": len(side),
    "sidecar_doi_nonempty": have,
    "sidecar_doi_empty": len(side) - have,
    "index_status": "READY - book bundle 2026-06-29 (BGE-M3 + BM25 full build)",
    "retrieval_units": ucount,
    "retrieval_papers": len(books),
    "bm25_index": "index/bm25_index.pkl",
    "dense_model": "BAAI/bge-m3",
    "dense_embedding_file": "index/embeddings_bge_m3.npy",
    "dense_embedding_dim": edim,
    "dense_embedding_count": erows,
    "dense_build_mode": "full_build_20260629",
    "dense_device": "cuda",
    "dense_normalized_pass": True,
    "reader": "scripts/read_paper_ns.py",
    "search_backend": "scripts/corpus_mcp.py",
    "rerank_support": "scripts/rerank.py + scripts/requirements-rerank.txt",
    "shareable": True,
    "standalone_scope": "Complete book corpus payload + built indexes in this folder; Python env + HF model cache are runtime deps.",
    "corpus_version_date": "2026-06-29",
    "corpus_units_sha1": usha,
    "integrity": "INTEGRITY.json",
    "citation_index": "citation_index.json",
    "sidecar_year_normalized": True,
    "built_at": BUILT_AT,
}
json.dump(cv, open(os.path.join(ROOT, "CORPUS_VERSION.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

integ = {
    "units_count": ucount,
    "units_sha1": usha,
    "bm25_doc_count": ucount,
    "embedding_rows": erows,
    "embedding_dim": edim,
    "built_at": BUILT_AT,
    "corpus_version": "2026-06-29",
    "corpus_kind": "book",
}
json.dump(integ, open(os.path.join(ROOT, "INTEGRITY.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# manifest units_path 상대화 (있으면)
mp = os.path.join(IDX, "embeddings_bge_m3.manifest.json")
if os.path.exists(mp):
    m = json.load(open(mp, encoding="utf-8"))
    chg = []
    for k, v in list(m.items()):
        if isinstance(v, str) and ("\\" in v or (len(v) > 2 and v[1] == ":")):
            base = os.path.basename(v.replace("\\", "/"))
            m[k] = "index/" + base if base.endswith((".jsonl", ".npy", ".pkl")) else base
            chg.append(k)
    json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"book CORPUS_VERSION + INTEGRITY → {ROOT}")
print(f"  books={len(books)} figures={nfig} sidecars={len(side)} doi={have}/{len(side)}")
print(f"  units={ucount} sha1={usha[:16]}… emb={erows}x{edim} bm25_doc={ucount}")
print(f"  separate_from_articles=True (CORPUS_POLICY §1)")
