"""오격리 34편: MD(quarantine) + PDF(refs/batch/D:) 짝 확인 → 복구셋. 감으로 안 하고 검증."""
import os, re, json, sys, glob
sys.stdout.reconfigure(encoding="utf-8")
Q = r"G:\corpus_md_export_20260602\_renewal_20260609\_new_dup_quarantine"
miss = json.load(open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\QUARANTINE_MISSING.json", encoding="utf-8"))
PDF_DIRS = [r"G:\corpus_refs_v20260616\papers", r"G:\batch1_in", r"G:\batch5_in", r"G:\batch6_in",
            r"G:\corpus_pdfs", r"D:\Academia\References"]

# 모든 PDF 인덱싱 (title 토큰)
def toks(s): return set(re.findall(r"[a-z0-9]{3,}", s.lower()))
pdfs = []
for d in PDF_DIRS:
    if os.path.isdir(d):
        for f in glob.glob(os.path.join(d, "**", "*.pdf"), recursive=True):
            name = re.sub(r"^[0-9a-f]{8,16}__", "", os.path.basename(f)[:-4])
            pdfs.append((toks(name), f))

paired = []; md_only = []
for title in miss:
    mt = toks(title)
    mdpath = os.path.join(Q, title + ".md")
    md_ok = os.path.exists(mdpath)
    best = (0, None)
    for pt, pf in pdfs:
        j = len(mt & pt)/max(1, len(mt | pt))
        if j > best[0]: best = (j, pf)
    if best[0] >= 0.45:
        paired.append((title[:55], round(best[0],2), best[1]))
    else:
        md_only.append((title[:55], md_ok, round(best[0],2)))

print(f"오격리 {len(miss)}편 짝 확인:")
print(f"  MD+PDF 둘 다 있음(완전 복구가능): {len(paired)}")
print(f"  MD만(PDF 못찾음): {len(md_only)}")
print(f"\n=== MD+PDF 짝 맞음 (복구셋) ===")
for t,j,pf in paired:
    print(f"  ✓ {t}  ←PDF {os.path.basename(pf)[:40]}")
print(f"\n=== PDF 못찾음 (MD만, PDF 위치 추가확인 필요) ===")
for t,mok,j in md_only:
    print(f"  ? {t}  (MD={mok}, best_pdf_j={j})")
json.dump({"paired":[{"title":t,"pdf":pf} for t,j,pf in paired], "md_only":[t for t,m,j in md_only]},
          open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\RECOVERY_SET.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n→ RECOVERY_SET.json 저장")
