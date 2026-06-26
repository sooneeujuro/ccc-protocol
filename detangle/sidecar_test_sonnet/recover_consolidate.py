"""오격리 34편 복구셋을 한 곳에 모으기: MD(quarantine)+PDF 짝 복사 + 매니페스트.
연도불일치(내용확인 필요) 플래그. COPY(원본 보존)."""
import os, re, json, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
Q = r"G:\corpus_md_export_20260602\_renewal_20260609\_new_dup_quarantine"
OUT = r"G:\corpus_recovery_20260625"
rs = json.load(open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\RECOVERY_SET.json", encoding="utf-8"))
os.makedirs(os.path.join(OUT, "md"), exist_ok=True)
os.makedirs(os.path.join(OUT, "pdf"), exist_ok=True)

def yr(s):
    m = re.findall(r"(19|20)\d{2}", s)
    return m[0:1] and re.findall(r"((?:19|20)\d{2})", s)[0] or ""

manifest = []
copied_md = copied_pdf = 0
for item in rs["paired"]:
    title = item["title"]; pdf = item["pdf"]
    # MD: quarantine에서 title로 시작하는 파일 찾기
    mds = [f for f in os.listdir(Q) if f.endswith(".md") and f[:-3].startswith(title[:40])]
    md_src = os.path.join(Q, mds[0]) if mds else None
    if md_src and os.path.exists(md_src):
        shutil.copy2(md_src, os.path.join(OUT, "md", os.path.basename(md_src))); copied_md += 1
    if os.path.exists(pdf):
        shutil.copy2(pdf, os.path.join(OUT, "pdf", os.path.basename(pdf))); copied_pdf += 1
    my = re.findall(r"\((\d{4})\)", title)
    py = re.findall(r"(19|20)\d{2}", os.path.basename(pdf))
    yr_mismatch = bool(my and py and my[0] not in os.path.basename(pdf))
    manifest.append({"title": title, "md": bool(md_src), "pdf": os.path.basename(pdf),
                     "year_check_needed": yr_mismatch})

json.dump(manifest, open(os.path.join(OUT, "RECOVERY_MANIFEST.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
mism = [m for m in manifest if m["year_check_needed"]]
print(f"복구셋 → {OUT}")
print(f"  MD 복사: {copied_md} | PDF 복사: {copied_pdf} | 매니페스트: {len(manifest)}편")
print(f"  연도 불일치(내용확인 필요): {len(mism)}편")
for m in mism:
    print(f"    ⚠️ {m['title'][:50]} ↔ {m['pdf'][:45]}")
print(f"\n실제 폴더: md/ {len(os.listdir(os.path.join(OUT,'md')))}개, pdf/ {len(os.listdir(os.path.join(OUT,'pdf')))}개")
