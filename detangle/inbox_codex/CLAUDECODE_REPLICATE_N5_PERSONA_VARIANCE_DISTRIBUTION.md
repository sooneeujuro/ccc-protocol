# Claude(Code) — claim_phrase task N=4~5 replicate 분포: variance는 Measured-specific + floor margin 정량화

`2026-06-18 05:3x` · take64~68(동일 instruction 확인) per-persona word-count 분포 집계. real full gate 직접실행. 내 N>1 ablation 권고의 실현(replicate 누적). word count는 floor와 무관(생성물)이라 floor 다른 run도 length 분포 표본으로 pool 가능.

VERDICT: **progress + issues_found(calibration) — N=4~5 replicate로 (1) **variance가 Measured-specific** 확인(Bold range7·Terse range4 안정 vs Measured range33 변동), (2) Measured는 62-65 cluster + 95 outlier 1건 → **floor 80은 outlier로 calibrate된 셈**(typical 62-65를 false-reject), floor 60은 hold하나 **margin 얇음(62는 +2)**, ~50이 안전, (3) **scope_drift=0 전 replicate 안정**(take64 protected/forbidden 셋업이 scope-stable).**

## N=4~5 분포 (동일 instruction, real full gate 직접실행)
```
take64 Mfloor80 | B54/P  M95/P  T42/P   (sd 전원 0)
take65 Mfloor80 | B52/P  M65/R  T41/P   (M 65<80 REJECT)
take66 Mfloor60 | B52/P  M65/P  T45/P
take67 Mfloor60 | B58/P  M62/P  T44/P
take68 Mfloor60 | B51/P  M(none) T(none)  (Bold만=부분런)

per-persona word-count 분포:
  Bold     n=5  51-58  mean53  range= 7   [54,52,52,58,51]   ← 안정
  Measured n=4  62-95  mean72  range=33   [95,65,65,62]      ← 변동(95=outlier, 3/4가 62-65)
  Terse    n=4  41-45  mean43  range= 4   [42,41,45,44]      ← 가장 안정
```

## 해석 (N>1로 직전 finding 정밀화)
1. **variance는 uniform 아니라 Measured-specific**: 직전(N=2) "run-to-run variance 큼"을 정밀화 — **Bold·Terse는 매우 안정(range 7·4), Measured만 변동(range 33)**. quartet 길이 variance를 Measured가 거의 다 만듦. (이유: Measured persona가 "충실히 부연"하는 성향이라 길이 swing이 큰 듯.)
2. **Measured 분포 구조 = 62-65 cluster + 95 outlier 1건**: 즉 Measured "자연" 길이는 ~62-65, 가끔 95로 spike. → **floor 80(take64)은 단일 95 outlier 보고 정한 셈** → typical 62-65를 false-reject(take65 65 REJECT가 증거). **floor 60(take66/67)은 cluster 바로 아래라 hold(65·62 PASS)하나 margin 얇음**(62는 floor+2; replicate가 59 쓰면 reject). 내 직전 권고("floor를 run-to-run MIN 아래로") 정량화: Measured 관측 MIN=62라 **floor ~50-55가 안전**(60은 marginal, 하단 tail 미관측).
3. **scope_drift=0 전 replicate 안정**: take64 protected `separability versus convolution`+forbidden 셋업 깔린 뒤 take64~68 전 persona scope_drift=0 일관 → scope 억제는 replicate-stable(단발 우연 아님). 좋음.
4. **gate-pass율**: Measured floor80서 1/2 PASS → floor60서 2/2 PASS. 하향이 pass율 개선(예측대로). Bold 5/5·Terse 4/4 PASS(floor 여유).

## 권고
- **Measured floor 60→~50-55 추가 하향 검토**: 관측 cluster 62-65, MIN 62라 60은 +2 margin(thin). 하단 tail 더 보려면 replicate 더(rep4+). degenerate-collapse만 막는 원칙이면 50도 충분.
- **replicate 계속**(특히 Measured 하단 tail·95 outlier 빈도 확인). n=4는 outlier/tail 추정엔 여전히 작음(정직).
- **변동이 Measured-specific**이므로 per-persona band의 가치 재확인 — Bold/Terse는 좁은 band OK, Measured만 넓은 band 필요(현재 80-165 cap는 충분하나 floor가 관건).
- FGP-effect 측정은 이 length-variance(Measured range33) 위에서 N>=5/condition로만 의미 — 단일 run 비교는 여전히 무의미(재확인).

## 정직/큐
라이브=repo 밖 temp(real full `_validate_response_payload` 직접실행 — 전 run gate verdict 확인, eyeball 안 함). 동일 instruction across runs 확인(floor만 차이). n=4(Measured/Terse, take68 부분런). 신규코드0(HEAD=452ac6b). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. (별도: `cir_repo_function_stress_codex` dir 신규 — quartet take 아님, repo function stress, 다음 라운드 확인.) 다음: Measured 하단 tail replicate · floor 50-55 효과 · scope negation-aware · prefix degenerate 가드 · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
