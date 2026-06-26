"""1편 까보기: Gemma 인벤토리 변수 vs Sonnet 변수 side-by-side. 환각 vs granularity 판별."""
import json, sys, re, os, glob, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
ARTS = r"C:\Users\USER\corpus_md_export_20260612\articles"
STAGE = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging"
sys.argv += [""]
pool = [f[:-5] for f in sorted(os.listdir(STAGE)) if f.endswith(".json")
        and glob.glob(os.path.join(ARTS, f[:-5] + ".md"))]
dev = pool[0::max(1, len(pool)//12)][:10]
pid = dev[1]   # 2번째 dev (1번째는 006f3a79 noble gas)
print("논문:", pid[:55])

SCHEMA = {"type": "object", "properties": {
    "variables_reported": {"type": "array", "items": {"type": "object", "properties": {
        "raw_label": {"type": "string"}, "id": {"type": "string"}},
        "required": ["raw_label"]}}}, "required": ["variables_reported"]}
INSTR = ("List EXHAUSTIVELY every distinct quantity/data variable present in this geochemistry paper, "
         "each separately (each element, isotope ratio, oxide). Plain text labels, no LaTeX. "
         "Only what is actually in the paper. PAPER:\n")
md = open(glob.glob(os.path.join(ARTS, pid + ".md"))[0], encoding="utf-8", errors="replace").read()[:95000]
body = json.dumps({"model": "gemma4:12b", "messages": [{"role": "user", "content": INSTR + md}],
                   "stream": False, "format": SCHEMA,
                   "options": {"temperature": 0, "num_ctx": 32768, "num_predict": 8192}}).encode("utf-8")
req = urllib.request.Request("http://localhost:11434/api/chat", data=body, headers={"Content-Type": "application/json"})
out = json.loads(urllib.request.urlopen(req, timeout=900).read().decode("utf-8"))["message"]["content"]
gvars = [v.get("raw_label", "") for v in json.loads(out).get("variables_reported", [])]
son = json.load(open(os.path.join(STAGE, pid + ".json"), encoding="utf-8"))
svars = [v.get("raw_label", "") for v in (son.get("variables_measured") or [])]

def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower())
def toks(s): return set(re.findall(r"[a-z0-9]{2,}", (s or "").lower()))
def m(lab, others):
    lt, ln = toks(lab), norm(lab)
    for o in others:
        on, ot = norm(o), toks(o)
        if ln and (ln in on or on in ln): return True
        if lt and ot and len(lt & ot)/max(1, len(lt | ot)) >= 0.34: return True
    return False

print(f"\n=== Gemma {len(gvars)}개 / Sonnet {len(svars)}개 ===")
print("\n[Gemma만 (Sonnet에 매칭 없음 = 환각? or 더 잘게?)]")
for g in gvars:
    if not m(g, svars): print("   +", g[:60])
print("\n[Sonnet만 (Gemma가 놓침)]")
for s in svars:
    if not m(s, gvars): print("   -", s[:60])
print("\n[양쪽 매칭]")
both = [g for g in gvars if m(g, svars)]
print(f"   {len(both)}개:", ", ".join(b[:22] for b in both[:12]))
