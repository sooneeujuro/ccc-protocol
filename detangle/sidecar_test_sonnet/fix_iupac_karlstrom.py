import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
import fitz
IN = r"G:\books_v5_in"
# 1) iupac 분할 (timeout → 2등분, 데이터표 dense)
src = os.path.join(IN, "iupac_solubility_vol62_1996.pdf")
if os.path.exists(src):
    d = fitz.open(src); n = d.page_count; mid = n//2
    for tag,a,b in [("pt1",0,mid-1),("pt2",mid,n-1)]:
        nd = fitz.open(); nd.insert_pdf(d, from_page=a, to_page=b)
        nd.save(os.path.join(IN, f"iupac_solubility_vol62_1996_{tag}_p{a+1}_p{b+1}.pdf")); nd.close()
        print(f"  iupac {tag}: {b-a+1}p")
    d.close(); os.remove(src)
    print("iupac 2분할 완료")
else:
    print("iupac 이미 분할됨/없음")

# 2) karlstrom MD: 그림참조 있나 / 완결성
OUT = r"G:\books_v5_out\aebe31dccbb0"
md = [f for f in os.listdir(OUT) if f.endswith(".md")][0]
t = open(os.path.join(OUT,md), encoding="utf-8", errors="replace").read()
fig_mentions = len(re.findall(r'[Ff]ig(?:ure)?', t))
img_refs = len(re.findall(r'!\[[^\]]*\]\(', t))
tail = t[-200:].strip()
print("\nkarlstrom MD:", len(t), "자")
print("  'Fig'/'Figure' 언급:", fig_mentions, "회")
print("  이미지 참조:", img_refs, "개")
print("  본문 끝 200자: ...", tail)