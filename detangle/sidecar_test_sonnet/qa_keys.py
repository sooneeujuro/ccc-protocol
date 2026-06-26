"""staging sidecar 키 분류: variables_reported(신, Gemma) vs variables_measured(구, Haiku) vs 둘다없음.
'빈 실패'가 실은 Gemma 미처리(Haiku원본)인지 = 데이터 보존됐나."""
import json, glob, os, sys
sys.stdout.reconfigure(encoding="utf-8")
STG = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging"
gemma_full = 0      # variables_reported 있음
haiku_only = 0      # variables_measured 있고 variables_reported 없음 = Gemma 미처리(데이터는 구키에 보존)
truly_empty = 0     # 둘 다 없음/빔 = 진짜 데이터 없음
vm_empty_too = 0
for f in glob.glob(os.path.join(STG, "*.json")):
    try: j = json.load(open(f, encoding="utf-8"))
    except: continue
    vr = j.get("variables_reported")
    vm = j.get("variables_measured")
    if vr: gemma_full += 1
    elif vm: haiku_only += 1
    else:
        truly_empty += 1
        if vm == [] : vm_empty_too += 1
tot = gemma_full + haiku_only + truly_empty
print(f"staging {tot}편:")
print(f"  Gemma 처리완료(variables_reported 있음): {gemma_full} ({100*gemma_full//tot}%)")
print(f"  Haiku원본만(variables_measured 있고 신키 없음 = Gemma 미처리): {haiku_only} ({100*haiku_only//tot}%)")
print(f"  둘 다 없음(진짜 빔): {truly_empty}")
print(f"\n→ 해석: haiku_only가 크면 '실패' 아니라 '아직 Gemma 안 돌린 원본'(데이터 구키에 보존).")
