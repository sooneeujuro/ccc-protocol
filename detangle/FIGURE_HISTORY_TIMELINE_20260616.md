# 그림(figure) 꼬임·suppress·복구 — 전체 이력 복원 (2026-06-16 13:4x)

작성: Claude(회사PC, a745303e). 4갈래 병렬 read-only 조사 교차검증. 비용=토큰만, 파일 수정 0.

## 한 줄
**꼬임 → 안 풀리는 거 allowlist로 "안 띄우게" 막음 → 그 다음 집/datalab에서 대량 복구(추가 조치 O) → 그래도 못 살린 604개(51편)가 남음 → 오늘 PDF로 50/51 회수.** 파괴적 조치 없었음(전부 additive/reversible).

## "안 띄우게 한" 메커니즘 = 2겹
1. **allowlist + gate**: `FIGURES_MISSING_ALLOWLIST.txt`에 이름 올린 이미지는 "알려진 공백"으로 처리 → `fig_render_audit.py` GATE가 FAIL 안 하고 PASS. (파일에서 안 지움. 그냥 "없어도 통과"로 등록.)
2. **reader caption-fallback**: `read_paper.py`가 이미지 파일이 실제로 없으면 깨진 `<img>` 대신 `*[Figure: 설명]*` 캡션 텍스트로 대체. (+ JS onerror로 로드 실패도 캡션 처리.) → 깨진 그림 아이콘 절대 안 뜸.

## 타임라인
- **06-10 (꼬임 발단)**: corpus 갱신 때 신규 ~867편 그림 jpg가 export에서 누락. 20260612 번들 패키징이 안 챙김. (이게 근본 원인.)
- **06-10 17:10**: reader가 누락 그림을 캡션으로 대체하도록 패치(깨짐 방지). gate(`fig_render_audit.py`) 도입.
- **06-13 04:5x (집PC 진단)**: region-hash 충돌 발견 → "tail 매칭 금지(남의 그림 박힘)" 규칙. fill 스크립트=exact full-name only.
- **06-13 05:22 (집PC, 추가조치 ①)**: 집 NAS에서 **7,856개** 그림 pre-fill(ADDENDUM). allowlist를 잔여 ~2,027개(163편)로 조임. (조이기 전 백업 .bak은 USB에만, G:엔 없음.)
- **06-13 06:01**: 현재 `FIGURES_MISSING_ALLOWLIST.txt` = **2,028줄** 확정.
- **06-13 (quarantine)**: 06-13 refill의 raw 출력(out_raw=region-hash 트리)은 병합 안 하고 **격리**(corpus_quarantine, MOVE·무손실).
- **06-15 (별개)**: 다른 머신 corpus_fixes_20260615 = **사이드카/논문섞임 복구**지 그림 아님. 라이브 인덱스 무변경.
- **06-16 00:58 (회사PC, 추가조치 ②)**: renewal 출력(`_renewal_20260609\{nuc,cha,kim}_out`)에서 **1,424개** 추가 fill(LEDGER). GATE PASS(allowlisted-missing 604, hard-missing 0).
- **06-16 09:09 (회사PC)**: datalab\pilot 상대 fill = **0 매칭**(충돌로 안전 바인딩 불가) → source-blocked 확정.
- **06-16 10:57**: 1차 PDF fuzzy 대조 = **오매칭 발생 → 폐기**(저자명 부분일치 버그).
- **06-16 13:0x~13:25 (오늘, 추가조치 ③)**: `G:\RefDB`(PDF 1,179) 엄격 재매칭 → **50/51 PDF 회수**. Busigny 2005(1장)만 미발견.

## ⚠️ 형이 알아야 할 핵심 (왜 헷갈리나)
- allowlist 파일엔 아직 **2,028개**가 적혀 있지만, 그 중 **1,424개는 이미 채워져서 실제로 뜸**. **진짜 안 뜨는 건 604개뿐.**
- 즉 allowlist가 **실제 공백(604)을 2.4배 과대표시** 중. 채운 항목을 안 지웠음(prune 안 함). `FIGURES_GAP_20260613.md`가 "채운 건 빼서 재조임하라"고 적어놨는데 그 정리는 미실행.
- → "안 풀린 게 많아 보이는" 착시의 일부는 이 **stale allowlist** 때문. 실제 미해결 = 604개/51편(그리고 그 중 50편은 오늘 PDF 확보).

## 남은 일 (둘 다 운영자 GO)
1. **allowlist 정리**: 2,028 → 실제 604로 재생성(채운 1,424 제거). 비파괴, 번들 메타만 갱신.
2. **PDF 재추출**: 50편 PDF → 그림 추출(per-paper, 충돌無) → 시각검증 → GATE. 변환 비용 발생.
- 영구공백: Busigny 2005(1장, PDF 오늘 LostnFound에 추가됨→재확인 필요) + classic 4편은 PDF 확보됨(영구 아니었음).
