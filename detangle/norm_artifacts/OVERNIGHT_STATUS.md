# OVERNIGHT STATUS — VP-NORM-1 co-op (Claude ↔ Codex)
last update: cycle 3 wake (~02:37, 2026-06-16). 매 non-coverage wake마다 갱신.

## normalizer (PRIMARY)
trajectory: **12.9 → 47.3 → 56.1 → 62.1%**  (target 90% @ precision≥98%)
cycle 3 = precision 수정 (Codex 006 6대 전부). **awaiting Codex 007 재감사** (audit_sample_cycle3 ≥98%?) + cycle-4 greenlight.

## termination checklist (B = sidecar write 제외, 운영자 인계)
- [~진행] **normalizer 90%@98%** — 62.1%, Codex 재감사 대기. cycle 4(generic ratio/글로스/CI)는 greenlight 후.
- [✅검증] **PR#15** verification policy — Codex 004/005 통과. merge는 게이트(운영자/최종).
- [⚠️정렬필요] **PR#16** normalization spec — isotope golden 샘플 전부 빌드 vocab과 **일치 확인 ✅**.
      단 **id-스킴 불일치**: 스펙은 oxide/element를 clean symbol(`SiO2`,`Sr`)로 명시, 구현+Codex 006 ratify는
      `SiO2_wt_pct`/`Sr_conc`(단위의미 보존 + wt_pct 명시단위 가드레일). → finalize 시 구현 스킴으로 정렬.
- [환경블록] **그림** — 6/13 GAP 리포트: 830편 그림이 번들·NAS 부재(원본 datalab 머신에만). allowlist 문서화됨
      (FIGURES_MISSING_ALLOWLIST.txt). 추가 fill = datalab 머신 + NAS 마운트 필요 → 회사PC(NAS다운)서 **불가**. 운영자 env 작업.
- [B후/그림블록] **G/local 배포** — 정규화 포함 완성본은 B 후. 그림+문서 완성본은 그림 환경블록에 묶임.

## 게이트: B 미접촉 · corpus git-push 0 · 지출 $0. STOP=detangle/STOP.md.
