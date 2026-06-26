"""실패(made_new=true & 빈) vs 정상 의 입력 MD 크기 비교 → 긴논문 원인인가."""
import json, glob, os, sys
sys.stdout.reconfigure(encoding="utf-8")
STG = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging"
ART = r"C:\Users\USER\corpus_md_export_20260612\articles"
fail_sz = []; ok_sz = []
for f in glob.glob(os.path.join(STG, "*.json")):
    try: j = json.load(open(f, encoding="utf-8"))
    except: continue
    pid = os.path.basename(f)[:-5]
    md = os.path.join(ART, pid + ".md")
    if not os.path.exists(md): continue
    sz = os.path.getsize(md)
    vr = j.get("variables_reported", [])
    mn = j.get("made_new_measurements")
    if not vr and mn is True: fail_sz.append(sz)
    elif vr: ok_sz.append(sz)
import statistics as st
def stats(a): return f"n={len(a)} mean={int(st.mean(a)//1024)}KB median={int(st.median(a)//1024)}KB max={max(a)//1024}KB" if a else "n=0"
print("실패(made_new=true&빈) MD크기:", stats(fail_sz))
print("정상(vars有)      MD크기:", stats(ok_sz))
# 임계 분석: 큰 MD일수록 실패율?
allp = [(s, True) for s in fail_sz] + [(s, False) for s in ok_sz]
for thr in [20, 40, 60, 80, 100]:
    big = [t for s, t in allp if s >= thr*1024]
    if big:
        fr = 100*sum(big)//len(big)
        print(f"  MD>={thr}KB: {len(big)}편 중 실패율 {fr}%")
