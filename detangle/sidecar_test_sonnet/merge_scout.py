# -*- coding: utf-8 -*-
"""scout_parts/b*.json(28) 병합 → DOI_SCOUT_CANDIDATES_claude.local.json + .safe.json.
미완 122편(spend limit batch) = DOI_SCOUT_NOT_SCOUTED.json. 로컬 $0."""
import os, json, glob, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet"
PARTS = os.path.join(BASE, "scout_parts")
MISS = os.path.join(BASE, "MISSING_822.json")

recs = {}
for f in sorted(glob.glob(os.path.join(PARTS, "b*.json"))):
    try: arr = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    if isinstance(arr, list):
        for r in arr:
            p = r.get("pid")
            if p and p not in recs: recs[p] = r
recs = list(recs.values())

all_missing = [m["pid"] for m in json.load(open(MISS, encoding="utf-8"))]
scouted = set(r["pid"] for r in recs if r.get("pid"))
not_scouted = [p for p in all_missing if p not in scouted]

conf = {}
for r in recs:
    c = r.get("confidence"); conf[c] = conf.get(c, 0) + 1
high_with_doi = sum(1 for r in recs if r.get("confidence") == "high" and r.get("candidate_doi"))

# local artifact (full)
LOCAL = os.path.join(BASE, "DOI_SCOUT_CANDIDATES_claude.local.json")
json.dump(recs, open(LOCAL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
local_sha = hashlib.sha256(json.dumps(recs, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]

# not-scouted list
NS = os.path.join(BASE, "DOI_SCOUT_NOT_SCOUTED.json")
json.dump(not_scouted, open(NS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ns_sha = hashlib.sha256("\n".join(sorted(not_scouted)).encode("utf-8")).hexdigest()[:16]

# safe summary (counts/hash only — CODEX contract)
SAFE = os.path.join(BASE, "DOI_SCOUT_CANDIDATES_claude.safe.json")
safe = {
    "input_missing_count": 822,
    "scouted_count": len(recs),
    "not_scouted_count": len(not_scouted),
    "not_scouted_reason": "workflow_monthly_spend_limit_batches_26_27_30_31_32",
    "high_confidence_candidate_count": conf.get("high", 0),
    "high_confidence_with_doi_value": high_with_doi,
    "medium_confidence_candidate_count": conf.get("medium", 0),
    "low_confidence_candidate_count": conf.get("low", 0),
    "none_found_count": conf.get("none", 0),
    "candidate_local_sha256_prefix": local_sha,
    "not_scouted_pidlist_sha256_prefix": ns_sha,
    "public_doi_values_relayed_in_ledger": False
}
json.dump(safe, open(SAFE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"local {len(recs)} records -> {os.path.basename(LOCAL)} (sha {local_sha})")
print(f"not_scouted {len(not_scouted)} -> {os.path.basename(NS)} (sha {ns_sha})")
print(f"safe summary: high {conf.get('high',0)} (doi값있음 {high_with_doi}) / med {conf.get('medium',0)} / low {conf.get('low',0)} / none {conf.get('none',0)}")
