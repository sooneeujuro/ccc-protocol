import re, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

def toks(s):
    s = re.sub(r"\.(pdf|md)$", "", s.lower())
    return set(re.findall(r"[a-z0-9]+|[가-힣]{2,}", s))

gaps = json.load(open(r"C:\Users\USER\Documents\ccc-protocol\detangle\REAL_GAPS.json", encoding="utf-8"))
gap_tok = [(g, toks(g)) for g in gaps]

t0 = time.time()
pdfs = []
for root in [Path("D:/"), Path("G:/")]:
    try:
        for p in root.rglob("*.pdf"):
            pdfs.append((p, toks(p.stem)))
    except Exception:
        pass
print(f"드라이브 PDF 총 {len(pdfs)}개 enum {time.time()-t0:.0f}s")

found = []; resid = []
for g, gt in gap_tok:
    best = None; bj = 0.0
    for p, pt in pdfs:
        if not pt:
            continue
        j = len(gt & pt) / max(1, len(gt | pt))
        if j > bj:
            bj = j; best = p
    if bj >= 0.5:
        found.append((g, str(best), round(bj, 2)))
    else:
        resid.append((g, str(best) if best else "", round(bj, 2)))

print(f"=== 64 갭 파일명매칭: 찾음 {len(found)} | 미발견(2차 본문매칭 필요) {len(resid)} ===")
print("--- 찾음 ---")
for g, p, j in found:
    print(f"  {j} {g[:34]:34} -> {Path(p).parent.name}\\{Path(p).name[:40]}")
print("--- 미발견 ---")
for g, p, j in resid:
    print(f"  (best {j}) {g[:50]}")
json.dump({"found": [{"gap": g, "pdf": p, "j": j} for g, p, j in found],
           "resid": [g for g, p, j in resid]},
          open(r"C:\Users\USER\Documents\ccc-protocol\detangle\GAP_HUNT.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("saved GAP_HUNT.json")
