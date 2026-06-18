#!/usr/bin/env python3
"""pilot_select.py — 재추출 파일럿 10편 선정 (충돌 figure 참조 ∩ PDF 보유). READ-ONLY."""
import re
import json
from pathlib import Path
from collections import defaultdict

ART = Path(r"G:\corpus_md_export_20260612\articles")
PDF_ROOTS = [
    Path(r"G:\RefDB\동환상\extracted"), Path(r"G:\RefDB\홍씨\JP (sooneeujuro)"),
    Path(r"G:\RefDB\홍씨\김동환 (sooneeujuro)"), Path(r"G:\RefDB\LostnFound"),
    Path(r"G:\WonheeLee\논문"), Path(r"G:\WonheeLee\References"),
]
OUT = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\PILOT10.json")
IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
BARE = re.compile(r"^([0-9a-f]{32})_img\.(jpg|jpeg|png)$")
CRUFT = re.compile(r"logo|check for update|crossmark|elsevier|springer|wiley|cover image|pergamon|\borcid\b|journal of", re.I)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", re.sub(r"\.(md|pdf)$", "", s.lower()))


href = defaultdict(list); mdh = defaultdict(set)
for md in ART.glob("*.md"):
    try:
        t = md.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    for m in IMG.finditer(t):
        n = m.group(2).strip().replace(chr(92), "/").rsplit("/", 1)[-1]
        b = BARE.match(n)
        if b:
            href[b.group(1)].append(m.group(1) or "")
            mdh[md.stem].add(b.group(1))
col = {h: v for h, v in href.items() if len(v) > 1}
cruft_h = {h for h in col if sum(1 for a in href[h] if CRUFT.search(a)) >= max(1, len(href[h]) * 0.5)}
fig_h = set(col) - cruft_h
contam = {stem for stem, hs in mdh.items() if hs & fig_h}

pdf = {}
for root in PDF_ROOTS:
    if root.exists():
        for p in root.rglob("*.pdf"):
            pdf.setdefault(norm(p.stem), p)
pdf_pre = defaultdict(list)
for k, p in pdf.items():
    pdf_pre[k[:40]].append((k, p))

matched = []
for stem in sorted(contam):
    mn = norm(stem)
    hit = None
    if mn in pdf:
        hit = pdf[mn]
    else:
        pk = mn[:40]
        if pk in pdf_pre and len(pdf_pre[pk]) == 1:
            hit = pdf_pre[pk][0][1]
    if hit:
        matched.append((stem, hit))
    if len(matched) >= 10:
        break

print(f"충돌 figure 참조 md: {len(contam)} | PDF 매칭 파일럿: {len(matched)}")
res = []
for stem, p in matched[:10]:
    print(f"  MD : {stem[:56]}")
    print(f"  PDF: {str(p)[:84]}")
    res.append({"md_stem": stem, "pdf": str(p)})
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"saved -> {OUT}")
