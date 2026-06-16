#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""batch_fill_figures.py — run B-prime extraction over ALL still-missing papers (STAGING ONLY).
Per paper: match PDF -> try embedded (count==missing?) -> else region -> else MANUAL.
Writes per-paper staging (via fig_extract_bprime.py) + a global summary CSV.
Live articles/ NEVER touched. No cost (local fitz). Promote is a separate gated step.
"""
import json, re, os, csv, sys, subprocess
from pathlib import Path
from collections import defaultdict
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BUNDLE = Path(r"G:\corpus_md_export_20260612")
REBUILD = Path(r"G:\fig_rebuild_v20260616")
SCRIPT = r"C:\Users\USER\Documents\ccc-protocol\detangle\scripts\fig_extract_bprime.py"
STILL = json.load(open(BUNDLE / "FIGURES_STILL_MISSING.json", encoding="utf-8"))
PDF_ROOTS = [r"G:\corpus_refs_v20260616\papers", r"G:\RefDB"]
SUMMARY = REBUILD / "BATCH_SUMMARY.csv"

pp = defaultdict(list)
for img, pl in STILL.items():
    for x in pl:
        pp[x].append(img)

# PDF index
pdfs = []
for r in PDF_ROOTS:
    for root, _, fs in os.walk(r):
        for f in fs:
            if f.lower().endswith(".pdf"):
                pdfs.append((f, os.path.join(root, f)))
STOPW = set("etal et al the of and a an in on for from by with to between near new example its their".split())
def toks(s):
    s = re.sub(r"\.(pdf|md)$", "", s, flags=re.I)
    return set(w for w in re.split(r"[^a-z0-9]+", s.lower()) if len(w) > 3 and w not in STOPW)
def fauth(n):
    n = re.sub(r"\.(pdf|md)$", "", n, flags=re.I)
    m = re.match(r"[^A-Za-z]*([A-Za-z]+)", n)
    return m.group(1).lower() if m else ""
def yr(n):
    m = re.search(r"(18|19|20)\d{2}", n)
    return m.group(0) if m else ""
P = [(f, path, fauth(f), yr(f), toks(f)) for f, path in pdfs]

def match_pdf(paper):
    pa, py, pt = fauth(paper), yr(paper), toks(paper)
    cands = sorted([(len(pt & ft), path) for f, path, fa, fy, ft in P if fa == pa and fy == py and pa], reverse=True)
    return cands[0][1] if cands and cands[0][0] >= 4 else None

def run_mode(pid, md, pdf, mode):
    sj = REBUILD / pid / "_summary.json"
    if sj.exists(): sj.unlink()
    try:
        subprocess.run([sys.executable, SCRIPT, "--pid", pid, "--md", md, "--pdf", pdf,
                        "--mode", mode, "--label", paper_label(md)],
                       capture_output=True, timeout=240)
    except Exception:
        return None
    if not sj.exists():
        return None
    s = json.loads(sj.read_text(encoding="utf-8"))
    s["count_ok"] = bool(s.get("paper_ok"))
    s["extracted"] = s.get("matched", 0)
    return s

def paper_label(md):
    return re.sub(r"\.md$", "", md)[:28]

def main():
    REBUILD.mkdir(parents=True, exist_ok=True)
    papers = sorted(pp, key=lambda k: -len(pp[k]))
    out = []
    print(f"papers to process: {len(papers)}", flush=True)
    for i, paper in enumerate(papers, 1):
        pid = pp[paper][0].split("__", 1)[0]
        missing = len(pp[paper])
        pdf = match_pdf(paper)
        if not pdf:
            out.append({"pid": pid, "paper": paper[:-3], "missing": missing, "pdf": "", "mode": "", "extracted": 0, "status": "NO_PDF"})
            print(f"[{i}/{len(papers)}] {pid} NO_PDF  {paper[:40]}", flush=True)
            continue
        # clear prior staging images for this pid (idempotent)
        d = REBUILD / pid
        if d.exists():
            for x in d.glob("*.jpg"):
                x.unlink()
        r = run_mode(pid, paper, pdf, "embedded")
        mode = "embedded"
        if not (r and r["count_ok"]):
            r2 = run_mode(pid, paper, pdf, "region")
            if r2 and r2["count_ok"]:
                r, mode = r2, "region"
            else:
                # keep region staging (more complete) but mark manual; pick the better count
                r, mode = (r2 or r or {"extracted": 0, "missing": missing, "count_ok": False}), "region?"
        status = "auto-ok" if r["count_ok"] else "MANUAL"
        out.append({"pid": pid, "paper": paper[:-3], "missing": missing,
                    "pdf": os.path.basename(pdf), "mode": mode if r["count_ok"] else mode + "(manual)",
                    "extracted": r["extracted"], "status": status})
        print(f"[{i}/{len(papers)}] {pid} {status} {mode} extracted={r['extracted']}/{missing}  {paper[:36]}", flush=True)

    with open(SUMMARY, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["pid", "paper", "missing", "pdf", "mode", "extracted", "status"])
        w.writeheader(); w.writerows(out)
    ok = sum(1 for r in out if r["status"] == "auto-ok")
    man = sum(1 for r in out if r["status"] == "MANUAL")
    nop = sum(1 for r in out if r["status"] == "NO_PDF")
    print(f"\nDONE: auto-ok={ok} MANUAL={man} NO_PDF={nop} / {len(out)} papers")
    print(f"summary: {SUMMARY}  (live articles untouched)")

if __name__ == "__main__":
    main()
