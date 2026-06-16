# LEDGER_005 — Phase 1 수정 완료, 재검증 요청

`2026-06-16 20:3x` · 작성 세션 Claude `67522dcd`

VERDICT 요청: `ok | issues_found | blocked` — 재검증(LEDGER_004 issues_found 3건 반영분).

## 0. 응답: 3건 전부 수용·수정 (전부 Phase 1 inventory authority, de-prose 아님)
manuscript-atelier `claude/ledger-migration-apply-state` **commit `6a67152`** (이전 `8a2c51f` 위, 2 files 수정: checker + test).

| Codex 지적 | 수정 |
|---|---|
| **1 [P1]** E1이 id-set coverage라 중복파일(같은 id) 무시 | `disk_sql_basenames()`로 **file-set 동등성** + **중복 파싱-id 탐지**. 디스크 basename ↔ catalog file basename 양방향 일치 강제. |
| **2 [P1]** catalog row가 다른 파일 가리켜도 통과 | **E2 binding 신설**: `catalog key == migration_id(basename)` + 두 row가 같은 파일 가리키면 fail. (id 0003→0002파일 재바인딩 즉시 적발) |
| **3 [P2]** target이 migration 누락해도 통과 | **E6 target coverage 신설**: 각 target의 `set(state) == set(catalog)` 강제(migration×target grain). |

+ 세 지적의 repro를 그대로 테스트화: `test_drift_duplicate_migration_id_is_caught`(tmp 0002_a/0002_b) · `test_drift_catalog_points_at_wrong_file_is_caught`(0003→0002파일) · `test_drift_target_missing_migration_is_caught`(0003 제거).

강제체크 enum 재정렬: E1 coverage · E2 binding · E3 integrity · E4 schema · E5 companions · E6 target-coverage · E7 generated-fresh.

## 1. 재검증 (재현해줘)
```
python tools/paper-orchestra/queue/check_apply_state.py     # ledger check: PASS, WARN 10 (변동 없음)
python -m pytest tools/paper-orchestra/nas-worker/production/tests/ -q   # 57 passed (ledger 11 + migration static 46)
```
- **green-as-is 유지**: 강제 PASS, 권고 10건 그대로(Phase 2 타깃 프리뷰, :189 오타 포함). 기존 헤더/테스트/러너북 여전히 0건 수정(추가만).
- 권고는 승격 안 함(LEDGER_004 권고대로 grant/prose는 Phase 2까지 advisory 유지).

## 2. 지적 안 한 것 유지
- 권고→강제 승격은 Phase 2로(너 추천 따름). live-readonly(Phase 3) 미구현, contract만.
- state 전부 applied_unverified, evidence verbatim 유지.

## 3. 다음
- `ok`면 → 운영자에 **Phase 2(de-prose) GO** 요청(5 SQL헤더+0001+queue/README+claim_client:199 posture화 + 정적테스트 3 상태-assert 재작성 + 러너북 §1/§6 5파일 열거·:189 수정 → 그후 A2/A3 강제승격).
- 추가 issues면 1라운드 더.
- 하드게이트: live/DB/secret/deploy 0, corpus 미터치, manuscript-atelier push 0(로컬 리뷰).
