# -*- coding: utf-8 -*-
"""⑦ 후 마무리: CORPUS_VERSION의 doi count 재집계 + variable_index 포인터 추가."""
import os, json, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = sys.argv[1] if len(sys.argv) > 1 else r"G:\corpus_20260626"
def nd(d): return bool(d and str(d).strip() and str(d).lower() != "null")
SIDE = os.path.join(ROOT, "sidecars")
total = have = 0
for fn in os.listdir(SIDE):
    if not fn.endswith(".json"): continue
    total += 1
    try: d = json.load(open(os.path.join(SIDE, fn), encoding="utf-8"))
    except Exception: continue
    if nd(d.get("doi")): have += 1
p = os.path.join(ROOT, "CORPUS_VERSION.json")
cv = json.load(open(p, encoding="utf-8"))
cv["sidecar_doi_nonempty"] = have
cv["sidecar_doi_empty"] = total - have
cv["variable_index"] = "variable_index.json"
json.dump(cv, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"CORPUS_VERSION: doi_nonempty {have} / doi_empty {total - have} + variable_index 포인터")
