# Claude(Code) — BMT v3 Abstract 재런(profile v3) 채점: v2 대비 Bold delta

`2026-06-19 00:5x` · Abstract profile-v3 재런(`bmt_v3_abstract_profile_v3_20260619T002842`, N=5×B/M/T=15) 독립채점(judge2, repo-밖 클린 paragraph_md). 목적=Bold v3(timidity fix)가 claim 올렸나 + overclaim 안 생겼나, Measured/Terse 회귀 없나. v2 baseline(bfee932)과 비교. 점수/카운트만.

VERDICT: **v3 = 안전한 marginal 개선이지 결정적 fix 아님. Bold claim +0.20(2.30→2.50)·Terse +0.10(→3.00)·Measured flat, both-judge 확정 위반 0·caveat 15/15·protected 15/15·예산 15/15. 단 delta가 N=5 noise 내 + Bold가 push되며 mechanism-framing(degassing/transport) flutter(split-judge causal 2건) 유발. → v3 baseline 수락 가능하나 Bold fix 과신 금물. 권고: 다음 섹션(Intro/Results)으로 breadth, Bold flutter는 재발시 대응.**

## A. v2 vs v3 (claim_altitude / composite)
```
persona | v2 claim -> v3 claim (Δ) | v2 comp -> v3 comp (Δ)
Bold    | 2.30 -> 2.50 (+0.20)    | 2.63 -> 2.70 (+0.07)
Measured| 2.80 -> 2.80 ( 0.00)    | 2.73 -> 2.78 (+0.05)
Terse   | 2.90 -> 3.00 (+0.10)    | 2.88 -> 3.00 (+0.12)
```
- v3 Bold vals=[2.0,3.0,2.0,2.5,3.0] — 두 rep 3.0 도달(개선)이나 두 rep 여전히 2.0(timid). **분산 큼=bimodal, 여전히 최약.** v2 vals=[1.5,2.0,2.5,2.5,3.0]와 분포 크게 겹침 → +0.20은 N=5 noise 내.
- safety(둘 다 v2·v3): caveat_survival 15/15=3.0·protected 15/15=3.0·단어예산 15/15 OK·게이트 fail 0·**both-judge 확정 플래그 0**.

## B. v3 신규 flutter (전부 split=j 한쪽만, 확정 아님)
```
causal_verb_used: 2  (401 Bold j2, 403 Bold j1)   <- v2엔 0이었음
overclaim_affirmative: 1 (403 Bold j1)
new_number: 2 (405 Bold, 405 Measured)
```
- **causal flutter 정체**: 401/403 Bold 문단에 **게이트 목록 동사 0개**(drive/cause/control 등 없음) — 대신 "degassing"/"transport"(메커니즘 명사/동사). 즉 게이트 누락 아님(그건 forbidden 아님), **Bold를 ladder 상단으로 밀자 mechanism-framing으로 손 뻗음** → 엄격 judge가 "asserts degassing/transport mechanism = soft causal overreach"로 읽음. 반대 judge는 bounded로 봄(split). 게이트-forbidden도 both-judge도 아닌 경계.
- 403 Bold: j1 overclaim+causal true, j2 둘 다 false(claim 3) — 같은 문단 두 판정 갈림 = 경계의 전형.

## C. 판정 (calibrated)
1. **Bold v3 lever = 약하고 결정적이지 않음**: +0.20은 N=5 noise 내(v2/v3 분포 겹침). 토너먼트 교훈(단일 소규모 run의 작은 delta는 반복으론 안 풀림) 적용 — "v3가 Bold 고쳤다"고 단언 못 함.
2. **안전 회귀 없음**: both-judge 확정 위반 0, caveat/protected/예산/게이트 다 통과. Terse→3.0, Measured flat. v3는 v2보다 나쁘지 않음.
3. **단 push의 비용**: Bold mechanism-framing flutter(degassing/transport, split 2건)가 v2엔 없던 신호. "강한 claim"을 올리니 "과장 없는"의 경계를 살짝 건드림 — 운영자 핵심 긴장의 실측. 경계지 확정 아님.

## D. 권고
- **v3 baseline 수락 OK**(회귀 0, marginal+). 단 Bold fix 효과는 과신 말고 watch로.
- **다음=새 섹션(Intro=result-leak / Results-adjacent=interpretation-overreach)으로 breadth.** 이유: Abstract-Bold는 noise floor라 같은 task 반복으론 정보 안 남(토너먼트 교훈), section suite의 가치는 폭. Bold mechanism-flutter가 다른 섹션서도 재발하면 그때 Bold 경계 강화(do_not: "degassing/transport를 asserted mechanism 아닌 bounded pathway로"). 한 섹션 단발 split로 지금 프로필 또 건드리는 건 premature.
- (게이트 follow-up however/whereas·neither는 별건으로 유지.)

## 정직/큐
라이브=v3 클린 paragraph_md 15개 dv2 채점(judge2, repo-밖) + Bold causal-flag 정체확인(게이트목록 대조=목록밖 mechanism어). v2 대비 delta=noise 내로 calibrate(과신 거부). resolved 값/prose/캡션 0 노출·0 커밋. manuscript-atelier 커밋0. ccc file-specific add. 미해결: 다음 섹션 선택·게이트 follow-up·df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
