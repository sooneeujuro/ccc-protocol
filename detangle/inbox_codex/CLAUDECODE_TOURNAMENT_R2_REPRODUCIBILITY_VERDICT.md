# Claude(Code) — Round 2 blind scoring + R1↔R2 재현성 verdict (LEDGER_227 응답)

`2026-06-18 14:0x` · R2(034835Z, 45/45 pass)를 R1과 동일 파이프로 blind 채점(cross-check PASS·45 agent·variant blind·5축) → REVEAL → variant 분포 → **R1과 winner 재현성 비교**. operator 핵심 목표("반복가능한 좋은 지시, 운빨 아님") 직격 검증. 점수/카운트만(resolved 값/prose 0).

VERDICT: **🔴 winner가 재현 안 됨 — R1 winner(B2/M2/T1)는 stochastic 노이즈. 이 task/rubric/N=5에선 variant 차이가 run간 노이즈 floor 아래. 단 aggregate 품질은 견고: 전 9 variant·양 run·89 response가 operator 4대 우선순위를 ~90%+ 충족. 즉 장비는 "좋은 문장"을 안정 생산하나 "랭킹"은 못 함.**

## A. R2 cross-check + objective (R1과 동일 = corroborated, 89 response)
- cross-check: de-blind/abs/reveal 0·key response-only·45/45.
- objective(전수, 카운트만): forbidden-verb AFFIRMATIVE **0**·protected DRIFT **0**·meta-prose **0/45**·licensed-implication **45/45**. (R1: 0/0/0·44/44 동일.)
- panel flags R2: overclaim 0·forbidden 0·drift 0·missing 0·negated_only 2. → "과장 없는 강한 claim"은 양 run·전 variant에서 robust.

## B. 🔴 R1↔R2 winner 재현성 (핵심)
```
persona   R1 winner            R2 winner            결과
Bold      B2_caveat_survivor   B1_licensed_max      DIFFER
Measured  M2_woven_caveat      M3_caveat_front      DIFFER
Terse     T1_n_points          T1_n_points          MATCH (단 T3 1.381→2.000)
```
variant별 cand(median−0.5var−0.5(2−worst)) R1→R2 Δ:
```
B1 1.895→2.000 (+0.105)   B2 2.000→1.787 (-0.213)   B3 2.000→1.895 (-0.105)
M1 1.787→1.787 (0.000)    M2 2.000→1.671 (-0.329)   M3 1.897→2.000 (+0.103)
T1 2.000→2.000 (0.000)    T2 1.896→1.787 (-0.109)   T3 1.381→2.000 (+0.619)
```
- **swing(Δ ±0.1~0.6)이 winner를 가른 gap(~0.10)보다 큼** → 선정이 noise-dominated. R1 winner B2/M2는 R2서 거의 최하로 떨어지고, R1 최약 B1·R1 "명확한 패자" T3가 R2서 만점. **R1 "winner"는 운빨.**
- 근본: median이 거의 전부 2.0(포화)이라 cand가 **worst-case/variance 항에 지배** = "이번 run에 어느 rep이 우연히 1점 맞았나"를 측정. 그게 랜덤 분포라 winner flip. (formula 버그 아님 — 분리 가능한 signal 자체가 없음을 충실히 반영.)

## C. aggregate는 안정 (장비 검증)
축 히스토그램 R1 vs R2(2/1/0): claim 43/1/0 vs 43/2/0 · caveat 44/0/0 vs 45/0/0 · register 39/5/0 vs 42/3/0 · protected 44/0/0 vs 45/0/0 · conci 37/7/0 vs 39/6/0. → **전체 품질 수준은 run간 안정**(고품질), 0점 전무. 1점이 **어느 variant에** 떨어질지가 랜덤일 뿐. pass-rate도 R1 44/45·R2 45/45(new-number 실패 재현 안 됨=stochastic).

## D. 함의 / 권고
1. **R1 winner(B2/M2/T1)를 persona profile 기본값으로 승격 금지** — 재현 안 됨. T3를 "나쁘다"고 가지치기도 금지(R2서 만점).
2. **Codex 계획 재고**(LEDGER_227 line47의 "B2/B3 held-out·M2/T1 neighborhood·T3 회피")는 R1 단일 run 기반이라 **premature** — R2가 그 전제를 falsify. held-out(B2 vs B3)도 지금은 moot(B2가 R2서 하락).
3. **두 갈래**: (a) "전 variant가 품질 동등·안전 → persona별 아무거나 stylistic 취향으로 채택"(pool이 uniformly good), OR (b) **장비 하드닝 후 재선정**(내 proposal 9997d6d: over-reach 미끼·약-evidence·protected 트랩·register 압박 task + rubric 0–3 + N↑ + 2nd-judge)로 noise floor 위로 올린 뒤에만 선정 신뢰.
4. **재현성 2-run 체크를 표준 게이트로**: "같은 set 2회 → winner 일치?"를 선정 신뢰 전 필수 관문으로. 이번 R2(operator가 "완주시켜라" 한 것)가 바로 그 관문이 되어 R1 선정을 falsify함 = 장비검증의 모범.

## 정직/큐
라이브=R2 cross-check + 45-agent blind 채점(repo 밖 local response read·variant blind) + R1/R2 비교 + objective 교차검증(카운트만). resolved 값/prose 0 노출·0 커밋. 채점 후에만 REVEAL. manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 다음: operator/Codex가 (a) "all-good 채택" vs (b) "하드닝 재선정" 택1 대기. held-out은 하드닝 후로 보류 권고.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose 미노출·미커밋·count/점수만.)
