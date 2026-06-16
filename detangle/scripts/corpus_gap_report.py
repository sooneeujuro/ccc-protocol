#!/usr/bin/env python3
"""corpus_gap_report.py — 187/741/9/13 갭 카테고리 구체화 (READ-ONLY, self-contained).

corpus↔PDF, supp↔corpus 매칭을 자체 재계산(백그라운드 복사와 독립).
"""
import re
import json
from collections import Counter
from pathlib import Path

ART = Path(r"G:\corpus_md_export_20260612\articles")
PDF_ROOTS = [
    Path(r"G:\RefDB\동환상\extracted"), Path(r"G:\RefDB\홍씨\JP (sooneeujuro)"),
    Path(r"G:\RefDB\홍씨\김동환 (sooneeujuro)"), Path(r"G:\RefDB\LostnFound"),
    Path(r"G:\WonheeLee\논문"), Path(r"G:\WonheeLee\References"),
]
SUPP = Path(r"G:\WonheeLee\논문_Supplementary material")
D = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", re.sub(r"\.(md|pdf)$", "", s.lower()))


def norm_supp(s):
    return re.sub(r"sm\d*$", "", norm(s))


def kor(s):
    return bool(re.search(r"[가-힣]", s))


def year(s):
    m = re.search(r"(19|20)\d{2}", s)
    return m.group(0) if m else "?"


KWS = ["volcan", "mantle", "isotop", "basalt", "magma", "subduction", "geochron", "melt",
       "peridotit", "eruption", "co2", "helium", "nitrogen", "groundwater", "seismic", "tecton"]

# ---- corpus ↔ PDF ----
md = {norm(p.stem): p.name for p in ART.glob("*.md")}
pdf = {}
for root in PDF_ROOTS:
    if root.exists():
        for p in root.rglob("*.pdf"):
            pdf.setdefault(norm(p.stem), p)
exact = set(md) & set(pdf)
md_un, pdf_un = set(md) - exact, set(pdf) - exact
md_pre = {}
for k in md_un:
    md_pre.setdefault(k[:40], []).append(k)
pre_md, pre_pdf = set(), set()
for k in pdf_un:
    pk = k[:40]
    if pk in md_pre and len(md_pre[pk]) == 1:
        pre_md.add(md_pre[pk][0]); pre_pdf.add(k)
n187 = sorted(md[k] for k in (md_un - pre_md))
out741 = sorted(pdf[k].name for k in (pdf_un - pre_pdf))

# ---- supp ↔ corpus ----
supp = {}
for d in SUPP.iterdir():
    if d.is_dir():
        k = norm_supp(d.name)
        if len(k) >= 8:
            supp.setdefault(k, []).append(d.name)
ambig, nomatch = {}, []
for sk, dirs in sorted(supp.items()):
    cands = [md[mk] for mk in md if mk.startswith(sk)]
    if len(cands) == 1 and len(dirs) == 1:
        pass
    elif len(cands) == 0:
        nomatch += dirs
    else:
        ambig[sk] = {"supp": dirs, "corpus": cands}

print("======== 187 = corpus인데 PDF 없음 (진짜 갭) ========")
print(f"  {len(n187)}편 | 한글 {sum(map(kor,n187))} / 영문 {sum(not kor(x) for x in n187)}")
print("  연도:", dict(sorted(Counter(year(x) for x in n187).items())))
for x in n187[:8]:
    print("   -", x[:68])

print("\n======== 741 = corpus 밖 PDF (신규 논문 후보) ========")
print(f"  {len(out741)}편 | 한글 {sum(map(kor,out741))} / 영문 {sum(not kor(x) for x in out741)}")
print("  연도:", dict(sorted(Counter(year(x) for x in out741).items())))
tc = Counter(t for x in out741 for t in KWS if t in x.lower())
print("  주제kw:", dict(tc.most_common(10)))
print("  영문 샘플:")
for x in [x for x in out741 if not kor(x)][:10]:
    print("   -", x[:68])
print("  한글 샘플:")
for x in [x for x in out741 if kor(x)][:6]:
    print("   -", x[:55])

print(f"\n======== 9 = supp 모호 ({len(ambig)}) ========")
for sk, info in ambig.items():
    print(f"  '{info['supp'][0]}' ↔ corpus {len(info['corpus'])}편: " + " | ".join(c[:34] for c in info['corpus'][:3]))

print(f"\n======== 13 = supp인데 corpus 없음 ({len(nomatch)}) ========")
for x in nomatch:
    print("   -", x[:66])

(D / "CORPUS_GAP_REPORT.json").write_text(json.dumps(
    {"n187_corpus_no_pdf": n187, "n741_pdf_no_corpus": out741,
     "supp_ambiguous": ambig, "supp_nomatch": nomatch}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"\nreport: {D/'CORPUS_GAP_REPORT.json'}")
