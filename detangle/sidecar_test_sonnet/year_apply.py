# -*- coding: utf-8 -*-
"""①year 정규화 적용 (in-place, 비파괴): bibliographic.year = int(year_print||year_online 앞4자리).
기존 필드 보존, year만 추가. 적용 직후 재검증."""
import os, json, sys
sys.stdout.reconfigure(encoding="utf-8")
SIDE = sys.argv[1] if len(sys.argv) > 1 else r"G:\corpus_20260626\sidecars"
def yint(y):
    try: return int(str(y)[:4])
    except Exception: return None

n = filled = skip = nofill = bad = 0
for fn in os.listdir(SIDE):
    if not fn.endswith(".json"): continue
    p = os.path.join(SIDE, fn)
    try: d = json.load(open(p, encoding="utf-8"))
    except Exception: bad += 1; continue
    n += 1
    if not isinstance(d.get("bibliographic"), dict):
        d["bibliographic"] = {}
    b = d["bibliographic"]
    if b.get("year") not in (None, "", 0): skip += 1; continue
    y = yint(b.get("year_print") or b.get("year_online"))
    if y is not None:
        b["year"] = y
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        filled += 1
    else:
        nofill += 1
print(f"적용: {n} sidecar | year 추가 {filled} | 이미있음 {skip} | year소스없음 {nofill} | 로드실패 {bad}")

# 재검증: 실제 채워졌나 + 구조 무손상
has = total = 0
for fn in os.listdir(SIDE):
    if not fn.endswith(".json"): continue
    total += 1
    try: d = json.load(open(os.path.join(SIDE, fn), encoding="utf-8"))
    except Exception: continue
    b = d.get("bibliographic") or {}
    if b.get("year") not in (None, "", 0): has += 1
print(f"검증: year 채워진 sidecar = {has}/{total}  (기대 ≈ {filled}, year소스없음 {nofill}편 제외)")
