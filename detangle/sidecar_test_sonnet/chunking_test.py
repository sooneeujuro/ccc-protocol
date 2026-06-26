"""청킹 검증: 롱페이퍼 1편을 단일컷(95000) vs 청킹(전문) 추출 비교 → 꼬리 변수 잡히나."""
import json, os, glob, re, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
A0624 = r"G:\corpus_20260624\articles"
CHUNK = 88000   # char/청크 (ctx49152 여유: ~22k tok + predict 16k < 49k)
SCHEMA = {"type":"object","properties":{
  "classification_type":{"type":"string","enum":["gas","petrology","both","other"]},
  "made_new_measurements":{"type":"boolean"},
  "variables_reported":{"type":"array","items":{"type":"object","properties":{
    "raw_label":{"type":"string"},"id":{"type":"string"}},"required":["raw_label"]}}},
  "required":["classification_type","made_new_measurements","variables_reported"]}
INSTR=("You build a DATA INVENTORY for a geochemistry paper. Output ONLY JSON per schema. "
  "List EACH quantity SEPARATELY. Only quantities actually present. id canonical else raw_label_only. raw_label PLAIN TEXT.\n\nPAPER TEXT:\n")
def norm(s): return re.sub(r"[^a-z0-9]","",(s or "").lower())
def call_parse(prompt):
    body=json.dumps({"model":"gemma4:12b","messages":[{"role":"user","content":prompt}],
      "stream":False,"think":False,"format":SCHEMA,"options":{"temperature":0,"num_ctx":49152,"num_predict":16384}}).encode()
    with urllib.request.urlopen(urllib.request.Request("http://localhost:11434/api/chat",data=body,headers={"Content-Type":"application/json"}),timeout=900) as r:
        c=json.loads(r.read())["message"]["content"]
    try: return json.loads(c)
    except:
        try: return json.JSONDecoder().raw_decode(c.strip())[0]
        except: return None
def chunk_md(md):
    if len(md)<=CHUNK: return [md]
    out=[]; i=0
    while i<len(md):
        end=min(i+CHUNK,len(md))
        if end<len(md):
            nl=md.rfind("\n",i+CHUNK//2,end)
            if nl>i: end=nl
        out.append(md[i:end]); i=end
    return out
def extract_chunked(md):
    vars={}; cls=made=None
    for ch in chunk_md(md):
        o=call_parse(INSTR+ch)
        if not o: continue
        if cls is None: cls=o.get("classification_type"); made=o.get("made_new_measurements")
        for v in o.get("variables_reported",[]):
            k=(v.get("id") or "")+"|"+norm(v.get("raw_label"))
            vars.setdefault(k,v)
    return cls,made,list(vars.values())

# 150~300KB char 롱페이퍼 하나
cand=[f for f in glob.glob(os.path.join(A0624,"*.md")) if 150000<len(open(f,encoding="utf-8",errors="replace").read())<300000]
f=cand[0]; md=open(f,encoding="utf-8",errors="replace").read()
print(f"테스트: {os.path.basename(f)[:45]} ({len(md)}자, {len(chunk_md(md))}청크)")
print(f"95000컷이면 뒤 {len(md)-95000}자 버려짐\n")
# 단일컷
o1=call_parse(INSTR+md[:95000]); v1=set(norm(x.get("raw_label")) for x in (o1.get("variables_reported") or [])) if o1 else set()
# 청킹
cls,made,vc=extract_chunked(md); v2=set(norm(x.get("raw_label")) for x in vc)
print(f"단일컷(95000): {len(v1)}개 변수")
print(f"청킹(전문):    {len(v2)}개 변수")
print(f"청킹이 추가로 잡은(단일컷 누락) 변수: {len(v2-v1)}개")
extra=[x.get('raw_label') for x in vc if norm(x.get('raw_label')) in (v2-v1)]
print(f"  추가 샘플: {extra[:12]}")
