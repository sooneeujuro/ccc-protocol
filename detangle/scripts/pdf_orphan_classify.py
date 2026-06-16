#!/usr/bin/env python3
"""pdf_orphan_classify.py — 660 corpus-밖 PDF 신규/중복 판별 (READ-ONLY, deterministic).

vision 없이 fitz(PyMuPDF)로 텍스트만 추출 → too long 원천 차단.
  - 제목형 파일명: 파일명 = 제목 (이미 corpus 매칭 실패했으므로 신규 후보).
  - raw 파일명(1-s2.0 / uuid / main 등): PDF 첫 페이지에서 '최대 폰트' 텍스트 = 제목 추출.
제목 정규화 prefix(30자)로 corpus 중복 확인. 주제 키워드로 적합성 판정.
"""
import re
import json
import fitz
from pathlib import Path

GAP = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\CORPUS_GAP_REPORT.json")
ART = Path(r"G:\corpus_md_export_20260612\articles")
OUT = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\PDF_ORPHAN_CLASSIFY.json")
PDF_ROOTS = [
    Path(r"G:\RefDB\동환상\extracted"), Path(r"G:\RefDB\홍씨\JP (sooneeujuro)"),
    Path(r"G:\RefDB\홍씨\김동환 (sooneeujuro)"), Path(r"G:\RefDB\LostnFound"),
    Path(r"G:\WonheeLee\논문"), Path(r"G:\WonheeLee\References"),
]
KW = ["volcan", "mantle", "isotop", "basalt", "magma", "subduction", "geochron", "melt",
      "peridotit", "eruption", "co2", "helium", "nitrogen", "noble gas", "groundwater",
      "hydrotherm", "seismic", "tecton", "oxygen", "argon", "xenolith", "trace element",
      "rare earth", "gondwana", "lithos", "ridge", "plume", "metasoma", "olivine",
      "crust", "subduct", "geochem", "petrogen", "zircon", "fluid", "carbon"]
RAW = re.compile(r"^(1-s2\.0|[0-9a-f]{8}-[0-9a-f]{4}|\d{6,}|main\.pdf|sciencedirect|\(\d|science)", re.I)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", re.sub(r"\.(md|pdf)$", "", s.lower()))


def is_raw(name):
    stem = name.rsplit(".", 1)[0]
    return bool(RAW.match(name)) or len(re.sub(r"[^a-zA-Z]", "", stem)) < 6


def title_from_pdf(path):
    try:
        doc = fitz.open(path)
        d = doc[0].get_text("dict")
        doc.close()
        spans = [(s["size"], s["text"].strip()) for b in d.get("blocks", [])
                 for l in b.get("lines", []) for s in l.get("spans", []) if s["text"].strip()]
        if not spans:
            return ""
        mx = max(s[0] for s in spans)
        return " ".join(t for sz, t in spans if sz >= mx - 0.4 and len(t) > 2)[:220]
    except Exception:
        return None


names = json.loads(GAP.read_text(encoding="utf-8"))["n741_pdf_no_corpus"]

pdf_paths = {}
for root in PDF_ROOTS:
    if root.exists():
        for p in root.rglob("*.pdf"):
            pdf_paths.setdefault(p.name, p)

md_pre = {}
for p in ART.glob("*.md"):
    n = norm(p.stem)
    md_pre.setdefault(n[:30], []).append(p.stem)

res = {"duplicate": [], "new_relevant": [], "new_irrelevant": [], "unreadable": [], "not_found": []}
n_raw = 0
for name in names:
    path = pdf_paths.get(name)
    if not path:
        res["not_found"].append(name)
        continue
    if is_raw(name):
        n_raw += 1
        title = title_from_pdf(path)
        if title is None:
            res["unreadable"].append(name)
            continue
        if not title:
            title = name
    else:
        title = name.rsplit(".", 1)[0].replace("_", " ")
    tn = norm(title)
    is_dup = len(tn) >= 20 and tn[:30] in md_pre
    rec = {"name": name, "title": title[:90]}
    if is_dup:
        rec["corpus"] = md_pre[tn[:30]][0][:60]
        res["duplicate"].append(rec)
    elif any(k in title.lower() for k in KW):
        res["new_relevant"].append(rec)
    else:
        res["new_irrelevant"].append(rec)

OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"총 {len(names)}편 | raw(fitz추출) {n_raw} / 제목형 {len(names)-n_raw}")
for k in ("duplicate", "new_relevant", "new_irrelevant", "unreadable", "not_found"):
    print(f"  {k:15} {len(res[k])}")
print("\n=== new_relevant 샘플 12 ===")
for r in res["new_relevant"][:12]:
    print("   +", r["title"][:72])
print("\n=== duplicate 샘플 8 (raw→corpus 복원) ===")
for r in res["duplicate"][:8]:
    print(f"   = {r['name'][:32]} → {r.get('corpus','')[:42]}")
print(f"\nreport: {OUT}")
