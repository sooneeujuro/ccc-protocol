import json, sys, re
sys.stdout.reconfigure(encoding="utf-8")
RP = r"G:\corpus_20260624\index\retrieval_papers.json"
data = json.load(open(RP, encoding="utf-8"))
papers = data if isinstance(data, list) else data.get("papers", list(data.values()) if isinstance(data, dict) else [])
print(f"retrieval_papers: {len(papers)}편 (모델의 논문 단위)\n")
# 구조
if papers: print("keys:", list(papers[0].keys()), "\n")

def blob(p): return json.dumps(p, ensure_ascii=False).lower()
queries = {
 "Torsvik 2014 (Deep mantle structure reference frame)": ["reference frame for movements", "10.1073/pnas.1318135111", "torsvik"],
 "Cande 2011 (Indian and African plate motions)": ["indian and african plate motions", "10.1038/nature10174"],
 "Mn/CH4/He anomalies in sea water": ["methane and helium anomalies", "manganese, methane"],
}
for name, terms in queries.items():
    hits = []
    for p in papers:
        b = blob(p)
        for t in terms:
            if t.lower() in b:
                hits.append((t, p.get("title") or p.get("doi") or list(p.values())[0]))
                break
    print(f"=== {name} ===")
    if hits:
        for t, ti in hits[:3]: print(f"   ◆ 모델에 있음 (matched '{t}'): {str(ti)[:70]}")
    else:
        print("   ✗ 모델(retrieval_papers)에 논문 단위로 없음")
    print()
