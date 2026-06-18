# Claude(Code) — hard-task pilot discriminating_v2 0-3 blind scoring result (LEDGER_231)

`2026-06-18 17:1x` · 064019Z(harder task·round1 variants·discriminating_v2 0-3·N5) 43 passed를 blind 채점(judge1 43 + **2nd-judge on <3 전원 43**, variant blind) → REVEAL → 분포·변별력·winner. 점수/카운트만(resolved 값/prose 0).

VERDICT: **🎯 하드닝 성공(부분) — 변별력이 생겼고 정확히 operator 2대 핵심축(claim_altitude·caveat_survival)에 집중. 단 full-6축은 4축 포화로 희석. winner는 N5 단일 run이라 2-run/N8 재현성 전엔 미확정. judge2가 judge1 확증(87% exact).**

## A. judge 신뢰성 (2nd-judge 효과)
judge1 vs judge2: **exact 224/258(87%)·mean|diff|=0.13·max|diff|=1**. → 채점은 judge-noise 작음(신뢰 가능). 0-3에서 전원이 어떤 축이든 <3 받음(=3은 "merely-safe보다 강할때만" 규칙대로 희소) → judge2 전원 발동.

## B. 🎯 변별력 = 생겼다, 핵심축에 집중 (scale-normalized stdev)
```
R3(easy,evolved)        0.035
R2(easy)                0.060
dv2 full-6축            0.065
R1(easy)                0.094
dv2 claim+caveat 전용   0.118   ← 전 라운드 최고
```
- **claim_altitude_two_sided**: 3=17·2=26 (**26/43이 <3**) → 0-2에선 전부 max였던 게 이제 3 vs 2로 갈림. **caveat_survival**: 3=10·2=27·1=6 (**33/43 <3**) → 갈림. = operator 2대 우선순위(과장없는 강한claim·caveat 안죽임)에서 실제 변별.
- **포화(희석원)**: bound_tightness 39/43=2(named bound 거의 0), register 40/43=2, protected 42/43=3(gate라 당연), conciseness 38/43=2. 이 4축이 full-6축 composite를 희석 → full normalized(0.065)는 중간, **claim+caveat만(0.118)은 최고**.
- **함의**: cand를 claim_altitude+caveat_survival에 집중(나머지는 gate/floor로) 하면 변별이 2배 선명.

## C. winner (claim+caveat 전용, full-6축과 순위 일치)
```
Bold:     B3_test_framed(1.96) > B1_licensed_max(1.65) > B2_caveat_survivor(0.94)  ← B2 급락
Measured: M3_caveat_front(1.92) > M2_woven_caveat(1.73) > M1_claim_then_caveat(1.23)
Terse:    T2_frame_bound(1.47) > T1_n_points(1.13) > T3_minimal_clause(1.08)
```
pass_rate: B1·M3 4/5(미끼 fail 1씩), 나머지 5/5. T3는 5/5지만 점수 최하.

## D. 교차-라운드 신호 (다른 task라 약하나 시사적)
- **T3_minimal_clause = R1 최하 + dv2 최하**(robust loser, 과압축이 easy/hard 둘다 약함). → 안전하게 드롭 가능.
- **M3_caveat_front = R2 winner + dv2 winner**(stable-ish strong).
- **B2_caveat_survivor = R1 best Bold → dv2 worst Bold(급락)**. 🔑 substantive: 하드닝(미끼) 하에선 **over-caveat 전략이 claim altitude를 깎음** — "caveat survivor"가 미끼 앞에서 과방어→claim 약화. 반대로 B3_test_framed(test로 frame)·B1_licensed_max(최강 licensed)가 강함. operator의 "caveat가 main claim 죽이면 안 됨"이 정확히 측정됨.
- **bait**: 물린 2건(Bold·Measured 각1)은 gate에서 forbidden_term으로 탈락, Terse 0 → **gate-level pass_rate 변별**. passed 중 took_overreach_bait=0(scorer).

## E. 한계 / 다음 (정직)
- **N=5 단일 run** — winner 미확정. 하드닝이 within-variant var를 **키움**(key축 var 최대 0.34, T3 0.34/M1 0.29) = task가 진짜 변별하니 rep마다 달라짐 → **N이 더 중요**해짐. R1↔R2 flip 교훈상 N5 단일론 winner 신뢰 불가.
- **권고**: (1) cand를 **claim_altitude+caveat_survival 중심**으로(포화 4축은 floor/gate로; protected는 이미 gate). (2) 그 다음 **N=8 + 2-run 재현성**으로 winner 확정(이번에 변별 신호 확인됐으니 이제 N8 투자가 정당 — 직전 운영자 논의대로 "신호 있으면 N10도 OK"). (3) **T3_minimal_clause 드롭**(easy+hard 둘다 최하). (4) Bold는 B3/B1가 후보, B2 제외 검토.
- objective(전수, 카운트만): overclaim-aff 0·protected drift 1(=M3 near-miss 1건, gate 0점 처리됨)·meta 0·took_bait 0(passed). 

## 정직/큐
라이브=43 2-judge blind 채점(repo 밖 local read·variant blind) + key-축 재집계 + 교차라운드 비교 + cross-check. resolved 값/prose 0 노출·0 커밋. 채점완료 후 REVEAL. manuscript-atelier 커밋0. ccc file-specific add. 다음: operator 결정(N8+2-run 갈지) · cand 재가중(claim+caveat) 합의 · T3 드롭.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose 미노출·미커밋·count/점수만.)
