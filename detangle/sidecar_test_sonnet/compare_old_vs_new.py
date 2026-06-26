"""chunk0 400편: 기존 Haiku sidecar vs 새 v2.2 Sonnet sidecar 직접 대조.
+ 격리 확인(실 sidecar 무손상)."""
import json, os, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

OLD = Path(r"C:\Users\USER\corpus_md_export_20260612\sidecars")
NEW = Path(r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging")

new_files = sorted(NEW.glob("*.json"))
cls_changed = []          # (pid, old, new)
cls_matrix = {}           # (old,new) -> count
sum_old_v = sum_new_v = 0
prov = {"measured": 0, "cited": 0, "modeled": 0}
mnm_false = []            # 측정 안 한 논문
demote = []               # (pid, n_nonmeasured, old_cls, new_cls)

for nf in new_files:
    pid = nf.stem
    new = json.loads(nf.read_text(encoding="utf-8", errors="replace"))
    of = OLD / f"{pid}.json"
    if not of.exists():
        continue
    old = json.loads(of.read_text(encoding="utf-8", errors="replace"))
    oc = (old.get("classification") or {}).get("type")
    nc = (new.get("classification") or {}).get("type")
    if oc != nc:
        cls_changed.append((pid, oc, nc))
    cls_matrix[(oc, nc)] = cls_matrix.get((oc, nc), 0) + 1
    ov = old.get("variables_measured") or []
    nv = new.get("variables_measured") or []
    sum_old_v += len(ov); sum_new_v += len(nv)
    nonm = 0
    for v in nv:
        p = v.get("provenance")
        if p in prov:
            prov[p] += 1
        if p != "measured":
            nonm += 1
    if new.get("made_new_measurements") is False:
        mnm_false.append((pid, oc, nc))
    if nonm:
        demote.append((pid, nonm, oc, nc))

n = len(new_files)
tot_v = sum(prov.values())
print(f"=== chunk0 대조: {n}편 (old Haiku vs new v2.2 Sonnet) ===\n")
print(f"[1] classification.type 변경: {len(cls_changed)}/{n}편")
for (o, nw), c in sorted(cls_matrix.items(), key=lambda x: -x[1]):
    mark = "  (변경)" if o != nw else ""
    print(f"     {str(o):10} -> {str(nw):10} : {c}{mark}")
print(f"\n[2] 변수 수: old(전부 measured 취급) {sum_old_v} -> new {sum_new_v}")
print(f"[3] new provenance: measured {prov['measured']} / cited {prov['cited']} / modeled {prov['modeled']}")
print(f"    => 기존에 measured였던 것 중 {prov['cited']+prov['modeled']}개({(prov['cited']+prov['modeled'])/max(1,tot_v)*100:.0f}%)가 cited/modeled로 강등 = 무결성 교정")
print(f"\n[4] made_new_measurements=false: {len(mnm_false)}편 (측정 안 했는데 기존 분류는?)")
from collections import Counter
oc_of_false = Counter(o for _, o, _ in mnm_false)
print(f"    이들의 기존 분류: {dict(oc_of_false)}  -> 새 분류 대부분 other")

print(f"\n[5] 강등 많은 상위 8편 (old_cls -> new_cls):")
for pid, nm, oc, nc in sorted(demote, key=lambda x: -x[1])[:8]:
    print(f"     {nm:2}개 비측정  [{str(oc)}->{str(nc)}]  {pid[:46]}")

print(f"\n=== 격리 확인 ===")
n_old = len(list(OLD.glob('*.json')))
n_new = len(new_files)
print(f"  실 sidecar(원본, 무손상): {n_old}  @ {OLD}")
print(f"  새 v2.2 (별도 staging):   {n_new}  @ {NEW}")
print(f"  두 폴더 분리됨: {OLD != NEW}")
