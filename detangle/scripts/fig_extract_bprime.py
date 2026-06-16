#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fig_extract_bprime.py — B-prime per-paper figure extraction (STAGING ONLY).
Never touches live articles/. Extracts a paper's figures from its PDF into an
isolated per-paper folder, builds a manifest + contact sheet for visual sign-off.

Usage: python fig_extract_bprime.py --pid <pid> --md "<article.md basename>" --pdf "<pdf path>"
Output: G:\\fig_rebuild_v20260616\\<pid>\\ { figNN.jpg, manifest.csv, contact_sheet.png, staged_md.diff.txt }
"""
import argparse, os, re, io, csv, hashlib, json
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BUNDLE = Path(r"G:\corpus_md_export_20260612")
ARTS = BUNDLE / "articles"
REBUILD = Path(r"G:\fig_rebuild_v20260616")
STILL = json.load(open(BUNDLE / "FIGURES_STILL_MISSING.json", encoding="utf-8"))
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
MINW, MINH, MINBYTES = 120, 120, 3000  # filter logos/rules/icons

def sha(b): return hashlib.sha256(b).hexdigest()
def toks(s): return set(w for w in re.split(r"[^a-z0-9]+", s.lower()) if len(w) > 3)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pid", required=True)
    ap.add_argument("--md", required=True)
    ap.add_argument("--pdf", required=True)
    A = ap.parse_args()
    outdir = REBUILD / A.pid
    outdir.mkdir(parents=True, exist_ok=True)

    # 1) article md: ordered image refs + alt; mark which are missing
    md_path = ARTS / A.md
    text = md_path.read_text(encoding="utf-8", errors="replace")
    present = {f.name for f in ARTS.iterdir() if f.suffix.lower() in (".jpg", ".jpeg", ".png")}
    missing_for_pid = set(STILL.keys())
    refs = []  # (alt, name, is_missing)
    for m in IMG_RE.finditer(text):
        alt, tgt = m.group(1), m.group(2).strip().split()[0]
        name = tgt.replace("\\", "/").rsplit("/", 1)[-1]
        if name.lower().endswith((".jpg", ".jpeg", ".png")):
            refs.append((alt, name, name not in present))
    missing_refs = [(alt, name) for alt, name, miss in refs if miss and name.startswith(A.pid)]
    print(f"md refs={len(refs)}  missing(this pid)={len(missing_refs)}", flush=True)

    # 2) extract embedded images from PDF (isolated to this paper's folder)
    pdf_bytes = Path(A.pdf).read_bytes()
    pdf_sha = sha(pdf_bytes)
    doc = fitz.open(A.pdf)
    seen_xref = set()
    cands = []  # dict per kept image
    page_text = {}
    for pno in range(len(doc)):
        page = doc[pno]
        page_text[pno] = page.get_text()
        for img in page.get_images(full=True):
            xref = img[0]
            if xref in seen_xref:
                continue
            seen_xref.add(xref)
            try:
                ext = doc.extract_image(xref)
            except Exception:
                continue
            b = ext["image"]; w = ext.get("width", 0); h = ext.get("height", 0)
            if w < MINW or h < MINH or len(b) < MINBYTES:
                continue
            cands.append({"page": pno + 1, "xref": xref, "bytes": b, "ext": ext.get("ext", "jpg"), "w": w, "h": h})
    # caption-anchored filter: keep only images on pages bearing a "Figure N" caption
    # (drops publisher logo / journal cover-banner pages, references, etc.)
    CAP_RE = re.compile(r"(?im)\bfig(?:ure)?\.?\s*\d+\b")
    fig_pages = {pno + 1 for pno, t in page_text.items() if CAP_RE.search(t)}
    raw_n = len(cands)
    if fig_pages:
        filtered = [c for c in cands if c["page"] in fig_pages]
        # safety: don't drop everything; if filter nukes all, fall back to raw
        if filtered:
            cands = filtered
    # reading order: by page then xref
    cands.sort(key=lambda c: (c["page"], c["xref"]))
    print(f"PDF pages={len(doc)}  raw-candidates={raw_n}  caption-page-filtered={len(cands)}", flush=True)

    # 3) PDF caption lines (Figure N ...) for cross-check
    pdf_caps = []
    for pno, t in page_text.items():
        for cm in re.finditer(r"(?im)^\s*(fig(?:ure)?\.?\s*\d+[^\n]{0,120})", t):
            pdf_caps.append(cm.group(1).strip())

    # 4) map missing refs (order) <-> candidates (order); save staging + manifest
    rows = []
    n = min(len(missing_refs), len(cands))
    for i in range(len(cands)):
        c = cands[i]
        img = Image.open(io.BytesIO(c["bytes"])).convert("RGB")
        ish = sha(c["bytes"])[:12]
        fig_no = i + 1
        newname = f"{A.pid}__refill20260616_fig{fig_no:02d}__{ish}.jpg"
        img.save(outdir / newname, "JPEG", quality=92)
        old_alt, old_ref = (missing_refs[i] if i < len(missing_refs) else ("", ""))
        # caption overlap confidence
        cap_ov = 0
        if old_alt:
            at = toks(old_alt)
            cap_ov = max((len(at & toks(pc)) for pc in pdf_caps), default=0)
        rows.append({
            "fig_no": fig_no, "page": c["page"], "src_pdf_sha256": pdf_sha,
            "img_sha256": sha(c["bytes"]), "w": c["w"], "h": c["h"],
            "new_name": newname, "old_ref": old_ref, "old_alt": old_alt[:160],
            "caption_overlap": cap_ov,
        })
    with open(outdir / "manifest.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else
                           ["fig_no","page","src_pdf_sha256","img_sha256","w","h","new_name","old_ref","old_alt","caption_overlap"])
        w.writeheader(); w.writerows(rows)

    # 5) 3-way check summary
    count_ok = (len(cands) == len(missing_refs))
    print(f"CHECK count: extracted={len(cands)} vs missing_refs={len(missing_refs)} -> {'OK' if count_ok else 'MISMATCH(manual)'}")

    # 6) contact sheet PNG (image + mapped old caption)
    k = len(rows)
    if k:
        cols = min(3, k); rows_n = (k + cols - 1) // cols
        fig, axes = plt.subplots(rows_n, cols, figsize=(cols * 4.2, rows_n * 4.6))
        axes = (axes.ravel() if hasattr(axes, "ravel") else [axes])
        for j, r in enumerate(rows):
            ax = axes[j]
            ax.imshow(Image.open(outdir / r["new_name"]))
            ax.axis("off")
            cap = (r["old_alt"][:90] + "…") if len(r["old_alt"]) > 90 else r["old_alt"]
            ax.set_title(f"fig{r['fig_no']:02d}  p.{r['page']}  {r['w']}x{r['h']}\n[md cap] {cap or '(no alt)'}",
                         fontsize=7)
        for j in range(k, len(axes)):
            axes[j].axis("off")
        title = f"{A.pid}  Lee&Walker2006  extracted={len(cands)} vs missing={len(missing_refs)}  count={'OK' if count_ok else 'MISMATCH'}"
        fig.suptitle(title, fontsize=10)
        fig.tight_layout(rect=[0, 0, 1, 0.97])
        fig.savefig(outdir / "contact_sheet.png", dpi=110)
        plt.close(fig)
        print(f"contact sheet: {outdir / 'contact_sheet.png'}")
    print(f"DONE staging: {outdir}  (live articles untouched)")

if __name__ == "__main__":
    main()
