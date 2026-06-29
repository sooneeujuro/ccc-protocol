# -*- coding: utf-8 -*-
"""①year 정규화 DRY-RUN: 정본 read-only. year 채울 수 있는 sidecar 집계 (쓰기 X)."""
import os, json, sys
sys.stdout.reconfigure(encoding="utf-8")
SIDE = sys.argv[1] if len(sys.argv) > 1 else r"G:\corpus_20260626\sidecars"
def yint(y):
    try: return int(str(y)[:4])
    except Exception: return None
n = has = fill = nofill = 0; ex = []
for fn in os.listdir(SIDE):
    if not fn.endswith(".json"): continue
    try: d = json.load(open(os.path.join(SIDE, fn), encoding="utf-8"))
    except Exception: continue
    n += 1
    b = d.get("bibliographic") if isinstance(d.get("bibliographic"), dict) else {}
    if b.get("year") not in (None, "", 0): has += 1; continue
    y = yint(b.get("year_print") or b.get("year_online"))
    if y:
        fill += 1
        if len(ex) < 5: ex.append((fn[:30], b.get("year_print"), b.get("year_online"), y))
    else:
        nofill += 1
print(f"대상: {SIDE}")
print(f"sidecar {n} | year 이미있음 {has} | year_print/online으로 채움가능 {fill} | 못채움(year소스 자체없음) {nofill}")
print("샘플(채움): " + " / ".join(f"{e[0]} yp={e[1]} yo={e[2]} -> year={e[3]}" for e in ex))
