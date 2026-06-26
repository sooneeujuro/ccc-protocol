"""15권(cook 제외, seafloor/seyfried 1권) 원본 PDF를 G:\books_v5_in 에 모으기 + 매핑 보고.
키워드 정밀화(mcdermott/taran 오매칭 방지). 결제 전 눈검증용. COPY($0)."""
import os, glob, shutil, sys, json
sys.stdout.reconfigure(encoding="utf-8")
import fitz
fitz.TOOLS.mupdf_display_errors(False)
OUT = r"G:\books_v5_in"
os.makedirs(OUT, exist_ok=True)
CAND = [r"D:\Academia\References", r"C:\Users\USER\Documents\References",
        r"G:\WonheeLee\References", r"G:\book_cook_in"]
# book key -> (필수 키워드 전부포함, 최소페이지)
SPEC = {
 "faure_mensing_2005":          (["faure"], 200),
 "seafloor_hydrothermal_1995":  (["seafloor","hydrothermal"], 200),   # = humphris=seyfried 한 책
 "iupac_solubility_vol62_1996": (["iupac"], 100),
 "burnard_2013_noble_gases":    (["burnard","noble"], 80),
 "clark_fritz_1997":            (["clark","fritz"], 100),
 "ozima_podosek_2002":          (["ozima"], 100),
 "rudnick_gao_2003_ccrust":     (["rudnick"], 20),
 "taran_2007_fischer_tropsch":  (["taran","fischer"], 1),
 "karlstrom_2012":              (["karlstrom"], 1),
 "mcdermott_abiotic_org_synth": (["mcdermott","abiotic"], 1),
 "mccollom_2006":               (["mccollom"], 1),
 "ryan_2009_gmrt":              (["ryan","topography"], 1),
 "teos10_seawater_2010":        (["thermodynamic","seawater"], 1),
 "german_2010_rainbow":         (["german","rainbow"], 1),
 "klein_2019_abiotic_methane":  (["klein","abiotic"], 1),
}
allpdf = []
for d in CAND:
    if os.path.isdir(d):
        for f in glob.glob(os.path.join(d, "**", "*.pdf"), recursive=True):
            allpdf.append((os.path.basename(f).lower(), f))
def pages(f):
    try: d=fitz.open(f); n=d.page_count; d.close(); return n
    except: return -1

mapping=[]; tot=0
print(f"{'book key':30} {'pg':>5}  소스 PDF")
for book,(kws,minp) in SPEC.items():
    best=None
    for nm,f in allpdf:
        if all(k in nm for k in kws):
            p=pages(f)
            if p>=minp and (best is None or p>best[0]): best=(p,f)
    if best:
        dst=os.path.join(OUT, book+".pdf")
        if not os.path.exists(dst): shutil.copy2(best[1], dst)
        tot+=best[0]
        mapping.append({"book":book,"pages":best[0],"src":os.path.basename(best[1])})
        print(f"{book:30} {best[0]:>5}  {os.path.basename(best[1])[:50]}")
    else:
        mapping.append({"book":book,"pages":None,"src":None})
        print(f"{book:30} {'?':>5}  ❌ PDF 못찾음")
json.dump(mapping, open(os.path.join(OUT,"_mapping.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
got=sum(1 for m in mapping if m['pages'])
print(f"\n모음: {got}/15권 | 총 {tot}p | 예상비용 ~${tot*0.006:.1f} (accurate+LLM, cook 제외)")
print(f"입력폴더: {OUT}  (복사본 {len(os.listdir(OUT))}개)")
