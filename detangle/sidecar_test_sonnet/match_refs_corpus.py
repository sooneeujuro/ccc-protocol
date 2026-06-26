"""refs(corpus_refs_v20260616) vs corpus(20260618 articles) 제목 대조 — corpus에 빠진 refs 논문 수.
title 기반 1차 추정(빠르고 $0). 매칭 안 되면 누락 의심 → 진짜 누락인지는 표본 확인."""
import os, re, sys, glob
sys.stdout.reconfigure(encoding="utf-8")

REFS = r"G:\corpus_refs_v20260616\papers"
ARTS = r"G:\corpus_md_export_20260618\articles"

def strip_slug(name):  # '06864141fcf9__Title.pdf' -> 'Title'
    n = name[:-4] if name.lower().endswith(".pdf") else name
    return re.sub(r"^[0-9a-f]{8,16}__", "", n)

def toks(s):
    return set(re.findall(r"[a-z0-9]{3,}", s.lower()))

# corpus 제목 토큰셋
corpus = []
for f in os.listdir(ARTS):
    if f.endswith(".md"):
        corpus.append(toks(f[:-3]))

refs = [(f, strip_slug(f)) for f in os.listdir(REFS) if f.lower().endswith(".pdf")]
print(f"refs PDF {len(refs)}편 | corpus articles {len(corpus)}편\n")

missing = []
matched = 0
for fname, title in refs:
    rt = toks(title)
    if len(rt) < 3:
        continue
    best = 0.0
    for ct in corpus:
        if not ct:
            continue
        j = len(rt & ct) / len(rt | ct)  # Jaccard
        if j > best:
            best = j
    if best >= 0.5:
        matched += 1
    else:
        missing.append((title[:60], round(best, 2)))

print(f"=== 대조 결과 ===")
print(f"corpus에 있음(Jaccard>=0.5): {matched}/{len(refs)} ({matched/max(1,len(refs))*100:.0f}%)")
print(f"corpus에 없음(누락 의심): {len(missing)} ({len(missing)/max(1,len(refs))*100:.0f}%)")
print(f"\n=== 누락 의심 예시 25편 (best 매칭점수) ===")
for t, b in sorted(missing, key=lambda x: x[1])[:25]:
    print(f"  [j={b}] {t}")
import json
json.dump([t for t, b in missing], open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\REFS_MISSING.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n→ 누락 {len(missing)}편 제목 저장: REFS_MISSING.json")
