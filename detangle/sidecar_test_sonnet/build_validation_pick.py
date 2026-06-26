"""검증배치 픽 빌드: 분쟁16 + 무분쟁8 = 24편. MD경로 resolve + 기존 Haiku 변수 첨부.
read-only. 출력=VALIDATION_PICK.json (Workflow에 주입할 데이터)."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

SF = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet")
ARTS = Path(r"C:\Users\USER\corpus_md_export_20260612\articles")
SIDE = Path(r"C:\Users\USER\corpus_md_export_20260612\sidecars")
tgt = json.loads((SF / "VALIDATION_TARGETS.json").read_text(encoding="utf-8"))
detail = tgt["detail"]

def md_path(pid):
    p = ARTS / (pid + ".md")
    return str(p) if p.exists() else None

def haiku_vars(pid):
    j = SIDE / (pid + ".json")
    if not j.exists():
        return None
    try:
        sc = json.loads(j.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None
    out = []
    for v in sc.get("variables_measured") or []:
        if isinstance(v, dict):
            out.append(v.get("raw_label") or v.get("id") or "")
        elif isinstance(v, str):
            out.append(v)
    return out

disp = [(pid, d) for pid, d in detail.items() if d["disputes"]]
clean = [(pid, d) for pid, d in detail.items() if not d["disputes"]]
disp.sort(key=lambda kv: -len(kv[1]["disputes"]))

pick = []
for pid, d in disp[:16] + clean[:8]:
    mp = md_path(pid)
    if not mp:
        print(f"  [skip:noMD] {pid[:50]}")
        continue
    pick.append({
        "paper_id": pid,
        "md_path": mp,
        "kind": "dispute" if d["disputes"] else "clean",
        "disputed": [{"label": x["label"], "expected": x["sonnet"]} for x in d["disputes"]],
        "haiku_vars_n": len(haiku_vars(pid) or []),
    })

out = SF / "VALIDATION_PICK.json"
out.write_text(json.dumps(pick, ensure_ascii=False, indent=1), encoding="utf-8")
nd = sum(1 for p in pick if p["kind"] == "dispute")
print(f"픽 {len(pick)}편 (분쟁 {nd} + 무분쟁 {len(pick)-nd}) → {out.name}")
for p in pick:
    exp = ", ".join(f"{x['label'][:24]}={x['expected']}" for x in p["disputed"][:2])
    print(f"  [{p['kind']:7}] {p['paper_id'][:44]}  {exp}")
