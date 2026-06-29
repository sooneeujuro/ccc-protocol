# -*- coding: utf-8 -*-
"""⑥ pdf_manifest.json: {paper_id: "pdfs/<file>.pdf"}.
pdfs/가 slug(12hex)명 → STEM_TO_SLUG(paper_id→slug)로 역매핑. pid명 pdf도 fallback."""
import os, json, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = sys.argv[1] if len(sys.argv) > 1 else r"G:\corpus_20260626"
s2s = json.load(open(os.path.join(ROOT, "index", "STEM_TO_SLUG.json"), encoding="utf-8"))
pdfdir = os.path.join(ROOT, "pdfs")
pdf_base = set(f[:-4] for f in os.listdir(pdfdir) if f.lower().endswith(".pdf"))

manifest = {}; by_slug = by_pid = 0
for pid, slug in s2s.items():
    if slug in pdf_base:
        manifest[pid] = "pdfs/" + slug + ".pdf"; by_slug += 1
    elif pid in pdf_base:
        manifest[pid] = "pdfs/" + pid + ".pdf"; by_pid += 1
mapped_files = set(os.path.basename(v)[:-4] for v in manifest.values())
unmapped = pdf_base - mapped_files

out = os.path.join(ROOT, "pdf_manifest.json")
json.dump(manifest, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"pdf 파일 {len(pdf_base)} | STEM_TO_SLUG 항목 {len(s2s)}")
print(f"manifest 매핑 {len(manifest)}편 (slug매칭 {by_slug} + pid매칭 {by_pid}) | 매핑안된 pdf {len(unmapped)}")
for k, v in list(manifest.items())[:3]:
    print(f"  {k[:30]} -> {v}")
print("wrote " + out)
