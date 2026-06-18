#!/usr/bin/env python3
"""corpus_sanitize_estimate.py — 재추출 견적 (READ-ONLY, 비용 0).

corpus 3903편을 '추출 시점부터 오염(cruft alt-text)' vs '깨끗'으로 deterministic 분류.
+ 이번 세션 수선 51편(그림 refill) + PDF 보유 교차 → 재추출 가능 대상 견적.
vision 안 씀(키워드/메타만) → 하한 추정. 실제 오염은 이보다 많을 수 있음(alt에 흔적 없는 cruft).
"""
import re
import json
from pathlib import Path

ART = Path(r"G:\corpus_md_export_20260612\articles")
D = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
# 추출 시점 cruft 흔적 (저널 로고/UI/플랫폼). 단어경계로 false-positive 줄임.
CRUFT = re.compile(
    r"\blogo\b|check for update|\borcid\b|crossmark|elsevier|springer|wiley|"
    r"taylor\s*&?\s*francis|geology review|image:\s*logo|view profile|"
    r"researchgate|figshare|\bscopus\b|publons|sci-hub|download pdf", re.I)

# 이번 세션 수선 51편(그림 refill) — DOI_PROVENANCE/RECON 기준 slug
recon = D / "FIG_COVERAGE_RECON.json"
repaired_slugs = set()
if recon.exists():
    try:
        r = json.loads(recon.read_text(encoding="utf-8"))
        for row in r.get("rows", []):
            if isinstance(row, dict) and row.get("slug"):
                repaired_slugs.add(row["slug"])
    except Exception:
        pass

# PDF 보유 (재추출 가능 대상 교차용)
pdfmap = D / "PDF_CORPUS_MAP.json"
have_pdf_md = set()
if pdfmap.exists():
    j = json.loads(pdfmap.read_text(encoding="utf-8"))
    # exact_sample/prefix_sample은 일부라, corpus_without_pdf로 역산
    no_pdf = set(j.get("corpus_without_pdf", []))
else:
    no_pdf = set()

contaminated, clean = [], []
cruft_examples = {}
for md in ART.glob("*.md"):
    t = md.read_text(encoding="utf-8", errors="replace")
    alts = [m.group(1) for m in IMG_RE.finditer(t) if m.group(1)]
    hits = [a for a in alts if CRUFT.search(a)]
    if hits:
        contaminated.append(md.name)
        if len(cruft_examples) < 12:
            cruft_examples[md.name] = list(dict.fromkeys(hits))[:3]
    else:
        clean.append(md.name)

total = len(contaminated) + len(clean)
contam_no_pdf = sum(1 for m in contaminated if m in no_pdf)

print(f"=== 재추출 견적 (deterministic, 비용 0 / 하한 추정) ===")
print(f"  corpus 총                 {total}")
print(f"  cruft alt-text 오염        {len(contaminated)}  ({100*len(contaminated)/total:.1f}%)")
print(f"  깨끗(흔적 없음)            {len(clean)}")
print(f"  ─ 오염 중 PDF 없음(재추출 불가) {contam_no_pdf}")
print(f"  ─ 오염 중 PDF 있음(재추출 가능) {len(contaminated)-contam_no_pdf}")
print(f"  (참고) 이번 세션 수선 slug   {len(repaired_slugs)}")
print(f"\n=== cruft 오염 샘플 (MD → alt-text 흔적) ===")
for m, ex in cruft_examples.items():
    print(f"  {m[:50]:52} {ex}")

(D / "CORPUS_SANITIZE_ESTIMATE.json").write_text(json.dumps({
    "total": total, "contaminated_cruft": len(contaminated), "clean": len(clean),
    "contam_no_pdf": contam_no_pdf, "contam_have_pdf": len(contaminated) - contam_no_pdf,
    "contaminated_list": sorted(contaminated),
}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"\nreport: {D/'CORPUS_SANITIZE_ESTIMATE.json'}")
