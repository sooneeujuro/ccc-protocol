"""배선된 gemma_production을 1편(잘린 논문) end-to-end: 0624읽기→청킹→Haiku머지→staging쓰기."""
import os, glob, json, sys
sys.stdout.reconfigure(encoding="utf-8")
import gemma_production as gp
pids = set(f[:-5] for f in os.listdir(gp.SIDE) if f.endswith(".json"))
pick = None
for f in glob.glob(os.path.join(gp.ARTS, "*.md")):
    pid = os.path.basename(f)[:-3]
    if pid in pids and len(open(f, encoding="utf-8", errors="replace").read()) > 95000:
        pick = pid; break
md = open(os.path.join(gp.ARTS, pick + ".md"), encoding="utf-8", errors="replace").read()
base = json.load(open(os.path.join(gp.SIDE, pick + ".json"), encoding="utf-8"))
print(f"테스트 pid: {pick[:50]}")
print(f"  0624 MD {len(md)}자, {len(gp.chunk_md(md))}청크 (단일컷이면 뒤 {len(md)-95000}자 버려짐)")
print(f"  Haiku base 필드수: {len(base)}개")
r = gp.process(pick)
print(f"  process 결과: {r}")
out = json.load(open(os.path.join(gp.STAGE, pick + ".json"), encoding="utf-8"))
print(f"  → variables_reported: {len(out.get('variables_reported', []))}개")
print(f"  → classification.type={out.get('classification',{}).get('type')}, made_new={out.get('made_new_measurements')}")
for k in ["bibliographic", "abstract", "references", "figure_summaries", "geography", "analytical"]:
    if k in base: print(f"  verbatim 보존 [{k}]: {'O 유지' if k in out else 'X 유실!'}")
