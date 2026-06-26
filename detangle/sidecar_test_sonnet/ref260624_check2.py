# -*- coding: utf-8 -*-
"""2차: 미매칭 37 DOI를 corpus article 본문에서 직접 grep (sidecar doi 누락 보정).
+ no_doi 5는 파일명 저자+연도+키워드로 article 파일명/본문 확인."""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
OUT = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\REF260624_CHECK.json"
ART = r"G:\corpus_20260626\articles"
CHK = json.load(open(OUT, encoding="utf-8"))
def core(d): return re.sub(r'[().,;>]+$', '', d).lower()

# 미매칭 DOI 코어 -> pdf
targets = {}
for u in CHK["unmatched"]:
    for d in u["dois"]:
        c = core(d)
        if len(c) > 12: targets.setdefault(c, u["pdf"])

# no_doi: 파일명에서 저자/연도/키워드 토큰
def toks(s): return [t for t in re.split(r'[^a-z0-9]+', s.lower()) if len(t) >= 4]
no_doi = CHK["no_doi"]

# corpus article 본문 1패스: DOI 존재 + no_doi 제목토큰 매칭
arts = [f for f in os.listdir(ART) if f.endswith(".md")]
art_names = [a[:-3] for a in arts]
found_doi = set()
# no_doi 각 PDF의 토큰셋
nd_tok = {pf: set(toks(pf)) for pf in no_doi}
nd_hit = {pf: None for pf in no_doi}

for i, af in enumerate(arts):
    try:
        t = open(os.path.join(ART, af), encoding="utf-8", errors="replace").read().lower()
    except Exception:
        continue
    for c in targets:
        if c not in found_doi and c in t:
            found_doi.add(c)
    # no_doi 제목토큰: article 본문에 PDF 토큰 다수 포함되면 후보
    an = af.lower()
    for pf, tk in nd_tok.items():
        if nd_hit[pf]: continue
        inter = sum(1 for x in tk if x in an or x in t[:3000])
        if len(tk) and inter / len(tk) >= 0.6 and inter >= 4:
            nd_hit[pf] = af

# 미매칭 37 분류
in_corpus = []; missing = []
for u in CHK["unmatched"]:
    if any(core(d) in found_doi for d in u["dois"]): in_corpus.append(u["pdf"])
    else: missing.append((u["pdf"], u["dois"]))

print(f"=== 미매칭 37 본문 DOI grep ===")
print(f"본문에 DOI 존재(=corpus有, sidecar doi만 누락): {len(in_corpus)}")
print(f"본문에도 DOI 없음(진짜 누락 후보): {len(missing)}")
for pf, ds in missing: print("   MISSING:", pf[:56], "|", (ds[0] if ds else ""))

print(f"\n=== no_doi 5 제목토큰 매칭 ===")
for pf in no_doi:
    print(("   FOUND  " if nd_hit[pf] else "   MISS   ") + pf[:50] + (" -> " + nd_hit[pf][:40] if nd_hit[pf] else ""))

# 최종 집계
matched1 = len(CHK["matched"])
total_in = matched1 + len(in_corpus) + sum(1 for pf in no_doi if nd_hit[pf])
total_miss = len(missing) + sum(1 for pf in no_doi if not nd_hit[pf])
print(f"\n=== 최종: 91편 중 corpus有 {total_in} / 진짜 누락후보 {total_miss} ===")
json.dump({"in_corpus_body": in_corpus, "truly_missing": [m[0] for m in missing],
           "no_doi_found": {pf: nd_hit[pf] for pf in no_doi if nd_hit[pf]},
           "no_doi_missing": [pf for pf in no_doi if not nd_hit[pf]]},
          open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\REF260624_CHECK2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
