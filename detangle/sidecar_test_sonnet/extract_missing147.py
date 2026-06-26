# -*- coding: utf-8 -*-
"""scout 안 된 147 pid → MISSING_822에서 메타 추출 → MISSING_147.json (2차 scout 입력)."""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
B = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet"
ns = json.load(open(B + r"\DOI_SCOUT_NOT_SCOUTED.json", encoding="utf-8"))
m822 = {m["pid"]: m for m in json.load(open(B + r"\MISSING_822.json", encoding="utf-8"))}
out = [m822[p] for p in ns if p in m822]
nometa = [p for p in ns if p not in m822]
json.dump(out, open(B + r"\MISSING_147.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"MISSING_147.json: {len(out)}편 (메타없음 {len(nometa)})")
