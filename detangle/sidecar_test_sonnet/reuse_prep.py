"""reuse-selective 준비: 격리 done 중 안 잘린(재추출 article ≤95000) 것 → canonical staging 복사(재사용).
잘린 done은 안 복사 = 재추출 todo로 남음. quarantine은 보존(복사만)."""
import os, glob, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
QUAR = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_QUARANTINE_oldinput_20260625"
STAGE = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_canonical"
A24 = r"G:\corpus_20260624\articles"
A12 = r"C:\Users\USER\corpus_md_export_20260612\articles"
os.makedirs(STAGE, exist_ok=True)
def art_len(pid):
    for d in (A24, A12):
        p = os.path.join(d, pid + ".md")
        if os.path.exists(p):
            return len(open(p, encoding="utf-8", errors="replace").read())
    return None
done = [f for f in os.listdir(QUAR) if f.endswith(".json")]
reuse = rerun_trunc = no_art = 0
for f in done:
    pid = f[:-5]
    n = art_len(pid)
    if n is None:
        no_art += 1; continue          # 입력 없음 → 재추출 todo서도 no_md
    if n <= 95000:
        shutil.copy2(os.path.join(QUAR, f), os.path.join(STAGE, f)); reuse += 1   # 재사용
    else:
        rerun_trunc += 1                # 잘림 → 재추출
print(f"격리 done {len(done)}편 분류:")
print(f"  재사용(안 잘림 ≤95000, staging 복사): {reuse}")
print(f"  재추출(잘림 >95000): {rerun_trunc}")
print(f"  입력없음: {no_art}")
print(f"→ canonical staging 시드: {len([x for x in os.listdir(STAGE) if x.endswith('.json')])}")
