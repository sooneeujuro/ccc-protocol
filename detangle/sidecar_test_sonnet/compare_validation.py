"""검증 Workflow 출력 vs 파일럿 분쟁 비교.
분쟁 변수가 보정 Sonnet에서 cited/modeled로 바로잡혔나(fix율) + 무분쟁 논문 false-positive율."""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

SF = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet")
TASKS = Path(r"C:\Users\USER\AppData\Local\Temp\claude\C--Users-USER-Documents-ccc-protocol\e243ae13-7b72-485a-965a-348e1f651638\tasks")
TASK_ID = sys.argv[1] if len(sys.argv) > 1 else "wtwxfeja2"

raw = json.loads((TASKS / f"{TASK_ID}.output").read_text(encoding="utf-8", errors="replace"))
res = raw.get("result", raw)
results = res.get("results", res if isinstance(res, list) else [])
pick = json.loads((SF / "VALIDATION_PICK.json").read_text(encoding="utf-8"))
disp_by_pid = {p["paper_id"]: p["disputed"] for p in pick if p["kind"] == "dispute"}

def norm(s):
    s = (s or "").lower()
    return re.sub(r"[^a-z0-9]", "", s)
def toks(s):
    return set(re.findall(r"[a-z0-9]{2,}", (s or "").lower()))

def find_prov(variables, label):
    lt = toks(label); ln = norm(label)
    best = None; bestsc = 0
    for v in variables:
        vl = v.get("raw_label", "")
        vn = norm(vl); vt = toks(vl)
        sc = 0
        if ln and (ln in vn or vn in ln):
            sc = 3
        elif lt and vt:
            sc = len(lt & vt) / max(1, len(lt | vt)) * 2
        if sc > bestsc:
            bestsc = sc; best = v
    return (best.get("provenance"), best.get("raw_label")) if (best and bestsc >= 0.34) else (None, None)

n_fixed = n_disp = 0
print("=== 분쟁 논문: Haiku=measured → 보정Sonnet provenance ===")
for r in results:
    pid = r.get("paper_id"); ext = r.get("extraction") or {}
    if pid not in disp_by_pid:
        continue
    vars_ = ext.get("variables") or []
    cls = ext.get("classification_type"); mnm = ext.get("made_new_measurements")
    print(f"\n[{pid[:48]}]  class={cls} new_meas={mnm} vars={len(vars_)}")
    for d in disp_by_pid[pid]:
        got, matched = find_prov(vars_, d["label"])
        n_disp += 1
        ok = got is not None and got != "measured"  # cited나 modeled로 바뀌면 fix
        exact = got == d["expected"]
        n_fixed += 1 if ok else 0
        flag = "✅FIX" + ("=exact" if exact else f"({got})") if ok else (f"❌still measured" if got == "measured" else f"⚠️no-match")
        print(f"   {flag:22} exp={d['expected']:8} | {d['label'][:46]}")

print(f"\n분쟁변수 {n_disp}개 중 측정→cited/modeled 교정 {n_fixed} ({n_fixed/max(1,n_disp)*100:.0f}%)")

print("\n=== 무분쟁(측정정상) 논문: false-positive 체크 ===")
fp_tot = fp_non = 0
for r in results:
    pid = r.get("paper_id"); ext = r.get("extraction") or {}
    if pid in disp_by_pid or not ext:
        continue
    vars_ = ext.get("variables") or []
    non = [v for v in vars_ if v.get("provenance") != "measured"]
    fp_tot += len(vars_); fp_non += len(non)
    mnm = ext.get("made_new_measurements")
    print(f"  [{pid[:42]}] new_meas={mnm} vars={len(vars_)} non-measured={len(non)}"
          + (f"  ⚠️{[v.get('raw_label','')[:18] for v in non[:4]]}" if non else ""))
print(f"\n무분쟁 변수 {fp_tot}개 중 measured 아님 {fp_non} ({fp_non/max(1,fp_tot)*100:.0f}%) — 낮을수록 좋음(과교정 적음)")

# 저장
(SF / "VALIDATION_RESULT.json").write_text(
    json.dumps({"fixed": n_fixed, "disputed": n_disp,
                "fp_nonmeasured": fp_non, "fp_total": fp_tot,
                "results": results}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"\n→ VALIDATION_RESULT.json 저장")
