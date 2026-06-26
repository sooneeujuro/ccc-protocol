"""no_md 2차검증: DOI 교차(언어무관·고유). 각 no_md 사이드카 DOI가 0624/0612 article 본문에 있나.
title매칭(1차)과 합쳐 최종판정: covered = DOI매칭 OR title고매칭. read-only."""
import os, glob, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
SIDE = r"C:\Users\USER\corpus_md_export_20260612\sidecars"
A24 = r"G:\corpus_20260624\articles"; A12 = r"C:\Users\USER\corpus_md_export_20260612\articles"
DOI = re.compile(r"10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+")
def nd(s): return DOI.search(s or "").group(0).lower().rstrip(".)") if s and DOI.search(s) else None
# corpus DOI 집합 (article 본문 앞 6000자)
corpus = set()
for d in (A24, A12):
    for f in glob.glob(os.path.join(d, "*.md")):
        for m in DOI.findall(open(f, encoding="utf-8", errors="replace").read(6000)):
            corpus.add(m.lower().rstrip(".)"))
print(f"corpus DOI 수집: {len(corpus)}\n")
a24 = set(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(A24, "*.md")))
a12 = set(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(A12, "*.md")))
pids = [os.path.basename(f)[:-5] for f in glob.glob(os.path.join(SIDE, "*.json"))]
nomd = [p for p in pids if p not in a24 and p not in a12 and "Chapter" not in p and "Bioaccum" not in p]
def get_doi(sc):
    b = sc.get("bibliographic") or {}
    for src in (b, sc):
        for k in ("doi", "DOI", "Doi"):
            if src.get(k): return src[k]
    return None
cov = unc = nodoi = 0
covered=[]; uncovered=[]
for p in sorted(nomd):
    try: sc = json.load(open(os.path.join(SIDE, p + ".json"), encoding="utf-8"))
    except: sc = {}
    doi = get_doi(sc); ndoi = nd(doi)
    if ndoi and ndoi in corpus: cov += 1; covered.append(p)
    elif not ndoi: nodoi += 1; uncovered.append((p, "DOI없음"))
    else: unc += 1; uncovered.append((p, f"DOI {ndoi[:30]} 정본에 없음"))
print(f"DOI로 covered(정본에 있음): {cov}")
print(f"DOI매칭 실패(no_md 후보): {unc+nodoi} (DOI없음 {nodoi} / DOI있는데 정본無 {unc})\n")
print("--- DOI로 정본에 확인된 것(중복=no_md 맞음) ---")
for p in covered: print("  OK", p[:50])
print("\n--- DOI 매칭 안 된 것(title도 같이 봐야) ---")
for p, why in uncovered: print(f"  ?  {p[:45]}  [{why}]")
