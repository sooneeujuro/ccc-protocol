#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fig_extract_bprime.py — B-prime per-paper figure extraction (STAGING ONLY).
Never touches live articles/. Extracts a paper's figures from its PDF into an
isolated per-paper folder, builds a rich manifest + staged md diff + contact
sheet for visual sign-off. (Codex 027 guards applied.)

Usage: python fig_extract_bprime.py --pid <pid> --md "<article.md basename>" --pdf "<pdf path>" [--label "<short>"]
Out: G:\\fig_rebuild_v20260616\\<pid>\\ { figNN.jpg, manifest.csv, contact_sheet.png, staged_md.diff.txt, staged.md }
"""
import argparse, os, re, io, csv, hashlib, json, difflib
from pathlib import Path
import fitz
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BUNDLE = Path(r"G:\corpus_md_export_20260612")
ARTS = BUNDLE / "articles"
REBUILD = Path(r"G:\fig_rebuild_v20260616")
STILL = set(json.load(open(BUNDLE / "FIGURES_STILL_MISSING.json", encoding="utf-8")).keys())
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
CAP_LINE_RE = re.compile(r"(?im)\bfig(?:ure)?\.?\s*(\d+)\b[^\n]{0,140}")
CAP_PAGE_RE = re.compile(r"(?im)\bfig(?:ure)?\.?\s*\d+\b")
MINW, MINH, MINBYTES = 120, 120, 3000

def sha(b): return hashlib.sha256(b).hexdigest()
def toks(s): return set(w for w in re.split(r"[^a-z0-9]+", s.lower()) if len(w) > 3)
def jacc(a, b):
    A, B = toks(a), toks(b)
    return round(len(A & B) / len(A | B), 3) if (A | B) else 0.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pid", required=True); ap.add_argument("--md", required=True)
    ap.add_argument("--pdf", required=True); ap.add_argument("--label", default="")
    ap.add_argument("--mode", choices=["embedded", "region"], default="embedded",
                    help="embedded=extract image XObjects (simple papers); region=render page area above each Figure caption (multi-panel papers)")
    A = ap.parse_args()
    outdir = REBUILD / A.pid; outdir.mkdir(parents=True, exist_ok=True)

    # 1) article md: ordered missing refs (this pid) + alt + line number
    md_path = ARTS / A.md
    raw = md_path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()
    present = {f.name for f in ARTS.iterdir() if f.suffix.lower() in (".jpg", ".jpeg", ".png")}
    def lineno(pos): return raw.count("\n", 0, pos) + 1
    missing_refs = []  # (alt, name, line)
    for m in IMG_RE.finditer(raw):
        alt, tgt = m.group(1), m.group(2).strip().split()[0]
        name = tgt.replace("\\", "/").rsplit("/", 1)[-1]
        if name.lower().endswith((".jpg", ".jpeg", ".png")) and name not in present and name.startswith(A.pid):
            missing_refs.append((alt, name, lineno(m.start())))
    print(f"missing refs (this pid) = {len(missing_refs)}", flush=True)

    # 2) extract embedded images, isolated to this paper's folder
    pdf_bytes = Path(A.pdf).read_bytes(); pdf_sha = sha(pdf_bytes)
    doc = fitz.open(A.pdf)
    seen, raw_cands, page_text = set(), [], {}
    for pno in range(len(doc)):
        page = doc[pno]; page_text[pno + 1] = page.get_text()
        idx_on_page = 0
        for img in page.get_images(full=True):
            xref = img[0]
            if xref in seen: continue
            seen.add(xref); idx_on_page += 1
            try: ext = doc.extract_image(xref)
            except Exception: continue
            b = ext["image"]; w = ext.get("width", 0); h = ext.get("height", 0)
            small = (w < MINW or h < MINH or len(b) < MINBYTES)
            raw_cands.append({"page": pno + 1, "xref": xref, "idx": idx_on_page,
                              "bytes": b, "w": w, "h": h, "small": small})
    raw_n = len([c for c in raw_cands if not c["small"]])
    if A.mode == "region":
        # caption-anchored page-region render: one image per "Figure N" caption
        kept = []
        for pno in range(len(doc)):
            page = doc[pno]; d = page.get_text("dict")
            pw, ph = page.rect.width, page.rect.height
            caps = []
            for blk in d.get("blocks", []):
                if blk.get("type") != 0: continue
                txt = " ".join(sp["text"] for ln in blk.get("lines", []) for sp in ln.get("spans", []))
                m = re.match(r"\s*fig(?:ure)?\.?\s*(\d+)", txt, re.I)
                if m: caps.append((float(blk["bbox"][1]), float(blk["bbox"][3]), int(m.group(1)), txt[:160]))
            caps.sort()
            prev_bottom = 0.0
            for i, (ytop, ybot, fno, txt) in enumerate(caps):
                top, bottom = prev_bottom, ytop
                prev_bottom = ybot
                if bottom - top < 60:  # too thin: figure likely on prev page / caption-only
                    continue
                clip = fitz.Rect(0, max(0, top - 4), pw, bottom + 2)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip)
                kept.append({"page": pno + 1, "xref": -1, "idx": i + 1, "bytes": pix.tobytes("jpg"),
                             "w": pix.width, "h": pix.height, "small": False, "cap_no": fno, "cap_text": txt})
        raw_n = len(kept)
    else:
        # caption-page prefilter (embedded)
        fig_pages = {p for p, t in page_text.items() if CAP_PAGE_RE.search(t)}
        kept = [c for c in raw_cands if not c["small"] and (c["page"] in fig_pages or not fig_pages)]
        if not kept:
            kept = [c for c in raw_cands if not c["small"]]
    kept.sort(key=lambda c: (c["page"], c["idx"]))
    print(f"PDF pages={len(doc)} raw(filtered-size)={raw_n} caption-page-kept={len(kept)} missing={len(missing_refs)}", flush=True)

    # 3) per-page captions: page -> [(fig_no, text)]
    caps_by_page = {}
    for p, t in page_text.items():
        cl = []
        for cm in CAP_LINE_RE.finditer(t):
            cl.append((int(cm.group(1)), cm.group(0).strip()[:160]))
        if cl: caps_by_page[p] = cl

    # 4) save staging (hash the SAVED file), build manifest rows
    count_ok = (len(kept) == len(missing_refs))
    rows = []
    for i, c in enumerate(kept):
        img = Image.open(io.BytesIO(c["bytes"])).convert("RGB")
        src_sha = sha(c["bytes"])
        tmp = io.BytesIO(); img.save(tmp, "JPEG", quality=92); out_bytes = tmp.getvalue()
        out_sha = sha(out_bytes)
        fig_no = i + 1
        newname = f"{A.pid}__refill20260616_fig{fig_no:02d}__{out_sha[:12]}.jpg"
        (outdir / newname).write_bytes(out_bytes)
        old_alt, old_ref, old_line = (missing_refs[i] if i < len(missing_refs) else ("", "", ""))
        if "cap_text" in c:  # region mode: caption is the anchor for this render
            pdf_cap_text = c["cap_text"]; pdf_cap_no = c["cap_no"]
        else:
            pcaps = caps_by_page.get(c["page"], [])
            pdf_cap_text = pcaps[0][1] if pcaps else ""
            pdf_cap_no = pcaps[0][0] if pcaps else ""
        cj = jacc(old_alt, pdf_cap_text) if (old_alt and pdf_cap_text) else 0.0
        fig_no_agree = (pdf_cap_no == fig_no) if pdf_cap_no != "" else ""
        multi = len([x for x in kept if x["page"] == c["page"]]) > 1
        conf = "high" if (count_ok and cj >= 0.1) else ("medium" if count_ok else "low")
        status = "auto-ok" if (count_ok and conf != "low") else "MANUAL"
        rows.append({
            "fig_no": fig_no, "page": c["page"], "xref": c["xref"], "idx_on_page": c["idx"],
            "raw_candidate_count": raw_n, "filtered_candidate_count": len(kept),
            "missing_ref_count": len(missing_refs), "count_match": count_ok,
            "multi_img_on_caption_page": multi, "filter": "caption_page",
            "src_pdf_sha256": pdf_sha, "source_image_sha256": src_sha, "output_file_sha256": out_sha,
            "w": c["w"], "h": c["h"], "article_md": A.md, "article_line": old_line,
            "old_ref": old_ref, "old_alt": old_alt[:200],
            "pdf_caption_fig_no": pdf_cap_no, "pdf_caption_text": pdf_cap_text,
            "caption_jaccard": cj, "fig_no_agree": fig_no_agree, "new_name": newname,
            "confidence": conf, "status": status,
        })
    if rows:
        with open(outdir / "manifest.csv", "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

    # 5) staged md diff (live md untouched) — replace only matched image refs in order
    patched = lines[:]
    if count_ok:
        for r in rows:
            ln = r["article_line"]
            if isinstance(ln, int) and 1 <= ln <= len(patched):
                patched[ln - 1] = patched[ln - 1].replace(r["old_ref"], r["new_name"])
    diff = "\n".join(difflib.unified_diff(lines, patched, fromfile="live/" + A.md, tofile="staged/" + A.md, lineterm=""))
    (outdir / "staged_md.diff.txt").write_text(diff or "(no diff — count mismatch, manual)\n", encoding="utf-8")
    if count_ok:
        (outdir / "staged.md").write_text("\n".join(patched), encoding="utf-8")

    # 6) contact sheet
    if rows:
        k = len(rows); cols = min(3, k); rn = (k + cols - 1) // cols
        fig, axes = plt.subplots(rn, cols, figsize=(cols * 4.2, rn * 4.7))
        axes = (axes.ravel() if hasattr(axes, "ravel") else [axes])
        for j, r in enumerate(rows):
            ax = axes[j]; ax.imshow(Image.open(outdir / r["new_name"])); ax.axis("off")
            cap = (r["old_alt"][:80] + "…") if len(r["old_alt"]) > 80 else r["old_alt"]
            ax.set_title(f"fig{r['fig_no']:02d} p.{r['page']} {r['w']}x{r['h']} J={r['caption_jaccard']}\n[md] {cap or '(no alt)'}", fontsize=7)
        for j in range(k, len(axes)): axes[j].axis("off")
        lab = A.label or A.pid
        fig.suptitle(f"{lab}  extracted={len(kept)} vs missing={len(missing_refs)}  count={'OK' if count_ok else 'MISMATCH→MANUAL'}", fontsize=10)
        fig.tight_layout(rect=[0, 0, 1, 0.96]); fig.savefig(outdir / "contact_sheet.png", dpi=110); plt.close(fig)
    print(f"DONE: extracted={len(kept)} missing={len(missing_refs)} count={'OK' if count_ok else 'MANUAL'} -> {outdir} (live untouched)")

if __name__ == "__main__":
    main()
