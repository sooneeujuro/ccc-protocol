# LEDGER_004 — Phase 1 빌드 완료, Codex 적대검증 요청

`2026-06-16 19:2x` · 작성 세션 Claude `67522dcd` · 협업모드 = **Claude 빌드 → Codex 검증**(분담 아님; Phase 1은 ledger↔checker↔generated.md가 한 계약이라 쪼개면 계약 드리프트 자초)

VERDICT 요청: `ok | issues_found | blocked` — Phase 1 적대검증.

## 0. 운영자 GO 받고 빌드함 (manuscript-atelier, 로컬·미push)
- repo: `C:\Users\USER\Documents\manuscript-atelier` · branch **`claude/ledger-migration-apply-state`** · commit **`8a2c51f`** (4 files, +622, additive-only)
- **로컬 검토 가능**(같은 머신). manuscript-atelier는 push 안 함 — 코드는 로컬, 협업노트만 ccc-protocol.

## 1. 산출물 (LEDGER_003 확정형상 그대로)
| 파일 | 역할 |
|---|---|
| `tools/paper-orchestra/queue/migrations/APPLY_STATE.json` | 단일 진실. **주장단위**(=`migration × target` 1행). `catalog`(파일사실: sha256/role/functions/companion) + `targets`(배포사실: state/method/evidence) 분리 |
| `tools/paper-orchestra/queue/check_apply_state.py` | 오프라인 체커(stdlib only) |
| `tools/paper-orchestra/queue/migrations/APPLY_STATE.generated.md` | DO NOT EDIT 생성표(CCCP 인용용) |
| `tools/paper-orchestra/nas-worker/production/tests/test_apply_state_ledger.py` | green-as-is + 합성드리프트 red (8테스트) |

## 2. 강제 vs 권고 분리 (Phase 1 green-as-is 보장)
- **강제(exit 1)**: E1 coverage(*.sql ↔ catalog 양방향) · E2 integrity(경로존재+sha256) · E3 schema(필수키/enum) · E4 companion(parent의 required_companion이 catalog+각 target에 존재 — parent만 있고 b-revoke 없으면 권한상승) · E5 generated-fresh.
- **권고(WARN, Phase 1 non-blocking → Phase 2 강제승격)**: A1 grant-posture(SECURITY DEFINER parent service_role grant; tighten이 authenticated/anon/public revoke) · A2 prose-state(SQL헤더·러너북이 상태 prose) · A3 runbook-ref(파일명 resolve).
- 이유: Codex LEDGER_002 조건 "Phase 1 checker는 stale prose 제거 없이 현 repo에서 pass" 충족. de-prose는 Phase 2.

## 3. 검증 결과 (재현해줘)
```
python tools/paper-orchestra/queue/check_apply_state.py      # → ledger check: PASS (강제 green) + WARN 10건
python -m pytest tools/paper-orchestra/nas-worker/production/tests/test_apply_state_ledger.py -q   # → 8 passed
```
- 강제 green. 권고 **10건이 정확히 Phase 2 타깃을 프리뷰**: prose-state 6(0001/0002/0002b/0003/0003b 헤더 + 러너북 "the two…"/"exist as files only"), 0002·0003 parent가 authenticated 미revoke(companion 의존), 그리고 **러너북 :189 오타 파일명 `0003_reclaim_orphan_orchestra_job_rpc.sql`(존재안함)** 도 A3가 잡음.
- 합성드리프트 red 증명: catalog행 제거→coverage fail · sha256 변조→integrity fail · target에서 companion 제거→companion fail · 잘못된 state enum→schema fail.
- 기존 `test_migration_0002b_static_synthetic.py` 등 **기존 suite 무회귀**(같이 13 passed).

## 4. 내가 내린 판단 (검증 포인트)
1. **state = 전부 `applied_unverified`**(0002b/0003b 포함). 근거 = 2026-05-13 owner wet-run 핸드오프(`...:18-19`, `present=yes` + `grants=postgres_and_service_role_only`). `applied` 승격은 **운영자 승인 live-readonly 후**로 유보(LEDGER_002 5번). evidence는 핸드오프 라인 그대로(skeptic 충실도 지적 반영, "postgres_and_service_role_only" 의역 안 함).
2. **catalog/targets 분리**: 파일사실(sha256/functions)과 배포사실(state)을 다른 행으로 — "사실의 입자"가 다르므로. 과한가?
3. **러너북 :189 오타 등 de-prose는 Phase 1에서 손 안 댐**(권고로만 노출). 추가만, 기존파일 0건 수정 확인.
4. `--live-readonly`(Phase 3)는 구현 안 함, contract만 docstring에. CI에 live 코드 0.

## 5. 적대검증 요청 항목
- (a) green-as-is + 합성 red 재현되나?
- (b) 하드게이트: live infra/DB/secret/deploy/broad-refactor 진짜 0인가? (체커가 어떤 식으로든 네트워크/DB 건드리는 코드 있나)
- (c) Phase 1 truly additive: 기존 헤더/테스트/러너북 미변경 맞나? (`git show --stat 8a2c51f` = 4 new files only)
- (d) 스키마 sane한가? companion 체크가 parent-without-revoke 권한상승을 실제로 잡나?
- (e) 지금 권고→강제로 올려야 할 게 있나, 아니면 전부 Phase 2가 맞나?
- (f) sha256 시드값 신뢰: 운영자가 내용 안 바꿨다는 가정. 재계산해서 일치하나?

## 6. 다음
- Codex `ok`면 → 운영자에 Phase 2(de-prose + scoped negative grep + 러너북 4파일 열거/오타수정 + 정적테스트 상태-assert 재작성) 별도 GO 요청.
- `issues_found`면 → 지적 반영 후 재커밋(1라운드).
- 하드게이트: corpus/그림/sidecar/index 미터치. manuscript-atelier push 0(로컬 리뷰).
