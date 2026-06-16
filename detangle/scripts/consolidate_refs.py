#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consolidate_refs.py — WS2: scattered PDF/supplementary -> one corpus-paired ref library.
COPY ONLY (originals untouched, reversible = delete dest). Codex 022 guards:
- SHA-256 dedup (content identity), keep ALL source paths (provenance) in manifest.
- collision-proof dest name: papers/<sha12>__<cleanname>.pdf
- supplementary -> supplementary/ (xlsx/docx/zip/csv/...); manifest rows for all.
- idempotent: skip copy if dest already exists.
Usage: python consolidate_refs.py [--dry-run]
"""
import os, sys, re, csv, hashlib, shutil, time
from pathlib import Path

DRY = "--dry-run" in sys.argv
SOURCES = [
    r"C:\Users\USER\Desktop\새 폴더 (2)",
    r"C:\Users\USER\Desktop\recent_added_pdfs_20260601",
    r"C:\Users\USER\Desktop\FinalList",
    r"C:\Users\USER\Desktop\10mantledynamics",
    r"G:\RefDB",
    r"D:\Academia",
]
DEST = Path(r"G:\corpus_refs_v20260616")
PAPERS = DEST / "papers"
SUPP = DEST / "supplementary"
MANIFEST = DEST / "MANIFEST.csv"
LOG = DEST / "_consolidate_log.txt"

PDF_EXT = {".pdf"}
SUPP_EXT = {".xlsx", ".xls", ".docx", ".doc", ".zip", ".csv", ".tsv", ".txt", ".rtf", ".pptx"}

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()

def cleanname(n):
    n = re.sub(r"\.(pdf|xlsx?|docx?|zip|csv|tsv|txt|rtf|pptx)$", "", n, flags=re.I)
    n = re.sub(r"[\\/:*?\"<>|]+", "_", n)
    n = re.sub(r"\s+", " ", n).strip()
    return n[:120]

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    if not DRY:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")

def main():
    t0 = time.time()
    if not DRY:
        PAPERS.mkdir(parents=True, exist_ok=True)
        SUPP.mkdir(parents=True, exist_ok=True)
    # scan
    files = []
    for s in SOURCES:
        sp = Path(s)
        if not sp.exists():
            log(f"source MISSING (skip): {s}")
            continue
        n = 0
        for f in sp.rglob("*"):
            if f.is_file():
                ext = f.suffix.lower()
                if ext in PDF_EXT:
                    files.append((f, "pdf")); n += 1
                elif ext in SUPP_EXT:
                    files.append((f, "supp")); n += 1
        log(f"scanned {s}: {n} files")
    log(f"total candidate files: {len(files)} ({time.time()-t0:.0f}s)")

    # hash + dedup
    by_hash = {}
    for i, (f, kind) in enumerate(files):
        try:
            h = sha256(f)
        except OSError as e:
            log(f"  hash FAIL {f}: {e}"); continue
        rec = by_hash.setdefault(h, {"kind": kind, "sources": [], "size": f.stat().st_size, "name": f.name})
        rec["sources"].append(str(f))
        if (i + 1) % 200 == 0:
            log(f"  hashed {i+1}/{len(files)} ({time.time()-t0:.0f}s)")
    uniq = len(by_hash)
    dup = len(files) - uniq
    total_bytes = sum(r["size"] for r in by_hash.values())
    log(f"unique by SHA-256: {uniq}  (dedup removed {dup})  unique size: {total_bytes/1e9:.2f} GB")

    # copy + manifest
    rows = []
    copied = skipped = 0
    for h, r in by_hash.items():
        sha12 = h[:12]
        base = cleanname(r["name"])
        if r["kind"] == "pdf":
            dst = PAPERS / f"{sha12}__{base}.pdf"
            relroot = "papers"
        else:
            ext = Path(r["name"]).suffix.lower()
            dst = SUPP / f"{sha12}__{base}{ext}"
            relroot = "supplementary"
        if not DRY:
            if dst.exists():
                skipped += 1
            else:
                try:
                    shutil.copy2(r["sources"][0], dst)
                    copied += 1
                except OSError as e:
                    log(f"  copy FAIL {dst.name}: {e}"); continue
            if (copied + skipped) % 200 == 0:
                log(f"  copied={copied} skipped={skipped} ({time.time()-t0:.0f}s)")
        rows.append({
            "sha256": h, "kind": r["kind"], "size_bytes": r["size"],
            "dest": f"{relroot}/{dst.name}", "dup_count": len(r["sources"]),
            "sources": " | ".join(r["sources"]),
        })

    if not DRY:
        with open(MANIFEST, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["sha256", "kind", "size_bytes", "dest", "dup_count", "sources"])
            w.writeheader(); w.writerows(rows)
    pdfn = sum(1 for r in rows if r["kind"] == "pdf")
    suppn = sum(1 for r in rows if r["kind"] == "supp")
    log(f"DONE{' (DRY)' if DRY else ''}: unique pdf={pdfn} supp={suppn} | copied={copied} skipped={skipped} | manifest rows={len(rows)} | {time.time()-t0:.0f}s")
    log(f"dest: {DEST}")

if __name__ == "__main__":
    main()
