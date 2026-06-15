# OVERNIGHT STATUS — VP-NORM-1 co-op (Claude ↔ Codex)
last update: cycle 4.1 wake (~03:35, 2026-06-16).

## normalizer (PRIMARY)
trajectory: **12.9 → 47.3 → 56.1 → 62.1 → 71.2 → 72.6 → 73.3%**  (target 90% @ precision≥98%)
cycle 5(73.3%) = 물리/지구물리량·flux·bare δ·용존산화물·age세분 + 010/011 가드(FeOT/REE-Y/TREE). Codex 4.1/4.2 PASS(98.3%).
**⚠️ 트래젝토리 평탄화 — 90% 천장 재평가**: 남은 8,828 미매칭 중 7,228 unique(싱글톤). 클린 cleanup으로 ~80% 가능,
90%는 싱글톤 꼬리(특이/모호/junk) force-match 필요 → precision 위험. 012로 Codex와 천장 합의 중(운영자 "90% 무리 금지" 발동 임박).
cycle 4 = generic ratio(genrat 1246)/isotope ratio(isorat 745)/gloss(1532)/CI(54), **precision-clean**.
**Codex 007 통합 완료** — 두 모델 수렴: 7개 hard false 중 Claude self-audit 4개(F(ppm)/age과탐/3H3He/mmol-mol) +
Codex 3개(Fe3+→Fe3_conc·REE-Y→REE_Y_sum·total Fe→Fe_total_conc, speciation/조성 nuance). + gloss ~25% false→보수화.
+ 008 retro + 009 재감사 통합 = **cycle 4.2**. **Codex 3라운드 감사(007/008/009) 전부 반영, false-match 12패턴 공동해소.**
4.2 신규: Pressure(GPa)→pressure(물리량 unit-agnostic), LaN/YbN→raw, REE profile 차단.
→ 011로 cycle-4.2 최종 재감사 + cycle-5 greenlight 요청. wake 정책(번호무관+3-quiet-ping) 미러.
남은 미매칭 ~9,270: junk(' ','"') + 물리/지구물리량·flux·δ34S bare → cycle 5(90% 향해, 최종 greenlight 대기).

## termination checklist (B = sidecar write 제외, 운영자 인계)
- [~진행] **normalizer 90%@98%** — 71.2%, precision self-audit 통과(Codex 재감사 대기). cycle 5(물리량·flux·잔여) 남음.
- [✅검증] **PR#15** — Codex 004/005 통과. merge 게이트.
- [⚠️정렬필요] **PR#16** — isotope golden 빌드 vocab과 일치. id-스킴(SiO2 vs SiO2_wt_pct) finalize 시 정렬.
- [환경블록] **그림** — 830편 datalab머신+NAS 필요(회사PC 불가). allowlist 문서화됨.
- [B후/그림블록] **G/local 배포** — 정규화 완성본은 B후.

## 게이트: B 미접촉 · corpus git-push 0 · 지출 $0. STOP=detangle/STOP.md.
