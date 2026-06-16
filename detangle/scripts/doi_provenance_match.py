#!/usr/bin/env python3
"""doi_provenance_match.py — 660 PDF를 DOI로 corpus 중복/신규 판별 (READ-ONLY).

corpus의 모든 sidecar에서 DOI(+제목)를 모아 'corpus 식별자 집합'을 만들고,
660 후보 PDF의 첫 페이지에서 DOI를 추출해 대조 → 같은 논문(다른 파일명)도 정확히 중복으로 잡는다.
DOI 못 찾으면 제목 정규화로 fallback.
"""
import json
import re
import fitz
from pathlib import Path

SIDE = Path(r"G:\corpus_md_export_20260612\sidecars")
GAP = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\CORPUS_GAP_REPORT.json")
OUT = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\DOI_PROVENANCE_MATCH.json")
PDF_ROOTS = [
    Path(r"G:\RefDB\동환상\extracted"), Path(r"G:\RefDB\홍씨\JP (sooneeujuro)"),
    Path(r"G:\RefDB\홍씨\김동환 (sooneeujuro)"), Path(r"G:\RefDB\LostnFound"),
    Path(r"G:\WonheeLee\논문"), Path(r"G:\WonheeLee\References"),
]
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def clean_doi(d):
    if not d:
        return ""
    m = DOI_RE.search(d)
    return m.group(0).lower().rstrip(".)") if m else ""


# corpus 식별자 집합
corpus_dois, corpus_titles = set(), set()
for s in SIDE.glob("*.json"):
    try:
        j = json.loads(s.read_text(encoding="utf-8"))
    except Exception:
        continue
    d = clean_doi(j.get("doi", ""))
    if d:
        corpus_dois.add(d)
    t = norm((j.get("bibliographic") or {}).get("title", ""))
    if len(t) >= 20:
        corpus_titles.add(t[:50])

# 660 PDF 경로 인덱스
names = json.loads(GAP.read_text(encoding="utf-8"))["n741_pdf_no_corpus"]
pdf_paths = {}
for root in PDF_ROOTS:
    if root.exists():
        for p in root.rglob("*.pdf"):
            pdf_paths.setdefault(p.name, p)


def pdf_doi_title(path):
    try:
        doc = fitz.open(path)
        meta_doi = clean_doi(doc.metadata.get("doi") or doc.metadata.get("subject") or "")
        txt = ""
        for pg in range(min(2, doc.page_count)):
            txt += doc[pg].get_text()
        doc.close()
        doi = meta_doi or clean_doi(txt)
        return doi, txt
    except Exception:
        return None, ""


dup_doi, dup_title, new, nodoi_notext = [], [], [], []
for n in names:
    path = pdf_paths.get(n)
    if not path:
        nodoi_notext.append(n)
        continue
    doi, txt = pdf_doi_title(path)
    if doi and doi in corpus_dois:
        dup_doi.append({"pdf": n, "doi": doi})
    elif txt and any(t in norm(txt[:400]) for t in corpus_titles):
        dup_title.append(n)
    elif doi or txt.strip():
        new.append({"pdf": n, "doi": doi or ""})
    else:
        nodoi_notext.append(n)   # 텍스트 없음(스캔이미지) → 판별 불가

res = {
    "total": len(names),
    "corpus_dois": len(corpus_dois),
    "dup_by_doi": len(dup_doi),
    "dup_by_title": len(dup_title),
    "genuinely_new": len(new),
    "undetermined_no_text": len(nodoi_notext),
}
OUT.write_text(json.dumps({**res, "new_sample": new[:40], "dup_doi_sample": dup_doi[:15],
                           "undetermined": nodoi_notext[:20]}, ensure_ascii=False, indent=1), encoding="utf-8")
print("=== 660 PDF, DOI/제목 provenance 판별 ===")
for k, v in res.items():
    print(f"  {k:22} {v}")
print(f"\n=== 진짜 신규 샘플 (DOI 있고 corpus에 없음) ===")
for r in new[:18]:
    print(f"   + {r['pdf'][:46]:48} {r['doi']}")
print(f"\n=== DOI 중복 샘플 (raw 파일명 → corpus DOI 일치) ===")
for r in dup_doi[:8]:
    print(f"   = {r['pdf'][:40]:42} {r['doi']}")
print(f"\nreport: {OUT}")
