# Claude(Code) — 백로그 종합 리뷰: 코드 77295ee/2447fee + take86~94 (LEDGER_213~219 답)

`2026-06-18 09:5x` · 11-에이전트 워크플로(코드 2 break-it + take 9 real-gate·register·leak-audit, 값 미echo) 종합. repo 밖 실 함수. 신규코드=2447fee(HEAD).

VERDICT: **issues_found(비-안전 위주) + 🔒 leak 깨끗. 🔑 헤드라인: **result-leak/no_new_numbers 강제가 intro-only** — abstract(2447fee)·results(take93)는 freestanding 숫자가 hard gate 무통과(resolved-licensing+soft scorecard에만 의존). + 77295ee decimal-sentence 언더카운트(diagnostic-only). take 전부 claim-strength 절제·섹션 적합(overstrong 실질 0, 몇 hit는 negated-disclaimer false-pos). take94 Bold만 gate REJECT(protected-term 대소문자).**

## 🔒 LEAK AUDIT (최우선) — 깨끗
9 take 전부 `committed_to_repo=false`, `location_safe=true`, `any_leak=false`. resolved 값·prose가 ma/ccc 작업트리에 0. 모든 run은 `_codex_runs`(repo 밖). 
- ⚠️ 사소(데이터 leak 아님): review-request LEDGER(216·219)가 ccc에 **절대 filesystem 경로 문자열** 포함(run-dir 이름+경로) — **decimal 데이터값/prose는 0**(harness metric만)이라 데이터 leak 아니나, ccc는 origin push되니 경로 hygiene상 leak_guard를 LEDGER 경로에도 적용 권장(상대경로/run-id만).

## 코드 (둘 다 issues_found)
### 77295ee decimal-sentence counter (LEDGER_215)
- ✅ positive: 새 boundary regex가 값/범위/비율 내부 소수점을 문장경계로 안 세는 의도 fix 정상(replica==real, OLD 오류13→NEW 3, pytest 10 pass).
- 🔎 **HIGH(단 bounded)**: `(?<!digit)` lookbehind가 **digit으로 끝나는 정상 문장경계도 억제** → value-final 연속 문장이 1개로 collapse(undercount). numeric-heavy 과학산문서 자주 발생·누적. **단 severity 제한**: `paragraph_sentence_count`는 어떤 gate/summary도 consume 안 함=diagnostic-only. + 회귀 untested(fixture가 전부 non-digit 종결). **fix**: decimal-point(digit 사이)와 value-final-terminator(digit+종결부호) 구분.

### 2447fee abstract quartet drafting
- ✅ positive: enum 하드닝 정확(appendix reject·abstract accept), 217 tests green, ID/placeholder/backslash/path leak-safety 균일.
- 🔎 **HIGH**: **result-leak guard가 `target_section=='intro'`에만 발동** — abstract엔 동등 leak gate 없음(abstract+guard-OFF accepted vs intro+guard-OFF rejected, 실 validate_writing_task 확인). abstract는 primary result를 compress하는데 hard 보호 0.
- 🔎 **HIGH**: accept/reject gate(`_validate_response_payload`)가 **section 무관·bare 숫자 미reject**(placeholder-slot drift·raw ID만 봄). 9 abstract 응답 전부 bare digit 있는데 gate PASS.
- medium: scorecard overstrong 강화 regex가 results에만(abstract는 generic) / abstract claim-strength forbidden_moves 4개 전부 prompt-only advisory(hard gate 0) / `AUDIT_TARGET_SECTIONS==TARGET_SECTIONS` 붕괴(이전 abstract audit-only 분리 제거).

## 🔑 systemic: 섹션-agnostic 숫자 게이트 갭 (abstract 2447fee + results take93 공통)
gate는 **`no_new_numbers`를 안 읽고**, intro 외 섹션엔 result-leak hard gate가 없음. → abstract·results는 freestanding literal 숫자가 무통과(placeholder 0·numeric_slot 0이면 그냥 통과). resolved-run에선 "licensed라 OK"이나, **gate가 보호를 안 줌**(soft scorecard count만) → 미래에 fabricated/unlicensed 숫자가 끼면 hard gate가 못 잡음. **권고**: (a) `no_new_numbers` 강제(instruction 숫자집합 대비 신규 숫자 reject), 또는 (b) abstract/results에도 intro류 result-leak section-branch 추가. 이게 backlog 최우선.

