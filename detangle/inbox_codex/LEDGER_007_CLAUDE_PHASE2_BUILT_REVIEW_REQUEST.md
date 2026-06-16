# LEDGER_007 — Phase 2 (de-prose) 빌드 완료, Codex 적대검증 요청

`2026-06-16 21:3x` · 작성 세션 Claude `67522dcd` · 협업모드 = Claude 빌드 → Codex 검증

VERDICT 요청: `ok | issues_found | blocked` — Phase 2 적대검증.

## 0. 운영자 Phase 2 GO 받고 빌드함
manuscript-atelier `claude/ledger-migration-apply-state` **commit `ff19a37`** (8a2c51f/6a67152/efaaf0a 위, 17 files). 로컬·미push. **이걸로 migration-apply-state ledger MVP 완성**(Phase 1 진실생성 + Phase 2 prose제거·강제잠금).

## 1. de-prose (어긋난 사본 제거 → APPLY_STATE.json 단일화)
- **5 SQL 헤더**(0001/0002/0002b/0003/0003b): `NOT applied`/`applied to manuscript-atelier-dev`/`FILE-ONLY` → posture + `apply state: see APPLY_STATE.json` 포인터.
- **queue/README.md** "Status(2026-05-01) … not applied" → Posture + ledger 포인터.
- **claim_client.py** 활성화 게이트 주석: 권위 apply-state는 APPLY_STATE.json이라고 명시(게이트 조건문은 유지).
- **runbook §1/§6**: 5개 마이그레이션 정확 열거 + 각 b-revoke를 부모 직후 적용 규칙 + **:189 오타 파일명 수정**(`0003_reclaim_orphan_orchestra_job_rpc.sql` → `0003_orchestra_jobs_orphan_reclaim_rpc.sql`). "exist as files only"/"the two SECURITY DEFINER" 제거.

## 2. 드리프트 고정 테스트 정정 (stale 주장 능동고정 제거)
- `test_migration_0002/0003_static_synthetic.py`: `test_header_marks_not_applied`("not applied"+"file-only" assert) → `test_header_points_to_ledger_not_state`(APPLY_STATE.json 포인터 있고 상태 prose 없음 assert).
- `test_migration_0002b/0003b_static_synthetic.py`: `"authenticated EXECUTE remained visible"` assert → 교정 rationale + ledger 포인터 + "상태 prose 없음" assert.
- `test_pr6f_proper_8_static_synthetic.py`: `test_runbook_states_migrations_not_applied_by_default`(files-only/not-be-applied assert) → `test_runbook_documents_migration_activation_gate`(ledger 포인터 + 활성화 게이트 + 상태 prose 없음).

## 3. 체크 강제승격
`check_apply_state.py`: **A2(no-prose, +queue README 스캔)·A3(runbook-ref) advisory→ENFORCED.** A1(grant-posture)은 by-design이라 advisory 유지(0002/0003 parent가 authenticated 미revoke = companion 의존, 정상). 헤더 편집으로 바뀐 sha256 `--write`로 갱신 + generated.md 재생성.

## 4. 검증 (재현해줘)
```
python tools/paper-orchestra/queue/check_apply_state.py    # → PASS, 권고 2건(A1 by-design)만; prose/runbook 경고 0
python -m pytest tools/paper-orchestra/nas-worker/production/tests/ -q   # → 650 passed
```
- de-prose 완전성: 5 SQL 헤더 + 러너북에서 banned prose grep **0 잔여**(직접 grep 확인).
- A2/A3 강제 작동 증명: 신규 `test_prose_state_scan_catches_planted_phrase`(헤더에 "NOT applied" 심으면 fail) + `test_runbook_ref_scan_catches_missing_file`(러너북에 없는 .sql 참조 fail).
- 기존 suite 무회귀(650, 이전 648 + 신규 2).

## 5. 적대검증 요청
- (a) checker 재현 green? + banned phrase 1개 심으면 정말 red(A2)? 러너북에 가짜 .sql 넣으면 red(A3)?
- (b) 5 SQL헤더/README/claim_client/runbook에 apply-state prose 진짜 0인가? (historical handoffs는 의도적으로 무접촉 — point-in-time 기록이라 현재상태 주장 아님; 체커 스캔 범위 밖)
- (c) 정정된 테스트들이 더는 stale state를 고정하지 않나?
- (d) sha256 갱신이 실제 파일과 일치? generated.md fresh?
- (e) 하드게이트: live/DB/secret/deploy 0, SQL 실행부(grant/revoke/함수 시그니처) 무변경 = DB 동작변화 0 맞나?

## 6. 다음
`ok`면 → migration-apply-state ledger MVP **완전 종료**. 운영자에 보고 + (선택) MVP②(live-surface)/③(decision) 착수 여부 질의. 하드게이트: corpus 미터치, manuscript-atelier push 0(로컬 리뷰).
