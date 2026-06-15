# OVERNIGHT STATUS — VP-NORM-1 co-op (Claude ↔ Codex)
last update: cycle 4 wake (~03:10, 2026-06-16).

## normalizer (PRIMARY)
trajectory: **12.9 → 47.3 → 56.1 → 62.1 → 71.2%**  (target 90% @ precision≥98%)
cycle 4 = generic ratio(genrat 1246)/isotope ratio(isorat 745)/gloss(1532)/CI(54), **precision-clean**.
**Codex 007 통합 완료** — 두 모델 수렴: 7개 hard false 중 Claude self-audit 4개(F(ppm)/age과탐/3H3He/mmol-mol) +
Codex 3개(Fe3+→Fe3_conc·REE-Y→REE_Y_sum·total Fe→Fe_total_conc, speciation/조성 nuance). + gloss ~25% false→보수화.
→ 009로 cycle-4 재감사 요청(retroactive 게이트). watcher 번호하드코딩 버그(둘 다, 007B) → 번호무관 수정.
남은 미매칭 9,267: junk(' ','"') + 물리량(Vp/Vs velocity·heat flow·density)·flux·δ34S bare → cycle 5 후보(greenlight 대기).

## termination checklist (B = sidecar write 제외, 운영자 인계)
- [~진행] **normalizer 90%@98%** — 71.2%, precision self-audit 통과(Codex 재감사 대기). cycle 5(물리량·flux·잔여) 남음.
- [✅검증] **PR#15** — Codex 004/005 통과. merge 게이트.
- [⚠️정렬필요] **PR#16** — isotope golden 빌드 vocab과 일치. id-스킴(SiO2 vs SiO2_wt_pct) finalize 시 정렬.
- [환경블록] **그림** — 830편 datalab머신+NAS 필요(회사PC 불가). allowlist 문서화됨.
- [B후/그림블록] **G/local 배포** — 정규화 완성본은 B후.

## 게이트: B 미접촉 · corpus git-push 0 · 지출 $0. STOP=detangle/STOP.md.
