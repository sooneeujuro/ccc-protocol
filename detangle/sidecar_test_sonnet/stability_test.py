"""격리: 같은 0624 MD를 2번 추출 → run1 vs run2 변수 overlap.
낮으면 Gemma 불안정(추출 비결정), 높으면 0612-vs-0624 차이가 진짜. raw_label + id 둘 다 + 라벨 출력."""
import json, os, glob, re, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
A0624 = r"G:\corpus_20260624\articles"
SCHEMA = {"type":"object","properties":{
  "classification_type":{"type":"string","enum":["gas","petrology","both","other"]},
  "made_new_measurements":{"type":"boolean"},
  "variables_reported":{"type":"array","items":{"type":"object","properties":{
    "raw_label":{"type":"string"},"id":{"type":"string"}},"required":["raw_label"]}}},
  "required":["classification_type","made_new_measurements","variables_reported"]}
INSTR=("You build a DATA INVENTORY for a geochemistry paper. Output ONLY JSON per schema. "
  "List EACH quantity SEPARATELY. Only quantities actually present. "
  "id canonical (3He/4He->He3_He4_RRa) else raw_label_only. raw_label PLAIN TEXT.\n\nPAPER TEXT:\n")
def norm(s): return re.sub(r"[^a-z0-9]","",(s or "").lower())
def gemma(md):
    body=json.dumps({"model":"gemma4:12b","messages":[{"role":"user","content":INSTR+md[:95000]}],
      "stream":False,"think":False,"format":SCHEMA,"options":{"temperature":0,"num_ctx":49152,"num_predict":16384}}).encode()
    with urllib.request.urlopen(urllib.request.Request("http://localhost:11434/api/chat",data=body,headers={"Content-Type":"application/json"}),timeout=900) as r:
        return json.loads(json.loads(r.read())["message"]["content"])
# Abiado 논문(아까 46 vs 33)
f = next(g for g in glob.glob(os.path.join(A0624,"*.md")) if "Abiado" in g)
print("MD:", os.path.basename(f)[:50])
o1=gemma(open(f,encoding="utf-8",errors="replace").read())
o2=gemma(open(f,encoding="utf-8",errors="replace").read())
v1=[x.get("raw_label") for x in o1.get("variables_reported",[])]
v2=[x.get("raw_label") for x in o2.get("variables_reported",[])]
n1=set(norm(x) for x in v1); n2=set(norm(x) for x in v2)
i1=set(norm(x.get("id")) for x in o1.get("variables_reported",[]))
i2=set(norm(x.get("id")) for x in o2.get("variables_reported",[]))
print(f"run1 {len(v1)}개 / run2 {len(v2)}개")
print(f"raw_label overlap(Jaccard): {len(n1&n2)/max(1,len(n1|n2)):.2f}")
print(f"id overlap(Jaccard): {len(i1&i2)/max(1,len(i1|i2)):.2f}")
print(f"\nrun1 라벨: {v1[:18]}")
print(f"\nrun2 라벨: {v2[:18]}")
