"""faure 927p를 2개(~464p)로 분할 → 각각 별도 slug폴더로 추출되니 충돌 불가.
나머진 다 <=536p(cook 검증)라 통째로 OK."""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
import fitz
IN = r"G:\books_v5_in"
src = os.path.join(IN, "faure_mensing_2005.pdf")
d = fitz.open(src); n = d.page_count; mid = n // 2
for tag, a, b in [("pt1", 0, mid-1), ("pt2", mid, n-1)]:
    nd = fitz.open(); nd.insert_pdf(d, from_page=a, to_page=b)
    dst = os.path.join(IN, f"faure_mensing_2005_{tag}_p{a+1}_p{b+1}.pdf")
    nd.save(dst); nd.close()
    print(f"  {os.path.basename(dst)}  ({b-a+1}p)")
d.close()
os.remove(src)   # 통짜 제거(쪼갠 2개로 대체)
print(f"faure 927p → 2분할 완료, 통짜 제거")
pdfs = [f for f in os.listdir(IN) if f.endswith(".pdf")]
print(f"books_v5_in PDF: {len(pdfs)}개 (15권, faure만 2파일 → 16 PDF)")
print("최대 페이지:", max(fitz.open(os.path.join(IN,f)).page_count for f in pdfs), "(<=536 검증범위)")
