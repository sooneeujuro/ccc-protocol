import os, json, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")

def cnt(p, patt=None):
    if not os.path.isdir(p):
        return "(없음)"
    if patt:
        return sum(1 for f in os.listdir(p) if f.endswith(patt))
    return len(os.listdir(p))

E = r"G:\corpus_md_export_20260618"
PDF = r"G:\corpus_pdfs_bundle"
SB = r"G:\corpus_supplementary_bundle"
idx = os.path.join(E, "index")

print("=== 20260618 정본 현황 ===")
if os.path.isdir(E):
    dirs = [d for d in os.listdir(E) if os.path.isdir(os.path.join(E, d))
            and d not in ("articles", "index", "scripts", "papers")]
    print("  슬러그 MD폴더:", len(dirs))
    print("  articles/ flat:", cnt(os.path.join(E, "articles"), ".md"))
    print("  index/ 파일:", os.listdir(idx) if os.path.isdir(idx) else "(없음)")
    rp = os.path.join(idx, "retrieval_papers.json")
    if os.path.exists(rp):
        d = json.load(open(rp, encoding="utf-8"))
        print("  index 커버 논문수(retrieval_papers):", len(d) if isinstance(d, (list, dict)) else "?")
    for nm, lbl in [("embeddings_bge_m3.npy", "dense npy"), ("bm25_index.pkl", "bm25 pkl"),
                    ("retrieval_units.jsonl", "units jsonl")]:
        fp = os.path.join(idx, nm)
        if os.path.exists(fp):
            print(f"  {lbl}: {os.path.getsize(fp)//1024//1024} MB")
else:
    print("  (20260618 폴더 없음 — G: 연결 확인)")

print("=== 번들 현황 ===")
print("  PDF 번들:", cnt(PDF, ".pdf"))
print("  supp 번들 총파일:", cnt(SB))

# 폴더 총 용량 추정 (빠르게)
def dirsize_gb(p):
    if not os.path.isdir(p):
        return None
    tot = 0
    for root, _, files in os.walk(p):
        for f in files:
            try:
                tot += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return round(tot/1024/1024/1024, 1)

print("=== 용량 (GB) ===")
for nm, p in [("20260618 정본", E), ("PDF 번들", PDF), ("supp 번들", SB)]:
    print(f"  {nm}: {dirsize_gb(p)} GB")

print("=== 드라이브 여유 ===")
for drv in ["G:\\", "C:\\"]:
    try:
        t, u, f = shutil.disk_usage(drv)
        print(f"  {drv} 여유 {f//1024//1024//1024} GB / 전체 {t//1024//1024//1024} GB")
    except Exception as e:
        print(f"  {drv} {e}")
