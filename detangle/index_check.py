import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

idx = Path(r"C:\Users\USER\Documents\manuscript-atelier\tools\paper-orchestra\corpus\index")
rp = idx / "retrieval_papers.json"
gaps = json.load(open(r"C:\Users\USER\Documents\ccc-protocol\detangle\REAL_GAPS.json", encoding="utf-8"))

def norm(s):
    return re.sub(r"[^a-z0-9가-힣]", "", str(s).lower())

data = json.load(open(rp, encoding="utf-8"))
# 구조 파악
if isinstance(data, dict):
    items = list(data.values()) if not isinstance(next(iter(data.values()), None), str) else [data]
    keys_sample = list(data.keys())[:3]
    print("retrieval_papers.json = dict, 키 샘플:", keys_sample)
    recs = data
else:
    recs = data
    print("retrieval_papers.json = list, len", len(data))

# 인덱스에 등재된 paper 식별자 집합 (id/title/md 등 가능한 필드 norm)
idx_norms = set()
def harvest(r):
    if isinstance(r, dict):
        for k in ("paper_id", "id", "title", "md_file", "text_path", "stem", "name", "source"):
            v = r.get(k)
            if v:
                idx_norms.add(norm(str(v).rsplit("/", 1)[-1].rsplit("\\", 1)[-1]))
    elif isinstance(r, str):
        idx_norms.add(norm(r))

if isinstance(recs, dict):
    for k, v in recs.items():
        idx_norms.add(norm(k))
        harvest(v)
else:
    for v in recs:
        harvest(v)

print("index 논문수(고유 norm):", len(idx_norms))

def in_index(g):
    ng = norm(g)
    if ng in idx_norms:
        return True
    p = ng[:28]
    return any(k.startswith(p) or ng.startswith(k[:28]) for k in idx_norms if len(k) >= 20)

inn = [g for g in gaps if in_index(g)]
out = [g for g in gaps if not in_index(g)]
print(f"\n64 갭 중 → index에 있음: {len(inn)} | index에 없음: {len(out)}")
print("--- index에 없는 것 (= 코퍼스 모델서 빠져있던 것) 샘플 ---")
for g in out[:20]:
    print("  ", g[:55])
