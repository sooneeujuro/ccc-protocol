import hashlib, re, sys, fitz
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

def pid_from(b):
    s = b[:-4] if b.lower().endswith(".pdf") else b
    return s.replace(" ", "_").replace("/", "_")
def slug(pid):
    return hashlib.md5(pid.encode("utf-8")).hexdigest()[:12]
def words(t):
    t = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", t)
    return set(re.findall(r"[a-z]{4,}", t.lower()))

SRC = Path(r"D:\Academia\References\논문_260624")
NEW = Path(r"G:\corpus_md_export_20260618")

skipped = []
for p in sorted(SRC.glob("*.pdf")):
    sg = slug(pid_from(p.name))
    d = NEW / sg
    # 이 batch가 만든 것? 판단: 폴더 MD 파일명이 이 PDF의 pid와 같으면 이번에 추출된 것(legit),
    # 다르면 = 기존 다른 폴더라 skip된 것 -> 검증 대상
    if (d / ".done").exists():
        mds = list(d.glob("*.md"))
        folder_md_stem = mds[0].stem if mds else ""
        if folder_md_stem != pid_from(p.name):
            skipped.append((p, sg, mds[0] if mds else None))

print(f"slug-skip된(기존폴더와 충돌) 후보: {len(skipped)}")
print("=== 본문 대조: 새 PDF 제목 vs 기존 폴더 내용 ===")
same = diff = 0
for p, sg, exmd in skipped:
    try:
        doc = fitz.open(p); pt = doc[0].get_text()[:3000]; doc.close()
        ptw = words(pt)
        ptitle = re.sub(r"\s+", " ", pt[:120]).strip()
    except Exception:
        ptw = set(); ptitle = "(읽기실패)"
    exw = words(exmd.read_text(encoding="utf-8", errors="replace")[:4000]) if exmd else set()
    j = len(ptw & exw) / max(1, len(ptw | exw))
    verdict = "SAME(정상dup)" if j >= 0.4 else "DIFFERENT(⚠️잘못skip!)"
    if j >= 0.4: same += 1
    else: diff += 1
    print(f"  [{verdict} j={j:.2f}] 새:{p.name[:36]}")
    print(f"       기존폴더({sg}): {exmd.name[:40] if exmd else '?'}")
print(f"\n정상 dup: {same} | 잘못 skip 의심: {diff}")
