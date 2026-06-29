# -*- coding: utf-8 -*-
"""⑦ no-DOI 재scout high-conf DOI를 sidecar에 적용 (중복 collision reject). G:canonical, 비파괴."""
import os, json, glob, re, sys
sys.stdout.reconfigure(encoding="utf-8")
B = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet"
SIDE = r"G:\corpus_20260626\sidecars"
def ndoi(d):
    if not d: return ""
    d = str(d).strip().lower(); d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d); return d.strip().strip(".")

recs = {}
for f in sorted(glob.glob(os.path.join(B, "scout_parts_nodoi", "b*.json"))):
    try: arr = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    if isinstance(arr, list):
        for r in arr:
            if isinstance(r, dict) and r.get("pid"): recs[r["pid"]] = r

existing = set()
for fn in os.listdir(SIDE):
    if not fn.endswith(".json"): continue
    try: d = json.load(open(os.path.join(SIDE, fn), encoding="utf-8"))
    except Exception: continue
    dd = ndoi(d.get("doi"))
    if dd: existing.add(dd)

applied = collision = skip = 0; ex = []
for pid, r in recs.items():
    if r.get("confidence") != "high" or not r.get("candidate_doi"): skip += 1; continue
    doi = ndoi(r["candidate_doi"])
    if not doi: skip += 1; continue
    if doi in existing: collision += 1; continue
    p = os.path.join(SIDE, pid + ".json")
    if not os.path.exists(p): skip += 1; continue
    d = json.load(open(p, encoding="utf-8"))
    if d.get("doi") and str(d["doi"]).strip() and str(d["doi"]).lower() != "null": skip += 1; continue
    d["doi"] = doi
    if not isinstance(d.get("extraction_meta"), dict): d["extraction_meta"] = {}
    d["extraction_meta"]["doi_backfill"] = "nodoi_rescout_20260629"
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    existing.add(doi); applied += 1
    if len(ex) < 5: ex.append((pid[:32], doi))

total = have = 0
for fn in os.listdir(SIDE):
    if not fn.endswith(".json"): continue
    total += 1
    try: d = json.load(open(os.path.join(SIDE, fn), encoding="utf-8"))
    except Exception: continue
    if ndoi(d.get("doi")): have += 1
print(f"⑦ 적용: high {applied} | collision reject {collision} | skip(medium/none/이미있음) {skip}")
print(f"sidecar doi 채움: {have}/{total}  (⑦ 전 3882)")
for p, doi in ex: print(f"  {p} -> {doi}")
