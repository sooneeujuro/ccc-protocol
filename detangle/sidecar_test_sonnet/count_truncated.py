"""입력 잘림 정확 카운트: len(MD 텍스트) > 95000 char = read()[:95000]에서 잘린 것.
정본(0624) + 0612 둘 다. 초과량 분포도."""
import os, glob, sys
sys.stdout.reconfigure(encoding="utf-8")
MAX = 95000
for label, d in [("정본 0624", r"G:\corpus_20260624\articles"),
                 ("0612(done입력)", r"C:\Users\USER\corpus_md_export_20260612\articles")]:
    fs = glob.glob(os.path.join(d, "*.md"))
    cut = []
    for f in fs:
        try: n = len(open(f, encoding="utf-8", errors="replace").read())
        except: continue
        if n > MAX: cut.append(n)
    print(f"\n=== {label}: {len(fs)}편 ===")
    print(f"  95000자 초과(=입력 잘림): {len(cut)}편 ({100*len(cut)//max(1,len(fs))}%)")
    if cut:
        cut.sort()
        import statistics as st
        print(f"  잘린 것들 크기: median {int(st.median(cut))}자 / max {max(cut)}자")
        # 초과량(버려진 분량) 구간
        buckets = {"95k~110k(소량컷)":0, "110k~150k":0, "150k~250k":0, ">250k(대량컷)":0}
        for n in cut:
            if n<110000: buckets["95k~110k(소량컷)"]+=1
            elif n<150000: buckets["110k~150k"]+=1
            elif n<250000: buckets["150k~250k"]+=1
            else: buckets[">250k(대량컷)"]+=1
        for k,v in buckets.items(): print(f"    {k}: {v}")
