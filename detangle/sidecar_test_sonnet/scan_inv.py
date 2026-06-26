"""저장된 Gemma 인벤토리 출력으로 recall-miss / precision-extra 성격 분석 ($0, Gemma 재호출 없음)."""
import json, re, os, sys
sys.stdout.reconfigure(encoding="utf-8")
SF = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet"
data = json.load(open(os.path.join(SF, "GEMMA_INV_OUTPUTS.json"), encoding="utf-8"))

_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
_SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
def canon(s):
    s = (s or "").translate(_SUP).translate(_SUB).lower().replace("δ", "d").replace("∆", "d").replace("delta", "d")
    return s
def norm(s): return re.sub(r"[^a-z0-9]", "", canon(s))
def toks(s): return set(re.findall(r"[a-z0-9]{2,}", canon(s)))
def m(lab, others):
    lt, ln = toks(lab), norm(lab)
    for o in others:
        on, ot = norm(o), toks(o)
        if ln and (ln in on or on in ln): return True
        if lt and ot and len(lt & ot)/max(1, len(lt | ot)) >= 0.34: return True
    return False

tot_miss = tot_extra = 0
print("=== 논문별 recall-miss(Sonnet에 있는데 Gemma 놓침) / extra(Gemma만) ===")
for d in data:
    g, s = d["g"], d["s"]
    miss = [x for x in s if not m(x, g)]
    extra = [x for x in g if not m(x, s)]
    tot_miss += len(miss); tot_extra += len(extra)
    if miss or extra:
        print(f"\n[{d['pid'][:40]}] g{len(g)} s{len(s)} | miss {len(miss)} extra {len(extra)}")
        if miss: print("   놓침:", " | ".join(x[:24] for x in miss[:6]))
        if extra: print("   추가:", " | ".join(x[:24] for x in extra[:6]))
print(f"\n총 놓침 {tot_miss} / 총 추가 {tot_extra}")
