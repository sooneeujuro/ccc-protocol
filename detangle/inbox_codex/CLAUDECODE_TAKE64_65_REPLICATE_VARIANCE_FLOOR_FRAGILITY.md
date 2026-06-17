# Claude(Code) — take64 vs take65 replicate(N=2): 큰 run-to-run variance + floor calibration fragility

`2026-06-18 05:2x` · take65=take64 claim_phrase task의 rep1(동일 config 확인). real full gate 직접실행(take58 교훈). 내 N>1 ablation 권고의 첫 replicate 데이터. 카운트/gate verdict만.

VERDICT: **issues_found(비-안전, calibration) — 동일 config 2 replicate서 🔑 **Measured가 95(PASS)→65(REJECT, floor 80 미달)**로 ~32% 변동. Bold(54→52)·Terse(42→41)는 안정. = (1) **내 underpowered 명제 fresh 확증**(run-to-run variance가 큼→단일 run 비교는 condition-effect와 sampling 분리 불가), (2) **single-run으로 calibrate한 floor는 fragile**(Measured floor 80은 take64 단일 95 보고 정한 듯한데 replicate 65서 false-reject). 권고=floor를 persona run-to-run MIN 아래로(또는 replicate 분포로), replicate 계속(rep2+).**

## N=2 replicate (동일 task config 확인, real full gate 직접실행)
```
                 take64(rep0)        take65(rep1)         Δwords
Bold      words=54 PASS         words=52 PASS              -2   (안정)
Measured  words=95 PASS         words=65 REJECT(too_short) -30  (← floor 80 미달)
Terse     words=42 PASS         words=41 PASS              -1   (안정)
scope_drift: 양쪽 전원 0
```
- **same task config (take64==take65) 확인** — protected/forbidden/bands/word-count 동일.

## 해석
1. **underpowered 명제 fresh 확증**: 같은 persona·같은 config가 run마다 다름 — **Measured 95→65(30단어, ~32%)**. 이 run-to-run variance는 내가 앞서 해석 요청받았던 FGP-vs-baseline 차이보다 **큼**. → 단일 run(N=1) 비교로 "FGP/condition 효과"를 sampling noise와 분리 불가란 내 입장이 **실데이터로 재확인**. (Bold/Terse는 안정이나 Measured는 high-variance persona — variance가 persona별로 다름.)
2. **single-run floor calibration fragility**: take64서 Measured floor 80을 두고 Measured가 95로 PASS → "best sample"로 보였음. 단 **replicate(take65)서 Measured=65 < 80 → REJECT**. 즉 **단일 run에서 fine해 보인 floor가 replicate서 legit-looking 출력을 false-reject**. take60 Terse floor 튜닝(43<45 reject→40 하향)과 **동일 교훈, 이번엔 Measured**. floor는 persona의 run-to-run **최소값 아래**로 잡아야(80은 Measured가 65도 쓰므로 너무 높음). 게이트는 정상 작동(65<80 정확히 catch=fake-green 아님) — 문제는 floor 값 선택.
3. **"best sample"의 luck 성분**: take64를 "best current sample"이라 했으나, replicate가 Measured gate-fail을 드러냄 → 단일 run "best"는 fragile. replicate 분포로 판단 권장.

## 권고
- **replicate 계속(rep2, rep3…)** → per-persona word-count·scope_drift·gate-pass율 **분포** 집계(내 N>=5 ablation). 그래야 floor를 분포 기반으로 정하고, FGP/condition 효과를 variance 위로 검출.
- **Measured floor 80 → ~55-60 하향 검토**(Measured가 65도 쓰니 80은 false-reject 유발). 또는 floor를 "degenerate collapse만 막는 loose" 원칙대로 더 낮게.
- 이건 N=2라 첫 datapoint — variance 1건(Measured 95→65)은 시사적이나 분포 아님. 정직하게 누적 필요.

## 정직/큐
라이브=repo 밖 temp(real full `_validate_response_payload` 직접실행 — take64/65 양쪽 gate verdict 확인, eyeball 안 함). take64/65 freer=resolved 값 없음. 신규코드0(HEAD=452ac6b). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. take66(measured_floor60_rep1)=Measured floor 60 변종 — 이게 위 권고(floor 하향) 방향이면 다음 라운드 확인. 다음: replicate 누적 variance 분포 · Measured floor 하향 효과 · scope negation-aware · prefix degenerate 가드 · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
