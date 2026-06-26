"""파일럿 출력에서 integrity 불일치(Haiku=measured인데 Sonnet=cited/modeled, 또는 hallucination)
를 가진 논문을 추출 → 검증배치 타깃 리스트. read-only."""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"C:\Users\USER\AppData\Local\Temp\claude\C--Users-USER-Documents-ccc-protocol\e243ae13-7b72-485a-965a-348e1f651638\tasks")
files = ["wf5arhqrt.output", "wobr8a12a.output"]

def judg(s):
    s = (s or "").lower()
    if "cite" in s: return "cited"
    if "model" in s or "calcul" in s or "thermomet" in s: return "modeled"
    if "halluc" in s or "fabricat" in s or "not in paper" in s or "absent" in s: return "hallucinated"
    if "measur" in s: return "measured"
    return s[:20]

papers = {}   # paper_id -> {disputes:[...], instr_disagree:bool}
for fn in files:
    p = BASE / fn
    if not p.exists():
        continue
    data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    for v in (data.get("result") or {}).get("verdicts", []):
        pid = v.get("paper_id")
        if not pid:
            continue
        rec = papers.setdefault(pid, {"disputes": [], "instr": None, "errs": []})
        instr = v.get("instrument") or {}
        if instr.get("agree") is False:
            rec["instr"] = f'{instr.get("haiku")}→{instr.get("sonnet")}'
        for vc in v.get("variables_checked", []):
            sj = judg(vc.get("sonnet_judgment"))
            hj = judg(vc.get("haiku_judgment"))
            if vc.get("agree") is False and sj in ("cited", "modeled", "hallucinated") and hj == "measured":
                rec["disputes"].append({"label": vc.get("label"), "sonnet": sj,
                                        "evidence": (vc.get("evidence") or "")[:160]})
        for e in (v.get("haiku_errors_found") or []):
            rec["errs"].append(e[:120])

# integrity 분쟁이 있는 논문 우선
ranked = sorted(papers.items(),
                key=lambda kv: (-len(kv[1]["disputes"]), -len(kv[1]["errs"])))
target = [pid for pid, r in ranked if r["disputes"] or r["errs"]]

print(f"파일럿 논문 총 {len(papers)} | integrity 분쟁/오류 보유 {len(target)}")
print("\n=== 검증 타깃 후보 (provenance 분쟁 상위) ===")
for pid, r in ranked:
    if not (r["disputes"] or r["errs"]):
        continue
    d = r["disputes"]
    tag = f"{len(d)}분쟁" + (f" +instr {r['instr']}" if r["instr"] else "")
    print(f"  [{tag:18}] {pid[:48]}")
    for x in d[:3]:
        print(f"        {x['sonnet']:11} ⟸ Haiku=measured : {x['label']}")

out = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\VALIDATION_TARGETS.json")
out.write_text(json.dumps({"targets": target,
                           "detail": {pid: papers[pid] for pid in target}},
                          ensure_ascii=False, indent=1), encoding="utf-8")
print(f"\n타깃 {len(target)}편 → {out.name}")
