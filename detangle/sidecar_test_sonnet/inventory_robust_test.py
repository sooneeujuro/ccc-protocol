"""오염의심 N편: 0624 MD로 인벤토리 재추출 → 격리(0612기반) variables_reported와 비교.
MD ~5% 단어차가 변수목록(=사이드카)에 영향 주나. 같으면 reuse 100% 안전."""
import json, os, glob, re, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
QUAR = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_QUARANTINE_oldinput_20260625"
A0624 = r"G:\corpus_20260624\articles"
diff = json.load(open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\MD_VERSION_DIFF.json", encoding="utf-8"))["contaminated"]
SCHEMA = {"type":"object","properties":{
  "classification_type":{"type":"string","enum":["gas","petrology","both","other"]},
  "made_new_measurements":{"type":"boolean"},
  "variables_reported":{"type":"array","items":{"type":"object","properties":{
    "raw_label":{"type":"string"},"id":{"type":"string"}},"required":["raw_label"]}}},
  "required":["classification_type","made_new_measurements","variables_reported"]}
INSTR=("You build a DATA INVENTORY for a geochemistry paper. Output ONLY JSON per schema. "
  "List EACH quantity SEPARATELY (each element/isotope ratio/oxide). Only quantities actually present. "
  "id canonical (3He/4He->He3_He4_RRa,87Sr/86Sr->Sr87_Sr86) else raw_label_only. raw_label PLAIN TEXT.\n\nPAPER TEXT:\n")
DOIre=re.compile(r"10\.\d{4,9}/[A-Za-z0-9._;()/:+\-]+")
def norm(s): return re.sub(r"[^a-z0-9]","",(s or "").lower())
def gemma(md):
    body=json.dumps({"model":"gemma4:12b","messages":[{"role":"user","content":INSTR+md[:95000]}],
      "stream":False,"think":False,"format":SCHEMA,"options":{"temperature":0,"num_ctx":49152,"num_predict":16384}}).encode()
    with urllib.request.urlopen(urllib.request.Request("http://localhost:11434/api/chat",data=body,headers={"Content-Type":"application/json"}),timeout=900) as r:
        return json.loads(json.loads(r.read())["message"]["content"])
# 0624 DOI 인덱스
c24={}
for f in glob.glob(os.path.join(A0624,"*.md")):
    m=DOIre.search(open(f,encoding="utf-8",errors="replace").read(4000))
    if m: c24[m.group(0).lower().rstrip(').,;')]=f
n=0
print(f"{'paper':34} {'0612vars':>8} {'0624vars':>8} {'overlap':>7}")
for pid in diff:
    if n>=5: break
    sc=json.load(open(os.path.join(QUAR,pid+".json"),encoding="utf-8"))
    doi=(sc.get("doi") or "").lower().rstrip(').,;')
    if not doi or doi not in c24: continue
    v12=set(norm(x.get("raw_label")) for x in (sc.get("variables_reported") or []))
    try: out=gemma(open(c24[doi],encoding="utf-8",errors="replace").read())
    except Exception as e: print(f"  {pid[:34]} 추출실패 {str(e)[:30]}"); continue
    v24=set(norm(x.get("raw_label")) for x in out.get("variables_reported",[]))
    ov=len(v12&v24)/max(1,len(v12|v24))
    n+=1
    print(f"{pid[:34]:34} {len(v12):>8} {len(v24):>8} {ov:>7.2f}")
print(f"\n(오염의심 {n}편: 0612기반 vs 0624재추출 변수목록 overlap)")
