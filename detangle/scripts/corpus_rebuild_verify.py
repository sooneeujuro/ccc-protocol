#!/usr/bin/env python3
"""corpus_rebuild_verify.py — 새 corpus 무결성 게이트 + 누락 figure 목록 (READ-ONLY).

'충돌'과 '누락'을 구분한다 (둘은 완전 다른 문제):
  - 충돌위험 = MD가 bare hash(<slug>__ 아님)를 참조하는데 그 파일이 실제로 있음 → 덮어쓰기 가능 (진짜 꼬임). 0이어야 PASS.
  - 누락 = MD가 참조하는데 폴더에 파일 없음 → Datalab이 그 figure를 못 뽑음 (꼬임 아님). 목록만 뽑아 수동 추출 대상으로.
출력: MISSING_FIGURES.json (논문 / figure 설명 / hash / 폴더) — 운영자가 PDF에서 직접 들고올 리스트.
"""
import re
import json
from pathlib import Path
from collections import defaultdict

REBUILD = Path(r"G:\corpus_rebuild_20260618")
OUT = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\MISSING_FIGURES.json")
IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")   # group1=alt(figure 설명), group2=target

slug_folders = [d for d in REBUILD.iterdir() if d.is_dir()]
n_md = n_img = n_done = 0
collision_risk = []      # bare 참조 + 파일 존재 = 진짜 충돌위험
missing_figs = []        # 참조했는데 파일 없음 = Datalab 누락 (수동 추출 대상)
hash_to_folders = defaultdict(set)

for d in slug_folders:
    mds = list(d.glob("*.md"))
    if not mds:
        continue
    n_md += 1
    if (d / ".done").exists():
        n_done += 1
    md = mds[0]
    imgs = {f.name for f in d.glob("*_img.*")}
    n_img += len(imgs)
    for f in imgs:
        m = re.match(r"^[0-9a-f]{12}__([0-9a-f]{32})", f)
        if m:
            hash_to_folders[m.group(1)].add(d.name)
    for mm in IMG.finditer(md.read_text(encoding="utf-8", errors="replace")):
        alt, tgt = mm.group(1), mm.group(2).strip().replace(chr(92), "/").rsplit("/", 1)[-1]
        if not re.search(r"\.(jpg|jpeg|png)$", tgt, re.I):
            continue
        is_namespace = tgt.startswith(d.name + "__")
        exists = tgt in imgs
        if not exists:
            missing_figs.append({"paper": md.stem[:70], "slug": d.name,
                                  "figure": alt[:90] or "(no caption)", "hash_ref": tgt})
        elif not is_namespace:
            collision_risk.append({"slug": d.name, "ref": tgt})   # 파일 있는데 bare = 위험

shared = sum(1 for h, fs in hash_to_folders.items() if len(fs) > 1)

print("=== 새 corpus 무결성 게이트 ===")
print(f"논문(slug 폴더): {n_md} (.done {n_done}) | 이미지: {n_img}")
print(f"[충돌위험] bare 참조 + 파일 존재(덮어쓰기 가능): {len(collision_risk)}  {'PASS ✅' if not collision_risk else 'FAIL ❌'}")
print(f"[격리 증명] 공유 hash {shared}건 = 각자 다른 slug 폴더로 물리 분리(덮어쓰기 0)")
print(f"[누락] Datalab이 못 뽑은 figure(꼬임 아님, 수동추출 대상): {len(missing_figs)}")
gate = not collision_risk
print(f"\n>>> 충돌 게이트: {'PASS — 꼬임 0' if gate else 'FAIL — 충돌위험 있음!'} <<<")
if collision_risk:
    print("충돌위험 샘플:", collision_risk[:5])

OUT.write_text(json.dumps({"collision_risk": collision_risk, "missing_figures": missing_figs},
                          ensure_ascii=False, indent=1), encoding="utf-8")
print(f"\n누락 figure {len(missing_figs)}건 → {OUT} (논문/figure설명/hash, PDF 수동추출용)")
if missing_figs:
    print("--- 누락 샘플 ---")
    for x in missing_figs[:8]:
        print(f"  [{x['paper'][:45]}] {x['figure'][:55]}")
