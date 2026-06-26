"""반대방향: articles MD 3978 중 모델(retrieval_papers) 안 들어간 76편 정체.
진짜 논문인데 검색 누락? vs 비논문/중복?"""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ART = r"G:\corpus_20260624\articles"
data = json.load(open(r"G:\corpus_20260624\index\retrieval_papers.json", encoding="utf-8"))
papers = next(v for v in data.values() if isinstance(v, list))
model_md = set(p.get("source_md_name","") for p in papers)
# source_md_name에 .md 없을 수 있음 → 정규화
model_norm = set(re.sub(r"\.md$","",m) for m in model_md)

art = [f for f in os.listdir(ART) if f.endswith(".md")]
not_in = [f for f in art if f[:-3] not in model_norm and f not in model_md]
print(f"articles {len(art)} | 모델 source_md {len(model_md)} | 모델 안 들어간 MD: {len(not_in)}\n")

def h1(f):
    try: t = open(os.path.join(ART,f), encoding="utf-8", errors="replace").read(1500)
    except: return ""
    m = re.search(r"^#\s+(.+)$", t, re.M); return (m.group(1) if m else "").strip()
NOISE = re.compile(r"^(article|chapter|index|abstract|references|scientific|technical|manual|reply|task)\b", re.I)
realp = junk = 0
print("=== 모델 누락 MD 상세 ===")
for f in sorted(not_in):
    ti = h1(f); kind = "잡/비논문" if (not ti or NOISE.match(ti) or len(ti)<8) else "진짜논문?"
    if kind=="진짜논문?": realp += 1
    else: junk += 1
    print(f"  [{kind}] {f[:48]}  | H1: {ti[:45]}")
print(f"\n진짜논문? {realp} | 잡/비논문 {junk}")
