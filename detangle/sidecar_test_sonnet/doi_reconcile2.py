"""정정판: corpus의 OWN PDF page-1 DOI를 기준(레퍼런스 오염 회피).
universe(refs+D:) PDF page-1 DOI vs corpus PDF page-1 DOI. DOI 캐싱."""
import os, re, glob, json, sys
sys.stdout.reconfigure(encoding="utf-8")
import fitz
fitz.TOOLS.mupdf_display_errors(False)

CORPUS_PDFS = r"G:\corpus_20260624\pdfs"
UNIV = [r"G:\corpus_refs_v20260616\papers", r"D:\Academia\References"]
DOI = re.compile(r"10\.\d{4,9}/[A-Za-z0-9._;()/:+\-]+")
def norm(d): return re.sub(r"[).,;\]>]+$", "", d.lower())
def pdf_doi(path):
    try:
        d = fitz.open(path); t = "".join(d[i].get_text() for i in range(min(2, len(d)))); d.close()
        m = DOI.search(t); return norm(m.group(0)) if m else None
    except: return None

def scan(dirs, label):
    res = {}
    n = 0
    for d in (dirs if isinstance(dirs, list) else [dirs]):
        for f in glob.glob(os.path.join(d, "**", "*.pdf"), recursive=True):
            n += 1
            if n % 300 == 0: print(f"   {label} ...{n}", flush=True)
            res[f] = pdf_doi(f)
    print(f"  {label}: {n} PDF, DOI보유 {sum(1 for v in res.values() if v)}", flush=True)
    return res

print("corpus PDF page-1 DOI...", flush=True)
corpus = scan(CORPUS_PDFS, "corpus")
corpus_dois = set(v for v in corpus.values() if v)
print(f"corpus own-DOI 유니크: {len(corpus_dois)}\n", flush=True)

print("universe PDF page-1 DOI...", flush=True)
univ = scan(UNIV, "univ")

seen = set(); matched = []; gap = []; no_doi = []
for f, doi in univ.items():
    nm = os.path.basename(f)
    if not doi: no_doi.append(nm); continue
    if doi in seen: continue
    seen.add(doi)
    if doi in corpus_dois: matched.append(nm)
    else: gap.append({"pdf": nm, "doi": doi, "path": f})

print(f"\n=== 정정 reconciliation (corpus PDF 기준) ===")
print(f"universe PDF 유니크DOI {len(seen)} | DOI없음 {len(no_doi)}")
print(f"  ✓ 정본에 있음: {len(matched)}")
print(f"  ✗ 갭(정본 PDF에 없음): {len(gap)}")
json.dump({"corpus_doi_count": len(corpus_dois), "matched": len(matched),
           "gap": gap, "no_doi_count": len(no_doi), "no_doi_sample": no_doi[:50]},
          open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\DOI_RECONCILE2.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n=== 갭 샘플 50 ===")
for g in gap[:50]: print(f"  ✗ {g['pdf'][:55]}  [{g['doi'][:34]}]")
print("→ DOI_RECONCILE2.json")
