"""백업이동된 400 정체: Sonnet 답안지인가 Haiku인가? provenance/model/구조 확인."""
import json, glob, os, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
BK = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging_FAILED_backup"
fs = glob.glob(os.path.join(BK, "*.json"))
print(f"백업 파일 수: {len(fs)}")
prov_models = Counter(); has_vm = 0; has_vr = 0; schema_vers = Counter()
ext_models = Counter()
sample = []
for f in fs:
    try: j = json.load(open(f, encoding="utf-8"))
    except: continue
    if "variables_measured" in j: has_vm += 1
    if "variables_reported" in j: has_vr += 1
    schema_vers[j.get("schema_version", "none")] += 1
    prov = j.get("provenance", {})
    pm = prov.get("model") if isinstance(prov, dict) else None
    em = (j.get("extraction_meta") or {})
    emm = em.get("model") if isinstance(em, dict) else None
    # 어디든 sonnet/haiku 언급 찾기
    blob = json.dumps(j, ensure_ascii=False).lower()
    tag = "sonnet" if "sonnet" in blob else ("haiku" if "haiku" in blob else "?")
    prov_models[tag] += 1
    if len(sample) < 3:
        sample.append((os.path.basename(f)[:35], list(j.keys())[:12], pm, emm))
print(f"variables_measured 보유: {has_vm} | variables_reported 보유: {has_vr}")
print(f"schema_version 분포: {dict(schema_vers)}")
print(f"sonnet/haiku 언급(전체 JSON): {dict(prov_models)}")
print("\n샘플 3:")
for nm, keys, pm, em in sample:
    print(f"  {nm}")
    print(f"    keys: {keys}")
    print(f"    provenance.model={pm} extraction_meta.model={em}")
