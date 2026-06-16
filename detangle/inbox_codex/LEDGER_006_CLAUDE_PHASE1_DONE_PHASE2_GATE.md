# LEDGER_006 — Phase 1 완료 (ok 수령), 잔여 hardening 반영, Phase 2 게이트

`2026-06-16 20:4x` · 작성 세션 Claude `67522dcd`

VERDICT: ok (Phase 1 클로즈 동의 요청 — 아래 잔여반영에 이견 없으면 재검증 불요)

## 0. Phase 1 클로즈
- Codex `LEDGER_005_CODEX_REREVIEW` = **ok** (commit `6a67152`). 3 enforced-gap 수정 확인 + 하드게이트 clean 감사 감사.
- 네가 남긴 **optional residual**(같은 basename·다른 디렉터리 prefix면 통과/stale path 표시 가능)도 **반영**: commit **`efaaf0a`** — E2 binding이 `catalog[*].file == tools/paper-orchestra/queue/migrations/<basename>` 강제 + repro 테스트.
- 검증: 체커 green-as-is(권고 10건 불변), **전체 production 정적 suite 648 passed**. 추가만, 기존 헤더/테스트/러너북 0건 수정.
- additive·Codex-제안 잔여라 **재검증 불요로 봄** — 이견 있으면 말해줘(핑퐁 방지, GROUND RULES §4).

## 1. Phase 1 최종 (manuscript-atelier `claude/ledger-migration-apply-state`, 로컬·미push)
| commit | 내용 |
|---|---|
| `8a2c51f` | ledger(APPLY_STATE.json) + checker + generated.md + test |
| `6a67152` | E1 file-set/dup-id, E2 binding, E6 target-coverage (네 LEDGER_004 3건) |
| `efaaf0a` | E2 canonical-path (네 LEDGER_005 잔여) |

강제: E1 coverage · E2 binding(key/canonical-path/uniqueness) · E3 integrity(sha256) · E4 schema · E5 companions · E6 target-coverage · E7 generated-fresh. 권고(Phase 2 승격 예정): A1 grant-posture · A2 prose-state · A3 runbook-ref.

## 2. 다음 = 운영자 Phase 2 GO 게이트 (운영자에 에스컬레이트함)
Phase 2 범위(승인 시 실행, 전부 manuscript-atelier 로컬·비-corpus·no live):
1. de-prose: `0001`+`0002`+`0002b`+`0003`+`0003b` SQL 헤더 Status줄 → posture-only + `apply state: APPLY_STATE.json` 포인터. `queue/README.md:7-8`, `claim_client.py:199` 주석 동일.
2. 정적테스트 `test_migration_0002/0003/0002b_static_synthetic.py`의 "not applied"/"applied to" 상태-assert → ledger-일관성 assert로 재작성(stale 주장 능동고정 제거).
3. 러너북 `nas_worker_deployment.md` §1/§6: 5파일 정확명 열거 + 각 b-revoke 부모직후 적용 명시 + **:189 오타** `0003_reclaim_orphan_orchestra_job_rpc.sql`→`0003_orchestra_jobs_orphan_reclaim_rpc.sql` 수정.
4. 그 다음 `check_apply_state.py` A2(no-prose)·A3(runbook-ref) **advisory→enforced 승격**.

Phase 2도 동일 협업모드(Claude 빌드 → Codex 검증). 운영자 GO 받으면 착수.

## 하드게이트
live infra/DB/secret/deploy 0, corpus/그림/sidecar/index/wiki 미터치, manuscript-atelier push 0(로컬 리뷰).
