# Claude(Code) — take95 Bold token-guard 검증: 내 take94 finding 닫힘 + case-sensitivity 구분 (LEDGER_221)

`2026-06-18 10:1x` · bbaa05c(Bold protected-token byte-for-byte guard, 내 take94 protected-term case-sensitivity finding 응답) take95 real-gate 재검. 신규코드=bbaa05c(HEAD).

VERDICT: **ok — 내 take94 finding 닫힘 확인: take95 Bold/Measured/Terse 전부 real-gate PASS(Bold이 delta18O/deltaD/delta13C-CO2 byte-for-byte 보존, overstrong/interp 0). + 🔑 calibration 구분: protected-term의 case-sensitivity는 **올바름**(과학 표기는 case-meaningful) — 내 forbidden-term case-sensitivity brittle 지적과 구분됨. Codex의 prompt-guidance(gate loosen 아님) 선택이 정확.**

## take95 검증 (real gate 직접)
```
take95 methods(bold_token_guard): Bold PASS  Measured PASS  Terse PASS  (overstrong 0·interp 0 전원)
```
- take94: Bold이 protected token(lowercase-d isotope)을 대문자화 → `gemma_candidate_protected_term_missing` REJECT.
- take95: bbaa05c가 Bold role에 "protected scientific token byte-for-byte 복사·isotope/unit notation normalize/capitalize 금지" 가이드 추가 → **Bold이 표기 보존, 3후보 전원 PASS.** 내 take94 finding 정확히 닫힘. (LEDGER_221 scorecard: meta/overstrong/scent/scope-drift 전원 0과 일치.)

## 🔑 calibration 구분 (내 case-sensitivity 코멘트 정밀화)
Codex가 **prompt-guidance로 고치고 gate는 case-sensitive 유지**한 게 **이 케이스엔 정확**:
- **protected-term(must-preserve 표기)**: case-sensitivity **올바름**. 과학 isotope/unit 표기는 case-meaningful(delta18O ≠ Delta18O ≠ DELTA18O; deltaD ≠ deltad) → case-drift는 **진짜 오류**라 잡아야 함. 고치는 법은 모델이 안 drift하게(prompt) — **gate를 case-insensitive로 loosen하면 틀린 표기를 허용**하므로 잘못. Codex 선택 정확.
- **forbidden-term(banned 의미)**: 여기선 내가 전에 case-sensitivity가 brittle하다 했음(문장시작 대문자 변종을 놓침) → **case-insensitive가 나음**(금지 의미를 case 무관 잡아야).
- → **case-sensitivity는 context-dependent**: protected=case-sensitive 정답(표기 강제), forbidden=case-insensitive 나음(의미 포착). 두 결론 모순 아니라 **목적이 반대**(보존 vs 금지). Codex의 protected 쪽 case-sensitive 유지+prompt fix는 맞음.

## take96 conclusion — pending
`quartet_lee_conclusion_take96_*` dir 비어있음(파일 0) — 준비됐으나 미생성(운영자 wrap-up 중인 듯). 생성되면 blind conductor(narrow constraint register). 현재 미검토.

## LEDGER_221 답
- **fix 확인?** 예 — take95 Bold token-guard로 take94 protected-term drift 닫힘(real-gate 3/3 PASS 독립확인). 새 이슈 없음.
- token-guard loop accepted. 다음(LEDGER_221 권고): 신규 섹션 profile 또는 cross-section conductor pass — 동의. (내 backlog synthesis의 systemic no_new_numbers/result-leak 게이트 갭이 더 우선순위 — abstract/results가 freestanding 숫자 무통과, 그게 닫히면 cross-section stitch가 더 견고.)

## 정직/큐
라이브=repo 밖 real `_validate_response_payload` take95 직접(값 미echo·gate verdict/probe count만). take95 methods=resolved지만 값 미노출. take96 empty. 신규코드=bbaa05c. manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 다음: **systemic no_new_numbers/result-leak 섹션 강제(최우선)** · take96 생성시 blind · 백로그(0a68ea8/9a03e90) · operator review. (Codex wrap-up 중이면 신규 줄어들 수 — STATUS-only 라운드 늘 것.)

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
