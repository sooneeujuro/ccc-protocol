# -*- coding: utf-8 -*-
"""3차: 누락후보(DOI 본문에도 없음)를 제목/저자 토큰으로 article 파일명 재확인.
DOI artifact(corpus에 다른표기로 존재) 거르고 진짜 누락 확정."""
import os, re, json, sys
sys.stdout.reconfigure(encoding="utf-8")
ART = r"G:\corpus_20260626\articles"
CHK2 = json.load(open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\REF260624_CHECK2.json", encoding="utf-8"))
miss = list(CHK2["truly_missing"]) + list(CHK2.get("no_doi_missing", []))

arts = [f[:-3] for f in os.listdir(ART) if f.endswith(".md")]
def toks(s):
    s = re.sub(r'\.pdf$', '', s, flags=re.I)
    return set(t for t in re.split(r'[^a-z0-9가-힣]+', s.lower()) if len(t) >= 4)
art_tok = {a: toks(a) for a in arts}

print(f"누락후보 {len(miss)}편 제목/저자 토큰 재확인\n")
found_alt = []; real_missing = []
for pf in miss:
    ft = toks(pf)
    best = (0.0, 0, None)
    for a, at in art_tok.items():
        inter = len(ft & at)
        if inter >= 3:
            j = inter / max(1, len(ft | at))
            if (j, inter) > (best[0], best[1]): best = (j, inter, a)
    if best[2] and best[1] >= 4 and best[0] >= 0.30:
        found_alt.append((pf, best[2], best[1], round(best[0], 2)))
    else:
        real_missing.append(pf)

print(f"[corpus에 다른표기로 존재 = DOI artifact, 누락 아님] {len(found_alt)}편")
for pf, a, inter, j in found_alt:
    print(f"   {pf[:42]}  ->  {a[:42]}  (공통{inter},J{j})")
print(f"\n[진짜 누락 확정] {len(real_missing)}편")
for pf in real_missing:
    print(f"   MISSING  {pf[:64]}")
json.dump({"doi_artifact_found": [{"pdf": x[0], "article": x[1]} for x in found_alt],
           "real_missing": real_missing},
          open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\REF260624_FINAL.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n=== 논문_260624 최종: 91편 중 corpus有 {91 - len(real_missing)} / 진짜누락 {len(real_missing)} ===")
