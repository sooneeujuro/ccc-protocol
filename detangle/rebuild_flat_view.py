import json, shutil, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

NEW = Path(r"G:\corpus_md_export_20260618")
ARTS = NEW / "articles"
S2S = json.loads(Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\SLUG_TO_STEM.json").read_text(encoding="utf-8"))

# 깨끗하게 재생성
if ARTS.exists():
    shutil.rmtree(ARTS)
ARTS.mkdir()

NONPAPER = {"index", "articles", "scripts", "papers"}
made = 0
new_stem2slug = {}
seen = set()
for d in sorted(NEW.iterdir()):
    if not d.is_dir() or d.name in NONPAPER:
        continue
    if not (d / ".done").exists():
        continue
    mds = list(d.glob("*.md"))
    if not mds:
        continue
    slug = d.name
    # 매핑된 reext/clean = 옛 stem名 (sidecar/index 정렬); 새 papers = 폴더 MD의 pid名
    stem = S2S.get(slug) or mds[0].stem
    name = re.sub(r'[\\/:*?"<>|]', "_", stem)[:150]
    dst = ARTS / (name + ".md")
    if dst.exists() or name in seen:
        k = 2
        while (ARTS / f"{name}__{k}.md").exists():
            k += 1
        dst = ARTS / f"{name}__{k}.md"
        name = dst.stem
    seen.add(name)
    shutil.copy2(mds[0], dst)
    new_stem2slug[name] = slug
    made += 1

# STEM_TO_SLUG 전체 갱신 (detangle + 번들)
det = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\STEM_TO_SLUG.json")
det.write_text(json.dumps(new_stem2slug, ensure_ascii=False), encoding="utf-8")
(NEW / "index" / "STEM_TO_SLUG.json").write_text(json.dumps(new_stem2slug, ensure_ascii=False), encoding="utf-8")

print(f"articles/ 재생성: {made} MD (= 폴더당 1개)")
print(f"articles/ 실제 파일수: {len(list(ARTS.glob('*.md')))}")
print(f"STEM_TO_SLUG 갱신: {len(new_stem2slug)} (detangle + index/ 번들)")
