"""Workflow 출력(task .output) → 기존 Haiku sidecar에 판단필드만 교체 → v2.2 staging 기록.
usage: python prod_merge_chunk.py <task_id>
유지: abstract/conclusions/refs/figures/geography/labs/instruments(별도 remap) 등.
교체: classification(type/confidence/evidence) + variables_measured(+provenance/evidence) + made_new_measurements."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

SIDE = Path(r"C:\Users\USER\corpus_md_export_20260612\sidecars")
STAGE = Path(r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_staging")
STAGE.mkdir(exist_ok=True)
TASKS = Path(r"C:\Users\USER\AppData\Local\Temp\claude\C--Users-USER-Documents-ccc-protocol\e243ae13-7b72-485a-965a-348e1f651638\tasks")
tid = sys.argv[1]

raw = json.loads((TASKS / f"{tid}.output").read_text(encoding="utf-8", errors="replace"))
res = raw.get("result", raw)
results = res.get("results", [])

wrote = skipped = nullx = 0
prov_counts = {"measured": 0, "cited": 0, "modeled": 0}
new_meas_false = 0
for r in results:
    pid = r.get("paper_id"); ext = r.get("extraction")
    if not ext:
        nullx += 1; continue
    src = SIDE / f"{pid}.json"
    if not src.exists():
        skipped += 1; continue
    sc = json.loads(src.read_text(encoding="utf-8", errors="replace"))
    # 판단필드 교체
    cls = ext.get("classification") or {}
    if cls.get("type"):
        sc.setdefault("classification", {})
        sc["classification"]["type"] = cls["type"]
        if cls.get("confidence") is not None:
            sc["classification"]["confidence"] = cls["confidence"]
        if cls.get("evidence"):
            sc["classification"]["evidence"] = cls["evidence"]
    vlist = []
    for v in ext.get("variables") or []:
        vlist.append({
            "id": v.get("id") or "raw_label_only",
            "raw_label": v.get("raw_label", ""),
            "unit": v.get("unit"),
            "phase": v.get("phase"),
            "provenance": v.get("provenance"),
            "evidence": v.get("evidence"),
        })
        if v.get("provenance") in prov_counts:
            prov_counts[v["provenance"]] += 1
    sc["variables_measured"] = vlist
    sc["made_new_measurements"] = ext.get("made_new_measurements")
    if ext.get("made_new_measurements") is False:
        new_meas_false += 1
    sc["schema_version"] = "v2.2"
    sc.setdefault("extraction_meta", {})
    sc["extraction_meta"]["provenance_reextract"] = {
        "model": "claude-sonnet (workflow subagent)",
        "fields": ["classification.type", "variables_measured+provenance", "made_new_measurements"],
        "task": tid,
        "kept_from_haiku": ["abstract_raw", "conclusions_raw", "references",
                            "figure_summaries", "page_anchors", "geography",
                            "analytical(instruments via $0 remap)"],
    }
    (STAGE / f"{pid}.json").write_text(json.dumps(sc, ensure_ascii=False, indent=1), encoding="utf-8")
    wrote += 1

print(f"머지 완료: 기록 {wrote} | null(throttle/실패) {nullx} | src없음 {skipped}")
print(f"  provenance 합계: {prov_counts}  | made_new_measurements=false: {new_meas_false}편")
print(f"  staging 누적: {len(list(STAGE.glob('*.json')))} / 3948")
