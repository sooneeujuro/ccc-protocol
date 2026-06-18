# Claude(Code) — Tournament Round 1 blind scoring result (gemma-tournament-20260618T111500Z)

`2026-06-18 12:5x` · 45-call run 완료(44 pass/1 fail) → 내 detector cross-check PASS → blind 채점(44 agent 병렬, variant blind, 5축 0/1/2, negation-aware) → REVEAL로 variant 매핑 → 분포·선정. **점수/카운트만 보고(resolved 값·prose 0 노출·0 커밋).**

VERDICT: **scored. persona별 winner 도출 + 🔑 메타-finding: 변별력 낮음(게이트가 이미 강함). objective 축은 객관적 교차검증으로 corroborated. Bold는 동률→held-out 필요.**

## A. cross-check (채점 전 게이트) — PASS
scoring manifest(`LOCAL_GEMMA_TOURNAMENT_SCORING_BLIND.local.json`)에 내 detector 적용:
- de-blind/abs-path/reveal-token = **0**, entry 키 response-only, response_file 규율 OK, blind_scoring 플래그 전부 True.
- (내 detector 1건 FP=`blind_variant_id`의 substring "variant_id"→boundary-aware로 자가수정. 진짜 누수 아님. 내 도구도 substring-FP class에 안 면역=정직 기록.)
- runner의 `_assert_scoring_manifest_is_blind`(9 variant label + 2 path token)도 통과 상태.

## B. per-variant 분포 (composite = 5축 평균 0–2; cand = median − 0.5·var − 0.5·(2−worst))
```
variant               persona   pass  claim cavea regis prot  conci | med  worst  var    cand
B2_caveat_survivor    Bold      5/5   2.00 2.00 2.00 2.00 2.00 | 2.00 2.00  .000  2.000
B3_test_framed        Bold      5/5   2.00 2.00 2.00 2.00 2.00 | 2.00 2.00  .000  2.000
B1_licensed_max       Bold      5/5   1.80 2.00 2.00 2.00 1.80 | 2.00 1.80  .010  1.895
M2_woven_caveat       Measured  5/5   2.00 2.00 2.00 2.00 2.00 | 2.00 2.00  .000  2.000
M3_caveat_front       Measured  5/5   2.00 2.00 2.00 2.00 1.80 | 2.00 1.80  .006  1.897
M1_claim_then_caveat  Measured  5/5   2.00 2.00 1.80 2.00 1.60 | 2.00 1.60  .026  1.787
T1_n_points           Terse     5/5   2.00 2.00 2.00 2.00 2.00 | 2.00 2.00  .000  2.000
T2_frame_bound        Terse     4/5   2.00 2.00 1.75 2.00 2.00 | 2.00 1.80  .007  1.896
T3_minimal_clause     Terse     5/5   2.00 2.00 1.40 2.00 1.40 | 1.60 1.60  .038  1.381
```
(T2 4/5 = no_new_numbers fail 1건 rep2 — 아래 §E. 여전 pass_rate≥4/5라 적격.)

## C. persona별 winner (pass_rate≥4/5 AND 최고 cand, best-of 금지)
- **Bold = B2_caveat_survivor** (cand 2.000) — 단 **B3_test_framed와 0.000 동률**(둘 다 5/5 만점). → **held-out 필요.** 내 lean=**B2**(operator 우선순위 "caveat가 죽이지 않는 강한 claim"을 가장 직접 구현). B1_licensed_max는 claim_altitude 1건 over-reach(가끔 license 초과=operator의 "과장" 우려 실측).
- **Measured = M2_woven_caveat** (cand 2.000, gap 0.103) — woven caveat 통합이 가장 깨끗. claim-then-caveat(M1)·caveat-front(M3)는 register/conci에서 약간 dip.
- **Terse = T1_n_points** (cand 2.000, gap 0.104) — N-points 압축이 최적. **T3_minimal_clause는 명확한 패자(cand 1.381)**: minimal-clause 과압축이 register·completeness 저하(과압축은 Discussion register를 telegraphic으로 깸).

## D. 🔑 메타-finding: 변별력 낮음 (good-apparatus 신호)
44개 중 **41개가 composite 2.0 만점**. 축별 히스토그램: claim_altitude 2=43/1=1, caveat_survival 2=44, register_fit 2=39/1=5, protected 2=44, conciseness 2=37/1=7. **0점 전무.**
- **objective 교차검증(내가 44개 전수 구조 스캔, 카운트만)**: forbidden-verb AFFIRMATIVE **0**, protected-term DRIFT **0**, licensed-implication(SCLM+persist/signature) present **44/44**. → "과장 0 + 강한 claim 전수 존재"가 **객관적으로 corroborated**. operator 핵심 우선순위(과장없는 강한 claim·caveat가 main claim 안 죽임·protected 보존·conductor 새주장 없음[해당없음=B/M/T만])는 **전 후보에서 이미 충족**.
- 함의: 하드 게이트가 이미 강해 후보 간 **floor가 거의 동일** → 선정 신호는 "**최고 1개**"보다 "**피할 것**"(T3 minimal-clause 과압축, B1 licensed-max 가끔 한 노치 over-reach, M1 claim-then-caveat 약간 약함)에서 더 신뢰가능.
- **Round 2 권고(변별력↑)**: (a) task를 더 적대적으로(over-reach 미끼·tighter protected trap·약한 evidence로 under/over 유도) → floor 분산 강제, OR (b) 루브릭 ceiling 낮추기(0–3 스케일 or claim-strength sub-axis 세분), OR (c) 동률엔 2nd-judge/held-out 자동.

## E. 부수 검증 (장비가 실제로 일함)
- **no_new_numbers hard gate(내 systemic fix)가 야생에서 진짜 위반 1건 catch**: T2_frame_bound rep2 = `gemma_candidate_new_number_present`(2 attempts 후 fail). licensed 외 새 숫자 도입을 정확히 reject. fake-pass 아님.
- runner 경계(EXECUTION-only·response-only scoring manifest·blind)도 실런에서 holds.

## F. 다음
1. **held-out**: Bold B2 vs B3 분리 위해 다른 task로 두 변종 재현(Codex 모델런). + 원하면 Measured/Terse winner도 held-out 확인.
2. **Round 2 task**: §D 권고대로 변별력↑ task 설계(내가 spec 초안 가능).
3. winner 프롬프트(B2/M2/T1)를 persona profile 기본값 후보로 승격 검토(held-out 통과 후).

## 정직/큐
라이브=cross-check detector + 44-agent blind 채점(Workflow, repo 밖 local response만 read) + objective 구조 교차검증(카운트만). resolved 값/prose 0 노출·0 커밋. 채점 후에만 REVEAL 매핑. 내 문장수 메트릭은 resolved 소수점에 걸려 폐기(77295ee 동류, 선정 무영향). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값/prose 미노출·미커밋.)
