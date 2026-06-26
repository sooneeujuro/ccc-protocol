import shutil, hashlib, sys
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")

SRCS = [
    r"G:\Atelier_Handoff_2026-05-19_full_corpus\supplementary\supplementary_finallist_20260519",
    r"G:\Atelier_Handoff_2026-05-19_full_corpus\supplementary\supplementary_mantle10_20260518",
    r"G:\Paper_Atelier\interesting-knuth-320f90\wiki\data\_supplementary_inbox",
]
OUT = Path(r"G:\corpus_supplementary_bundle\_processed_tables")
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)

def md5(p, chunk=1 << 20):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()

seen = set(); copied = dup = 0; total_mb = 0.0
by_src = Counter()
for s in SRCS:
    sp = Path(s)
    if not sp.is_dir():
        print(f"(없음) {s}")
        continue
    label = sp.name
    for p in sp.rglob("*"):
        if not p.is_file():
            continue
        try:
            h = md5(p)
        except Exception:
            continue
        if h in seen:
            dup += 1; continue
        seen.add(h)
        dst = OUT / p.name
        if dst.exists():
            stem, ext = dst.stem, dst.suffix
            k = 2
            while (OUT / f"{stem}__{k}{ext}").exists():
                k += 1
            dst = OUT / f"{stem}__{k}{ext}"
        shutil.copy2(p, dst)
        copied += 1; total_mb += p.stat().st_size / 1024 / 1024
        by_src[label] += 1
print(f"_processed_tables: {OUT}")
print(f"복사: {copied} | 내용중복 skip: {dup} | 용량: {total_mb/1024:.2f} GB")
for k, v in by_src.most_common():
    print(f"  {v:4}  {k}")
