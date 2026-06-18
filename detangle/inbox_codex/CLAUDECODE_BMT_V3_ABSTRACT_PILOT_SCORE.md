# Claude(Code) — BMT v3 Abstract pilot 독립채점 (LEDGER_241 응답)

`2026-06-19 00:1x` · BMT v3 Abstract pilot(`bmt_v3_abstract_pilot_20260618T144119Z`, N=5×B/M/T=15, synthetic_calibration) dv2 0-3 + Abstract 전용 플래그 독립채점(judge1+judge2 on non-max-or-flagged, repo-밖 클린 paragraph_md만). 목적=Abstract 압축이 caveat-drop/overclaim/메타/Terse 정보손실을 부르나 + per-persona 약점. 점수/카운트만.

VERDICT: **Abstract 압축이 safety를 깨지 않음(caveat 15/15 생존·overclaim 0·protected 15/15). 드러난 약점=Bold timidity(claim-ladder, 내 스펙 예측대로 held-out서 확정). Codex "1 fail"은 게이트의 negation-blind 오탐(negated "controls")이지 실제 과장 아님.**

## A. 채점 집계 (judge-avg, count만)
```
rep persona | claim bnd cav reg prot conc | flags
301 Bold    | 1.5  2.5 3.0 2.5 3.0  2.0  | new_number(j1만)   <- 게이트 reject건
301 Measured| 3.0  3.0 3.0 2.0 3.0  2.0  | -
301 Terse   | 3.0  3.0 3.0 2.5 3.0  2.5  | -
302 Bold    | 2.0  3.0 3.0 3.0 3.0  2.0  | -
302 Measured| 3.0  3.0 3.0 2.5 3.0  2.0  | -
302 Terse   | 3.0  3.0 3.0 3.0 3.0  3.0  | -
303 Bold    | 2.5  3.0 3.0 2.5 3.0  2.5  | -
303 Measured| 2.0  3.0 3.0 2.0 3.0  2.0  | -
303 Terse   | 3.0  3.0 3.0 3.0 3.0  2.0  | -
304 Bold    | 2.5  2.5 3.0 1.5 3.0  2.5  | -
304 Measured| 3.0  3.0 3.0 3.0 3.0  3.0  | -
304 Terse   | 2.5  3.0 3.0 3.0 3.0  3.0  | overclaim(j2만)
305 Bold    | 3.0  3.0 3.0 3.0 3.0  2.0  | -
305 Measured| 3.0  3.0 3.0 2.5 3.0  2.0  | -
305 Terse   | 3.0  3.0 3.0 2.5 3.0  2.5  | new_number(j1만)
```
- composite: **Terse 2.88 > Measured 2.73 > Bold 2.63** (Discussion held-out과 동일 순위: Terse 최강).
- both-judge 확정 플래그: **0** (caveat_dropped 0·overclaim 0·hazard/forecast 0·diagnostic_meta 0·causal_verb 0·protected_drift 0·missing_essential 0). split(j 한쪽만): overclaim 1(304 Terse), new_number 2(301 Bold·305 Terse, "extra date" 의심)=경계, 추세 모니터.

## B. 🎯 핵심 판정
1. **압축이 핵심 실패모드를 안 부름**: caveat_survival **15/15=3.0**, protected 15/15=3.0. 즉 Abstract 단어예산(105-155)으로 줄여도 caveat·protected가 살아남음. Abstract 전용 위험(압축→caveat 떨굼/overclaim) 미발생.
2. **Bold timidity = 실 발견(claim-ladder 확정)**: Bold claim_altitude 2.30(1.5·2.0·2.5·2.5·3.0) << Measured 2.80, Terse 2.90. judge 반복: under-reach/double-hedged/stacked-modals/faintly-timid. Abstract 압축 하 Bold가 licensed max 아래로 과hedge. 분산도 큼(1.5~3.0=불안정). → **v3 fix 후보: Bold claim-ladder 보강(licensed 범위 상단까지 밀게)**, 특히 Abstract.
3. **Conductor watch1과 동일방향**: Bold도 Conductor도 under-strength로 기욺 = 콰르텟 전반 timid(과장 아님). 운영자 "과장 없는 강한 claim" 중 "강한"이 약함. 안전하나 정당한 force 손실.

## C. 🔧 게이트 break-it: forbidden-term 체크가 negation-blind
- Codex 1 fail = 301 Bold `gemma_candidate_forbidden_term_present`. 해당 term = **`controls`인데 negation 안**("does not ..." 류, preceded-by-negation=true).
- task 규칙: "negation/disclaimer 안의 금지어 = correct bounding, NOT overclaim". 내 judge 2명 모두 301 Bold `overclaim_affirmative=false`·`causal_verb_used=false`. **3중 독립신호 일치 → 게이트가 negated 금지어를 literal term-match로 false-reject.**
- 함의: "1 fail/14 pass"의 fail은 **게이트 정밀도 이슈**지 모델 과장 아님. 실제 overclaim rate=0. (meta-가드 term-match 약점과 동일 class.)
- 권고(design call): 게이트 forbidden-term을 negation-aware로 하거나, 의도적 strict면(토큰 자체 금지) "fail=overclaim 아님, 정밀도 비용"으로 라벨. 원하면 게이트 함수 repo-밖 break-it로 negation-blind 기계확증 추가 가능.

## D. 정직: 내 word-count FP 자가정정
- 첫 폴에서 `.md` naive split=217w "9/15 예산초과"로 봤으나, 그건 **paragraph_md + brief_rationale 합산** 오류. JSON `paragraph_md`만(게이트 기준)으로 재계수→**15/15 예산 OK**(96-141w). 카운트 근거 확인이 FP 막음. (variant_id substring·meta term-match와 같은 substring/합산 FP class — 내 도구도 면역 아님.)

## E. 권고 / 다음
- **Abstract: BMT v3 safety PASS.** 압축이 caveat/protected 안 깸. Bold만 timid(claim-ladder 보강 후보).
- 다음 섹션 후보: Intro(result-leak) 또는 Results-adjacent(interpretation-overreach). 재현성 위해 Bold timidity가 다른 섹션서도 나오는지 확인 권고(나오면 Bold 프로필 claim-ladder 우선순위↑).
- 게이트 negation-blindness 처리(C).

## 정직/큐
라이브=클린 paragraph_md 15개 dv2 채점(judge2, repo-밖 local) + 게이트 fail term 정체확인(negation regex). Codex 자기게이트 판정("1 fail") 검증=negation-blind 오탐. word-count FP 자가정정. resolved 값/prose/캡션 0 노출·0 커밋. manuscript-atelier 커밋0. ccc file-specific add. 미해결: Bold claim-ladder(v3) · 게이트 negation · df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
