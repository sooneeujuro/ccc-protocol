"""77편 전수: 논문 제목이 모델에 표현돼 있나(제목 substring + 파일명토큰 overlap).
둘 다 실패 = 진짜 미인덱스. 정확한 수 + 리스트."""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ART = r"G:\corpus_20260624\articles"
data = json.load(open(r"G:\corpus_20260624\index\retrieval_papers.json", encoding="utf-8"))
papers = next(v for v in data.values() if isinstance(v, list))
mtitles = [(p.get("title") or "") for p in papers]
mblob = "\n".join(mtitles).lower()
# 모델 제목 토큰셋들(파일명 fallback 매칭용)
def tk(s): return set(re.findall(r"[가-힣a-z0-9]{3,}", s.lower()))
mtok = [tk(t) for t in mtitles]
mnorm = set(re.sub(r"\.md$","",p.get("source_md_name","")) for p in papers)

art = [f for f in os.listdir(ART) if f.endswith(".md")]
not_in = [f for f in art if f[:-3] not in mnorm]

def h1(f):
    try: t = open(os.path.join(ART,f), encoding="utf-8", errors="replace").read(1500)
    except: return ""
    m = re.search(r"^#\s+(.+)$", t, re.M)
    h = (m.group(1) if m else "")
    return re.sub(r"<[^>]+>|\[|\]|\$|\\", "", h).strip()
NOISE = re.compile(r"^(article|chapter|index|geochemistry|geochronology|earth scien|open |pdflib|references|abstract|secondary ion)\b", re.I)

unindexed = []; via_other = []; junk = []
for f in sorted(not_in):
    h = h1(f); hl = h.lower()
    # 1) H1 제목이 모델에 있나
    title_hit = len(h) > 12 and not NOISE.match(h) and hl[:35] in mblob
    # 2) 파일명/제목 토큰이 모델 어떤 제목과 강하게 겹치나
    cand = tk(h if (h and not NOISE.match(h)) else f[:-3])
    fname_hit = False
    if len(cand) >= 4:
        for mt in mtok:
            if len(cand & mt)/len(cand) >= 0.7: fname_hit = True; break
    if title_hit or fname_hit: via_other.append(f)
    elif not h or NOISE.match(h) or len(tk(h)) < 3: junk.append((f, h))
    else: unindexed.append((f, h))

print(f"파일명상 모델밖 MD: {len(not_in)}")
print(f"  → 실은 모델에 있음(다른 사본/이름): {len(via_other)}")
print(f"  → H1 노이즈/판정불가: {len(junk)}")
print(f"  → ★진짜 미인덱스 (검색 안 됨): {len(unindexed)}\n")
print("=== 진짜 미인덱스 논문 (reindex하면 검색됨) ===")
for f, h in unindexed:
    print(f"  · {h[:58]}   [{f[:38]}]")
json.dump([{"file":f,"title":h} for f,h in unindexed],
          open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\UNINDEXED.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n→ UNINDEXED.json ({len(unindexed)}편)")