## take86~94 rollup (real gate + 실 scorecard)
```
take86 discussion(resolved)   B/M/T PASS  overstrong0  numeric高(licensed, 0 fabricated)  leak-safe ✓
take87 discussion(resolved)   PASS         Bold 'establish'=negated disclaimer false-pos  leak-safe ✓
take88 minisection stitch     상류 take86+87 6응답 전부 PASS; take88b가 repetition 줄여 preferred  leak-safe ✓
take89 abstract(resolved)     PASS  numeric-dense→Results/Discussion hybrid(=take90 min_numbers 방향 지지)
take90 abstract(min_numbers)  PASS  좋은 gradient(Terse 최저 numeric·best compression, Measured densest)
take91 abstract(unit_guard)   PASS  Bold 'reveal' 1=약간 assertive; unit(per-mil/percent) 존재
take92 intro(no_result_leak)  PASS  frame-not-report·result_leak 0 ✓ (Bold 'Because' mild framing)
take93 results(observed)      PASS  register clean·overstrong/interp 0  단 🔑 no_new_numbers 미강제(위 systemic)
take94 methods(procedure)     M/T PASS, Bold REJECT=protected_term_missing(lowercase-d isotope 대문자화, case-sensitive)
```
- **claim-strength 전반 절제**: 실질 overstrong 0(take87 'establish'·take91 'reveal' hit는 negated/abstract-context false-pos — 내 scope-disclaimer 명제와 일관: lexical overstrong이 negated use 과대계수). 섹션 register 전부 적합.
- **take94 Bold case-sensitivity**: protected-term이 case-sensitive exact-substring이라 Bold이 lowercase isotope token 대문자화→reject(M/T는 verbatim 보존 PASS). gate 정상작동이나, 문장시작 대문자화 같은 양성 변이도 reject할 brittle함(내가 전에 본 forbidden/SHA case-sensitivity 테마와 동류) — protected-term을 case-insensitive 또는 normalize 고려.

## LEDGER_213~219 답
- **213 take86 resolved discussion**: ok — 3/3 PASS, bounded test register, 0 fabricated number, leak-safe.
- **214 take88b minisection**: ok — stitch가 persistence/SCLM 반복 줄임(take88 대비), claim-strength 불변, 상류 6응답 PASS, leak-safe.
- **215 decimal-sentence fix**: issues_found — 의도 fix OK이나 digit-final undercount(diagnostic-only·untested). 위 fix.
- **216 abstract profile take89**: ok-with-issue — 섹션 적합·claim 절제이나 numeric-dense(Results/Discussion hybrid)→min_numbers(take90) 방향 맞음. + 2447fee abstract result-leak gate 부재(HIGH). 사소: LEDGER_216에 절대경로 commit.
- **217 take90/91 abstract unit guard**: ok — min_numbers gradient 양호(Terse best). take91 Bold 'reveal' 약간 assertive(gate-pass). unit guard 동작(per-mil/percent 존재).
- **218 take92 intro**: ok — frame-not-report·result-leak 0. Bold 'Because'는 mild framing(causal-verb 아님).
- **219 take93 results**: issues_found — register clean이나 🔑 `no_new_numbers` 미강제로 freestanding 숫자 무통과(systemic 갭). claim-strength는 0/0/0.

## 정직/큐
라이브=11 서브에이전트 repo 밖(실 gate/scorecard·코드 break-it harness·leak-location git status). 값/prose/path 미echo(에이전트가 [value]·own-words로 보고, 종합도 값 0). 신규코드=77295ee/2447fee. manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 다음: **result-leak/no_new_numbers 섹션 강제(최우선)**·decimal-sentence digit-final fix·protected-term case·LEDGER 경로 hygiene · 0a68ea8/9a03e90 백로그 · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
