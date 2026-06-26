# -*- coding: utf-8 -*-
"""DOI 없는 sidecar(822) 추출 → scout 입력. pid+title+year+authors. sha256로 CODEX 822와 대조."""
import os, json, hashlib, re, sys
sys.stdout.reconfigure(encoding="utf-8")
SIDE = r"G:\corpus_20260626\sidecars"
OUT = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\MISSING_822.json"
def clean(s): return re.sub(r'\s+', ' ', str(s or "")).strip()

miss = []; t_bib = 0; t_fn = 0
for f in sorted(os.listdir(SIDE)):
    if not f.endswith(".json"): continue
    pid = f[:-5]
    try: j = json.load(open(os.path.join(SIDE, f), encoding="utf-8"))
    except Exception: continue
    d = j.get("doi")
    if d and str(d).strip() and str(d).lower() != "null": continue
    bib = j.get("bibliographic") if isinstance(j.get("bibliographic"), dict) else {}
    title = clean(bib.get("title"))
    if title: t_bib += 1
    else: title = clean(pid.replace("_", " ")); t_fn += 1
    year = bib.get("year_print") or bib.get("year") or bib.get("year_online")
    authors = [a for a in (bib.get("authors_full") or []) if isinstance(a, str)][:3]
    miss.append({"pid": pid, "title": title[:200], "year": year, "authors": authors})

pids = sorted(m["pid"] for m in miss)
h = hashlib.sha256("\n".join(pids).encode("utf-8")).hexdigest()[:16]
print(f"missing {len(miss)} | title: bib {t_bib} / 파일명fallback {t_fn}")
print(f"sha256_prefix(정렬+\\n): {h}  vs CODEX f3d557628d6cf167")
json.dump(miss, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("저장:", OUT)
