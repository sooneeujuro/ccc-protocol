"""no_md 19편 MD가 정본(corpus_20260624/articles)에 있나 — DOI/제목 content 매칭. 있으면 복구가능."""
import json, os, glob, re, sys
sys.stdout.reconfigure(encoding="utf-8")
SIDE = r"C:\Users\USER\corpus_md_export_20260612\sidecars"
CANON = r"G:\corpus_20260624\articles"
GEMIN = r"C:\Users\USER\corpus_md_export_20260612\articles"
j = json.load(open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\PROD_PROGRESS.json", encoding="utf-8"))
real = [p for p, s in j.get("fails", []) if s == "no_md" and not re.match(r"(Chapter-|Index_)", p)]

# 정본 content 인덱스: head(3500) DOI + H1 title 토큰
DOIre = re.compile(r"10\.\d{4,9}/[A-Za-z0-9._;()/:+\-]+")
def toks(s): return set(re.findall(r"[가-힣a-z0-9]{4,}", s.lower()))
canon = []
for f in glob.glob(os.path.join(CANON, "*.md")):
    try: t = open(f, encoding="utf-8", errors="replace").read(3500)
    except: continue
    m = DOIre.search(t); h1 = re.search(r"^#\s+(.+)$", t, re.M)
    canon.append((os.path.basename(f), (m.group(0).lower().rstrip(').,;') if m else ""), toks(h1.group(1) if h1 else "")))

found = miss = 0
for pid in real:
    sc = json.load(open(os.path.join(SIDE, pid + ".json"), encoding="utf-8"))
    doi = (sc.get("doi") or "").lower().rstrip(').,;')
    title = (sc.get("bibliographic") or {}).get("title") or ""
    tt = toks(title)
    hit = None
    for fn, cdoi, ctok in canon:
        if doi and cdoi and doi == cdoi: hit = (fn, "DOI"); break
        if tt and ctok and len(tt & ctok)/max(1, len(tt | ctok)) >= 0.6: hit = (fn, "title"); break
    if hit: found += 1; print(f"  ✅ {pid[:34]:34} → 정본 {hit[1]}: {hit[0][:42]}")
    else: miss += 1; print(f"  ✗ {pid[:34]:34} (정본에도 없음, doi={doi[:22]})")
print(f"\n정본에 있음(복구가능): {found} / {len(real)}  | 정본에도 없음: {miss}")
