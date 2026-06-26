"""완료 게이트: 모든 SIDE sidecar가 Gemma 통과(variables_reported=list)했나.
미처리 = has_md(재시도 가능) vs no_md(입력 없음, 제외). has_md 잔여>0이면 exit 1(루프 계속)."""
import json, os, glob, sys
sys.stdout.reconfigure(encoding="utf-8")
SIDE = r"C:\Users\USER\corpus_md_export_20260612\sidecars"
STAGE = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_canonical"   # 캐노니컬 재추출 staging
ARTS = r"G:\corpus_20260624\articles"                          # 정본 0624 우선
ARTS_FB = r"C:\Users\USER\corpus_md_export_20260612\articles"  # 0612 fallback
SF = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet"

def has_input(p):
    return os.path.exists(os.path.join(ARTS, p + ".md")) or os.path.exists(os.path.join(ARTS_FB, p + ".md"))

side = {f[:-5] for f in os.listdir(SIDE) if f.endswith(".json")}
processed = set()
for f in glob.glob(os.path.join(STAGE, "*.json")):
    try: j = json.load(open(f, encoding="utf-8"))
    except: continue
    if isinstance(j.get("variables_reported"), list):
        processed.add(os.path.basename(f)[:-5])
unproc = side - processed
has_md = sorted(p for p in unproc if has_input(p))
no_md  = sorted(p for p in unproc if not has_input(p))
print(f"SIDE {len(side)} | Gemma통과 {len(processed)} ({100*len(processed)//len(side)}%) | 미처리 {len(unproc)}")
print(f"  ├ has_md(재시도 가능): {len(has_md)}")
print(f"  └ no_md(입력 MD 없음 = 책챕터 등, 제외대상): {len(no_md)}")
json.dump({"processed": len(processed), "has_md_unproc": has_md, "no_md_unproc": no_md},
          open(os.path.join(SF, "COMPLETE_GATE.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if has_md:
    print(f"  → 재시도 잔여 {len(has_md)}편 (exit 1, 루프 계속)")
    sys.exit(1)
print("  ✅ MD 있는 sidecar 전부 Gemma 통과 (no_md만 잔여 = 제외) — 완료")
sys.exit(0)
