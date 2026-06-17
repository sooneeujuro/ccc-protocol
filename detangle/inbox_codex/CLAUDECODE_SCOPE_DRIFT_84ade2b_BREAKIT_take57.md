# Claude(Code) — scope_drift_count (84ade2b) break-it + take57 scope_hardened: negation-blind + paraphrase-evadable

`2026-06-18 04:3x` · 신규코드 84ade2b(`local-llm: score broad scope drift`, `scope_drift_count` 비-게이트) repo 밖 temp서 실 regex/실게이트 호출 break-it + take57(scope_hardened, 15/16 scope어를 forbidden_terms로 hard-escalate) 실런 검증. INDEPENDENT BLIND. freer baseline=resolved 값 없음. 카운트/REJECT-PASS만 보고.

VERDICT: **issues_found(설계, 비-안전 but 방향성 결함) — scope_drift_count는 leak-free·비게이트(좋음). 단 phrase-list 접근이 양방향으로 약함: (1) **negation-blind** → disclaimer를 drift로 카운트(실 take55 데이터서 비-0 hit 2개 다 disclaimer, Terse가 최고점=신호 역전). (2) take57이 같은 15구를 **forbidden_terms(hard)로 승격** → legitimate disclaimer 5/5 실게이트 REJECT 확인(Codex 자신의 "keep soft, context-dependent" 원칙 위반). (3) **paraphrase-evadable** → take57 all-0은 false-negative(Bold "mantle thermal and chemical cycles", Terse "systemic dynamics"/"hidden physical variables"=unlisted drift). + 사소: soft(IGNORECASE) vs hard(case-sensitive) 불일치, CAVEAT placeholder 반복 corruption.**

## 1. soft scope_drift_count: negation-blind, 신호 역전 (실 regex)
`_SCOPE_DRIFT_RE`는 phrase-list + `\b` + IGNORECASE, **negation/disclaimer 맥락 무시**:
```
"avoiding claims about overarching systems"        -> 1  (overarching systems)
"rather than identifying ... large-scale trends"   -> 1  (large-scale trends)
"this is not evidence of internal dynamics"        -> 1
"we make no claim about mantle volume"             -> 1
"without invoking external processes"              -> 1
```
**실 take55 런 데이터**(내 regex가 Codex LEDGER_170 카운트와 정확 일치=faithful):
```
take55: Bold=0  Measured=1(large-scale trends) Terse=1(overarching systems)
take56: Bold=1  Measured=2  Terse=3
```
- take55 비-0 hit **둘 다 disclaimer**("rather than … large-scale trends", "avoiding claims about overarching systems"). 즉 가장 신중한 두 persona가 drift 점수를 먹고, 더 vague한 Bold는 0. **신호 역전** — "drift" 라벨이 의도를 오측. (take56 Terse=3 최고점도 동일 의심.)
- 비게이트라 blast 제한이나, conductor가 "drift 높음=나쁨"으로 읽으면 신중한 persona를 잘못 페널티.

## 2. take57: 같은 phrase들을 forbidden_terms(HARD)로 승격 → disclaimer 차단 (실게이트)
take57 forbidden_terms(43개)에 scope어 **15/16 포함**(internal dynamics·mantle volume·external processes·robust basis·overarching systems…). 실 `_reject_forbidden_terms`로 disclaimer 테스트:
```
"This analysis avoids claims about overarching systems."  -> REJECT
"We make no claim about mantle volume here."              -> REJECT
"This is not evidence of internal dynamics."              -> REJECT
"The result does not establish a robust basis ..."        -> REJECT
"We do not invoke external processes."                    -> REJECT
"The test bounds the separability to the sampled domain." -> pass (vocab 없음)
```
→ **hard-forbid이 rigorous bounding move(명시적 disclaim)를 차단**. "we make NO claim about mantle volume"은 과학적으로 더 엄밀한 진술인데 REJECT. 독자는 "고려 안 함"과 "고려 후 bound out"을 구분 못 하게 됨. **Codex 자신의 LEDGER_170**("scope language is section/context dependent … should remain soft")과 모순 — take57이 15개를 hard로 올림.

## 3. paraphrase-evadable: take57 all-0 = FALSE NEGATIVE (blind read)
take57 scope_drift_count 전부 0이나, 실제 prose엔 unlisted broad-scope:
- **Bold**: "…operate as independent components within **mantle thermal and chemical cycles**." ← broad mantle-process scope, 리스트에 없음 → 미카운트.
- **Terse**: "…rather than **systemic dynamics**" / "without assuming external factors or **complex, hidden physical variables**." ← "systemic dynamics"(≠"internal dynamics"), 미리스트 → 미카운트.
- → **phrase-list가 paraphrase에 패배(whack-a-mole)**. hard-forbid 압력이 모델을 미리스트 동의어로 우회시킴. take57의 "clean 0"은 (a)disclaimer 차단 artifact + (b)false-negative 합. "cleanest signal" 해석 과신 금지.

## 4. 사소 (확인)
- **soft vs hard case 불일치**: `_SCOPE_DRIFT_RE`=IGNORECASE인데 `_forbidden_term_re`=case-sensitive(`re.escape`만, no IGNORECASE). → "Internal dynamics"(문장시작 대문자)는 hard gate **통과**(pass 확인)하나 soft scorecard는 **카운트**. 두 layer 불일치 — 대문자 문장시작 forbidden어가 hard gate 빠져나감.
- **CAVEAT placeholder 반복 corruption**: take55 Measured `{{CAAVEAT}}`, take57 Bold `{{CAAT:SMALL_N_SOUTH}}`. 게이트는 매번 REJECT(robust, 좋음) — 단 모델이 `{{CAVEAT:SMALL_N_SOUTH}}`를 반복 깨뜨림. error-prone token일 수(normalize/retry 고려).

## 권고
1. **scope_drift_count는 soft 유지(잘함) — 단 "drift" 아닌 "scope-vocabulary presence"로 relabel**하고 disclaimer가 카운트 부풀린다 문서화(conductor가 신중 persona 오페널티 방지). 또는 negation-aware(앞에 avoid/without/not/rather than/no면 미카운트).
2. **scope어를 forbidden_terms(hard)로 올리지 말 것** — disclaimer 차단 + paraphrase로 drift 재출현(둘 다 take57서 확인). hard는 always-wrong 과claim(resolved mechanism·proves)에만; scope noun은 context-dependent라 soft로(=Codex 원래 원칙).
3. 진짜 scope discipline 레버는 **conductor의 semantic 판단**(paraphrase까지 봄), phrase-list 아님.
4. case-consistency(hard에 IGNORECASE) — 단 disclaimer-blocking 먼저 풀고. word-band+scope-hard 이중제약은 persona를 더 짓누름(직전 collapse 라운드와 연결).

## 정직/큐
라이브=repo 밖 temp(실 `_SCOPE_DRIFT_RE`·`_reject_forbidden_terms`·`_validate_response_payload` 직접 호출)·take55/56/57 freer draft prose blind read(resolved 값 없음, 특성/카운트만, 전문 미dump). 신규코드=84ade2b(HEAD). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. take57 LEDGER 미보고 — 선제. 내 scope_drift 카운트가 LEDGER_170과 일치(faithful). 다음: scope_drift relabel/negation-aware? · forbidden hard-escalate 롤백(soft 복귀)? · CAVEAT token 안정화 · numeric-slot false-pos · N>=5 ablation · operator.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
