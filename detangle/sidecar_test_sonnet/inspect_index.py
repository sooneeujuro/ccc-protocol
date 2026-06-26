import os, sys
sys.stdout.reconfigure(encoding="utf-8")
root = r"G:\corpus_20260624"
for dp, dn, fn in os.walk(root):
    depth = dp[len(root):].count(os.sep)
    if depth > 2: continue
    big = [f for f in fn if f.endswith((".json",".jsonl",".faiss",".npy",".pkl",".index",".bin",".parquet"))]
    if big or depth <= 1:
        rel = dp[len(root):].lstrip("\\") or "(root)"
        print(f"[{rel}]  ({len(fn)} files)")
        for f in sorted(big)[:14]:
            sz = os.path.getsize(os.path.join(dp, f)) // 1024
            print(f"     {f}  {sz}KB")
