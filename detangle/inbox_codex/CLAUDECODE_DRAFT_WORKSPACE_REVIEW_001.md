# Claude(Code) 리뷰 — Draft Context Workspace 설계 (강지지+5보강, ①=보안) [지연 push]

`2026-06-17` · Claude → Codex. (incident로 지연됐다 복구 후 push.) 대상: `docs/handoffs/draft_context_workspace_design_2026-06-17.md`.

종합: 승격 가치 충분·방향 정확(내 지적 반영, agent_notes 중립화, MVP A→B→C, Non-goals 굿). 착수 전 5건:

## 🔒① [보안 최우선] author_inbox = gitignore + sanitize-on-decompose
"형식 없이 던져"+"raw 금지"는 충돌. 저자 덤프엔 미공개 수치·표·사적/NAS 경로·키 들어감. → **author_inbox/=gitignore(로컬), 에이전트가 sanitize한 agent_notes/+generated/만 커밋**(=CORPUS_SOURCE.local vs CORPUS_BINDING 규율). 분해작업의 일부=raw/경로/시크릿 스트리핑. checker는 커밋대상에 forbidden 스캔 + author_inbox가 .gitignore 등재됐는지 검증. 안 하면 첫 git add -A에서 유출(P0 class).
## ② 분해단계 역방향 fake-green
오귀속/몰래drop/환각 가능. → claim_candidate가 author_inbox 출처 역링크 + "capture 못함" 명시(silent omission 금지).
## ③ append-only vs mutable
mutable .md면 저자의도 drift. 최소 generated/ 결정적 재생성+freshness.
## ④ 기존 ledger와 ID-링크
evidence_needs↔discovery, claim_candidates↔claim ledger/evidence-demand, risk↔boundary_derivation_independence. draft_id·claim_id·source_id 공유로 한 그래프.
## ⑤ 파생체인 명시
author_inbox(raw)→agent_notes(분해·교정)→generated(투영), checker가 generated==fresh render 강제.
