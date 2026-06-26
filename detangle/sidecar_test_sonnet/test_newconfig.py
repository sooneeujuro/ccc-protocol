"""새 config(num_ctx 49152, num_predict 16384) 검증: 가장 큰 실패논문에서 JSON 완결되나."""
import json, os, glob, urllib.request, sys
sys.stdout.reconfigure(encoding="utf-8")
BK = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging_FAILED_backup"
ARTS = r"C:\Users\USER\corpus_md_export_20260612\articles"
MAXCHARS = 95000
SCHEMA = {"type":"object","properties":{
  "classification_type":{"type":"string","enum":["gas","petrology","both","other"]},
  "made_new_measurements":{"type":"boolean"},
  "variables_reported":{"type":"array","items":{"type":"object","properties":{
    "raw_label":{"type":"string"},"id":{"type":"string"},
    "unit":{"type":["string","null"]},"phase":{"type":["string","null"]},"kind":{"type":["string","null"]}},
    "required":["raw_label"]}}},
  "required":["classification_type","made_new_measurements","variables_reported"]}
INSTR = ("You build a DATA INVENTORY for a geochemistry paper. Output ONLY JSON per the schema.\n"
  "List EACH quantity SEPARATELY (each element, isotope ratio, oxide). Only quantities actually present.\n\nPAPER TEXT:\n")

# 가장 큰 실패논문 MD
sized = []
for f in glob.glob(os.path.join(BK,"*.json")):
    pid = os.path.basename(f)[:-5]
    md = os.path.join(ARTS, pid+".md")
    if os.path.exists(md): sized.append((os.path.getsize(md), pid, md))
sized.sort(reverse=True)
sz, pid, mdp = sized[0]
print(f"테스트 논문(최대 실패MD): {pid[:45]} ({sz//1024}KB)")
md = open(mdp, encoding="utf-8", errors="replace").read()[:MAXCHARS]
print(f"입력 MD chars: {len(md)} (~{len(md)//4}토큰 추정)")

body = json.dumps({"model":"gemma4:12b","messages":[{"role":"user","content":INSTR+md}],
  "stream":False,"think":False,"format":SCHEMA,
  "options":{"temperature":0,"num_ctx":49152,"num_predict":16384}}).encode("utf-8")
req = urllib.request.Request("http://localhost:11434/api/chat", data=body, headers={"Content-Type":"application/json"})
import time; t0=time.time()
with urllib.request.urlopen(req, timeout=900) as r:
    resp = json.loads(r.read().decode("utf-8"))
el = time.time()-t0
c = resp.get("message",{}).get("content","")
print(f"\n소요 {el:.0f}s | done_reason={resp.get('done_reason')} | eval_count(출력토큰)={resp.get('eval_count')}")
print(f"content 길이: {len(c)}자")
try:
    j = json.loads(c)
    print(f"✅ JSON 완결 | class={j['classification_type']} made_new={j['made_new_measurements']} vars={len(j['variables_reported'])}개")
    print("  vars 샘플:", [v.get('raw_label') for v in j['variables_reported'][:8]])
except Exception as e:
    print(f"❌ JSON 파싱실패: {str(e)[:60]}")
    print("  끝 120자:", c[-120:])
