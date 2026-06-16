#!/usr/bin/env python3
"""fig_merge.py — 51편 그림 채우기 머지 (비파괴, idempotent, dry-run 기본).

전략 (운영자 결정 2026-06-16: cruft 필터 안 함, 10편 있는 그대로):
  STEP A (재변환 10편): articles의 기존 corpus MD를 fig_refix 새 MD로 교체
       (기존 MD는 BACKUP으로 먼저 복사). fig_refix 이미지 전부 articles로 복사.
  STEP B (나머지 derived fill): STEP A 반영 후 남은 missing ref를
       derived\<slug>\images\<hash>_img.jpg -> articles\<slug>__<hash>_img.jpg 로 복사.

비파괴: 덮어쓰는 건 MD뿐이고 전부 BACKUP에 원본 보관. 이미지는 articles에
없는 것만 추가(additive). 다시 돌려도 안전(idempotent).

dry-run(기본): 아무것도 안 씀, 카운트만. 실제 적용: --apply
"""
import re
import sys
import shutil
import time
from collections import defaultdict
from pathlib import Path

CORPUS = Path(r"G:\corpus_md_export_20260612")
ARTICLES = CORPUS / "articles"
DERIVED = Path(r"G:\datalab_runs_v20260616\derived")
REFIX = Path(r"G:\fig_refix_out")
BACKUP = CORPUS / "_fig_merge_backup_20260616"
LEDGER = CORPUS / "FIGURES_MERGE_LEDGER_20260616.txt"
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
IMG_EXT = (".jpg", ".jpeg", ".png")
SLUG_RE = re.compile(r"^([0-9a-f]{12})__(.+)$")
APPLY = "--apply" in sys.argv


def md_refs(text):
    out = []
    for m in IMG_RE.finditer(text):
        tgt = m.group(1).strip().split()[0] if m.group(1).strip() else ""
        if not tgt or tgt.startswith(("http://", "https://", "data:")):
            continue
        out.append(tgt.replace("\\", "/").rsplit("/", 1)[-1])
    return out


def main():
    t0 = time.time()
    mode = "APPLY (실제 쓰기)" if APPLY else "DRY-RUN (안 씀)"
    print(f"=== fig_merge {mode} ===\n")
    led = []

    articles_have = {f.name for f in ARTICLES.iterdir() if f.suffix.lower() in IMG_EXT}
    md_to_refs = {md.name: md_refs(md.read_text(encoding="utf-8", errors="replace"))
                  for md in ARTICLES.glob("*.md")}

    # slug -> 기존 corpus MD (slug__ missing 참조하는 것)
    slug_existing = defaultdict(set)
    for md, refs in md_to_refs.items():
        for r in refs:
            if r not in articles_have:
                m = SLUG_RE.match(r)
                if m:
                    slug_existing[m.group(1)].add(md)

    refix_slugs = sorted(p.name for p in REFIX.iterdir() if p.is_dir())

    # ---------- STEP A ----------
    print("=== STEP A: 재변환 10편 (MD 교체 + 이미지 복사) ===")
    if APPLY:
        BACKUP.mkdir(exist_ok=True)
    md_replaced = imgA = 0
    warn = []
    for slug in refix_slugs:
        folder = REFIX / slug
        new_md = sorted(folder.rglob("*.md"))[0]
        existing = sorted(slug_existing.get(slug, []))
        same = new_md.name in existing
        print(f"[{slug}] same_name={same} existing={len(existing)}")
        if not existing:
            warn.append(f"{slug}: 기존 corpus MD를 못 찾음 (missing ref 역추적 실패)")
        # 기존 MD 백업 + (이름 다르면) 제거
        for em in existing:
            src = ARTICLES / em
            if src.exists():
                if APPLY:
                    shutil.copy2(src, BACKUP / em)
                if em != new_md.name and APPLY:
                    src.unlink()
            md_to_refs.pop(em, None)
        # 새 MD 반영
        if APPLY:
            shutil.copy2(new_md, ARTICLES / new_md.name)
        md_to_refs[new_md.name] = md_refs(new_md.read_text(encoding="utf-8", errors="replace"))
        md_replaced += 1
        # 이미지 복사 (additive)
        for img in folder.rglob("*"):
            if img.suffix.lower() in IMG_EXT and img.name not in articles_have:
                if APPLY:
                    shutil.copy2(img, ARTICLES / img.name)
                    led.append(f"A\t{img.name}\t{img.stat().st_size}")
                articles_have.add(img.name)
                imgA += 1
    print(f"-> MD 교체 {md_replaced}, refix 이미지 복사 {imgA}\n")

    # ---------- STEP B ----------
    print("=== STEP B: 나머지 derived fill ===")
    missing = {}
    for md, refs in md_to_refs.items():
        for r in refs:
            if r not in articles_have:
                missing.setdefault(r, md)
    imgB = 0
    still = []
    for name in sorted(missing):
        m = SLUG_RE.match(name)
        if not m:
            still.append(name)
            continue
        slug, rest = m.group(1), m.group(2)
        src = DERIVED / slug / "images" / rest
        if src.exists():
            if APPLY:
                shutil.copy2(src, ARTICLES / name)
                led.append(f"B\t{name}\t{src.stat().st_size}")
            articles_have.add(name)
            imgB += 1
        else:
            still.append(name)
    print(f"-> derived 복사 {imgB}, 여전히 missing {len(still)}")
    if still:
        print("   still sample:", still[:8])

    if APPLY and led:
        with LEDGER.open("a", encoding="utf-8") as f:
            f.write("\n".join(led) + "\n")

    print(f"\n=== 요약 ({mode}) ===")
    print(f"MD 교체: {md_replaced} | 이미지 복사: STEP A {imgA} + STEP B {imgB} = {imgA + imgB}")
    print(f"잔여 missing: {len(still)} (게이트는 allowlist로 처리)")
    if warn:
        print("⚠ 경고:")
        for w in warn:
            print("  ", w)
    print(f"백업 위치: {BACKUP}")
    print(f"({time.time()-t0:.0f}s)")
    if not APPLY:
        print("\n실제 적용하려면: python detangle/scripts/fig_merge.py --apply")


if __name__ == "__main__":
    main()
