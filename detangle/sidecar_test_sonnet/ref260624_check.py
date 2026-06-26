# -*- coding: utf-8 -*-
"""논문_260624 91 PDF가 0626 corpus에 있나 — DOI(fitz 본문) 기반 1차 대조.
파일명 fuzzy 금지. sidecar DOI + (2차는 본문 grep)."""
import fitz, os, re, json, sys
sys.stdout.reconfigure(encoding="utf-8")
PDFDIR = r"D:\Academia\References\논문_260624"
SIDE = r"G:\corpus_20260626\sidecars"
OUT = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\REF260624_CHECK.json"
DOI_RE = re.compile(r'10\.\d{4,9}/[^\s"<>}\])]+')
def ndoi(d): return re.sub(r'[).,;>]+$', '', d.strip().lower())

pdfs = sorted([f for f in os.listdir(PDFDIR) if f.lower().endswith(".pdf")])
pdf_doi = {}
for pf in pdfs:
    txt = ""
    try:
        doc = fitz.open(os.path.join(PDFDIR, pf))
        txt = "".join(doc[i].get_text() for i in range(min(3, len(doc))))
        doc.close()
    except Exception:
        pass
    seen = []
    for m in DOI_RE.finditer(txt):
        d = ndoi(m.group(0))
        if d not in seen: seen.append(d)
    pdf_doi[pf] = seen[:4]

# corpus sidecar DOI 셋
corpus_dois = set()
nside = nside_doi = 0
for f in os.listdir(SIDE):
    if not f.endswith(".json"): continue
    nside += 1
    try:
        d = json.load(open(os.path.join(SIDE, f), encoding="utf-8")).get("doi")
        if d: corpus_dois.add(ndoi(str(d))); nside_doi += 1
    except Exception:
        pass

matched = []; no_doi = []; unmatched = []
for pf in pdfs:
    ds = pdf_doi[pf]
    if not ds: no_doi.append(pf); continue
    hit = [d for d in ds if d in corpus_dois]
    if hit: matched.append((pf, hit[0]))
    else: unmatched.append((pf, ds))

print(f"PDF {len(pdfs)} | sidecar {nside}개(doi채워진 것 {nside_doi})")
print(f"-> sidecar DOI 매칭 {len(matched)} | DOI추출실패 {len(no_doi)} | DOI있는데 sidecar에없음 {len(unmatched)}")
json.dump({"pdf_doi": pdf_doi,
           "matched": [m[0] for m in matched],
           "no_doi": no_doi,
           "unmatched": [{"pdf": u[0], "dois": u[1]} for u in unmatched]},
          open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("저장:", OUT)
print(f"\n[sidecar DOI 미매칭 {len(unmatched)} — 2차 본문 grep 대상]")
for pf, ds in unmatched: print("  ", pf[:54], "|", (ds[0] if ds else ""))
print(f"\n[DOI 추출실패 {len(no_doi)} — 제목으로 2차]")
for pf in no_doi: print("  ", pf[:62])
