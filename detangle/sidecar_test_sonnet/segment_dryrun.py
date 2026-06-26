"""책 segmentation dry-run (CODEX 7.6): 17폴더 분절 가능성 맵 + md_quality + low-conf 플래그.
CPU·GPU무관·staging. tier1(heading) 우선, table_dense/fixed_window 폴백. 분절 confidence 필수."""
import os, re, json, sys
sys.stdout.reconfigure(encoding="utf-8")
OUT = r"G:\books_v5_out"
DRY = os.path.join(OUT, "_seg_dryrun"); os.makedirs(DRY, exist_ok=True)
man = {}
for ln in open(os.path.join(OUT,"_manifest.jsonl"), encoding="utf-8"):
    r = json.loads(ln)
    if r.get("slug") and not r.get("err"): man[r["slug"]] = r["pid"]

def analyze(slug, pid):
    bp = os.path.join(OUT, slug)
    mds = [f for f in os.listdir(bp) if f.endswith(".md")]
    if not mds: return None
    t = open(os.path.join(bp, mds[0]), encoding="utf-8", errors="replace").read()
    nlines = max(1, len(t.splitlines()))
    h1 = len(re.findall(r'^#\s+\S', t, re.M)); h2 = len(re.findall(r'^##\s+\S', t, re.M))
    h3 = len(re.findall(r'^#{3}\s+\S', t, re.M)); headings = h1+h2+h3
    pagemarks = len(re.findall(r'\{\d+\}-{5,}', t))
    tablerows = len(re.findall(r'^\s*\|.*\|\s*$', t, re.M))
    eqs = len(re.findall(r'\$', t))
    # md_quality gate
    if tablerows > nlines*0.3: q = "table_weak"
    elif pagemarks > 0 and headings < 3: q = "page_markers_only"
    elif headings < 3: q = "heading_weak"
    else: q = "ok"
    # segmentation tier
    if headings >= 5:
        method, stype, conf, nseg = "heading", "chapter/section", "high", headings
    elif tablerows > nlines*0.3:
        method, stype, conf, nseg = "table_dense", "reference_table_group", "medium", max(1, pagemarks//20)
    else:
        method, stype, conf, nseg = "fixed_window", "page_window", "low", max(1, pagemarks//15)
    return {"slug":slug, "pid":pid, "pages_est":pagemarks, "headings":headings, "h1":h1, "h2":h2,
            "tablerows":tablerows, "eqs":eqs, "md_quality":q,
            "seg_method":method, "seg_type":stype, "seg_confidence":conf, "seg_count_est":nseg}

rows = [a for slug,pid in man.items() if (a:=analyze(slug,pid))]
rows.sort(key=lambda x:-x["pages_est"])
print(f"{'book':32} {'pg':>4} {'head':>4} {'tbl':>5} {'md_quality':>16} {'method':>13} {'conf':>6} {'seg~':>4}")
for r in rows:
    print(f"{r['pid'][:32]:32} {r['pages_est']:>4} {r['headings']:>4} {r['tablerows']:>5} {r['md_quality']:>16} {r['seg_method']:>13} {r['seg_confidence']:>6} {r['seg_count_est']:>4}")
low = [r for r in rows if r["seg_confidence"] != "high" or r["md_quality"] != "ok"]
print(f"\n⚠️ 라운드2 검토대상(저신뢰/품질주의): {len(low)}/{len(rows)}")
for r in low: print(f"   {r['pid'][:34]:34} — md={r['md_quality']}, {r['seg_method']}/{r['seg_confidence']}")
json.dump(rows, open(os.path.join(DRY,"segmentation_report.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n→ {DRY}\\segmentation_report.json")
