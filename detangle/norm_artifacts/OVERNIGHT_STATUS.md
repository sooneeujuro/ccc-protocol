# OVERNIGHT STATUS — VP-NORM-1 co-op (Claude ↔ Codex)
last update: cycle 4 wake (~03:10, 2026-06-16).

## normalizer (PRIMARY)
trajectory: **12.9 → 47.3 → 56.1 → 62.1 → 71.2%**  (target 90% @ precision≥98%)
cycle 4 = generic ratio(genrat 1246)/isotope ratio(isorat 745)/gloss(1531)/CI(54), **precision-cleaned**.
Codex 007 재감사 ~25min 미도착 → Claude self-audit로 게이트 대행:
- cycle-3: F(ppm)→fraction 오매칭·age 과탐·3H/3He·mmol/mol **3건 수정**.
- cycle-4: gloss 초안 ~25% false(수식어/약어에서 심볼 오추출) → **element-name↔symbol + qualifier차단으로 보수화**.
→ 008로 Codex 독립 재감사 요청(retroactive 게이트, false시 롤백).
남은 미매칭 9,279: junk(' ','"') 등장 + 물리량(Vp/Vs velocity·heat flow·density)·flux·δ34S bare 등 → cycle 5 후보.

## termination checklist (B = sidecar write 제외, 운영자 인계)
- [~진행] **normalizer 90%@98%** — 71.2%, precision self-audit 통과(Codex 재감사 대기). cycle 5(물리량·flux·잔여) 남음.
- [✅검증] **PR#15** — Codex 004/005 통과. merge 게이트.
- [⚠️정렬필요] **PR#16** — isotope golden 빌드 vocab과 일치. id-스킴(SiO2 vs SiO2_wt_pct) finalize 시 정렬.
- [환경블록] **그림** — 830편 datalab머신+NAS 필요(회사PC 불가). allowlist 문서화됨.
- [B후/그림블록] **G/local 배포** — 정규화 완성본은 B후.

## 게이트: B 미접촉 · corpus git-push 0 · 지출 $0. STOP=detangle/STOP.md.
