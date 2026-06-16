# RECONCILE AUDIT — 전수검토·합치기 계획 (2026-06-16, 압축 생존용)

운영자 지시: 이번 세션 작업 ↔ origin/main 전수 비교. 중복이어도 **코드가 다르니 비교해 좋은 걸 채용**. Claude+Codex 둘 다 확인, 파트 나눠 의견 교환 후 합쳐 PR. **"있는 걸 두 번 고쳐 합치는 게 제일 어려움"** — 신중히.

> **압축/새 세션 복구 앵커**: 이 파일 + `STATUS_claude.md` + `HANDOFF_LEDGER_CONTEXT_20260616.md` + 메모리(`project_ledger_mvp_drift`, `feedback_check_origin_main_before_work`). **철칙: 작업 전 `git fetch origin` + origin/main 분기 확인**(이번 사단 원인 = 39커밋 뒤 stale 베이스).

## 베이스 사실
- origin/main = 공통조상 PR#9 `c488d5f`에서 **39커밋 앞**(리뷰 후속 fix + senpAI 전체 + 0004 + MIGRATION_STATUS.md, 2026-06-10/11 landed).
- 내 작업 브랜치 `claude/corpus-binding-ledger`(= migration 브랜치 위에 쌓임) = origin/main 대비 15앞/39뒤(분기).

## 컴포넌트 매트릭스 (전수)
| # | 컴포넌트 | Claude 버전 | origin/main | 판정 | 검토/빌드 |
|---|---|---|---|---|---|
| 1 | migration apply-state ledger | `APPLY_STATE.json` + `check_apply_state.py`(기계검증: coverage/no-prose/companion/runbook-ref/sha/cp949) | `MIGRATION_STATUS.md`(prose 표, 운영자채택 6/11) | **main 표 유지 + 내 체커 이식**(`check_migration_status.py`) | **Claude 빌드 → Codex 검증** |
| 2 | SQL헤더 de-prose 0001~0003b | de-prose(posture+ledger 포인터) | de-prose(다른 워딩, 5~9줄 변경) | **비교→깔끔/정합 쪽**(MIGRATION_STATUS와 일치) | Claude |
| 3 | runbook §1/§6 (+:189 오타) | de-prose + :189 수정 + 5파일 열거 | 43줄 편집 | **비교→best, :189 수정 확인** | Claude |
| 4 | 0004 content tripwire | 없음 | 있음(247b443) | **main 채용**(비교 불요) | — |
| 5 | **corpus-version binding ledger** | 신규 `CORPUS_BINDING.json`+`check_corpus_binding.py`+tests | **없음** | **내 것 채용**, origin/main 위로 rebase | **Codex 검증 → Claude 빌드** |
| 6 | **67b1 → single-source(논리)** | 하드코딩 제거, binding서 읽기, D1=sha 리터럴 금지 | **아직 `67b1` 하드코딩** | **내 것 채용**(main의 stale 고침). #5와 한 묶음 | Codex 검증 |
| 7 | 037 dense (manifest 6/16·dense_search Windows-safe·smoke) | 완료(G:, Codex 037B=ok) | git 밖(corpus 데이터) | **유지**(standalone) | 완료 |
| 8 | `.mcp.json` geochem-corpus 6/12 | 로컬 핫픽스 | **등록 자체 없음**(0건) | 로컬 유지 or 운영자 결정(머신별) | — |
| 9 | webhook/worker입력/no-hits/caps jsonb/OrchestraJobRow/error_code | drift-map만(미수정) | **수정 완료** | **main 채용** | — |
| 10 | senpAI 서브시스템 | 미터치(.scratch 참조뿐) | **머지 완료(PR#11)** | **main 채용** | — |
| 11 | CORPUS_SSOT.md | 신규(ccc-protocol) | n/a | 유지(기록) | — |

→ **실제 "두 번 고쳐 합치기" 어려운 구간 = #1·2·3(migration 클러스터, 양쪽이 손댐).** #5·6 = 내 것 채용(main 없음, 충돌 X). #4·9·10 = main 채용(완료). #7·8·11 = standalone/local.

## 파트 분업 (CCCP, 서브에이전트 fleet 금지=비용캡)
- **Claude**: #1·2·3 — main `MIGRATION_STATUS.md` 정본 유지하면서 내 체커를 `check_migration_status.py`로 이식(coverage/no-prose/companion/runbook-ref enforced) + de-prose/runbook 워딩 정합. **현재 origin/main 위 새 브랜치.**
- **Codex**: #5·6 — corpus-binding+single-source를 origin/main 위로 rebase 적용 가능한지 검증(draft-spine J2 의존 한 끗 포함) + Claude의 #1·2·3 교차검증.
- **합의 후**: 각자 PR 초안 → 의견 교환 → 운영자 머지 게이트.

## 방법 (철칙)
1. 각자 파트 시작 전 `git fetch origin` + origin/main 대조(또 stale 금지).
2. 충돌/판정은 노트(LEDGER_*)로 교환, 빨리 수렴(핑퐁 금지).
3. corpus 본문/index push 0. manuscript-atelier 머지는 운영자 게이트.
4. 비용캡 $500·크레딧잠금 — 내부 fleet 금지, 2-에이전트로.

## 다음 액션
Codex에 `LEDGER_021`로 분업 제안. 운영자 GO 시 각자 현재 origin/main 위에서 파트 착수.
