import hashlib, os, re, shutil, sys, fitz
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

def pid_from(b):
    s = b[:-4] if b.lower().endswith(".pdf") else b
    return s.replace(" ", "_").replace("/", "_")

def slug(pid):
    return hashlib.md5(pid.encode("utf-8")).hexdigest()[:12]

def words(t):
    t = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", t)
    return set(re.findall(r"[a-z]{4,}", t.lower()))

NUC = Path(r"D:\Academia\References\Nuc")
NEW = Path(r"G:\corpus_md_export_20260618")
MDOUT = NUC / "MD"
MDOUT.mkdir(exist_ok=True)

# 폴더 word-set 인덱스 (본문 매칭용)
fold_ws = {}
for d in NEW.iterdir():
    if d.is_dir() and (d / ".done").exists():
        m = list(d.glob("*.md"))
        if m:
            fold_ws[d.name] = words(m[0].read_text(encoding="utf-8", errors="replace")[:4000])

copied = miss = 0
report = []
for p in sorted(NUC.glob("*.pdf")):
    sg = slug(pid_from(p.name))
    target = None
    how = ""
    if (NEW / sg / ".done").exists():
        target = sg
        how = "slug"
    else:
        try:
            d = fitz.open(p)
            pt = words(d[0].get_text()[:3000])
            d.close()
        except Exception:
            pt = set()
        best = None
        bj = 0.0
        for fn, fw in fold_ws.items():
            j = len(pt & fw) / max(1, len(pt | fw))
            if j > bj:
                bj = j
                best = fn
        if bj >= 0.5:
            target = best
            how = f"content({bj:.2f})"
    if target:
        dst = MDOUT / target
        if not dst.exists():
            shutil.copytree(NEW / target, dst)
        copied += 1
        report.append((how, p.name[:42], target))
    else:
        miss += 1
        report.append(("MISS", p.name[:48], ""))

print(f"copied: {copied} | missing: {miss}  -> {MDOUT}")
for how, n, t in report:
    print(f"  [{how}] {n}  {('-> ' + t) if t else ''}")
