"""17권 정확 매칭: 각 book4_md 폴더 -> 소스 PDF(키워드, 최대페이지) -> 페이지수."""
import os, glob, sys
sys.stdout.reconfigure(encoding="utf-8")
import fitz
fitz.TOOLS.mupdf_display_errors(False)

CAND = [r"D:\Academia\References", r"C:\Users\USER\Documents\References",
        r"G:\WonheeLee\References", r"G:\book_cook_in", r"G:\corpus_refs_v20260616"]
# book4_md 폴더 -> (필수키워드들 중 전부 포함, 최소페이지)
SPEC = {
 "burnard_2013_noble_gases":      (["burnard"], 80),
 "clark_fritz_1997":              (["clark","fritz"], 100),
 "cook_2000_env_tracers":         (["cook","environmental"], 100),
 "faure_mensing_2005":            (["faure"], 200),
 "german_2010_rainbow_36n":       (["german","rainbow"], 1),
 "humphris/seyfried_1995_book":   (["seafloor","hydrothermal"], 200),
 "iupac_solubility_vol62":        (["iupac"], 1),
 "karlstrom_2012_rocky_mtn":      (["karlstrom"], 1),
 "klein_2019_abiotic_methane":    (["klein","abiotic"], 1),
 "mccollom_2006":                 (["mccollom"], 1),
 "mcdermott_abiotic_org":         (["mcdermott"], 1),
 "ozima_podosek_2002":            (["ozima"], 1),
 "rudnick_gao_2003_ccrust":       (["rudnick"], 1),
 "ryan_2009_gmrt":                (["ryan","gmrt"], 1),
 "seyfried_1995_phase_equil":     (["seyfried","phase"], 1),
 "taran_2007_fischer":            (["taran"], 1),
 "teos10_seawater":               (["teos"], 1),
}
# 전체 PDF 인덱스 (이름,페이지,경로)
allpdf = []
for d in CAND:
    if os.path.isdir(d):
        for f in glob.glob(os.path.join(d, "**", "*.pdf"), recursive=True):
            allpdf.append((os.path.basename(f).lower(), f))

def pages(f):
    try: doc = fitz.open(f); n = doc.page_count; doc.close(); return n
    except: return -1

print(f"{'book4_md 폴더':30} {'pages':>6}  소스 PDF")
tot = 0; found = 0
for book,(kws,minp) in SPEC.items():
    best = None
    for nm,f in allpdf:
        if all(k in nm for k in kws):
            p = pages(f)
            if p >= minp and (best is None or p > best[0]): best = (p, f)
    if best:
        found += 1; tot += best[0]
        print(f"{book:30} {best[0]:>6}  {os.path.basename(best[1])[:46]}")
    else:
        print(f"{book:30} {'?':>6}  (PDF 못찾음)")
print(f"\n매칭 {found}/17 | 총 페이지(중복 seyfried/humphris 주의): {tot}")
