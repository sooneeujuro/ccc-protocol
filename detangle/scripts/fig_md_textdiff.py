#!/usr/bin/env python3
"""fig_md_textdiff.py — 교체된 10편 MD의 본문 텍스트가 실제로 바뀌었는지 확인.

backup(교체 전) vs articles(교체 후)를 이미지 ref 제외한 본문 텍스트로 비교.
sim=1.0이면 텍스트 동일(=재색인 불필요). 낮으면 본문 바뀜(=재색인 필요).
READ-ONLY.
"""
import re
import difflib
from pathlib import Path

BACKUP = Path(r"G:\corpus_md_export_20260612\_fig_merge_backup_20260616")
ART = Path(r"G:\corpus_md_export_20260612\articles")
IMG_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")


def textonly(p):
    t = p.read_text(encoding="utf-8", errors="replace")
    t = IMG_RE.sub("", t)              # 이미지 ref 줄 제거
    return re.sub(r"\s+", " ", t).strip()  # 공백 정규화 (줄바꿈 차이 무시)


print(f"{'MD':44} {'len(전→후)':>16} {'sim':>6}")
worst = 1.0
for bak in sorted(BACKUP.glob("*.md")):
    cur = ART / bak.name
    if not cur.exists():
        print(f"{bak.name[:42]:44} MISSING in articles")
        continue
    a, b = textonly(bak), textonly(cur)
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    worst = min(worst, ratio)
    flag = "  <-- 거의 동일" if ratio > 0.97 else ("  <-- 차이 큼" if ratio < 0.85 else "")
    print(f"{bak.name[:42]:44} {len(a):>7}->{len(b):<7} {ratio:6.3f}{flag}")

print(f"\n최저 유사도: {worst:.3f}")
print("→ 전부 >0.97 이면 본문 거의 동일 = 재색인 사실상 불필요(이미지만 바뀜)" if worst > 0.97
      else "→ 본문 차이 있음 = 재색인 권장")
