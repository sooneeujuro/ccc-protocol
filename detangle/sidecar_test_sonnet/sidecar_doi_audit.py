# -*- coding: utf-8 -*-
"""sidecar doi 채움률 진단: 본문 DOI와 교차해 'Haiku 누락' vs '원래 DOI 없음' 구분.
+ variables_reported(Gemma 인벤토리) 채움률 = sidecar 주력 가치 확인."""
import os, re, json, sys
sys.stdout.reconfigure(encoding="utf-8")
ART = r"G:\corpus_20260626\articles"
SIDE = r"G:\corpus_20260626\sidecars"
DOI_RE = re.compile(r'10\.\d{4,9}/[^\s"<>}\])]+')

# sidecar: doi 유무 + variables_reported 개수
side_doi = {}; side_vars = {}
for f in os.listdir(SIDE):
    if not f.endswith(".json"): continue
    pid = f[:-5]
    try:
        j = json.load(open(os.path.join(SIDE, f), encoding="utf-8"))
        d = j.get("doi"); side_doi[pid] = bool(d and str(d).strip() and str(d).lower() != "null")
        v = j.get("variables_reported"); side_vars[pid] = len(v) if isinstance(v, list) else 0
    except Exception:
        side_doi[pid] = False; side_vars[pid] = 0

n_side = len(side_doi)
doi_filled = sum(side_doi.values())
vars_filled = sum(1 for v in side_vars.values() if v > 0)
vars_vals = sorted(side_vars.values())
med = vars_vals[len(vars_vals)//2] if vars_vals else 0

# article 본문 DOI 교차
both = body_only = side_only = neither = 0
backfill = []
for af in os.listdir(ART):
    if not af.endswith(".md"): continue
    pid = af[:-3]
    try:
        t = open(os.path.join(ART, af), encoding="utf-8", errors="replace").read()
    except Exception:
        t = ""
    body_has = bool(DOI_RE.search(t))
    side_has = side_doi.get(pid, False)
    if body_has and side_has: both += 1
    elif body_has and not side_has: body_only += 1; backfill.append(pid)
    elif side_has and not body_has: side_only += 1
    else: neither += 1

print("=== sidecar 채움률 (3996) ===")
print(f"  doi 채워짐         : {doi_filled}/{n_side} ({100*doi_filled//n_side}%)")
print(f"  variables_reported : {vars_filled}/{n_side} ({100*vars_filled//n_side}%) 채워짐, median {med}개/편")
print("\n=== 본문 DOI vs sidecar doi 교차 (article 3997 기준) ===")
print(f"  본문O sidecarO (정상)             : {both}")
print(f"  본문O sidecarX (★Haiku 누락=백필가능): {body_only}")
print(f"  본문X sidecarO (Haiku가 외부서 보강): {side_only}")
print(f"  본문X sidecarX (원래 DOI 없음=책/한국/구논문): {neither}")
print(f"\n=> sidecar doi 빈 것 중 {body_only}편은 본문에 DOI 있음 → $0 결정론적 백필 가능")
print(f"=> {neither}편은 본문에도 DOI 없음 → 원래 DOI 미보유(정상)")
json.dump({"doi_filled": doi_filled, "vars_filled": vars_filled, "vars_median": med,
           "cross": {"both": both, "body_only": body_only, "side_only": side_only, "neither": neither},
           "backfill_pids": backfill},
          open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\SIDECAR_DOI_AUDIT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
