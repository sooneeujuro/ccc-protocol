import os, shutil, hashlib, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

def pid_from(b):
    s = b[:-4] if b.lower().endswith(".pdf") else b
    return s.replace(" ", "_").replace("/", "_")

def slug(pid):
    return hashlib.md5(pid.encode("utf-8")).hexdigest()[:12]

srcs = ["batch1_in","batch2_in","batch3_in","batch4_in","batch5_in","batch6_in",
        "batch_recover_in","batch_recover2_in","batch_recover3_in","batch_recover4_in","book_cook_in"]
out = Path(r"G:\corpus_pdfs_bundle")
out.mkdir(exist_ok=True)
seen = set(); copied = dup = 0; total_mb = 0.0
for s in srcs:
    d = Path("G:/") / s
    if not d.is_dir():
        continue
    for p in d.glob("*.pdf"):
        sg = slug(pid_from(p.name))
        if sg in seen:
            dup += 1; continue
        seen.add(sg)
        dst = out / (sg + ".pdf")
        if not dst.exists():
            shutil.copy2(p, dst); copied += 1; total_mb += p.stat().st_size / 1024 / 1024
print(f"통합 PDF 폴더: {out}")
print(f"복사: {copied} (고유 slug) | 중복skip: {dup}")
print(f"용량: {total_mb/1024:.1f} GB")
corpus = Path(r"G:\corpus_md_export_20260618")
print(f"corpus 폴더수: {len([x for x in corpus.iterdir() if x.is_dir()])}")
print(f"bundle PDF수: {len(list(out.glob('*.pdf')))}")
