# -*- coding: utf-8 -*-
"""sidecar doi 백필: doi 빈 sidecar를 article 본문(상단 라벨 우선)에서 regex 추출해 채움.
결정론적 $0, LLM 불필요. reference DOI 오염 방지 = doi.org/doi: 라벨 우선 + 상단 6000자."""
import os, re, json, sys
sys.stdout.reconfigure(encoding="utf-8")
ART = r"G:\corpus_20260626\articles"
SIDE = r"G:\corpus_20260626\sidecars"
LABEL_RE = re.compile(r'(?:doi\.org/|dx\.doi\.org/|doi[:\s]+)(10\.\d{4,9}/[^\s"<>}\])]+)', re.I)
PLAIN_RE = re.compile(r'10\.\d{4,9}/[^\s"<>}\])]+')
def clean(d): return re.sub(r'[).,;>]+$', '', d.strip())

def find_doi(t):
    head = t[:6000]
    m = LABEL_RE.search(head)        # 1) 상단 라벨부착 DOI (가장 신뢰)
    if m: return clean(m.group(1))
    m = PLAIN_RE.search(head)        # 2) 상단 평문 DOI (제목 근처)
    if m: return clean(m.group(0))
    m = LABEL_RE.search(t)           # 3) 전체 라벨부착(평문 reference DOI는 안 잡음)
    if m: return clean(m.group(1))
    return None

filled = 0; scanned = 0; skipped_have = 0; no_body = 0
for f in os.listdir(SIDE):
    if not f.endswith(".json"): continue
    pid = f[:-5]; p = os.path.join(SIDE, f)
    try:
        j = json.load(open(p, encoding="utf-8"))
    except Exception:
        continue
    d = j.get("doi")
    if d and str(d).strip() and str(d).lower() != "null":
        skipped_have += 1; continue
    ap = os.path.join(ART, pid + ".md")
    if not os.path.exists(ap):
        no_body += 1; continue
    scanned += 1
    t = open(ap, encoding="utf-8", errors="replace").read()
    doi = find_doi(t)
    if doi:
        j["doi"] = doi
        if not isinstance(j.get("extraction_meta"), dict): j["extraction_meta"] = {}
        j["extraction_meta"]["doi_backfill"] = "body_regex_20260626"
        json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        filled += 1

# 백필 후 채움률
total = sum(1 for f in os.listdir(SIDE) if f.endswith(".json"))
have = 0
for f in os.listdir(SIDE):
    if not f.endswith(".json"): continue
    try:
        d = json.load(open(os.path.join(SIDE, f), encoding="utf-8")).get("doi")
        if d and str(d).strip() and str(d).lower() != "null": have += 1
    except Exception: pass
print(f"백필: {filled}편 채움 (빈것 {scanned}편 스캔, article없음 {no_body})")
print(f"doi 채움률: {have}/{total} ({100*have//total}%)  [백필 전 1914=47%]")
