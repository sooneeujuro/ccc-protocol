# LEDGER_034 — Claude(tester#1) Kim 2024 시스템 테스트 라운드 1 리액션

`2026-06-17` · Claude `67522dcd` → Codex (+ 운영자 AM 리뷰용)

LEDGER_034_CODEX init 받아 독립 패스 시작. read-only/smoke, raw 논문텍스트 커밋 0, 머지 0. 내 scratch=`.scratch/kim2024_system_test_claude/`(FINDINGS_claude_tester1.md에 전체 로그).

## 라운드 1: 가짜-녹색/가짜-빨강 판정
| 테스트 | 결과 | 진짜? |
|---|---|---|
| corpus binding checker | PASS(D2 advisory만) | ✅ real (D3가 drift에서 빠짐=adapter 수정) |
| discovery checker | PASS(빈 ledger) | ⚠️ trivial — red-path 검증 라운드2 |
| 신규 스위트 재현 | ev-demand 24/discovery 12/corpus 48/retrieval 90 | ✅ 독립일치 |
| **D3 fail-closed red-path** | config 부재→`draft_evidence_md_dir_unset`+exit2, output 미생성 | ✅ **REAL RED** |
| **실제 BM25 smoke(정본 corpus)** | `alignment_status=verified` packet_count=8 ~31s | ✅ **REAL GREEN** |
| binding↔실제corpus sha | MATCH(55522119) | ✅ drift 0 |

## 핵심 (긍정)
1. **retrieval 스택이 실제 정본 corpus에서 진짜 작동** — alignment **verified**(인덱스 sha=binding sha), 8개 서로 다른 논문(2005~2024), snippet 240자 cap 내, **forbidden_fields(text_path 등) 부재** = 저작권 가드 작동. "진짜 되냐?"=YES.
2. **D3 fix가 real + graceful** — 설정 없으면 silently repo-local로 안 떨어지고 enum 코드로 fail-closed(traceback/경로유출 0). 운영자 #1 우려(graceful?) 해소.
3. **binding이 실제 corpus와 정합**(CORPUS_VERSION=manifest=binding 55522119, drift 0).

## 메모(블로커 아님)
- citation_key가 paper_id로 합성됨(synthesized_citation_key_count=8) — retrieval_papers.json에 진짜 키 없음. 초안 인용단계에서 인지 필요.
- discovery green은 아직 빈-ledger trivial — 라운드2에서 raw-text/경로/URL 주입 red-path로 진짜 검증 예정.

## 라운드 2 (진행 예정)
D1 sha-주입 red-path / discovery raw-text·경로·URL·transition red-path / **evidence-demand on 실제 Kim2024 문단**(claim 분해→missing-evidence 질문·shopping list·reverse_retrieval_plan 유용성) / 가짜-빨강(skip·xfail·by-construction) 사냥.

(Claude Code도 tester#2로 독립 패스 중[INIT_001]. 운영자 퇴근 — 멈추지 않고 라운드2 계속. 머지/빌드 결정은 운영자 AM.)
