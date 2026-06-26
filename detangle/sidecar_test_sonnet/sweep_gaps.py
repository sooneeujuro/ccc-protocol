"""전수 sweep: refs+D:\Academia PDF universe vs 정본 corpus → 모든 갭.
갭이 quarantine/renewal출력에 있으면 복구가능, 없으면 미추출. CPU $0."""
import os, re, glob, json, sys
sys.stdout.reconfigure(encoding="utf-8")

PDF_DIRS = [r"G:\corpus_refs_v20260616\papers", r"D:\Academia\References"]
CORPUS = r"G:\corpus_20260624\articles"
# 복구가능 MD 출처(추출됐으나 corpus 밖)
MD_RECOV = [r"G:\corpus_md_export_20260602\_renewal_20260609\_new_dup_quarantine",
            r"G:\corpus_md_export_20260602\_renewal_20260609\cha_out",
            r"G:\corpus_md_export_20260602\_renewal_20260609\kim_out",
            r"G:\corpus_md_export_20260602\_renewal_20260609\nuc_out",
            r"G:\corpus_quarantine"]
STOP = set("the of and in a to for on with from by an at as is are this study using used between within".split())
def sig(s):
    s = re.sub(r"^[0-9a-f]{8,16}__", "", s)
    return frozenset(t for t in re.findall(r"[a-z0-9]{3,}", s.lower()) if t not in STOP)

def collect_pdfs(dirs):
    out = {}
    for d in dirs:
        if os.path.isdir(d):
            for f in glob.glob(os.path.join(d, "**", "*.pdf"), recursive=True):
                name = os.path.basename(f)[:-4]
                sg = sig(name)
                if len(sg) >= 4: out[sg] = (name, f)   # dedup by signature
    return out

def collect_mds(dirs):
    sigs = []
    for d in dirs:
        if os.path.isdir(d):
            for f in glob.glob(os.path.join(d, "**", "*.md"), recursive=True):
                sg = sig(os.path.basename(f)[:-3])
                if len(sg) >= 4: sigs.append(sg)
    return sigs

pdfs = collect_pdfs(PDF_DIRS)
corpus = collect_mds([CORPUS])
recov = collect_mds(MD_RECOV)
print(f"PDF 유니크 {len(pdfs)} | 정본 corpus MD {len(corpus)} | 복구가능 MD(quarantine/renewal) {len(recov)}\n")

def best(sg, pool):
    b = 0.0
    for c in pool:
        j = len(sg & c)/len(sg | c)
        if j > b: b = j
        if b >= 0.6: break
    return b

gaps_recov = []; gaps_none = []
for sg,(name,f) in pdfs.items():
    if best(sg, corpus) >= 0.5: continue          # 정본에 있음
    if best(sg, recov) >= 0.5: gaps_recov.append(name)   # 복구가능(추출됨, corpus밖)
    else: gaps_none.append(name)                          # 미추출
print(f"=== 갭(정본에 없음) ===")
print(f"  복구가능(quarantine/renewal에 MD有): {len(gaps_recov)}")
print(f"  미추출(MD 아예 없음): {len(gaps_none)}")
json.dump({"recoverable": sorted(gaps_recov), "never_extracted": sorted(gaps_none)},
          open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\SWEEP_GAPS.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n=== 미추출 샘플 30 (PDF는 있는데 MD 어디에도 없음) ===")
for n in sorted(gaps_none)[:30]: print(f"  · {n[:70]}")
print(f"\n→ SWEEP_GAPS.json 저장")
