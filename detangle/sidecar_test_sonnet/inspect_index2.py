import os, json, sys
sys.stdout.reconfigure(encoding="utf-8")
root = r"G:\corpus_20260624"
# depth-1 named(비hex) 폴더 = articles/index/pdfs/supp
print("=== corpus_20260624 depth-1 named 폴더 ===")
for d in sorted(os.listdir(root)):
    p = os.path.join(root, d)
    if os.path.isdir(p) and not (len(d) == 12 and all(c in "0123456789abcdef" for c in d)):
        print(f"  [{d}]/")
        for f in sorted(os.listdir(p))[:12]:
            fp = os.path.join(p, f)
            tag = "/" if os.path.isdir(fp) else f"  {os.path.getsize(fp)//1024}KB"
            print(f"      {f}{tag}")
print("\n=== _manifest.jsonl 첫 2줄 구조 ===")
with open(os.path.join(root, "_manifest.jsonl"), encoding="utf-8", errors="replace") as fh:
    for i, line in enumerate(fh):
        if i >= 2: break
        try: print(" keys:", list(json.loads(line).keys()))
        except: print(" raw:", line[:200])
# 줄 수
n = sum(1 for _ in open(os.path.join(root, "_manifest.jsonl"), encoding="utf-8", errors="replace"))
print(f" _manifest.jsonl 총 {n}줄")
