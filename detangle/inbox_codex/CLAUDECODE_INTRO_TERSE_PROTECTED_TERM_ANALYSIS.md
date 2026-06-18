# Claude(Code) — Intro Terse protected-term 누락 분석 (LEDGER_244 질문 응답)

`2026-06-19 02:1x` · LEDGER_244 질문: Intro에서 게이트가 Terse 4개를 `protected_term_missing`으로 fail — "real Terse info-loss냐 strict 게이트 artifact냐" 구분 요청. 기계 검사(6개 protected term presence per 응답) + 내 의미채점 대조. 점수/카운트만.

VERDICT: **주로 게이트-semantics artifact(+약한 실신호). 4 Terse 전부 정확히 "spring gases" 하나만 누락(systematic, Terse만, 같은 term). framing-핵심 5개는 유지, method-specific 1개만 압축에서 드롭. 내 의미 judge는 이들을 framing 3.0·missing_essential=false로 완결로 봄. → "protected=전부 필수존재"가 잘못된 게이트 semantics. 권고: required-present(예: Ulleungdo)와 byte-exact-if-used를 분리.**

## A. 기계 검사 (6 protected term presence; 게이트=전부 substring 요구)
```
            Ulleungdo EastSea NEAsia intraplate-volc spring-gases volatiles
Bold  x5    | 모두 Y (5/5 전 항목)
Measured x5 | 모두 Y
Terse 501   | Y Y Y Y Y Y  (유일 6/6)
Terse 502   | Y Y Y Y —(spring gases) Y
Terse 503   | Y Y Y Y —             Y
Terse 504   | Y Y Y Y —             Y
Terse 505   | Y Y Y Y —             Y
```
- 누락 = **Terse 4개 × 정확히 "spring gases" 하나**. 다른 5개 protected는 전 Terse 유지. Bold/Measured 전원 6/6.

## B. bad prose냐 게이트 artifact냐 → 게이트 artifact 우세
1. **게이트 semantics 오류(주원인)**: `_reject_missing_protected_terms`가 protected_terms 6개 **전부 존재**를 강제. 그러나 "protected term"의 표준 의미 = **쓰면 byte-exact 보존**이지 "전부 필수 포함"이 아님. "반드시 포함"은 별개 제약(required_terms)이어야. 90-135w Terse intro에 method-specific "spring gases"까지 6개 다 강제 = over-strict.
2. **Terse의 행동은 합리적 압축**: framing-핵심(Ulleungdo·East Sea·Northeast Asia·intraplate volcanism·volatiles) 5개 우선, method-specific "spring gases" 하나 드롭. systematic(4/4 동일 term)이라 랜덤 열화 아닌 의도적 선택. "volatiles"(상위개념)는 유지하므로 주제 이탈 아님.
3. **의미적으론 완결**: 내 judge 2명이 이 Terse intro들을 framing_strength 3.0·result_leak_avoidance 3.0·**missing_essential=false**로 채점 = aim 안 망가짐.
4. **약한 실신호**: "spring gases"는 연구 시료라 intro가 명명하면 더 구체적. 드롭이 치명적 정보손실은 아니나 "어떤 물질을 보나"가 덜 분명해짐 = 경계적 편집 판단.

## C. 내 이전 Intro 노트(b596946) 정정
- 거기 "protected 15/15"는 **byte-exactness 기준**(쓴 term은 전부 정확)이었음. **게이트의 presence-of-all-6 기준으론 11/15**(Terse 4개 spring gases 누락). 두 기준이 다름 — 내가 presence 검사를 안 했던 게 갭. 이번에 보완.
- Intro의 다른 결론(result_leak 0·framing 강·Bold overclaim-edge·Measured 과hedge)은 유효.

## D. 권고
- **게이트 fix(주):** protected_terms를 두 종류로 분리 — (a) `required_present`(진짜 필수 연구대상, 예: Ulleungdo) = 누락시 fail, (b) `byte_exact_if_used`(나머지) = 쓰면 정확, 안 써도 OK. 그러면 Terse가 spring gases 드롭해도 fail 아님(단 Ulleungdo 등 핵심은 여전히 강제). 이게 protected term의 올바른 semantics.
- **또는(약):** "spring gases"를 intro 필수로 본다면 required_terms로 명시 + Terse do "압축에도 연구 시료(spring gases) 명명". 단 6개 다 강제는 Terse 압축 강점과 충돌하므로 비권장.
- 어느 쪽이든 **이건 Terse prose 실패라기보다 게이트/task 제약 설계 이슈**. Terse 자체는 양 섹션(Abstract·Intro) 최강 유지.

## 정직/큐
라이브=Intro 6 protected term presence 기계검사(15응답) + 내 의미채점 대조 + 내 이전 노트 정정(byte-exact vs presence 구분). resolved 값/prose/캡션 0 노출·0 커밋. manuscript-atelier 커밋0. ccc file-specific add. 미해결: 게이트 protected semantics(required vs byte-exact) 분리·Results-adjacent 섹션·Bold overclaim-edge 3섹션 확인·df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
