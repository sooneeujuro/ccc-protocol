#!/usr/bin/env python3
"""fig_coverage_recon.py — READ-ONLY recon of figure-refill coverage (no writes to corpus).

Answers, per the 51 target papers:
  - how many image refs in each corpus articles/*.md are currently MISSING (no file in articles/)
  - how many of those missing refs can be supplied by:
      (a) derived\<slug>\images\<hash>_img.jpg  -> renamed to <slug>__<hash>_img.jpg
      (b) fig_refix_out\<slug>\<slug>__<hash>_img.jpg  (fresh convert, drop-in)
  - for the 10 reconvert papers: is the NEW fig_refix MD self-consistent
    (every image it references exists in fig_refix_out\<slug>\)?
  - RG-cruft candidates in fig_refix_out (tiny pixel dimensions)

Writes a JSON + text report under the repo (NOT the corpus). Touches no live file.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

CORPUS = Path(r"G:\corpus_md_export_20260612")
ARTICLES = CORPUS / "articles"
DERIVED = Path(r"G:\datalab_runs_v20260616\derived")
REFIX = Path(r"G:\fig_refix_out")
OUT_DIR = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle")

IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
IMG_EXT = (".jpg", ".jpeg", ".png")
SLUG_RE = re.compile(r"^([0-9a-f]{12})__(.+)$")


def md_refs(text):
    out = []
    for m in IMG_RE.finditer(text):
        tgt = m.group(1).strip().split()[0] if m.group(1).strip() else ""
        if not tgt or tgt.startswith(("http://", "https://", "data:")):
            continue
        out.append(tgt.replace("\\", "/").rsplit("/", 1)[-1])
    return out


def main():
    # 1. present files + audit-style missing refs across the WHOLE corpus
    present = {f.name for f in ARTICLES.iterdir() if f.suffix.lower() in IMG_EXT}
    missing_to_mds = defaultdict(list)   # missing ref name -> [md names]
    md_to_text = {}
    for md in sorted(ARTICLES.glob("*.md")):
        text = md.read_text(encoding="utf-8", errors="replace")
        md_to_text[md.name] = text
        for name in md_refs(text):
            if name not in present:
                missing_to_mds[name].append(md.name)
    total_missing = len(missing_to_mds)

    # categorize missing by slug prefix
    missing_by_slug = defaultdict(set)   # slug -> {missing ref names}
    bare_missing = set()
    for name in missing_to_mds:
        m = SLUG_RE.match(name)
        if m:
            missing_by_slug[m.group(1)].add(name)
        else:
            bare_missing.add(name)

    # 2. target slugs from derived folder names
    derived_slugs = sorted(p.name for p in DERIVED.iterdir() if p.is_dir())
    refix_slugs = sorted(p.name for p in REFIX.iterdir() if p.is_dir())

    rows = []
    grand = dict(missing=0, by_derived=0, by_refix=0, uncovered=0)
    for slug in sorted(set(derived_slugs) | set(missing_by_slug)):
        miss = missing_by_slug.get(slug, set())
        # derived source: bare hash files -> normalize to slug__hash
        dpath = DERIVED / slug / "images"
        derived_names = set()
        if dpath.exists():
            for f in dpath.iterdir():
                if f.suffix.lower() in IMG_EXT:
                    derived_names.add(f"{slug}__{f.name}")
        # refix source: already slug__hash
        rpath = REFIX / slug
        refix_names = set()
        if rpath.exists():
            for f in rpath.rglob("*"):
                if f.suffix.lower() in IMG_EXT:
                    refix_names.add(f.name)
        cov_d = miss & derived_names
        cov_r = miss & refix_names
        cov_any = miss & (derived_names | refix_names)
        uncov = miss - (derived_names | refix_names)
        rows.append(dict(
            slug=slug, is_refix=bool(refix_names),
            missing=len(miss), derived_imgs=len(derived_names), refix_imgs=len(refix_names),
            cov_derived=len(cov_d), cov_refix=len(cov_r), cov_any=len(cov_any),
            uncovered=sorted(uncov),
            mds=sorted({m for n in miss for m in missing_to_mds[n]}),
        ))
        grand["missing"] += len(miss)
        grand["by_derived"] += len(cov_d)
        grand["by_refix"] += len(cov_r)
        grand["uncovered"] += len(uncov)

    # 3. self-consistency of the 10 fresh MDs (do they reference imgs present in their folder?)
    refix_consistency = {}
    for slug in refix_slugs:
        rpath = REFIX / slug
        md_files = list(rpath.rglob("*.md"))
        imgs_here = {f.name for f in rpath.rglob("*") if f.suffix.lower() in IMG_EXT}
        info = dict(md_count=len(md_files), imgs_in_folder=len(imgs_here))
        if md_files:
            mdtext = md_files[0].read_text(encoding="utf-8", errors="replace")
            refs = md_refs(mdtext)
            refs_missing = [r for r in refs if r not in imgs_here]
            info.update(md_name=md_files[0].name, md_refs=len(refs),
                        md_refs_resolved=len(refs) - len(refs_missing),
                        md_refs_unresolved=refs_missing[:20])
        refix_consistency[slug] = info

    # 4. RG-cruft candidates: tiny pixel dims in fig_refix_out
    from PIL import Image
    cruft = defaultdict(list)
    for slug in refix_slugs:
        for f in (REFIX / slug).rglob("*"):
            if f.suffix.lower() in IMG_EXT:
                try:
                    with Image.open(f) as im:
                        w, h = im.size
                    if w < 120 or h < 120 or (w * h) < 20000:
                        cruft[slug].append(dict(name=f.name, w=w, h=h, bytes=f.stat().st_size))
                except Exception as e:
                    cruft[slug].append(dict(name=f.name, error=str(e)))

    report = dict(
        corpus_total_missing_refs=total_missing,
        bare_missing_count=len(bare_missing),
        bare_missing_sample=sorted(bare_missing)[:10],
        target_slugs_derived=len(derived_slugs),
        target_slugs_refix=len(refix_slugs),
        grand=grand,
        rows=rows,
        refix_consistency=refix_consistency,
        cruft={k: v for k, v in cruft.items()},
    )
    (OUT_DIR / "FIG_COVERAGE_RECON.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- console summary ----
    print(f"corpus total missing refs : {total_missing}")
    print(f"  bare (no slug) missing  : {len(bare_missing)}  sample={sorted(bare_missing)[:3]}")
    print(f"target slugs (derived/refix): {len(derived_slugs)} / {len(refix_slugs)}")
    print(f"GRAND: missing={grand['missing']} by_derived={grand['by_derived']} "
          f"by_refix={grand['by_refix']} uncovered={grand['uncovered']}")
    print()
    print(f"{'slug':14} {'rx':2} {'miss':>4} {'derv':>4} {'rfix':>4} {'covD':>4} {'covR':>4} {'covANY':>6} {'UNCOV':>5}")
    for r in rows:
        flag = "R" if r["is_refix"] else "."
        print(f"{r['slug']:14} {flag:2} {r['missing']:>4} {r['derived_imgs']:>4} {r['refix_imgs']:>4} "
              f"{r['cov_derived']:>4} {r['cov_refix']:>4} {r['cov_any']:>6} {len(r['uncovered']):>5}")
    print()
    print("=== fig_refix_out fresh-MD self-consistency ===")
    for slug, info in refix_consistency.items():
        ur = info.get("md_refs_unresolved", [])
        print(f"{slug}: md_refs={info.get('md_refs','?')} resolved={info.get('md_refs_resolved','?')} "
              f"unresolved={len(ur)} imgs_in_folder={info['imgs_in_folder']}")
    print()
    print("=== RG-cruft candidates (tiny dims, <120px or <20k px area) ===")
    for slug, items in cruft.items():
        print(f"{slug}: {len(items)} -> " + ", ".join(f"{i['name'][:24]}({i.get('w','?')}x{i.get('h','?')})" for i in items[:8]))
    print(f"\nreport: {OUT_DIR / 'FIG_COVERAGE_RECON.json'}")


if __name__ == "__main__":
    main()
