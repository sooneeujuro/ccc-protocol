"""빈 variables_reported 진단: made_new_measurements=true인데 빈 것 = 추출실패.
made_new=false면 정상(리뷰/이론). classification.type 분포도."""
import json, glob, os, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
fs = glob.glob(r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging\*.json")
# 빈 것 중 made_new / type
mn_true_empty = []; mn_false_empty = 0; mn_other = 0
type_empty = Counter()
made_new_vals = Counter()
total_empty = 0
for f in fs:
    try: j = json.load(open(f, encoding="utf-8"))
    except: continue
    vr = j.get("variables_reported", [])
    if vr: continue
    total_empty += 1
    mn = j.get("made_new_measurements")
    made_new_vals[str(mn)] += 1
    typ = (j.get("classification") or {}).get("type", "?")
    type_empty[typ] += 1
    if mn is True:
        if len(mn_true_empty) < 12: mn_true_empty.append(os.path.basename(f)[:50])
print(f"빈 것 {total_empty}편 분석:")
print(f"  made_new_measurements 분포: {dict(made_new_vals)}")
print(f"  → made_new=true인데 vars 빈 것 = 추출실패 의심: {made_new_vals.get('True',0)}")
print(f"  → made_new=false = 정상(측정 안 함): {made_new_vals.get('False',0)}")
print(f"\n  빈 것 classification.type 분포: {dict(type_empty.most_common())}")
print(f"\n  made_new=true & 빈 것 샘플(실패 의심):")
for x in mn_true_empty: print("    ⚠️", x)
