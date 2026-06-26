"""연도불일치 14편: MD 본문에서 실제 제목/연도/DOI/저자 추출 → 파일명 말고 본문으로 확정.
같은 논문인지 + 진짜 연도 확인."""
import os, re, json, sys
sys.stdout.reconfigure(encoding="utf-8")
OUT = r"G:\corpus_recovery_20260625"
man = json.load(open(os.path.join(OUT, "RECOVERY_MANIFEST.json"), encoding="utf-8"))
need = [m for m in man if m.get("year_check_needed")]

def head(path, n=2500):
    return open(path, encoding="utf-8", errors="replace").read()[:n]

print(f"=== 연도불일치 {len(need)}편 본문확인 (파일명 무시) ===\n")
for m in need:
    title = m["title"]
    mds = [f for f in os.listdir(os.path.join(OUT, "md")) if f[:-3].startswith(title[:40])]
    if not mds:
        print(f"  ✗ MD 못찾음: {title[:45]}"); continue
    h = head(os.path.join(OUT, "md", mds[0]))
    # 본문 첫 H1(제목)
    h1 = re.search(r"^#\s+(.+)$", h, re.M)
    # DOI
    doi = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", h)
    # 연도 후보 (본문 상단 = 출판정보)
    years = re.findall(r"(?:19|20)\d{2}", h)
    yr_md_name = re.findall(r"\((\d{4})\)", title)
    yr_pdf_name = re.findall(r"(?:19|20)\d{2}", m["pdf"])
    print(f"[{title[:46]}]")
    print(f"   본문제목: {(h1.group(1)[:70] if h1 else '(H1없음)')}")
    print(f"   본문 연도들: {years[:6]}  | DOI: {doi.group(0) if doi else '없음'}")
    print(f"   파일명연도: MD={yr_md_name} PDF={yr_pdf_name}\n")
