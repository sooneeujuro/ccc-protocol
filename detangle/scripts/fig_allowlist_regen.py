#!/usr/bin/env python3
"""fig_allowlist_regen.py — allowlist를 실제 missing으로 재생성 (백업 후).

머지 후 allowlist(2028개, stale 다수)를 실제 잔여 missing ref만 남기고 재생성.
기존 .txt는 .bak_20260616_pre_prune 로 백업. 비파괴.
"""
import re
import shutil
from pathlib import Path

CORPUS = Path(r"G:\corpus_md_export_20260612")
ARTICLES = CORPUS / "articles"
ALLOW = CORPUS / "FIGURES_MISSING_ALLOWLIST.txt"
BAK = CORPUS / "FIGURES_MISSING_ALLOWLIST.txt.bak_20260616_pre_prune"
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
IMG_EXT = (".jpg", ".jpeg", ".png")

present = {f.name for f in ARTICLES.iterdir() if f.suffix.lower() in IMG_EXT}
missing = set()
for md in ARTICLES.glob("*.md"):
    text = md.read_text(encoding="utf-8", errors="replace")
    for m in IMG_RE.finditer(text):
        tgt = m.group(1).strip().split()[0] if m.group(1).strip() else ""
        if not tgt or tgt.startswith(("http://", "https://", "data:")):
            continue
        name = tgt.replace("\\", "/").rsplit("/", 1)[-1]
        if name not in present:
            missing.add(name)

old = len(ALLOW.read_text(encoding="utf-8").splitlines()) if ALLOW.exists() else 0
if ALLOW.exists() and not BAK.exists():
    shutil.copy2(ALLOW, BAK)
ALLOW.write_text("\n".join(sorted(missing)) + ("\n" if missing else ""), encoding="utf-8")
print(f"allowlist {old} -> {len(missing)} (backup: {BAK.name})")
print("remaining:", sorted(missing))
