"""격리된 98편(_new_dup_quarantine)이 진짜 corpus에 있나(진짜dup) vs 없나(오격리=복구대상) 대조."""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
Q = r"G:\corpus_md_export_20260602\_renewal_20260609\_new_dup_quarantine"
ARTS = r"G:\corpus_20260624\articles"

def toks(s): return set(re.findall(r"[a-z0-9]{3,}", s.lower()))
corpus = [toks(f[:-3]) for f in os.listdir(ARTS) if f.endswith(".md")]
qfiles = [f for f in os.listdir(Q) if f.endswith(".md")]

in_corpus = []; missing = []
for f in qfiles:
    rt = toks(f[:-3])
    best = max((len(rt & ct)/len(rt | ct) for ct in corpus if ct), default=0)
    if best >= 0.5: in_corpus.append(f[:-3])
    else: missing.append((f[:-3], round(best,2)))

print(f"격리 {len(qfiles)}편 → corpus에 있음(진짜dup): {len(in_corpus)} | corpus에 없음(오격리=복구대상): {len(missing)}")
print(f"\n=== 오격리(복구 필요) {len(missing)}편 ===")
for t,b in sorted(missing, key=lambda x:x[1]):
    print(f"  [j={b}] {t[:72]}")
import json
json.dump([t for t,b in missing], open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\QUARANTINE_MISSING.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n→ 저장: QUARANTINE_MISSING.json")
