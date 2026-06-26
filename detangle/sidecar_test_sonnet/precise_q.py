"""격리/inbox 풀 정밀 정합성: 본문 H1 전체제목 difflib 시퀀스 매칭(도메인단어 보존).
매칭된 정본 논문 제목까지 보여줘서 '같은 논문인지' 눈으로 검증 가능. Li 2024 특정."""
import os, re, glob, json, sys
from difflib import SequenceMatcher
sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"G:\corpus_20260624\articles"
POOLS = {
 "Q_duplicates(20260602)": r"G:\corpus_md_export_20260602\articles\_duplicates_quarantine",
 "Q_newdup(20260609)": r"G:\corpus_md_export_20260602\_renewal_20260609\_new_dup_quarantine",
 "Q_20260612": r"G:\corpus_md_export_20260612\quarantine",
 "coop_inbox": r"G:\corpus_build_history\outputs\corpus_v2_coop_inbox",
}
STOP = set("the of and in a to for on with from by an at as is are this".split())
def get_title(path):
    try: t = open(path, encoding="utf-8", errors="replace").read(1800)
    except: return None
    m = re.search(r"^#\s+(.+)$", t, re.M)
    return (m.group(1) if m else os.path.basename(path)[:-3]).strip()
def toks(s): return frozenset(x for x in re.findall(r"[a-z0-9]{3,}", s.lower()) if x not in STOP)
def norm(s): return " ".join(re.findall(r"[a-z0-9]+", s.lower()))

print("정본 인덱스(도메인단어 보존)...", flush=True)
ctitles = []; inv = {}
for f in glob.glob(os.path.join(CORPUS, "*.md")):
    ti = get_title(f)
    if not ti: continue
    tk = toks(ti)
    if len(tk) < 3: continue
    i = len(ctitles); ctitles.append((ti, norm(ti), tk))
    for t in tk: inv.setdefault(t, []).append(i)
print(f"  정본 {len(ctitles)}편\n", flush=True)

def best_match(ti):
    tk = toks(ti); nq = norm(ti)
    cand = {}
    for t in tk:
        for i in inv.get(t, []): cand[i] = cand.get(i, 0)+1
    best = (0.0, None)
    for i,_ in sorted(cand.items(), key=lambda x:-x[1])[:40]:
        r = SequenceMatcher(None, nq, ctitles[i][1]).ratio()
        if r > best[0]: best = (r, ctitles[i][0])
    return best

results = {}
for name, d in POOLS.items():
    if not os.path.isdir(d): continue
    incorp = []; gap = []; borderline = []
    for f in glob.glob(os.path.join(d, "*.md")):
        ti = get_title(f)
        if not ti: continue
        r, cm = best_match(ti)
        rec = {"q_title": ti[:60], "corpus_match": (cm[:60] if cm else None), "ratio": round(r,2)}
        if r >= 0.85: incorp.append(rec)
        elif r >= 0.7: borderline.append(rec)
        else: gap.append(rec)
    results[name] = {"in_corpus": len(incorp), "borderline": len(borderline), "gap": len(gap),
                     "gap_list": gap, "borderline_list": borderline}
    print(f"{name:24} 총{len(incorp)+len(borderline)+len(gap):>4}  정본有{len(incorp):>4}  애매{len(borderline):>3}  갭{len(gap):>4}")

json.dump(results, open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\PRECISE_Q.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n=== Q_newdup(20260609) 갭+애매 상세 (오격리 후보) ===")
for r in results.get("Q_newdup(20260609)",{}).get("gap",[]) + results.get("Q_newdup(20260609)",{}).get("borderline_list",[]):
    pass
qn = results.get("Q_newdup(20260609)",{})
for r in qn.get("gap_list",[]):
    print(f"  ✗갭   r={r['ratio']}  {r['q_title']}")
for r in qn.get("borderline_list",[]):
    print(f"  ?애매 r={r['ratio']}  {r['q_title']}  ↔ {r['corpus_match']}")
# Li 2024 특정
print("\n=== Li 2024 Beishan 추적 ===")
for name in POOLS:
    rr = results.get(name,{})
    for cat in ("gap_list","borderline_list"):
        for r in rr.get(cat,[]):
            if "beishan" in r["q_title"].lower() or ("li" in r["q_title"].lower()[:4] and "disposa" in r["q_title"].lower()):
                print(f"  [{name}/{cat}] r={r['ratio']} {r['q_title']} ↔ {r['corpus_match']}")
print("→ PRECISE_Q.json")
