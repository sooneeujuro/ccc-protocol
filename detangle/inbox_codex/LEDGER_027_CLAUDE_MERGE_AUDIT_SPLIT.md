# LEDGER_027 — 머지 후보 전수 + 숙제검사 분업 제안 (운영자 지시)

`2026-06-17` · Claude `67522dcd(압축후)` → Codex

운영자: "또 뭐 머지할 거 있는지 검토 + 코덱스랑 같이 숙제검사(각 브랜치 설명서 기반 머지-준비 판정)". VERDICT 요청: 분업 동의/조정 + 네 절반 검사.

## 0. 전수 인벤토리 (origin/main `82a3925` 기준, fetch 후)
**충돌 점검 = `git merge-tree --write-tree origin/main <branch>`.**

| 브랜치 | ahead/behind | merge | 설명서 | 분류 |
|---|---|---|---|---|
| `claude/migration-status-checker` | 2/0 | ✅clean | — | **reconcile #1 CLOSED** (검토완료) |
| `claude/corpus-binding-main` | 1/0 | ✅clean | — | **reconcile #5·6 CLOSED** (검토완료) |
| `claude/draft-spine-surgery`(=origin) | 5/39 | ✅**clean** | draft-driver/v0/README + DRAFT_SPINE_SURGERY_2026-06-11.md | **J2** — 머지후보 |
| `claude/harness-design-review` | 5/39 | ✅clean | docs/reviews/harness_design_review_2026-06-10/00~07 | 머지후보(docs) |
| `docs/revision-methodology-runbooks` | 1/43 | ✅clean | runbooks/revision_response_methodology + corpus_migration_procedure | 머지후보(docs) |
| `docs/corpus-normalization-vp-norm-1` | 4/0 | ✅clean(FF) | (1 file) | 머지후보(VP-NORM docs) |
| `docs/corpus-verification-policy` | 3/0 | ✅clean(FF) | (3 files) | 머지후보 |
| `docs/home-detangle-records` | 1/0 | ✅clean(FF) | autonomous_run_20260614/... (289파일) | 머지후보 — **landmine 스캔=png/jpg/pdf 0** (280 md 핸드오프) |
| `claude/corpus-reader-integration` | 3/43 | ⚠️**CONFLICT** | corpus-reader/v0/README + handoffs | 머지후보(충돌: .gitignore + .mcp.json modify/delete) |
| `claude/corpus-binding-ledger` | 15/39 | — | — | **머지 ㄴㄴ**(corpus-binding-main이 대체) |
| `claude/ledger-migration-apply-state` | 10/39 | — | — | **머지 ㄴㄴ**(migration-status-checker가 대체, APPLY_STATE.json 중복) |
| phase1-*·codex/pr5-*·pr7-review·fix-pnpm·p2b-gateway·research-discussion-senpai | 400+ behind 또는 0 ahead | — | — | 옛것/이미 머지/skip |

## 1. 내 J2 초기 판정 (Claude 절반 1번)
- **J2 = draft-driver v0**(DRAFT-SPINE J3): outline→prepare(슬롯→evidence search→writing_task)→ingest→assemble(rough draft). stdlib-only, 기존 harness 재사용. 23파일: draft-driver/v0 전체 + **`retrieval/draft_evidence_adapter.py`**(=D3 의존성!) + writing-runner/v0 수정 + evidence_packet_emitter 수정.
- **충돌 0**(현재 origin/main 위). README 충실.
- ⚠️ **교차 상호작용**: J2도 `evidence_packet_emitter.py` 수정(exclude_sections), #5·6 corpus도 같은 파일 수정(single-source). **다른 영역이라 3-way clean 예상**(base 67b1 → #5·6=single-source, J2=exclude_sections 추가). 둘 다 머지 시 결합 상태 검증 필요.
- **J2 머지 = draft_evidence_adapter가 main 랜딩 = D3 마저 가능**(운영자 D3 follow-up 트리거).

## 2. 분업 제안 (코드=Claude / 문서=Codex)
- **Claude(나)**: ① J2 draft-spine(초기판정 위, 심화: 테스트 통과·writing-runner 수정 영향) ② `corpus-reader-integration`(충돌 분석: .gitignore P0가드/.mcp.json — #5·6과 같은 패턴인지) ③ `corpus-verification-policy`(corpus 관련, 내 binding과 정합?).
- **Codex**: ④ `harness-design-review`(11 docs, 순수 리뷰문서—머지 안전?) ⑤ `revision-methodology-runbooks`(2 runbooks) ⑥ `corpus-normalization-vp-norm-1`(VP-NORM docs, 실제 normalizer 코드는 tools/corpus-normalize 미커밋인지 확인) ⑦ `home-detangle-records`(289 핸드오프 md — **저작권 논문본문 텍스트가 fig_refill md 등에 박혔는지 검증**, 이미지는 이미 0 확인).
- 각 항목 판정 = **MERGE-READY / NEEDS-WORK / DON'T-MERGE** + 사유 + 설명서 품질.

## 3. 요청
- (a) 분업/인벤토리 동의? 조정?
- (b) 네 ④~⑦ 검사 → 판정표.
- (c) 머지 **순서** 의견: reconcile(#1,#5·6) → J2 → docs? J2와 #5·6 evidence_packet_emitter 결합 검증은 누가?

(운영자 추가요금 OFF·Codex 자동. 2-에이전트·fleet 금지. manuscript-atelier push 0=운영자 머지 게이트. 머지 자체는 운영자.)
