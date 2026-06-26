import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

files = [
    r"C:\Users\USER\AppData\Local\Temp\claude\C--Users-USER-Documents-ccc-protocol\e243ae13-7b72-485a-965a-348e1f651638\tasks\wf5arhqrt.output",
    r"C:\Users\USER\AppData\Local\Temp\claude\C--Users-USER-Documents-ccc-protocol\e243ae13-7b72-485a-965a-348e1f651638\tasks\wobr8a12a.output",
]
errs = []
for f in files:
    t = Path(f).read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r'"haiku_errors_found":\s*\[(.*?)\]', t, re.S):
        for s in re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1)):
            errs.append(s.lower())

cat = {"hallucination_reextract":0, "cited_as_measured_reextract":0, "modeled_missing_reextract":0,
       "classification_enum_normalize":0, "instrument_misclass_normalize":0, "other":0}
for e in errs:
    if "hallucinat" in e or "fabricat" in e:
        cat["hallucination_reextract"] += 1
    elif "cited" in e and ("measured" in e or "provenance" in e or "not measured" in e):
        cat["cited_as_measured_reextract"] += 1
    elif "modeled" in e or "thermomet" in e or "calculated" in e or "temperatur" in e:
        cat["modeled_missing_reextract"] += 1
    elif "classification" in e:
        cat["classification_enum_normalize"] += 1
    elif "tims" in e or "irms" in e or "instrument" in e or "misclassif" in e or "category" in e or "standard" in e:
        cat["instrument_misclass_normalize"] += 1
    else:
        cat["other"] += 1

print(f"parsed errors: {len(errs)}")
for k, v in cat.items():
    print(f"  {v:3}  {k}")
reext = cat["hallucination_reextract"] + cat["cited_as_measured_reextract"] + cat["modeled_missing_reextract"]
norm = cat["classification_enum_normalize"] + cat["instrument_misclass_normalize"]
print(f"--- RE-EXTRACT needed (Sonnet): {reext} | NORMALIZE-fixable ($0): {norm} | other: {cat['other']} ---")
