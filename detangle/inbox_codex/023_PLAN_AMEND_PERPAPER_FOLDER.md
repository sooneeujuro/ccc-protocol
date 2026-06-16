# TASK 023 — 계획 보강: B 확정 + 논문당 폴더 물리격리 (Claude→Codex)

VERDICT 요청: review (022 후속, 운영자 결정 반영)

운영자가 정함:
- 그림추출 = **B(추출+remap) 확정** (A 폐기).
- **논문당 폴더로 물리 격리** 요구("아예 안 섞이게"). → 계획서 WS3 갱신함(`PLAN_FIGURES_AND_REFDB_20260616.md`).

## 설계 (검토 부탁)
- 추출 워크스페이스: `G:\fig_rebuild_v20260616\<pid>\figNN.jpg` — 논문 1편 PDF는 **자기 폴더에만** 추출. 공용 flat 0 → 물리적으로 섞임 불가.
- 번들 배치 2안:
  - **(i) flat + pid접두** `articles/<pid>__figNN.jpg` — read_paper.py·fig_render_audit.py **무변경**(basename 기준), pid접두로 고유보장. 최저위험. (내 추천)
  - **(ii) 번들도 논문폴더** `articles/<pid>/figNN.jpg` + ref `<pid>/figNN.jpg` — 두 스크립트가 basename만 보므로 **상대경로 지원 소폭 수정** 필요.

## 너에게
1. (i) vs (ii) 권고? (i)면 audited 스크립트 무변경이라 안전한데, (ii)가 장기적으로 더 깨끗한지?
2. B remap 검증: 추출순서 ↔ 본문 `![Figure N]` 순서 매칭 신뢰성 + 시각검증 프로토콜(샘플 N편, 사람확인) 제안?
3. 본문 md 이미지줄 교체 = corpus 무결성상 OK인가(논문별 .md 백업 + GATE + 시각검증 전제)?

1편 시범(Seton 2012)으로 (i)+B 먼저 보여주고 너 리뷰 받을 계획. 실행은 운영자 GO 후. 지금 $0·read-only.
