# Claude(Code) — profile v2 held-out smoke test VERDICT (LEDGER_237)

`2026-06-18 21:2x` · v2 held-out run 112008Z(take87 magmatism, B/M/T×10, 30 문단) dv2 0-3 채점(judge1+judge2; reboot로 1차 채점 죽어 재실행). 목적=v2가 Lee task 과적합/과조심/말라붙음 아닌지(variant 비교 아님). 점수/카운트만(prose/값 0).

VERDICT: **v2 = 안정적으로 좋음. operator의 "과조심/dried" 우려 반증(claim_altitude timid 0%, register/conci 1점 0건). 오히려 bound_tightness 개선. 유일 이슈=Measured 1/30 eruption-bait over-reach(과조심 반대방향). Conductor는 이 run 미포함=tie-breaker 별도 검증 필요.**

## A. 채점 신뢰성
30/30 채점(judge2 24건 발동). judge1/2 exact 109/144(76%)·mean|diff|0.25(2↔3 경계 soft, big signal은 robust). reboot 후 재실행(데이터 손실 0, 30 md 디스크 보존).

## B. 🎯 과조심 탐지 = 반증 (claim_altitude_two_sided)
```
3(full strength)=12  2(some force left)=17  1(timid OR over)=1  0=0   /30
```
- **timid 0%**(유일 1은 timid 아닌 over-reach). 12/30 최대강도. → v2는 claim 세게 유지, 말라붙지 않음.

## C. persona 분포 (composite 0-3, judge-avg) + 축
```
Bold     comp 2.66 (med 2.62 worst 2.33) | claim2.30 bound2.65 cav3.00 reg2.60 prot3.00 conc2.40
Measured comp 2.57 (med 2.54 worst 1.83) | claim2.30 bound2.60 cav2.90 reg2.40 prot2.90 conc2.30
Terse    comp 2.73 (med 2.67 worst 2.42) | claim2.55 bound2.95 cav2.90 reg2.50 prot3.00 conc2.45  <- 최고(T2 승격)
```
축별(30, judge1): caveat_survival 28/30=3(woven 생존)·protected 30/30=3(1.37Ma 포함 byte-exact, drift0)·**bound_tightness 24/30=3**(토너먼트 땐 ~all-2 포화였음→v2 "정확 limit 명시" 지침 실효)·register 14×3/16×2·conci 12×3/18×2(**어색/dried 1점 0건**).

## D. 유일 이슈 (1/30)
Measured rep(gemma-quartet-...12427Z): **eruption 예측 미끼 물림**(eruption-recency frame + affirmative magmatic-influence, claim_altitude=1, 두 judge 다 eruption_or_causal_overreach=true). = 과조심 아닌 **over-reach**(토너먼트의 "claim-pushing persona 가끔 bait" 패턴이 새 bait서 1회 재현). protected_drift 0·missing_essential 0.

## E. verdict / 권고
- **v2 default 유지 OK**: held-out(다른 Lee task=magmatism)서 timid/dried 안 됨, 일반화 확인, bound_tightness는 오히려 개선. profile v2 promotion(c7e3b06) 정당.
- **잔여 리스크**: Measured eruption-bait 1/30(노이즈 내). 재발 추이 보고, 재발하면 Measured/Conductor do_not에 eruption-예측 가드(이미 forbidden_terms엔 있으나 register-level 유도 추가) 고려. 지금 당장 조치 불요.
- **미검증=Conductor**: 이 run은 B/M/T만(stitch 출력 없음). 새 tie-breaker(claim altitude+caveat survival)·Conductor 새주장0은 **별도 stitch run 1회**로 확인 권고(B/M/T 드래프트 → Conductor merge 출력 채점).
- 한계: N=10 단일 held-out=smoke test 1회. 더 강한 확신 원하면 다른 held-out task 1개 더(easy/hard 섞어) 또는 2-run.

## 정직/큐
라이브=v2 30 md 2-judge 채점(repo 밖 local read) + 분포/flag 집계. reboot 1차 채점 실패는 STATUS 사유기록 후 재실행(우회 아님). resolved 값/prose/캡션 0 노출·0 커밋. manuscript-atelier 커밋0. ccc file-specific add. 미해결: df052b0 leak(MISSING_FIGURES.json) 대응 · Conductor stitch 검증 run · operator 다음.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
