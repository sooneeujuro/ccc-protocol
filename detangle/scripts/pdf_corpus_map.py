#!/usr/bin/env python3
"""pdf_corpus_map.py — corpus(MD) ↔ RefDB/WonheeLee PDF 매칭 + (--apply) corpus명 복사.

제목 정규화 exact → prefix(앞40자, corpus 유일) 매칭. 검증: prefix 샘플 12/12 정확.
--apply: 매칭 PDF를 G:\corpus_pdfs\<corpus_md_stem>.pdf 로 복사(additive, idempotent).
dry-run(기본): 통계만.
"""
import re
import json
import sys
import shutil
from pathlib import Path

ART = Path(r"G:\corpus_md_export_20260612\articles")
PDF_ROOTS = [
    Path(r"G:\RefDB\동환상\extracted"),
    Path(r"G:\RefDB\홍씨\JP (sooneeujuro)"),
    Path(r"G:\RefDB\홍씨\김동환 (sooneeujuro)"),
    Path(r"G:\RefDB\LostnFound"),
    Path(r"G:\WonheeLee\논문"),
    Path(r"G:\WonheeLee\References"),
]
OUT = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\PDF_CORPUS_MAP.json")
DST = Path(r"G:\corpus_pdfs")
APPLY = "--apply" in sys.argv


def norm(s):
    s = s.lower()
    s = re.sub(r"\.(md|pdf)$", "", s)
    return re.sub(r"[^a-z0-9]", "", s)


md = {norm(p.stem): p.name for p in ART.glob("*.md")}

pdfs = []
for root in PDF_ROOTS:
    if root.exists():
        pdfs += [p for p in root.rglob("*.pdf")]
pdf = {}
dup = 0
for p in pdfs:
    k = norm(p.stem)
    if k in pdf:
        dup += 1
    else:
        pdf[k] = p

exact = set(md) & set(pdf)
md_un = set(md) - exact
pdf_un = set(pdf) - exact
PRE = 40
md_pre = {}
for k in md_un:
    md_pre.setdefault(k[:PRE], []).append(k)
pre_matched = {}
for k in list(pdf_un):
    pk = k[:PRE]
    if pk in md_pre and len(md_pre[pk]) == 1:
        pre_matched[md_pre[pk][0]] = k

# corpus_md_stem -> pdf Path (복사용)
copymap = {Path(md[k]).stem: pdf[k] for k in exact}
for mdk, pdfk in pre_matched.items():
    copymap[Path(md[mdk]).stem] = pdf[pdfk]

if APPLY:
    DST.mkdir(exist_ok=True)
    copied = skipped = fail = 0
    for stem, src in copymap.items():
        d = DST / (stem + ".pdf")
        try:
            if d.exists():
                skipped += 1
            else:
                shutil.copy2(src, d)
                copied += 1
        except OSError as e:
            print(f"  FAIL {stem}: {e}")
            fail += 1
    print(f"[APPLY] corpus_pdfs 복사: {copied} new, {skipped} skip, {fail} fail -> {DST}")

result = {
    "corpus_md": len(md), "pdf_total_files": len(pdfs), "pdf_unique_norm": len(pdf),
    "pdf_dup_norm": dup, "matched_exact": len(exact), "matched_prefix_extra": len(pre_matched),
    "matched_total": len(exact) + len(pre_matched),
    "corpus_without_pdf": len(md) - len(exact) - len(pre_matched),
    "pdf_without_corpus": len(pdf_un) - len(pre_matched),
}
OUT.write_text(json.dumps({"stats": result,
                           "exact_sample": {md[k]: pdf[k].name for k in sorted(exact)[:15]},
                           "prefix_sample": {md[mk]: pdf[pk].name for mk, pk in list(pre_matched.items())[:30]},
                           "corpus_without_pdf": sorted(md[k] for k in (md_un - set(pre_matched))),
                           "pdf_without_corpus": sorted(pdf[k].name for k in (pdf_un - set(pre_matched.values())))},
                          ensure_ascii=False, indent=1), encoding="utf-8")
print("=== PDF ↔ corpus 매칭 ===")
for k, v in result.items():
    print(f"  {k:24} {v}")
print(f"매칭률: {result['matched_total']}/{result['corpus_md']} = {100*result['matched_total']/result['corpus_md']:.1f}%")
print(f"report: {OUT}")
if not APPLY:
    print("복사하려면: python detangle/scripts/pdf_corpus_map.py --apply")
