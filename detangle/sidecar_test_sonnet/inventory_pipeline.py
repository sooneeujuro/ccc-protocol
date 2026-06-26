"""B: MA 패키징용 — 재사용 파이프라인 스크립트의 하드코딩 경로 인벤토리 + 위치 확인.
일반화(경로 configurable) 필요량 파악."""
import os, re, glob, sys
sys.stdout.reconfigure(encoding="utf-8")
ABS = re.compile(r'(?:[A-Za-z]:\\\\|[A-Za-z]:\\|/[cg]/)[^\s"\'<>]+', re.I)

cands = {
 "convert_pdfs(PDF→MD)": r"C:\Users\USER\corpus_md_export_20260612\scripts\convert_pdfs.py",
 "gemma_production(sidecar)": r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\gemma_production.py",
 "check_complete(gate)": r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\check_complete.py",
 "loop_gemma_v2(루프)": r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\loop_gemma_v2.bat",
 "segment_dryrun_v1(책분절)": r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\segment_dryrun_v1_codex.py",
}
print("=== 하드코딩 절대경로 인벤토리 ===")
for name, p in cands.items():
    if not os.path.exists(p): print(f"  [{name}] ❌ 파일없음"); continue
    t = open(p, encoding="utf-8", errors="replace").read()
    paths = set(m.group(0) for m in ABS.finditer(t))
    has_argparse = "argparse" in t or "ArgumentParser" in t
    print(f"  [{name}] 하드코딩경로 {len(paths)}개 | argparse={'Y' if has_argparse else 'N'}")
    for pp in sorted(paths)[:4]: print(f"       {pp[:70]}")

print("\n=== 인덱스 빌더 / 리더 위치 탐색 ===")
for pat in ["build_bm25*","build_bge*","build_retrieval*","read_paper_ns*"]:
    hits = glob.glob(rf"C:\Users\USER\**\{pat}.py", recursive=False) + glob.glob(rf"G:\**\{pat}.py", recursive=False)
    # 얕은 탐색 실패시 알려진 위치
    found = []
    for base in [r"G:\corpus_20260624\scripts", r"G:\corpus_20260624\index\scripts", r"C:\Users\USER\corpus_md_export_20260612\scripts"]:
        found += glob.glob(os.path.join(base, pat + ".py"))
    shown = [os.path.basename(f) + " @ " + os.path.dirname(f) for f in found[:3]]
    print("  " + pat + ": " + (str(shown) if shown else "미발견(딴 위치)"))
