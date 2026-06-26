import json, glob, os, sys
sys.stdout.reconfigure(encoding="utf-8")
fs = glob.glob(r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging\*.json")
n = len(fs); nonempty = 0; empty = 0; samp_empty = []; samp_full = []
for f in fs:
    try: j = json.load(open(f, encoding="utf-8"))
    except: continue
    vr = j.get("variables_reported", [])
    if vr:
        nonempty += 1
        if len(samp_full) < 5: samp_full.append((os.path.basename(f)[:42], len(vr)))
    else:
        empty += 1
        if len(samp_empty) < 8: samp_empty.append(os.path.basename(f)[:55])
print(f"staging {n}편 | vars 있음 {nonempty} ({100*nonempty//max(1,n)}%) | 빈 것 {empty} ({100*empty//max(1,n)}%)")
print("\n빈 샘플:")
for x in samp_empty: print("  ", x)
print("\n정상 샘플:")
for x, c in samp_full: print("  ", x, "→", c, "vars")
