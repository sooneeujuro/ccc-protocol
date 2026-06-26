import shutil, hashlib, sys
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")

SRcs = [
    r"G:\corpus_supplementary",
    r"G:\WonheeLee\논문_Supplementary material",
    r"G:\corpus_refs_v20260616\supplementary",
    r"G:\Atelier_Handoff_2026-05-19_full_corpus\supplementary\supplementary_mantle10_20260518",
    r"G:\Atelier_Handoff_2026-05-19_full_corpus\supplementary\supplementary_finallist_20260519",
    r"G:\Paper_Atelier\interesting-knuth-320f90\wiki\data\_supplementary_inbox",
]
OUT = Path(r"G:\corpus_supplementary_bundle")
OUT.mkdir(exist_ok=True)

def md5(p, chunk=1 << 20):
    h = hashlib.md5()
    with open(p, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

seen_hash = {}      # content hash -> dest name (true dup skip)
copied = dup = renamed = 0
total_mb = 0.0
by_src = Counter()
for s in SRcs:
    sp = Path(s)
    if not sp.is_dir():
        print(f"(없음) {s}")
        continue
    for p in sp.rglob("*"):
        if not p.is_file():
            continue
        try:
            h = md5(p)
        except Exception:
            continue
        if h in seen_hash:
            dup += 1
            continue
        # 이름 충돌(다른 내용 동명) -> 접미사
        dst = OUT / p.name
        if dst.exists():
            stem, ext = p.stem, p.suffix
            k = 2
            while (OUT / f"{stem}__{k}{ext}").exists():
                k += 1
            dst = OUT / f"{stem}__{k}{ext}"
            renamed += 1
        shutil.copy2(p, dst)
        seen_hash[h] = dst.name
        copied += 1
        total_mb += p.stat().st_size / 1024 / 1024
        by_src[sp.name] += 1
print(f"통합 supplementary 폴더: {OUT}")
print(f"복사: {copied} | 내용중복 skip: {dup} | 동명-다른내용 접미사: {renamed}")
print(f"용량: {total_mb/1024:.2f} GB")
print("출처별:")
for k, v in by_src.most_common():
    print(f"  {v:4}  {k}")
print(f"bundle 파일수: {len(list(OUT.iterdir()))}")
