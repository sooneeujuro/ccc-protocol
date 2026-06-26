"""REFS_MISSING.json(205)를 분류: 진짜 논문(읽을 제목) vs UUID/해시 vs 잡파일.
진짜-논문-누락만이 실제 갭. UUID는 매칭불가 가짜누락(slug/DOI로 따로 확인 필요)."""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
m = json.load(open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\REFS_MISSING.json", encoding="utf-8"))

JUNK = re.compile(r"\b(sup|suppl|supplement|s0\d|menu|toc|cover|index|readme)\b", re.I)
def classify(t):
    toks = re.findall(r"[A-Za-z0-9]+", t)
    if not toks: return "empty"
    alpha = [x for x in toks if re.search(r"[a-z]{3,}", x.lower()) and not re.fullmatch(r"[0-9a-f]{4,}", x.lower())]
    hexish = [x for x in toks if re.fullmatch(r"[0-9a-f]{4,}", x.lower())]
    # UUID/해시 우세 = 제목없음
    if len(hexish) >= 3 and len(alpha) < 2: return "uuid_hash"
    if JUNK.search(t) and len(alpha) < 4: return "junk"
    if len(alpha) >= 3: return "real_paper"
    return "ambiguous"

buckets = {}
for t in m:
    buckets.setdefault(classify(t), []).append(t)

print("=== REFS_MISSING 205편 분류 ===")
for k in ["real_paper", "uuid_hash", "junk", "ambiguous", "empty"]:
    print(f"  {k}: {len(buckets.get(k,[]))}")
print(f"\n=== 진짜 논문인데 누락 (실제 갭) — {len(buckets.get('real_paper',[]))}편 ===")
for t in sorted(buckets.get("real_paper", []))[:40]:
    print(f"  · {t}")
json.dump(buckets.get("real_paper", []), open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\REFS_MISSING_REAL.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n→ 진짜누락 {len(buckets.get('real_paper',[]))}편 저장: REFS_MISSING_REAL.json (UUID {len(buckets.get('uuid_hash',[]))}편은 slug/DOI로 별도확인 필요)")
