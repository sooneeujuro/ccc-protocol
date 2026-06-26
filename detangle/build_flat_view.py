import json, shutil, sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

NEW = Path(r"G:\corpus_md_export_20260618")
ARTS = NEW / "articles"
SLUG2STEM = json.loads(Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\SLUG_TO_STEM.json").read_text(encoding="utf-8"))

ARTS.mkdir(exist_ok=True)
made = skip = coll = 0
seen = set()
bad = []
for slug, stem in SLUG2STEM.items():
    d = NEW / slug
    if not d.is_dir():
        continue
    mds = [p for p in d.glob("*.md")]
    if not mds:
        continue
    # flat name = old stem (sidecar + reader alignment); sanitize for FS
    name = re.sub(r'[\\/:*?"<>|]', "_", stem)[:150]
    dst = ARTS / (name + ".md")
    if dst.exists() or name in seen:
        # collision (dup paper / same stem) -> suffix to keep both, but rare
        k = 2
        while (ARTS / f"{name}__{k}.md").exists():
            k += 1
        dst = ARTS / f"{name}__{k}.md"
        coll += 1
    seen.add(name)
    shutil.copy2(mds[0], dst)
    made += 1

print(f"flat articles/ view: {made} md (name collisions suffixed: {coll})")
print(f"articles/ 파일수: {len(list(ARTS.glob('*.md')))}")
