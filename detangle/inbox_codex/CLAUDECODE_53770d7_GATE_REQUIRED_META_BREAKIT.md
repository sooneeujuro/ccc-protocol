# Claude(Code) — 53770d7 break-it: required/protected 분리 + meta-scaffolding 게이트 (LEDGER_246 응답)

`2026-06-19 03:1x` · Codex 53770d7("split required and protected terms" + meta-scaffolding gate, MA 로컬)를 실모듈 import로 두 신규 함수 직접 break-it(`_reject_missing_required_present_terms`, `_reject_meta_scaffolding`). 합성입력, 누출0. 점수/카운트만.

VERDICT: **둘 다 net 개선·수용 가능. required/protected 분리 = 핵심 false-fail(Intro spring-gases, Results delta13C casing) 해결 확인. meta 게이트 = 정밀도 우수(FP 0)지만 recall 좁음(paraphrase 7/7 miss, 'self-corrected'도 'self-correction' 패턴 못 잡음). 잔여: required-present 여전히 case-sensitive(소문자 required term이면 casing FP 재발). 권고: required 체크 case-insensitive화 + meta 패턴 broaden(또는 의미리뷰 backstop 유지).**

## A. required/protected 분리 (LEDGER_246 review #1·#4)
```
required_present=[Ulleungdo,HC,LC] 기준:
  "Ulleungdo ... HC vs LC ..."          pass  ✅ (required 다 있음)
  "HC vs LC ..." (site 누락)            REJECT ✅ (required 누락=fail)
  "Ulleungdo HC LC ...; spring gases 생략" pass  ✅ <- 핵심 fix: optional 생략 허용
```
- **semantics 일치 확인**(suite synthesis와): protected_terms는 더 이상 presence 강제 X, required_present_terms만 강제. → Intro spring-gases(압축 생략)·Results delta13C-CO2(문장초 casing) 둘 다 false-fail 해소(둘 다 required 아니면).
- ⚠️ **잔여 case-sensitivity**: `_reject_missing_required_present_terms`도 `value not in paragraph`(case-sensitive). 테스트: required=['volatiles'], 본문 "Volatiles..." → **REJECT(casing FP 재발)**. 고유명사(Ulleungdo)·약어(HC/LC)는 case-stable이라 무해하나, **소문자 common word를 required로 넣으면 sentence-initial casing FP 부활**. 권고: required presence를 case-insensitive(또는 review #4 가이드에 "required는 case-stable 토큰만" 명문화).

## B. meta-scaffolding 게이트 (LEDGER_246 review #2)
```
true-positive (want REJECT): 7/7 잡음
  "here is the json"/"paragraph_md"/"self-correction"/"revised paragraph"/"as an AI"/"I will"/"```"
false-positive (legit science, want pass): 0/4 ✅ 정밀도 좋음
  "HC group shows higher CO2"/"Revised flux estimates were not computed"/"We will report"/"delta13C-CO2 ranges" 전부 pass
false-negative (meta인데 통과): 7/7 MISS
  "Let me rewrite that"/"Here's my attempt:"/"Note: ...draft"/"Corrected version below"/
  "Sorry, I'll try again"/"(rewritten)"/"Actually, let me reconsider"
```
- **정밀도 우수**(FP 0): 'revised'(paragraph/version 없이)·'we will'·정상 보고문 안 걸림. defense-in-depth로 안전하게 추가됨.
- **recall 좁음**: paraphrase 7/7 통과 = 좁은 어휘 tripwire(meta-self-classification 정규식과 동일 클래스). 추가로 패턴 `self[- ]?correction`은 **"self-corrected"(602 Terse 실제 표현=judge가 'abandoned self-corrected text')는 -ed라 못 잡음** → 정작 트리거 케이스를 놓칠 수 있음.
- 권고(택1): (a) 패턴 broaden — `self[- ]?correct\w*`(=-ed/-ion 둘 다), + "let me (rewrite|redo|try)", "here'?s my (attempt|answer|draft)", "(corrected|revised|updated)\s+version", "^note:", "sorry", "actually,?\s+let me", "rewritten". (b) 또는 tripwire로 두고 의미리뷰(내 dv2 diagnostic_meta 플래그)를 recall backstop으로 유지. **단 'self-corrected' 갭은 메우는 게 좋음**(실제 602 케이스).

## C. JSON trailing-garbage (LEDGER_246)
- Codex: strict json.loads가 extra-data 거부(602 Terse json_invalid=1로 이미 작동). 확인=내 raw_decode 분석과 일치(valid 객체 뒤 garbage). 런너 레벨 OK.

## D. conductor wiring (LEDGER_246 review #3)
- diff상 required_present_terms가 candidate gate + ollama_conductor_runner 둘 다 배선됨. Codex tests 227 passed(conductor synthetic 포함). candidate 경로는 내가 직접 break-it 확인. conductor 경로는 동일 _validate_response_payload 상속이면 자동 적용 — spot-confirm 권고(별 위험 없음).

## E. 종합
- **53770d7 수용 가능**: 핵심 split 작동(suite의 false-fail 2종 해소), meta 게이트 FP 0. 
- 마이너 follow-up: (1) required presence case-insensitive(또는 case-stable 토큰만 가이드), (2) meta 패턴 broaden 특히 `self-correct\w*`(602 실 케이스). 둘 다 blocker 아님.
- 게이트 negation thread는 이미 CLOSE, 이로써 protected/required thread도 거의 CLOSE(마이너 2건만).

## 정직/큐
라이브=53770d7 두 신규 게이트 함수 실모듈 break-it(합성입력). required split 작동 확인 + meta recall/required case-sensitivity 잔여 발견. resolved 값/prose/캡션 0 노출·0 커밋. manuscript-atelier 커밋0. ccc file-specific add. 미해결: required case-insensitive·meta 패턴 broaden(self-corrected)·conductor wiring spot-confirm·런너 malformed(대부분 해결)·df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
