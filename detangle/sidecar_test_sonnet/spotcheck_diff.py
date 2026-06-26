"""오염의심(1664) 몇 편: 0612 MD vs 0624 MD 단어 Jaccard 직접 측정.
exact-hash가 '1단어 차이도 다름'이라 과대했는지 확인. DOI로 0624 짝 찾음."""
import json, os, glob, re, sys
sys.stdout.reconfigure(encoding="utf-8")
SIDE = r"C:\Users\USER\corpus_md_export_20260612\sidecars"
A0612 = r"C:\Users\USER\corpus_md_export_20260612\articles"
A0624 = r"G:\corpus_20260624\articles"
diff = json.load(open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\MD_VERSION_DIFF.json", encoding="utf-8"))["contaminated"]
IMG = re.compile(r"!\[[^\]]*\]\([^)]*\)"); ALNUM = re.compile(r"[a-z]{2,}")
DOIre = re.compile(r"10\.\d{4,9}/[A-Za-z0-9._;()/:+\-]+")
def words(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    return set(ALNUM.findall(IMG.sub(" ", t).lower())), len(IMG.sub(" ", t))

# 0624 DOI 인덱스(head)
c24 = []
for f in glob.glob(os.path.join(A0624, "*.md")):
    h = open(f, encoding="utf-8", errors="replace").read(4000)
    m = DOIre.search(h)
    c24.append((f, m.group(0).lower().rstrip(').,;') if m else None))

n = 0
print(f"{'paper':40} {'0612w':>6} {'0624w':>6} {'Jaccard':>7}  판정")
for pid in diff:
    if n >= 12: break
    sp = os.path.join(SIDE, pid + ".json")
    if not os.path.exists(sp): continue
    doi = (json.load(open(sp, encoding="utf-8")).get("doi") or "").lower().rstrip(').,;')
    if not doi: continue
    match = next((f for f, d in c24 if d and d == doi), None)
    if not match: continue
    n += 1
    w12, l12 = words(os.path.join(A0612, pid + ".md"))
    w24, l24 = words(match)
    jac = len(w12 & w24) / max(1, len(w12 | w24))
    verdict = "사소(reuse가능)" if jac >= 0.9 else ("부분차이" if jac >= 0.6 else "심각(재추출)")
    print(f"{pid[:40]:40} {len(w12):>6} {len(w24):>6} {jac:>7.2f}  {verdict}")
print(f"\n(DOI 매칭된 오염의심 {n}편 샘플)")
