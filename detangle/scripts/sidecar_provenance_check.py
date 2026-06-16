#!/usr/bin/env python3
"""sidecar_provenance_check.py — 660 corpus-밖 PDF를 sidecar provenance로 정확 판별.

sidecar 파일명 = 원본 PDF stem. 따라서:
  - 660 PDF stem 이 sidecars/ 에 있으면 = 이미 변환됨 = corpus 중복(파일명 표기차로 fuzzy만 실패).
  - 없으면 = 진짜 미변환 = 신규 후보.
sidecar 있는 건 bibliographic.title / provenance.md_file 로 어느 논문인지까지 확인.
READ-ONLY.
"""
import json
from pathlib import Path

SIDE = Path(r"G:\corpus_md_export_20260612\sidecars")
GAP = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\CORPUS_GAP_REPORT.json")
OUT = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\SIDECAR_PROVENANCE_CHECK.json")

sidecar_stems = {p.stem: p for p in SIDE.glob("*.json")}
names = json.loads(GAP.read_text(encoding="utf-8"))["n741_pdf_no_corpus"]

dup_via_sidecar = []   # sidecar 있음 = 변환됨
genuinely_new = []     # sidecar 없음 = 신규
for n in names:
    stem = n.rsplit(".", 1)[0]
    if stem in sidecar_stems:
        info = {"pdf": n}
        try:
            j = json.loads(sidecar_stems[stem].read_text(encoding="utf-8"))
            info["title"] = (j.get("bibliographic") or {}).get("title", "")
            info["md_file"] = (j.get("provenance") or {}).get("md_file", "")
            info["doi"] = j.get("doi", "")
        except Exception:
            pass
        dup_via_sidecar.append(info)
    else:
        genuinely_new.append(n)

OUT.write_text(json.dumps({
    "total_660": len(names),
    "dup_via_sidecar": len(dup_via_sidecar),
    "genuinely_new": len(genuinely_new),
    "dup_sample": dup_via_sidecar[:15],
    "new_sample": genuinely_new[:30],
}, ensure_ascii=False, indent=1), encoding="utf-8")

print(f"=== 660 corpus-밖 PDF, sidecar provenance 판별 ===")
print(f"  총 {len(names)}")
print(f"  sidecar 있음 (이미 변환된 중복): {len(dup_via_sidecar)}")
print(f"  sidecar 없음 (진짜 신규 후보)  : {len(genuinely_new)}")
print(f"\n=== 중복 샘플 (raw PDF → sidecar가 가리키는 실제 논문) ===")
for d in dup_via_sidecar[:10]:
    print(f"  {d['pdf'][:34]:36} → {d.get('title','')[:50]}")
print(f"\n=== 진짜 신규 샘플 ===")
for n in genuinely_new[:15]:
    print("   +", n[:70])
print(f"\nreport: {OUT}")
