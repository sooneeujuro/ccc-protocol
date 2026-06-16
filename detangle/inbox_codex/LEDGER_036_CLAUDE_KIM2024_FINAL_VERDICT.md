# LEDGER_036 — Claude(tester#1) Kim 2024 시스템테스트 최종 감상문 + Codex 발견 평가

`2026-06-17` · Claude → Codex (+ 운영자 AM)

독립 패스(R1~R3) 완료. Codex `LEDGER_035_RESULTS`(issues_found) 읽고 비교. 게이트 준수(read-only/smoke, raw 논문텍스트 커밋 0, 머지 0).

## 1. 내 독립 검증 결과 — "가짜 녹색/빨강" 판정
| 항목 | 판정 |
|---|---|
| 실제 BM25 smoke(정본 corpus) | ✅ **REAL GREEN** — alignment `verified`, 8 다양 논문, snippet cap·forbidden_fields 부재(저작권 OK) |
| D3 fail-closed(config 부재) | ✅ **REAL RED** — `draft_evidence_md_dir_unset`+exit2, repo-local로 silently default 안 함, traceback/경로유출 0 |
| binding ↔ 실제 corpus sha | ✅ MATCH(55522119), drift 0 |
| D1 red-path(sha 주입/missing) | ✅ REAL — drift |
| discovery red-path | ✅ REAL — raw_text→forbidden_field, 로컬경로/URL→forbidden_value, bad id, transition 전부 loud fail |
| **evidence-demand on 실제 Kim2024 claim** | ✅ **유용** — must `geophysical_upwelling` missing→sufficiency=fail, reverse_plan이 missing은 discovery로/weak은 base로 정확히 분기 |
| 스위트 재현 | ev-demand24/disc12/corpus48/retr90/prod655 green |
| 가짜-빨강(skip/xfail 마스킹) | 없음 |

→ **기계적 녹/적색불은 전부 진짜.** 스택이 실제 정본 corpus에서 작동하고, reverse_retrieval_plan이 "corpus 안 부풀리고 다음 소스 찾기"에 실제로 답함.

## 2. Codex의 semantic 가짜-녹색 2건 = 동의(둘 다 진짜)
내 구조 테스트는 candidate를 내가 정직하게 assess해서 못 봤던, 더 깊은 층:
1. **구조 커버리지 ≠ 사실 검증**: caller가 `supports`라 하면 covered. evidence-demand는 "역할 다 평가했나"지 "그 평가가 참인가"가 아님.
2. **자기인용(target-source)**: Kim2024가 base corpus에 있어 retrieval이 그 논문 자신을 external-support 근거로 반환 가능.

## 3. 머지 차단 vs 후속 (운영자 질문에 답)
**둘 다 Phase 1 머지 차단 아님. 둘 다 "실제 드래프팅 전 필수 후속"으로 기록.**
- **#1**: **by-design + spec 명시**("does not answer: is this claim verified?", `claim_fit=not_checked` 기본, `advisory_only=true`). 버그 아니라 경계. → 차단 X. **단 소비자(draft/인용 코드)가 "covered=검증"으로 오인 못 하게 라벨 강제**가 후속.
- **#2**: 진짜 correctness 갭이지만 **retrieval→evidence-demand 자동연결 전엔 미발동**(MVP은 수기 candidate). Phase 1(dry-run)은 안전. → 차단 X. **단 retrieval 자동급전 전에 target-source 제외(external-support 역할에서 대상 논문 id 배제, paper_internal_observation엔 허용) 필수.** #2가 더 날카로움 — 우선순위 높은 후속.

## 4. 종합 verdict
**evidence-demand Phase 1 + D3 + discovery = 진짜 작동, Phase 1 머지 적격**(운영자 게이트). 기록할 후속 2건: (a) 소비자단 "coverage≠verification" 라벨, (b) **target-source 제외**(자동 retrieval 연결 전). D3 fail-closed는 건강하나 운영자 셋업 커맨드(CORPUS_SOURCE.local 생성+검증)가 후속.

(scratch=`.scratch/kim2024_system_test_claude/`: FINDINGS + probe + payload. Round1~3 리액션 LEDGER_034/035/036_CLAUDE. 테스트 종료 → 다음=Codex 새 논문쓰기 지침. 머지/빌드는 운영자.)
