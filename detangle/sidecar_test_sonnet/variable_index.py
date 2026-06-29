# -*- coding: utf-8 -*-
"""enrich: 변수/프록시 인덱스 (Gemma inventory 활용).
sidecar.variables_reported → variable_index.json:
  {variable_index:{vid:{label,kind,n_papers,papers}}, paper_variables:{pid:[vid]}, isotope_systems:{sys:[vid]}}
측정변수 기반 검색용("어느 논문이 어느 동위원소계 측정")."""
import os, json, re, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")
ROOT = sys.argv[1] if len(sys.argv) > 1 else r"G:\corpus_20260626"
SIDE = os.path.join(ROOT, "sidecars")
def nrm(s): return re.sub(r"[^a-z0-9]", "", str(s or "").lower())

# 동위원소계/프록시 그룹 (canonical id prefix → system)
SYS = [
    ("He", r"^he\d|he3_he4|he4|3he|4he|r_?ra|rcra|co2_3he"),
    ("Ne", r"^ne\d|ne20|ne21|ne22"),
    ("Ar", r"^ar\d|ar36|ar40|40ar"),
    ("Kr_Xe", r"^kr\d|^xe\d|kr8|xe12"),
    ("Sr", r"sr87_sr86|87sr"),
    ("Nd", r"nd143|143nd|epsilon_?nd"),
    ("Pb", r"pb20|20[6-8]pb"),
    ("O", r"delta_?18o|d18o|17o|delta_?17o"),
    ("H", r"delta_?d|d2h|deltad"),
    ("C", r"delta_?13c|d13c|14c"),
    ("S", r"delta_?34s|d34s|33s|36s"),
    ("N", r"delta_?15n|d15n|15n15n"),
    ("B_Li", r"delta_?11b|d11b|delta_?7li|d7li"),
    ("Cl", r"36cl|delta_?37cl|d37cl"),
    ("U_Th", r"^u$|^th$|u_th|234u|230th"),
]
def sysof(vid):
    v = vid.lower()
    for name, pat in SYS:
        if re.search(pat, v): return name
    return None

var2p = defaultdict(set); p2v = {}; vlabel = {}; vkind = {}; np_ = 0
for fn in os.listdir(SIDE):
    if not fn.endswith(".json"): continue
    try: d = json.load(open(os.path.join(SIDE, fn), encoding="utf-8"))
    except Exception: continue
    np_ += 1
    pid = d.get("id") or fn[:-5]
    vids = set()
    for v in (d.get("variables_reported") or []):
        if not isinstance(v, dict): continue
        vid = v.get("id") or ("raw:" + nrm(v.get("raw_label")))
        if vid in (None, "", "raw:"): continue
        var2p[vid].add(pid); vids.add(vid)
        vlabel.setdefault(vid, v.get("raw_label"))
        if v.get("kind"): vkind.setdefault(vid, v.get("kind"))
    p2v[pid] = sorted(vids)

vindex = {vid: {"label": vlabel.get(vid), "kind": vkind.get(vid), "n_papers": len(ps), "papers": sorted(ps)}
          for vid, ps in var2p.items()}
isosys = defaultdict(list)
for vid in vindex:
    s = sysof(vid)
    if s: isosys[s].append(vid)

out = {"corpus": "corpus_20260626", "n_papers": np_, "n_variables": len(vindex),
       "variable_index": vindex, "paper_variables": p2v, "isotope_systems": dict(isosys)}
json.dump(out, open(os.path.join(ROOT, "variable_index.json"), "w", encoding="utf-8"), ensure_ascii=False)

top = sorted(vindex.items(), key=lambda x: -x[1]["n_papers"])[:15]
pairs = sum(len(p) for p in p2v.values())
print(f"papers {np_} | unique variables {len(vindex)} | (var,paper) pairs {pairs}")
print("isotope_systems: " + " / ".join(f"{s}={len(v)}vid" for s, v in sorted(isosys.items())))
print("top 변수(논문수): " + " / ".join(f"{vid}({v['n_papers']})" for vid, v in top))
print("wrote variable_index.json (%.0f KB)" % (os.path.getsize(os.path.join(ROOT, "variable_index.json")) / 1024))
