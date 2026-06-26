"""73 미인덱스 주장 검증: 샘플 제목을 retrieval_papers에서 직접 찾기.
모델에 정말 없나(title 매칭) — 파일명매칭 오탐 아닌지."""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
data = json.load(open(r"G:\corpus_20260624\index\retrieval_papers.json", encoding="utf-8"))
papers = next(v for v in data.values() if isinstance(v, list))
titles = [(p.get("title") or "").lower() for p in papers]
blob = "\n".join(titles)

samples = [
 "Identification of He sources and estimation",      # Wei 2015
 "Evidence for terrigenous",                          # Koh 2007 SF6
 "Hidden magma reservoirs",                           # Huang 2024
 "Baseline geochemical characteristics of groun",    # Koh 2009
 "Boron isotopic composition of subduction-zone",    # Peacock 1999
 "Deep hydrous mantle reservoir provides",           # Sobolev 2019
 "Metasomatized lithospheric mantle as a reserv",    # Lee W 2026
 "Imaging of Lithospheric Structure Beneath Jej",    # Song 2018
]
print(f"모델 논문 {len(papers)}편\n검증:")
miss = 0
for s in samples:
    found = s.lower() in blob
    print(f"  {'있음 ✅' if found else '없음 ✗(미인덱스 확정)'}  {s}")
    if not found: miss += 1
print(f"\n샘플 {len(samples)}개 중 모델에 없음: {miss}")
