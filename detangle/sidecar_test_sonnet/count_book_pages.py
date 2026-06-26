"""책 17권 PDF 찾아 페이지수 카운트 → 재추출 비용 산정용."""
import os, glob, sys, re
sys.stdout.reconfigure(encoding="utf-8")
import fitz
fitz.TOOLS.mupdf_display_errors(False)

CAND = [r"D:\Academia\References\Books", r"C:\Users\USER\Documents\References\Books",
        r"G:\WonheeLee\References\Books", r"G:\book_cook_in", r"G:\books_rebuild",
        r"G:\Paper_Atelier", r"D:\Academia\References", r"G:\corpus_refs_v20260616"]
# 17권 키워드
BOOKS = ["burnard","clark_fritz","clark","fritz","cook","faure","mensing","german","rainbow",
         "humphris","seafloor","iupac","solubility","karlstrom","rocky","klein","abiotic_methane",
         "mccollom","mcdermott","ozima","podosek","rudnick","gao","ccrust","ryan","gmrt",
         "seyfried","phase_equil","taran","fischer","teos","seawater","noble_gas","noble gases"]

seen = {}
for d in CAND:
    if not os.path.isdir(d): continue
    for f in glob.glob(os.path.join(d, "**", "*.pdf"), recursive=True):
        nm = os.path.basename(f).lower()
        if any(k in nm for k in BOOKS):
            key = os.path.basename(f)
            if key in seen: continue
            try:
                doc = fitz.open(f); pg = doc.page_count; doc.close()
            except Exception as e:
                pg = -1
            mb = os.path.getsize(f)//(1024*1024)
            seen[key] = (pg, mb, f)

print(f"{'PDF':62} {'pages':>6} {'MB':>5}")
tot = 0
for k in sorted(seen):
    pg, mb, f = seen[k]
    if pg > 0: tot += pg
    print(f"{k[:62]:62} {pg:>6} {mb:>5}")
print(f"\n발견 PDF: {len(seen)}권 | 총 페이지: {tot}")
