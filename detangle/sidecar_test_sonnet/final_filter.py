"""107 거짓양성 제거: 후보 H1을 정리(마크다운링크/URL 제거) 후 '정본최근접'과 difflib.
같은 논문(>=0.7)이면 정본에 있음 → 제외. 진짜 없는 것만."""
import json, re, sys
from difflib import SequenceMatcher
sys.stdout.reconfigure(encoding="utf-8")
ms = json.load(open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\DEFINITIVE_MISSING.json", encoding="utf-8"))
def clean(s):
    s = re.sub(r"\(https?://[^)]*\)?", " ", s)      # (url)
    s = re.sub(r"https?://\S+", " ", s)
    s = re.sub(r"\[|\]|\(#[^)]*\)|<[^>]+>", " ", s)  # 마크다운/태그
    s = re.sub(r"\b(orcid|https|http|www|frontiersin|articles|full|abstract|doi|org)\b", " ", s, flags=re.I)
    return " ".join(re.findall(r"[가-힣a-z0-9]+", s.lower()))
def near_title(fn):
    if not fn: return ""
    fn = re.sub(r"\.md$", "", fn)
    fn = re.sub(r"^[A-Za-z]+_et_al\.?,?_?|\(\d{4}\)|^\w+_\d{4}_|^\w+,_\d{4},_", " ", fn)
    return " ".join(re.findall(r"[가-힣a-z0-9]+", fn.lower()))

NOISE = re.compile(r"scientific (reports|data)|logo|red gear|binary code|a red line drawing", re.I)
truly = []
for m in ms:
    if NOISE.search(m["title"]): continue
    ct = clean(m["title"]); nt = near_title(m.get("near"))
    r = SequenceMatcher(None, ct, nt).ratio() if nt else 0.0
    if r >= 0.62:   # 같은 논문 = 정본에 있음
        continue
    truly.append({**m, "clean_vs_near": round(r,2)})

print(f"107 → 노이즈/같은논문 제거 후 진짜 없음 후보: {len(truly)}\n")
for m in sorted(truly, key=lambda x: x["clean_vs_near"]):
    print(f"  ✗ {m['title'][:78]}")
    print(f"     DOI={m['doi'] or '없음'}  pools={len(m['pools'])}개  (정본최근접 difflib={m['clean_vs_near']}: {(m.get('near') or '')[:55]})")
json.dump(truly, open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\TRULY_MISSING_FINAL.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n→ TRULY_MISSING_FINAL.json ({len(truly)}편)")
