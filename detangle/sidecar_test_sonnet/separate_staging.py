"""staging 분리: Gemma 완료(variables_reported=list)는 유지(rerun시 skip),
fail/haiku-only(variables_reported 없음)는 백업폴더로 이동(rerun시 재처리). 삭제 아님."""
import json, os, glob, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
STG = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging"
BK = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging_FAILED_backup"
os.makedirs(BK, exist_ok=True)
keep = moved = 0
for f in glob.glob(os.path.join(STG, "*.json")):
    try: j = json.load(open(f, encoding="utf-8"))
    except:
        shutil.move(f, os.path.join(BK, os.path.basename(f))); moved += 1; continue
    vr = j.get("variables_reported")
    if isinstance(vr, list):        # Gemma 처리완료(빈 list도 made_new=false 정상) → 유지
        keep += 1
    else:                            # variables_reported 없음 = 미처리/실패 → 이동
        shutil.move(f, os.path.join(BK, os.path.basename(f))); moved += 1
print(f"staging 유지(Gemma완료, rerun skip): {keep}")
print(f"백업이동(재처리 대상): {moved}  → {BK}")
print(f"현재 staging 잔여: {len(glob.glob(os.path.join(STG,'*.json')))}")
