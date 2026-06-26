"""parallel-2 viability: ctx49152에서 88000자 입력 2개 동시호출 OOM/stall 안 나나."""
import json, os, glob, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding="utf-8")
A24 = r"G:\corpus_20260624\articles"
SCHEMA = {"type":"object","properties":{
  "classification_type":{"type":"string","enum":["gas","petrology","both","other"]},
  "made_new_measurements":{"type":"boolean"},
  "variables_reported":{"type":"array","items":{"type":"object","properties":{"raw_label":{"type":"string"}},"required":["raw_label"]}}},
  "required":["classification_type","made_new_measurements","variables_reported"]}
# 서로 다른 긴 논문 2편의 앞 88000자
longs=[f for f in glob.glob(os.path.join(A24,"*.md")) if len(open(f,encoding="utf-8",errors="replace").read())>120000][:2]
def call(idx):
    md=open(longs[idx],encoding="utf-8",errors="replace").read()[:88000]
    t=time.time()
    body=json.dumps({"model":"gemma4:12b","messages":[{"role":"user","content":"DATA INVENTORY JSON only.\n"+md}],
      "stream":False,"think":False,"format":SCHEMA,"options":{"temperature":0,"num_ctx":49152,"num_predict":16384}}).encode()
    with urllib.request.urlopen(urllib.request.Request("http://localhost:11434/api/chat",data=body,headers={"Content-Type":"application/json"}),timeout=900) as r:
        c=json.loads(r.read())["message"]["content"]
    n=len(json.loads(c).get("variables_reported",[])) if c.strip() else -1
    return idx, len(c), n, round(time.time()-t,1)
t0=time.time()
with ThreadPoolExecutor(max_workers=2) as ex:
    res=list(ex.map(call,[0,1]))
wall=round(time.time()-t0,1)
for idx,clen,nv,dt in res:
    print(f"  worker{idx}: resp {clen}자, {nv}변수, {dt}s  ({'OK' if clen>0 and nv>=0 else 'EMPTY/FAIL'})")
print(f"동시 2개 wall: {wall}s (직렬이면 ~합계). 둘 다 OK면 parallel-2 가능.")
