import json, sys, os
sys.stdout.reconfigure(encoding="utf-8")
RP = r"G:\corpus_20260624\index\retrieval_papers.json"
ART = r"G:\corpus_20260624\articles"
data = json.load(open(RP, encoding="utf-8"))
if isinstance(data, dict):
    print("top keys:", list(data.keys()))
    papers = next((v for v in data.values() if isinstance(v, list)), [])
else:
    papers = data
print(f"모델 논문: {len(papers)} | articles MD: {len(os.listdir(ART))}\n")

def find(title_subs, doi_subs):
    out = []
    for p in papers:
        t = (p.get("title") or "").lower(); d = (p.get("doi") or "").lower()
        if any(s in t for s in title_subs) or (doi_subs and any(s in d for s in doi_subs if d)):
            out.append(p)
    return out

cases = {
 "Torsvik 2014 Deep mantle structure": (["deep mantle structure", "reference frame for movements"], ["pnas.1318135111"]),
 "Cande 2011 Indian/African plate motions": (["indian and african plate motions"], ["nature10174"]),
 "Mn/CH4/He anomalies sea water": (["manganese, methane and helium", "methane and helium anomalies"], []),
}
for name, (ts, ds) in cases.items():
    print(f"=== {name} ===")
    hits = find(ts, ds)
    if not hits:
        print("   ✗ 모델에 논문단위 없음 (제목/DOI 매칭 0)\n"); continue
    for p in hits[:3]:
        smd = p.get("source_md_name") or ""
        smp = p.get("source_md_path") or ""
        in_art = os.path.exists(os.path.join(ART, smd)) if smd else False
        anywhere = os.path.exists(smp) if smp else False
        print(f"   ◆ 모델有: '{(p.get('title') or '')[:60]}'  ({p.get('year')}, {p.get('first_author')})")
        print(f"      paper_id={p.get('paper_id')}  doi={p.get('doi') or '없음'}  chunks={p.get('chunk_count')}")
        print(f"      source_md_name={smd[:55]}")
        print(f"      articles/에 그 MD 있나: {in_art}  | source_md_path 존재: {anywhere}")
    print()
