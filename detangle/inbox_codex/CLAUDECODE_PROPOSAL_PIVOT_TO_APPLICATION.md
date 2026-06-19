# CLAUDECODE_PROPOSAL_PIVOT_TO_APPLICATION

ORIGIN: **운영자(사용자) 지시로 작성** — Claude(독립 리뷰어) 제안. 운영자가 Codex에 전달.
STATUS: proposal / redirect (VERDICT 불요, 방향 제안)

## 배경 (왜 이 제안)
- 검증아크 닫힘 + CIR subsection 4단락 PASS = **장비 작동 증명됨**.
- 최근 스윕(259→309+: SHA256 / manifest-ID / timestamp / path / leaf-filename / hex 포맷 하드닝)은 **단일운영자·로컬·신뢰 파이프**에선 막는 위협 확률이 낮아 효용 체감 다이미니싱. (운영자가 "자동으로 할만한 거 하고 있어라" 지시 → 하드닝 스프리로 흐른 것으로 추정.)
- 권장: **무결성-플러밍 → application(실제 글)으로 피벗.** 얇은 baseline 무결성(손상 response 조용히 안 쓰기)만 유지.

## 제안 작업 (우선순위)
- **P1. CIR p3 polish** — 내가 최약 단락으로 찍은 곳. protected token 복원 + altitude 캘리브레이션(timid도 overbroad도 아니게). → 끝나면 B/M/T+Conductor 재-run, 내가 재채점.
- **P2. 705/817 biology explicit bounding** — biology 배제가 현재 implicit. **implicit→explicit bounding**으로 보강(abiotic-compatible가 biological보다 명시적으로 더 consistent하다는 결을 두 갈래로). → 내가 재검토.
- **P3. repair 루프 실전 1회** — near-bound 후보에 length repair + semantic review를 **실제로 run** → accepted repair(원본+수정본 쌍) 산출. → 내가 altitude drift **의미 재채점**(repair 인프라 첫 실전 검증). 인프라를 더 하드닝하는 것보다 **한 번 돌려서 검증**이 효용 큼.
- **P4. 다음 claim unit / 다음 subsection / 다음 섹션** (CIR Discussion 확장 또는 다음 섹션 착수).

## 착륙 형식 (내 독립채점 가능하게)
- run은 **JSON**으로 (paragraph_md를 raw_decode 가능하게) + **LEDGER**로 announce.
- repair는 **원본/수정본 둘 다** (drift 비교용).
- claim unit은 column/summary 패킷 + B/M/T/Conductor run.

## 멈춰도 되는 것
- 포맷/해시/ID/timestamp **추가** 하드닝 스윕(baseline 초과분). 재사용 **제품화**가 확정 목표가 되면 그때 재개 — 단 **application 효용 더 증명 후**가 순서.

## 게이트
- 본 노트: 제안/우선순위만 · 논문 resolved값/prose/캡션 0 · MA 커밋 0 · ccc file-specific add.
