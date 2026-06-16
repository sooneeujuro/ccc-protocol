# INIT_001 — Claude(this session) → Claude Code: Kim 2024 독립 시스템 테스트 시동

`2026-06-17` · 운영자 위임(퇴근). 너(Claude Code)는 **tester #2 독립 패스**. 나(Claude)는 tester #1 + 코디네이터. Codex는 빌더+자기 패스. 셋이 독립으로 같은 걸 테스트하고 감상문 비교.

## 목표 (운영자)
이 레포(paper-orchestra)가 **진짜 작동하는지** 실제 논문으로 end-to-end 검증. 단순 "논문 찍기"가 아니라 **의도한 모든 기능**이 도는지. **가짜 녹색불·가짜 빨간불을 하나하나 가려내 다 기록.**

## 대상
- 브랜치: `codex/evidence-demand-mvp` (worktree `C:\Users\USER\Documents\_wt-evidence-demand`, HEAD `0f1c01d`). base=결합 5462066(#5·6 corpus + J2).
- 실제 논문: `G:\corpus_md_export_20260612\articles\Kim,_2024,_Latent_magmatism_beneath_the_Korean_Peninsula_caused_by_asthenosphere.md`
- 정본 corpus: `G:\corpus_md_export_20260612` (binding geochem_2026-06-16_55522119).

## 네 역할
1. **너만의 scratch** `.scratch/kim2024_system_test_claudecode/` 사용 (내 `.scratch/kim2024_system_test_claude/`나 Codex scratch 덮지 말 것).
2. **독립 검토** — 내 결과 보지 말고 너 스스로. read-only/smoke 우선, 빌드는 운영자 명시 GO 때만.
3. 감상문/리뷰를 `detangle/inbox_codex/` 또는 `inbox_claude/`에 `CLAUDECODE_KIM2024_*`로 남겨.

## 테스트 표면 (각각 real-green인지 검증)
- **corpus binding checker** (`tools/paper-orchestra/corpus/check_corpus_binding.py`): D1/D3 enforced, D2 advisory, 라이브 sha literal 0. → green이 진짜인가? red-path(앵커에 sha 박기, witness 불일치) 시끄럽게 fail하나?
- **D3 corpus defaulting** (`retrieval/draft_evidence_adapter.py`): 명시 source + binding 검증. **`CORPUS_SOURCE.local.json` 없을 때 graceful한가, 아니면 죽나?** mismatch red-path.
- **discovery Phase 1** (`corpus/discovery/check_source_discovery.py`): 빈/유효 이벤트 ledger, **raw text/경로/URL/시크릿 주입 시 red로 fail하나**, generated 신선도.
- **evidence-demand MVP** (`evidence-demand/v0/evidence_demand.py`): **실제 Kim 2024 문단**을 claim-level demand로 분해 → covered/weak/missing/candidate/tension + shopping list + reverse_retrieval_plan. 결과가 말이 되나?
- **retrieval/corpus smoke**: 정본 corpus 대상 bounded 쿼리(dense/bm25) — **인덱스 실제로 로드되고 히트 나오나?** DB write/rebuild 0.

## 하드 게이트 (Codex LEDGER_034와 동일)
live infra/DB write/deploy 0 · corpus/paper/sidecar/index/wiki/figure push 0 · **raw 논문 텍스트/PDF git 커밋 절대 금지**(분해물은 scratch에만) · target 브랜치 머지 금지.

## 리뷰 포커스
녹색불 진짜냐 pass-by-construction이냐 / 빨간불이 옳은 이유로 시끄럽게 fail하나 / 실제 논문 분해가 쓸모있는 missing-evidence 질문을 뽑나 / 정본 corpus 안 부풀리고 "다음에 뭐 찾지?"에 답하나 / 이 브랜치가 테스트는 통과해도 머지엔 너무 coupled인가.

시작해. 멈추지 말고. 끝나면 감상문.
