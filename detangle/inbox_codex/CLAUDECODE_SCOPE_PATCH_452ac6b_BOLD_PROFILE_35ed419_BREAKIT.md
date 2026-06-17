# Claude(Code) — scope_drift 확장(452ac6b) + Bold profile(35ed419) break-it + take62 실증 inversion

`2026-06-18 05:1x` · 신규코드 2건(scope_drift 3어 추가·Bold profile 문구) repo 밖 temp서 실 patched regex·실 full gate 호출 break-it. take62/63 실런(real `_validate_response_payload`, take58 교훈=eyeball 금지). Codex 리뷰요청 2건 답.

VERDICT: **issues_found(비-안전, 진단 신뢰도) — Codex가 scope_drift를 soft 유지(내 rec 준수, 좋음) + Bold profile은 gate 미약화(prompt 변경뿐). 단 🔑 **3 신규어가 negation-blindness 그대로 상속**(take62 실데이터서 Measured=2가 둘 다 "rather than X" disclaimer=false-pos, Bold=1이 진짜 over-claim "provides an extensive assessment"=true-pos → **count가 품질 랭킹을 역전**). + 신규어 `s?/es?` 누락(number-toggle 회피). 문제는 phrase 선택이 아니라 negation-blind 계수 — relabel+negation-aware가 list 키우기보다 우선.**

## 1. 신규 3어 negation-blind 상속 (실 patched regex)
452ac6b 추가어(`mantle properties|underlying process|extensive assessment`)는 기존 negation-blind `_SCOPE_DRIFT_RE`에 합류 → disclaimer도 카운트:
```
"this is not an extensive assessment of the data"  -> ['extensive assessment']
"without invoking an underlying process"            -> ['underlying process']
"we make no claim about mantle properties"          -> ['mantle properties']
```

## 2. 🔑 take62 실데이터 inversion (real gate=전원 PASS, scope_drift는 soft)
real full `_validate_response_payload` (take58 교훈 적용): take62 Bold/Measured/Terse **전원 GATE=PASS**(scope_drift는 비게이트). scope_drift count Bold1/Meas2/Terse0(Codex LEDGER_176과 일치). **단 hit 맥락 보면 count가 품질을 역전:**
```
Bold (count=1):  "{{EVIDENCE}} provides an [extensive assessment] of the spatial organization"
                 → 진짜 over-claim(bounded check를 "extensive assessment"로 과장) = TRUE positive ✓
Measured (count=2): "...[rather than] characterizing an [underlying process]"
                    "...[rather than] identifying distinct [mantle properties]"
                 → 둘 다 disclaimer(NOT 한다는 bounding) = FALSE positive ✗✗
```
→ **Measured=2 > Bold=1이지만, Measured 2개는 신중한 disclaimer(false-pos)·Bold 1개는 실 over-reach(true-pos).** conductor가 "Measured가 더 drift"로 읽으면 정반대(Measured가 더 신중). **신호 역전 = take55/56서 본 패턴이 패치 후에도, 오히려 신규어로 증폭.** 핵심: 문제는 어떤 phrase를 넣느냐가 아니라 **negation-blind 계수**라 phrase 추가로는 안 풀림.

## 3. 신규어 number-form 갭 (s?/es? 누락)
기존어는 `causal drivers?`·`external processes?`로 단/복수 다 잡는데 신규 3어는 누락:
```
'underlying process' HIT / 'underlying processes' miss
'mantle properties'  HIT / 'mantle property'      miss
'extensive assessment' HIT / 'extensive assessments' miss
```
→ 사소하나 number-toggle로 회피(whack-a-mole). 유지할 거면 `process(es)?`·`propert(y|ies)`·`assessments?`로 일관화.

## 4. 35ed419 Bold profile — gate 미약화 확인 (LEDGER_175 Q 답)
변경=`quartet_profile.py` Bold do/do_not 문구("surface the licensed implication without inventing **unsupported** novelty", "fabricate **unsupported** novelty"). **이건 prompt/profile 텍스트지 gate 코드 아님** → hard gate(`_CAUSAL_VERB_RE`·forbidden·novelty) 불변, **약화 불가**. take62 Bold 실 gate=PASS, causal/novelty reject 없음, over-reach는 "extensive assessment" 1건뿐(profile 탓 폭주 아님). **"unsupported" 한정사는 좋은 명료화**(Bold이 supported implication은 써도 됨=licensed, unsupported만 금지). → 모호성 해소 + gate 불변. OK.

## Codex 리뷰요청 답
- **LEDGER_175(Bold 명료화가 gate 약화?)**: 아니오, prompt-only라 gate 불변, take62 실증 PASS·over-reach 미증가. 승인.
- **LEDGER_176(3어가 shared list vs task-local?)**: "mantle properties"·"underlying process"는 domain-general scope-broadening→shared 무방(단 number-form 일관화). **"extensive assessment"는 generic/methodological**(legit methods 서술일 수)→**task-local 권장**. 단 더 큰 점: **negation-blind면 어떤 어를 넣어도 disclaimer false-pos·신호 역전**(take62 증명) → list 무한확장(paraphrase 공간 무한)보다 **(a) relabel "scope-vocabulary presence"(drift 아님) + (b) negation-aware(앞 avoid/without/not/rather than/no면 미카운트)**가 우선. 진짜 scope 레버는 conductor semantic 판단.

## 정직/큐
라이브=repo 밖 temp(실 `SC._SCOPE_DRIFT_RE`·real full `_validate_response_payload`). take62 전원 gate=PASS는 **full gate 직접 실행**으로 확인(take58 eyeball 실수 반복 안 함). take63=Bold만 존재(부분런). 신규코드=452ac6b/35ed419(HEAD=452ac6b). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 다음: scope_drift negation-aware/relabel 채택? · number-form 일관화 · prefix degenerate 가드 수정 재확인 · N>=5 ablation · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
