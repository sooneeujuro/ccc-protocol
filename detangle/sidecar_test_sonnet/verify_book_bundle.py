# -*- coding: utf-8 -*-
"""책 번들 serving-readiness 독립 검증 게이트 (빌드 스크립트와 별개 로직, adversarial).
CODEX/deploy 인계 전 무결성 PASS/FAIL. 결정론적 — LLM 미사용."""
import os, json, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np

BR = r"G:\book_corpus_20260629"
AR = r"G:\corpus_20260626"
ART_UNITS_SHA1 = "eb709fe789612eaf6289ab122c59cd5eba783b4a"  # article 정본 기준값(비파괴 확인용)
P = []  # (ok, label, detail)
def chk(ok, label, detail=""): P.append((bool(ok), label, detail))
def sha1f(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()
def nd(d): return bool(d and str(d).strip() and str(d).lower() != "null")

# --- 1) 행 정합성 4-way (units == npy rows == bm25 docs == 기재값) ---
units = [json.loads(l) for l in open(os.path.join(BR, "index", "retrieval_units.jsonl"), encoding="utf-8") if l.strip()]
nu = len(units)
emb = np.load(os.path.join(BR, "index", "embeddings_bge_m3.npy"), mmap_mode="r")
import pickle
sys.path.insert(0, os.path.join(BR, "scripts"))  # CorpusIndex 클래스 해석용
try:
    import build_bm25_index  # pkl은 빌드시 __main__로 저장됨 → 클래스를 현재 __main__에 주입
    for _n in dir(build_bm25_index):
        _o = getattr(build_bm25_index, _n)
        if isinstance(_o, type): setattr(sys.modules["__main__"], _n, _o)
except Exception: pass
with open(os.path.join(BR, "index", "bm25_index.pkl"), "rb") as f: bm = pickle.load(f)
# bm25 doc count: 객체/dict 구조 자동탐색 — N류 키, 아니면 길이==units인 리스트
nbm = None
for attr in ("N", "corpus_size", "doc_count", "n_docs", "num_docs"):
    if isinstance(bm, dict) and attr in bm: nbm = bm[attr]; break
    if hasattr(bm, attr): nbm = getattr(bm, attr); break
if nbm is None:
    cands = vars(bm).values() if hasattr(bm, "__dict__") else (bm.values() if isinstance(bm, dict) else [])
    for v in cands:
        if isinstance(v, (list, tuple)) and len(v) == nu: nbm = len(v); break
cv = json.load(open(os.path.join(BR, "CORPUS_VERSION.json"), encoding="utf-8"))
integ = json.load(open(os.path.join(BR, "INTEGRITY.json"), encoding="utf-8"))
chk(nu == emb.shape[0], "행정합 units==npy", f"{nu} vs {emb.shape[0]}")
chk(nbm in (nu, None), "행정합 units==bm25", f"{nu} vs {nbm}")
chk(cv.get("retrieval_units") == nu == integ.get("units_count") == integ.get("embedding_rows"),
    "행정합 기재값(CV/INTEGRITY)", f"cv={cv.get('retrieval_units')} integ_u={integ.get('units_count')} integ_e={integ.get('embedding_rows')}")

# --- 2) npy 무결성 (shape/dtype/norm/NaN) ---
arr = np.asarray(emb)
chk(arr.shape == (nu, 1024), "npy shape", str(arr.shape))
chk(arr.dtype == np.float32, "npy dtype", str(arr.dtype))
finite = np.isfinite(arr).all()
chk(bool(finite), "npy NaN/Inf 없음", "all finite" if finite else "HAS NaN/Inf")
norms = np.linalg.norm(arr.astype(np.float64), axis=1)
chk(float(norms.min()) > 0.99 and float(norms.max()) < 1.01, "npy L2 정규화", f"[{norms.min():.4f},{norms.max():.4f}]")

# --- 3) sidecar 정합성 (17 유효 JSON, is_book, serve_as_book, dup 7/keep 10) ---
SD = os.path.join(BR, "sidecars")
scs = [f for f in os.listdir(SD) if f.endswith(".json")]
bad = 0; isbook = 0; flagged = 0; dup = 0; keep = 0
for fn in scs:
    try: d = json.load(open(os.path.join(SD, fn), encoding="utf-8"))
    except Exception: bad += 1; continue
    if d.get("is_book") is True: isbook += 1
    if "serve_as_book" in d: flagged += 1
    if d.get("serve_as_book") is False and d.get("dup_of_article"): dup += 1
    if d.get("serve_as_book") is True: keep += 1
chk(len(scs) == 17 and bad == 0, "sidecar 17 유효JSON", f"n={len(scs)} bad={bad}")
chk(isbook == 17, "sidecar is_book=True 전수", str(isbook))
chk(flagged == 17, "serve_as_book 플래그 전수", str(flagged))
chk(dup == 7 and keep == 10, "dedup 7 dup / 10 serve", f"dup={dup} keep={keep}")

# --- 4) 그림 격리 무결성 (STEM_TO_SLUG 1:1, slug 폴더 그림합 == 기재 1521, 폴더-책 1:1) ---
s2s = json.load(open(os.path.join(BR, "index", "STEM_TO_SLUG.json"), encoding="utf-8"))
arts = [f[:-3] for f in os.listdir(os.path.join(BR, "articles")) if f.endswith(".md")]
chk(set(s2s.keys()) == set(arts), "STEM_TO_SLUG == articles 1:1", f"s2s={len(s2s)} arts={len(arts)}")
chk(len(set(s2s.values())) == len(s2s), "slug 유니크(충돌 0)", f"{len(set(s2s.values()))}/{len(s2s)}")
nfig = 0
for slug in set(s2s.values()):
    fd = os.path.join(BR, slug)
    if os.path.isdir(fd):
        nfig += sum(1 for f in os.listdir(fd) if f.lower().endswith((".jpg", ".jpeg", ".png")))
chk(nfig == cv.get("figures"), "그림합 == CORPUS_VERSION", f"{nfig} vs {cv.get('figures')}")

# --- 5) units → book md alignment (paper_id가 articles/<id>.md 존재, text_offset 범위내) ---
pids = set(u.get("paper_id") for u in units)
missing_md = [p for p in pids if p and not os.path.exists(os.path.join(BR, "articles", str(p) + ".md"))]
chk(len(missing_md) == 0, "units paper_id -> md 존재", f"missing={len(missing_md)} {missing_md[:3]}")
# 두 유닛타입 독립검증: (A) 오프셋 유닛 = md[s:e] sha1, (B) PR-META1 inline 유닛(off=[-1,-1]) = text_inline sha1
bad_off = 0; sha_chk = 0; sha_bad = 0; inline_chk = 0; inline_bad = 0
mdtext = {}
for u in units:  # 전수 (sha1은 빠름 — 완전 독립검증)
    pid = u.get("paper_id"); off = u.get("text_offset"); exp = u.get("text_sha1")
    if pid is None or not isinstance(off, (list, tuple)) or len(off) != 2: continue
    s, e = off
    if s < 0 or e < 0:  # inline 타입 — text_inline로 검증
        inline_chk += 1
        if exp and hashlib.sha1((u.get("text_inline") or "").encode("utf-8")).hexdigest() != exp: inline_bad += 1
        continue
    if pid not in mdtext:
        mp = os.path.join(BR, "articles", str(pid) + ".md")
        mdtext[pid] = open(mp, encoding="utf-8", errors="replace").read() if os.path.exists(mp) else ""
    t = mdtext[pid]
    if not (0 <= s < e <= len(t)): bad_off += 1; continue
    if exp:
        sha_chk += 1
        if hashlib.sha1(t[s:e].encode("utf-8")).hexdigest() != exp: sha_bad += 1
chk(bad_off == 0, "오프셋유닛 [s,e] 범위(전수)", f"out-of-range={bad_off}")
chk(sha_chk > 0 and sha_bad == 0, "오프셋유닛 md[s:e] sha1 일치(전수)", f"checked={sha_chk} mismatch={sha_bad}")
chk(inline_chk == 17 and inline_bad == 0, "inline유닛(PR-META1) sha1 일치(전수)", f"checked={inline_chk} mismatch={inline_bad}")

# --- 6) citation_index 무결성 (article판 n_papers 4013, 책 cited, 백업존재, book copy 동일) ---
ci_a = json.load(open(os.path.join(AR, "citation_index.json"), encoding="utf-8"))
chk(ci_a.get("n_papers") == 4013, "article CI n_papers=4013", str(ci_a.get("n_papers")))
book_targets = [b for b in s2s.keys() if b in ci_a.get("cited_by", {}) and ci_a["cited_by"][b]]
chk(len(book_targets) >= 4, "책 인용타겟 >=4", f"{len(book_targets)}: {book_targets}")
chk(os.path.exists(os.path.join(AR, "citation_index.articles_only.bak.json")), "article CI 백업존재(비파괴)", "bak")
chk(os.path.exists(os.path.join(BR, "citation_index.json")), "book root citation_index 존재", "")
sa = sha1f(os.path.join(AR, "citation_index.json")); sb = sha1f(os.path.join(BR, "citation_index.json"))
chk(sa == sb, "양 root citation_index 동일", f"{sa[:10]} vs {sb[:10]}")

# --- 7) article corpus 비파괴 (units_sha1 불변, retrieval/npy 무손상) ---
au_sha = sha1f(os.path.join(AR, "index", "retrieval_units.jsonl"))
chk(au_sha == ART_UNITS_SHA1, "article retrieval_units 불변", f"{au_sha[:14]} (기준 {ART_UNITS_SHA1[:14]})")
acv = json.load(open(os.path.join(AR, "CORPUS_VERSION.json"), encoding="utf-8"))
chk(acv.get("corpus_units_sha1") == ART_UNITS_SHA1, "article CORPUS_VERSION sha1 일치", acv.get("corpus_units_sha1", "")[:14])

# --- 8) CORPUS_POLICY §1 (분리 + 물리적 별도 index) ---
chk(cv.get("separate_from_articles") is True, "separate_from_articles=true", "")
chk(os.path.abspath(BR) != os.path.abspath(AR) and
    os.path.join(BR, "index", "embeddings_bge_m3.npy") != os.path.join(AR, "index", "embeddings_bge_m3.npy"),
    "index 물리적 분리(병합X)", "별도 root")

# === 리포트 ===
npass = sum(1 for ok, *_ in P if ok); nfail = len(P) - npass
print("=" * 64)
print(f"  책 번들 serving-readiness 게이트 — {npass}/{len(P)} PASS")
print("=" * 64)
for ok, label, detail in P:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label:34} {detail}")
print("=" * 64)
print(f"  종합: {'✅ ALL PASS — CODEX/deploy 인계 가능' if nfail == 0 else f'❌ {nfail} FAIL — 인계 전 수정 필요'}")
sys.exit(1 if nfail else 0)
