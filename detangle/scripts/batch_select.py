#!/usr/bin/env python3
"""batch_select.py <N> — 재추출 배치 N편 선정 (충돌 figure 참조 ∩ PDF 보유). READ-ONLY.

이미 corpus_rebuild_20260618 에 .done 인 건 제외(중복 추출 방지). PDF 경로 출력.
"""
import re
import sys
import json
import hashlib
from pathlib import Path
from collections import defaultdict

N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
ART = Path(r"G:\corpus_md_export_20260612\articles")
REBUILD = Path(r"G:\corpus_rebuild_20260618")
PDF_ROOTS = [
    Path(r"G:\RefDB\동환상\extracted"), Path(r"G:\RefDB\홍씨\JP (sooneeujuro)"),
    Path(r"G:\RefDB\홍씨\김동환 (sooneeujuro)"), Path(r"G:\RefDB\LostnFound"),
    Path(r"G:\WonheeLee\논문"), Path(r"G:\WonheeLee\References"),
]
OUT = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\BATCH1.json")
IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
BARE = re.compile(r"^([0-9a-f]{32})_img\.(jpg|jpeg|png)$")
CRUFT = re.compile(r"logo|check for update|crossmark|elsevier|springer|wiley|cover image|pergamon|\borcid\b|journal of", re.I)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", re.sub(r"\.(md|pdf)$", "", s.lower()))


def slug(pid):
    return hashlib.md5(pid.encode("utf-8")).hexdigest()[:12]


# 이미 추출 완료된 slug (중복 방지). convert_pdfs slug = md5(PDF stem) 기준이므로 PDF stem으로 비교.
done = set()
if REBUILD.exists():
    done = {d.name for d in REBUILD.iterdir() if d.is_dir() and (d / ".done").exists()}

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
contam = sorted(stem for stem, hs in mdh.items() if hs & fig_h)

pdf = {}
for root in PDF_ROOTS:
    if root.exists():
        for p in root.rglob("*.pdf"):
            pdf.setdefault(norm(p.stem), p)
pdf_pre = defaultdict(list)
for k, p in pdf.items():
    pdf_pre[k[:40]].append((k, p))

matched = []
for stem in contam:
    mn = norm(stem)
    hit = None
    if mn in pdf:
        hit = pdf[mn]
    else:
        pk = mn[:40]
        if pk in pdf_pre and len(pdf_pre[pk]) == 1:
            hit = pdf_pre[pk][0][1]
    if not hit:
        continue
    if slug(hit.stem) in done:   # 이미 추출됨
        continue
    matched.append({"md_stem": stem, "pdf": str(hit), "slug": slug(hit.stem)})
    if len(matched) >= N:
        break

OUT.write_text(json.dumps(matched, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"충돌 figure md: {len(contam)} | 이미 추출(done): {len(done)}")
print(f"배치 선정: {len(matched)} 편 (목표 {N})")
print(f"PDF 소스 분포:")
from collections import Counter
c = Counter(Path(m["pdf"]).parent.name for m in matched)
for k, v in c.most_common():
    print(f"  {k}: {v}")
print(f"saved -> {OUT}")
