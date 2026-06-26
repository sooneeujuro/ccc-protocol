"""신뢰가능 reconciliation: 논문 OWN DOI로 매칭(파일명 X).
PDF 1~2p + corpus MD head에서 첫 DOI(=논문 자체 DOI, 레퍼런스 아님) 추출 → 비교."""
import os, re, glob, json, sys
sys.stdout.reconfigure(encoding="utf-8")
import fitz

PDF_DIRS = [r"G:\corpus_refs_v20260616\papers", r"D:\Academia\References"]
CORPUS = r"G:\corpus_20260624\articles"
MD_RECOV = [r"G:\corpus_md_export_20260602\_renewal_20260609\_new_dup_quarantine",
            r"G:\corpus_md_export_20260602\_renewal_20260609\cha_out",
            r"G:\corpus_md_export_20260602\_renewal_20260609\kim_out",
            r"G:\corpus_md_export_20260602\_renewal_20260609\nuc_out"]
DOI = re.compile(r"10\.\d{4,9}/[A-Za-z0-9._;()/:+\-]+")
def norm(d): return re.sub(r"[).,;\]>]+$", "", d.lower())
def first_doi(text):
    m = DOI.search(text); return norm(m.group(0)) if m else None

def md_doi(path, n=3500):
    try: return first_doi(open(path, encoding="utf-8", errors="replace").read(n))
    except: return None
def pdf_doi(path):
    try:
        d = fitz.open(path); t = "".join(d[i].get_text() for i in range(min(2, len(d)))); d.close()
        return first_doi(t)
    except: return None

print("corpus MD own-DOI 추출...", flush=True)
corpus_dois = set()
cn = 0
for f in glob.glob(os.path.join(CORPUS, "*.md")):
    d = md_doi(f); cn += 1
    if d: corpus_dois.add(d)
print(f"  corpus MD {cn}개, own-DOI {len(corpus_dois)}개 보유", flush=True)

print("복구가능 MD own-DOI 추출...", flush=True)
recov_dois = set()
for dd in MD_RECOV:
    for f in glob.glob(os.path.join(dd, "*.md")):
        d = md_doi(f)
        if d: recov_dois.add(d)
print(f"  복구가능 MD own-DOI {len(recov_dois)}개", flush=True)

print("PDF own-DOI 추출(fitz)...", flush=True)
seen = set(); matched = 0; gap_recov = []; gap_none = []; no_doi = []; total = 0
for d in PDF_DIRS:
    for f in glob.glob(os.path.join(d, "**", "*.pdf"), recursive=True):
        total += 1
        if total % 200 == 0: print(f"   ...{total}", flush=True)
        doi = pdf_doi(f)
        nm = os.path.basename(f)
        if not doi: no_doi.append(nm); continue
        if doi in seen: continue            # 중복 PDF
        seen.add(doi)
        if doi in corpus_dois: matched += 1
        elif doi in recov_dois: gap_recov.append({"pdf": nm, "doi": doi})
        else: gap_none.append({"pdf": nm, "doi": doi})

print(f"\n=== DOI reconciliation ===")
print(f"PDF 총 {total} | DOI 없음(스캔본/추출실패) {len(no_doi)} | 유니크 DOI {len(seen)}")
print(f"  ✓ 정본에 있음: {matched}")
print(f"  ⚠ 갭-복구가능(quarantine/renewal에 MD有): {len(gap_recov)}")
print(f"  ✗ 갭-미추출(MD 아예 없음): {len(gap_none)}")
json.dump({"matched": matched, "gap_recoverable": gap_recov, "gap_never": gap_none,
           "no_doi_count": len(no_doi), "no_doi_sample": no_doi[:40]},
          open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\DOI_RECONCILE.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n=== 갭-미추출 (DOI 있고 corpus/quarantine 어디에도 없음) ===")
for g in gap_none[:40]: print(f"  ✗ {g['pdf'][:55]}  [{g['doi'][:35]}]")
print("→ DOI_RECONCILE.json")
