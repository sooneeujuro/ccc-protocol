"""QC: canonical staging 3899 검증 (정본 승격 전). read-only.
- enum 준수 / 빈 변수 / 필드 누락 / 변수수 분포
- 청킹 효과: 입력 잘린(>95000) 논문이 변수 빈약(<8)하지 않나 = 단일컷이면 사라졌을 꼬리 잡혔나"""
import os, glob, json, sys, statistics as st
sys.stdout.reconfigure(encoding="utf-8")
STAGE = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_canonical"
A24 = r"G:\corpus_20260624\articles"; A12 = r"C:\Users\USER\corpus_md_export_20260612\articles"
ENUM = {"gas", "petrology", "both", "other"}
def artlen(pid):
    for d in (A24, A12):
        p = os.path.join(d, pid + ".md")
        if os.path.exists(p): return len(open(p, encoding="utf-8", errors="replace").read())
    return None
files = glob.glob(os.path.join(STAGE, "*.json"))
n = len(files)
vcounts = []; enum_bad = []; empty_vars = []; no_cls = []; no_made = []
cls_dist = {}; made_dist = {"True":0,"False":0,"None":0}
trunc_vcounts = []; trunc_sparse = []  # 입력 잘린 논문
for f in files:
    pid = os.path.basename(f)[:-5]
    try: sc = json.load(open(f, encoding="utf-8"))
    except Exception as e: enum_bad.append((pid, f"JSON err {e}")); continue
    vr = sc.get("variables_reported")
    nv = len(vr) if isinstance(vr, list) else -1
    vcounts.append(nv if nv >= 0 else 0)
    if nv == 0: empty_vars.append(pid)
    ct = (sc.get("classification") or {}).get("type") if isinstance(sc.get("classification"), dict) else None
    cls_dist[ct] = cls_dist.get(ct, 0) + 1
    if ct not in ENUM: enum_bad.append((pid, f"cls={ct}"))
    mm = sc.get("made_new_measurements")
    made_dist[str(mm)] = made_dist.get(str(mm), 0) + 1
    if "made_new_measurements" not in sc: no_made.append(pid)
    al = artlen(pid)
    if al and al > 95000 and nv >= 0:
        trunc_vcounts.append(nv)
        if nv < 8: trunc_sparse.append((pid, nv, al))
vcounts = [v for v in vcounts]
print(f"=== QC: canonical staging {n}편 ===")
print(f"변수수 분포: min {min(vcounts)} / median {int(st.median(vcounts))} / mean {st.mean(vcounts):.1f} / max {max(vcounts)}")
print(f"빈 변수(0개): {len(empty_vars)}편")
print(f"classification.type 분포: {cls_dist}")
print(f"  enum 위반(gas/petrology/both/other 밖): {len([1 for p,e in enum_bad if 'cls=' in e])}편")
print(f"made_new 분포: {made_dist}")
print(f"필드 누락(made_new 없음): {len(no_made)}")
print(f"\n=== 청킹 효과: 입력 잘린(>95000) 논문 {len(trunc_vcounts)}편 ===")
if trunc_vcounts:
    print(f"  변수수: median {int(st.median(trunc_vcounts))} / mean {st.mean(trunc_vcounts):.1f} / max {max(trunc_vcounts)}")
    print(f"  변수 빈약(<8, 청킹 실패 의심): {len(trunc_sparse)}편 ({100*len(trunc_sparse)//max(1,len(trunc_vcounts))}%)")
    for p, nv, al in trunc_sparse[:8]: print(f"    {nv}변수 / {al}자 | {p[:45]}")
print(f"\n=== 이상치 샘플 ===")
print(f"빈 변수 논문 예시: {[p[:35] for p in empty_vars[:8]]}")
if enum_bad: print(f"enum/JSON 이상 예시: {enum_bad[:8]}")
print(f"\n판정: {'⚠️ 확인필요' if (len(enum_bad) or len(no_made) or len(trunc_sparse) > len(trunc_vcounts)*0.05) else '✅ 클린(승격 가능)'}")
