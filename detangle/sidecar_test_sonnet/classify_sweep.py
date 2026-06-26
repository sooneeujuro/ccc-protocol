"""262 미추출 후보 분류: 잡파일 / 고기후(타도메인 의심) / 진짜 in-scope 논문."""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
g = json.load(open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\SWEEP_GAPS.json", encoding="utf-8"))
ne = g["never_extracted"]

JUNK = re.compile(r"sup-00|supporting info|supplement|summary report|_author\b|si-s0|-t-sup|\bdiss\b|thesis|^\d{4}gc|^\d{5}_\d{4}|moesm", re.I)
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}", re.I)
PALEO = re.compile(r"\bcave\b|hydroclim|paleoclim|\bforam|glaciation|holocene|\bkyr\b|speleothem|monsoon|seawater t|benthic|stalagmite|tropical andes|PETM|deglaci|land st|wet period", re.I)

def strip(s): return re.sub(r"^[0-9a-f]{8,16}__", "", s)
b = {"junk":[], "paleo_oos":[], "real_paper":[]}
for n in ne:
    t = strip(n)
    if JUNK.search(n) or UUID.search(t) or len(re.findall(r"[a-z]{3,}", t.lower())) < 3:
        b["junk"].append(t)
    elif PALEO.search(t):
        b["paleo_oos"].append(t)
    else:
        b["real_paper"].append(t)
print("=== 262 미추출 분류 ===")
for k in b: print(f"  {k}: {len(b[k])}")
print(f"\n=== 진짜 in-scope 논문 후보 (미추출, 네 도메인 가능성) — {len(b['real_paper'])} ===")
for t in sorted(b["real_paper"])[:50]: print(f"  · {t[:68]}")
json.dump(b, open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\SWEEP_CLASSIFIED.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n→ SWEEP_CLASSIFIED.json")
