"""52 Sonnet 식별 + 루프가 staging에 Gemma로 덮어썼나 피해평가. (이동 안 함, 평가만)"""
import json, glob, os, sys
sys.stdout.reconfigure(encoding="utf-8")
BK = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging_FAILED_backup"
STG = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging"
sonnet_pids = []
for f in glob.glob(os.path.join(BK, "*.json")):
    try: j = json.load(open(f, encoding="utf-8"))
    except: continue
    if (j.get("extraction_meta") or {}).get("extraction_model") == "claude-sonnet-4-5":
        sonnet_pids.append(os.path.basename(f)[:-5])
print(f"백업의 Sonnet 추출본: {len(sonnet_pids)}편")
# 이 중 staging에 지금 Gemma판(variables_reported)으로 덮어써진 게 있나
overwritten = []
for pid in sonnet_pids:
    sp = os.path.join(STG, pid + ".json")
    if os.path.exists(sp):
        try: sj = json.load(open(sp, encoding="utf-8"))
        except: continue
        if isinstance(sj.get("variables_reported"), list):
            overwritten.append(pid)
print(f"루프가 staging에 Gemma로 덮어쓴 Sonnet: {len(overwritten)}편 (백업에 원본 있어 복구가능)")
for p in overwritten[:10]: print("   ⚠️", p[:55])
print(f"\n안전(백업에만, 덮어쓰기 안 됨): {len(sonnet_pids)-len(overwritten)}편")
import json as _j
_j.dump({"sonnet_pids": sonnet_pids, "overwritten_in_staging": overwritten},
        open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\SONNET52.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("→ SONNET52.json")
