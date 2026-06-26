import os, sys
sys.stdout.reconfigure(encoding="utf-8")
roots = ["G:/", "D:/Academia"]
seen = {}
for r in roots:
    for dp, dn, fn in os.walk(r):
        c = sum(1 for f in fn if f.endswith(".md"))
        if c >= 20:
            seen[dp] = c
for k in sorted(seen, key=lambda x: -seen[x])[:45]:
    print(f"{seen[k]:>6}  {k}")
print(f"\n총 MD폴더(>=20): {len(seen)}  | MD합계: {sum(seen.values())}")
