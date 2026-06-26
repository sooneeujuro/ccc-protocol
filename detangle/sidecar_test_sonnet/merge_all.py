# -*- coding: utf-8 -*-
"""scout_parts(1차 675) + scout_parts2(2차 147) 병합 → 822 전체 candidate + safe + not_scouted."""
import os, json, glob, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8")
B = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet"

recs = {}
for pd in ["scout_parts", "scout_parts2"]:
    for f in sorted(glob.glob(os.path.join(B, pd, "b*.json"))):
        try: arr = json.load(open(f, encoding="utf-8"))
        except Exception: continue
        if isinstance(arr, list):
            for r in arr:
                p = r.get("pid")
                if p and p not in recs: recs[p] = r
recs = list(recs.values())

all_missing = [m["pid"] for m in json.load(open(B + r"\MISSING_822.json", encoding="utf-8"))]
scouted = set(r["pid"] for r in recs if r.get("pid"))
not_scouted = [p for p in all_missing if p not in scouted]

conf = {}
for r in recs: conf[r.get("confidence")] = conf.get(r.get("confidence"), 0) + 1
high_doi = sum(1 for r in recs if r.get("confidence") == "high" and r.get("candidate_doi"))

LOCAL = B + r"\DOI_SCOUT_CANDIDATES_claude.local.json"
json.dump(recs, open(LOCAL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
local_sha = hashlib.sha256(json.dumps(recs, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]
ns_sha = hashlib.sha256("\n".join(sorted(not_scouted)).encode("utf-8")).hexdigest()[:16]

SAFE = B + r"\DOI_SCOUT_CANDIDATES_claude.safe.json"
safe = {"input_missing_count": 822, "scouted_count": len(recs), "not_scouted_count": len(not_scouted),
        "high_confidence_candidate_count": conf.get("high", 0), "high_confidence_with_doi_value": high_doi,
        "medium_confidence_candidate_count": conf.get("medium", 0), "low_confidence_candidate_count": conf.get("low", 0),
        "none_found_count": conf.get("none", 0), "candidate_local_sha256_prefix": local_sha,
        "not_scouted_pidlist_sha256_prefix": ns_sha, "public_doi_values_relayed_in_ledger": False}
json.dump(safe, open(SAFE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(not_scouted, open(B + r"\DOI_SCOUT_NOT_SCOUTED.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

proj = 3174 + high_doi
print(f"전체 scouted {len(recs)}/822 | high {conf.get('high',0)}(doi값 {high_doi}) / med {conf.get('medium',0)} / low {conf.get('low',0)} / none {conf.get('none',0)} | not_scouted {len(not_scouted)}")
print(f"CODEX 적용 시 doi: 3174 -> {proj}/3996 ({100*proj//3996}%)")
print(f"local_sha {local_sha} / ns_sha {ns_sha}")
