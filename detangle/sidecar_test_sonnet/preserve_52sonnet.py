"""52 Sonnet을 독립 폴더에 보존(corpus와 별개 고품질 레퍼런스). 원본은 백업서 복사."""
import json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
BK = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging_FAILED_backup"
DEST = r"C:\Users\USER\corpus_md_export_20260612\sonnet52_independent"
os.makedirs(DEST, exist_ok=True)
pids = json.load(open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\SONNET52.json", encoding="utf-8"))["sonnet_pids"]
n = 0
for pid in pids:
    src = os.path.join(BK, pid + ".json")
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(DEST, pid + ".json")); n += 1
# README
open(os.path.join(DEST, "_README.txt"), "w", encoding="utf-8").write(
    "Sonnet(claude-sonnet-4-5) 추출 52편 독립 보존본 (2026-06-25).\n"
    "corpus 본 sidecar는 All-Gemma/Only-Gemma로 통일 → 이 52편도 corpus엔 Gemma판이 들어감.\n"
    "이 폴더는 고품질 Sonnet 레퍼런스/답안지로 별도 보존. variables_measured(measured/cited/modeled provenance) 보유.\n")
print(f"52 Sonnet 독립 보존: {n}편 → {DEST}")
print(f"폴더 내용: {len([f for f in os.listdir(DEST) if f.endswith('.json')])} json")
print("→ corpus엔 이 52편도 Gemma판으로 들어감(reprocess), Sonnet은 여기 따로 생존.")
