"""MD↔CORPUS 정합성: 모든 추출MD 풀의 본문 H1 제목이 정본 corpus에 있나.
파일명 아님(본문 H1). 역색인 Jaccard. 결정론적 $0."""
import os, re, glob, json, sys
sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"G:\corpus_20260624\articles"
POOLS = {
 "20260618(=정본 재빌드)": r"G:\corpus_md_export_20260618\articles",
 "20260602": r"G:\corpus_md_export_20260602\articles",
 "20260610": r"G:\corpus_md_export_20260610\articles",
 "20260612": r"G:\corpus_md_export_20260612\articles",
 "Atelier_pilot": r"G:\Atelier_Handoff_2026-05-19_full_corpus\article_corpus\pilot",
 "PaperAtelier_datalab": r"G:\Paper_Atelier\datalab\pilot",
 "Q_duplicates(20260602)": r"G:\corpus_md_export_20260602\articles\_duplicates_quarantine",
 "Q_newdup(20260609)": r"G:\corpus_md_export_20260602\_renewal_20260609\_new_dup_quarantine",
 "Q_20260612": r"G:\corpus_md_export_20260612\quarantine",
 "coop_inbox": r"G:\corpus_build_history\outputs\corpus_v2_coop_inbox",
}
STOP = set("the of and in a to for on with from by an at as is are this study using used between within new evidence isotope isotopes".split())
def title_tokens(path):
    try: t = open(path, encoding="utf-8", errors="replace").read(1800)
    except: return None
    m = re.search(r"^#\s+(.+)$", t, re.M)
    raw = m.group(1) if m else os.path.basename(path)[:-3]
    toks = frozenset(x for x in re.findall(r"[a-z0-9]{3,}", raw.lower()) if x not in STOP)
    return toks if len(toks) >= 3 else None

# 정본 인덱스 + 역색인
print("정본 corpus 인덱스...", flush=True)
corpus = []
inv = {}
for f in glob.glob(os.path.join(CORPUS, "*.md")):
    tk = title_tokens(f)
    if tk:
        i = len(corpus); corpus.append(tk)
        for t in tk: inv.setdefault(t, []).append(i)
print(f"  정본 {len(corpus)}편 인덱싱\n", flush=True)

def in_corpus(tk):
    cand = {}
    for t in tk:
        for i in inv.get(t, []): cand[i] = cand.get(i, 0) + 1
    best = 0.0
    for i, sh in sorted(cand.items(), key=lambda x:-x[1])[:30]:
        c = corpus[i]; j = len(tk & c)/len(tk | c)
        if j > best: best = j
        if best >= 0.7: break
    return best

summary = []; gaps = {}   # norm_title -> {"pools":[], "sample": tokens}
for name, d in POOLS.items():
    if not os.path.isdir(d): summary.append((name, 0, 0, 0)); continue
    tot = mat = 0; pg = 0
    for f in glob.glob(os.path.join(d, "*.md")):
        tk = title_tokens(f)
        if not tk: continue
        tot += 1
        if in_corpus(tk) >= 0.6: mat += 1
        else:
            pg += 1
            key = " ".join(sorted(tk))
            gaps.setdefault(key, {"pools": [], "n": len(tk)})
            if name not in gaps[key]["pools"]: gaps[key]["pools"].append(name)
    summary.append((name, tot, mat, pg))
    print(f"  {name:28} 총{tot:>5}  정본有{mat:>5}  갭{pg:>4}", flush=True)

print(f"\n=== 유니크 갭(제목 기준, 정본에 없음): {len(gaps)} ===")
# 격리 풀에만 있는 갭(=실제 복구대상) 우선
json.dump({"summary": summary, "unique_gaps": len(gaps),
           "gaps": [{"title_tokens": k, "pools": v["pools"]} for k, v in gaps.items()]},
          open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\MD_CORPUS_GAPS.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
poolcount = Counter()
for v in gaps.values():
    for p in v["pools"]: poolcount[p] += 1
print("갭이 나온 풀별 분포:")
for p, c in poolcount.most_common(): print(f"   {p:28} {c}")
print("\n→ MD_CORPUS_GAPS.json")
