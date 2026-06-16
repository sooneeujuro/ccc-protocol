#!/usr/bin/env python3
"""supp_corpus_map.py — supplementary 폴더 ↔ corpus 매칭 + (--apply) corpus명 복사.

supp 폴더명 '저자 (연도) SM'은 짧아서, corpus norm이 supp norm으로 startswith 하는지로 매칭.
유일하면 확정, 복수면 ambiguous(수동), 0이면 미매칭.
--apply: G:\corpus_supplementary\<corpus_md_stem>\ 로 supp 폴더 통째 복사.
"""
import re
import json
import sys
import shutil
from pathlib import Path

ART = Path(r"G:\corpus_md_export_20260612\articles")
SUPP = Path(r"G:\WonheeLee\논문_Supplementary material")
OUT = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\SUPP_CORPUS_MAP.json")
DST = Path(r"G:\corpus_supplementary")
APPLY = "--apply" in sys.argv


def norm(s):
    s = s.lower()
    s = re.sub(r"\.(md|pdf)$", "", s)
    return re.sub(r"[^a-z0-9]", "", s)


def norm_supp(s):
    return re.sub(r"sm\d*$", "", norm(s))   # 'SM'/'SM3' 접미 제거


md = {norm(p.stem): p.stem for p in ART.glob("*.md")}   # norm -> corpus stem
supp = {}                                               # supp norm -> [folder Path]
for d in SUPP.iterdir():
    if d.is_dir():
        k = norm_supp(d.name)
        if len(k) >= 8:
            supp.setdefault(k, []).append(d)

matched = {}   # corpus stem -> supp folder Path
ambig = {}
nomatch = []
for sk, dirs in sorted(supp.items()):
    cands = [mk for mk in md if mk.startswith(sk)]
    if len(cands) == 1 and len(dirs) == 1:
        matched[md[cands[0]]] = dirs[0]
    elif len(cands) == 0:
        nomatch += [d.name for d in dirs]
    else:
        ambig[sk] = {"corpus": [md[c] for c in cands], "supp_dirs": [d.name for d in dirs]}

if APPLY:
    DST.mkdir(exist_ok=True)
    copied = skipped = 0
    for stem, src in matched.items():
        tgt = DST / stem
        if tgt.exists():
            skipped += 1
        else:
            shutil.copytree(src, tgt)
            copied += 1
    print(f"[APPLY] corpus_supplementary 복사: {copied} new, {skipped} skip -> {DST}")

result = {
    "corpus_md": len(md), "supp_folders": sum(len(v) for v in supp.values()),
    "supp_unique_norm": len(supp), "matched": len(matched),
    "ambiguous": len(ambig), "nomatch": len(nomatch),
}
OUT.write_text(json.dumps({"stats": result,
                           "matched_sample": {k: v.name for k, v in list(matched.items())[:20]},
                           "ambiguous": ambig, "nomatch": nomatch},
                          ensure_ascii=False, indent=1), encoding="utf-8")
print("=== supplementary ↔ corpus 매칭 ===")
for k, v in result.items():
    print(f"  {k:18} {v}")
print("\n=== 매칭 샘플 8 ===")
for k, v in list(matched.items())[:8]:
    print(f"  {v.name[:42]:44} -> {k[:48]}")
if ambig:
    print(f"\n=== ambiguous {len(ambig)} (수동확인) ===")
    for sk, info in list(ambig.items())[:6]:
        print(f"  supp={info['supp_dirs']} ↔ corpus후보 {len(info['corpus'])}편")
print(f"\nreport: {OUT}")
if not APPLY:
    print("복사하려면: python detangle/scripts/supp_corpus_map.py --apply")
