"""no_md 진짜논문: sidecar의 provenance.md_file로 실제 MD 찾히나(=filename-mismatch 복구가능?)."""
import json, os, glob, re, sys
sys.stdout.reconfigure(encoding="utf-8")
SIDE = r"C:\Users\USER\corpus_md_export_20260612\sidecars"
ARTS = r"C:\Users\USER\corpus_md_export_20260612\articles"
j = json.load(open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\PROD_PROGRESS.json", encoding="utf-8"))
nomd = [p for p, s in j.get("fails", []) if s == "no_md"]
real = [p for p in nomd if not re.match(r"(Chapter-|Index_)", p)]
print(f"no_md 진짜논문 {len(real)}편 — provenance.md_file로 복구되나:\n")
via_mdfile = via_title = miss = 0
for pid in real:
    sp = os.path.join(SIDE, pid + ".json")
    if not os.path.exists(sp): print(f"  ? {pid[:40]} (sidecar도 없음)"); continue
    sc = json.load(open(sp, encoding="utf-8"))
    mdf = (sc.get("provenance") or {}).get("md_file", "")
    if mdf and os.path.exists(os.path.join(ARTS, mdf)):
        via_mdfile += 1
        print(f"  ✅ {pid[:38]}  →MD: {mdf[:45]}")
    else:
        # 제목/DOI로 grep 매칭 시도
        title = ((sc.get("bibliographic") or {}).get("title") or "")[:40]
        doi = sc.get("doi", "")
        miss += 1
        print(f"  ✗ {pid[:38]}  (md_file='{mdf[:30]}' 없음, doi={doi[:25]})")
print(f"\n복구가능(provenance.md_file 존재): {via_mdfile} / {len(real)}")
print(f"미발견: {miss}")
