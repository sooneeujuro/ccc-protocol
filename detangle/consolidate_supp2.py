import shutil, hashlib, sys, re
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")

OUT = Path(r"G:\corpus_supplementary_bundle")
# 깨끗하게 재생성
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()

WONHEE = Path(r"G:\WonheeLee\논문_Supplementary material")
CORPSUP = Path(r"G:\corpus_supplementary")          # 논문별 폴더
CORPREFS = Path(r"G:\corpus_refs_v20260616\supplementary")  # slug__제목
SLUGRE = re.compile(r"^[0-9a-f]{12}__")

def md5(p, chunk=1 << 20):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()

seen = {}
copied = dup = 0
total_mb = 0.0
by_src = Counter()

def put(src_path, name, srclabel):
    global copied, dup, total_mb
    try:
        h = md5(src_path)
    except Exception:
        return
    if h in seen:
        dup += 1
        return
    dst = OUT / name
    if dst.exists():
        stem, ext = dst.stem, dst.suffix
        k = 2
        while (OUT / f"{stem}__{k}{ext}").exists():
            k += 1
        dst = OUT / f"{stem}__{k}{ext}"
    shutil.copy2(src_path, dst)
    seen[h] = dst.name
    copied += 1
    total_mb += src_path.stat().st_size / 1024 / 1024
    by_src[srclabel] += 1

# 1) WonheeLee: 이름 그대로 (양식 기준). 하위폴더는 폴더명 prefix
if WONHEE.is_dir():
    for p in WONHEE.rglob("*"):
        if p.is_file():
            rel = p.relative_to(WONHEE)
            name = p.name if len(rel.parts) == 1 else (rel.parts[0] + "__" + p.name)
            put(p, name, "WonheeLee")

# 2) corpus_supplementary: 논문별 폴더 -> <논문폴더>__<파일>
if CORPSUP.is_dir():
    for p in CORPSUP.rglob("*"):
        if p.is_file():
            rel = p.relative_to(CORPSUP)
            name = (rel.parts[0] + "__" + p.name) if len(rel.parts) > 1 else p.name
            put(p, name, "corpus_supplementary")

# 3) corpus_refs: slug__ 접두어 제거 -> 읽기쉬운 제목
if CORPREFS.is_dir():
    for p in CORPREFS.rglob("*"):
        if p.is_file():
            name = SLUGRE.sub("", p.name)
            put(p, name, "corpus_refs")

print(f"통합(원본 SM만): {OUT}")
print(f"복사: {copied} | 내용중복 skip: {dup}")
print(f"용량: {total_mb/1024:.2f} GB")
for k, v in by_src.most_common():
    print(f"  {v:4}  {k}")
print(f"제외(가공본): supplementary_finallist(csv splits), mantle10, inbox")
