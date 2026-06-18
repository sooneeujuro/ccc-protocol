# Claude(Code) — harder task + 0-3 rubric 설계 스펙 (operator (b) 결정 반영)

`2026-06-18 15:2x` · operator 결정=(b) 하드닝: 무작정 45-run 중단(R3=포화/노이즈 재확인 입증, 060329Z R4 의도적 6/45 중지). 다음=새 task/rubric으로 변별력 생성 후 45-run. 본 노트=그 빌드 스펙(값은 Codex instantiation·value-free 구조 설계). proposal 9997d6d를 actionable하게 구체화.

## 0. 실험 설계 원리
변별 병목=task/rubric(NOT variants; evolved가 오히려 spread 0.619→0.213로 줄임). 따라서 **variant set은 round1 원본 9개 재사용**(B/M/T 각 3축, 깨끗한 axis 변주)하고 **task를 하드닝 + rubric을 0–3**으로. 그래야 "어느 persona-전략이 난도 압박에서 버티나"가 분리됨. (evolved set은 가드로 균질화돼 변별 실험엔 부적합.)

## 1. 0–3 rubric (핵심 instrument 업그레이드)
현 0–2는 41/45가 2 만점=ceiling 포화. **3=탁월 tier 추가**로 현재 전부-2 덩어리를 가름. protected는 **scored 축에서 빼고 hard gate로**(이미 byte-exact 강제·항상 2=무변별). 대신 **새 변별 축(evidence_binding)** 추가.

**SCORED 축 (각 0–3, semantic·negation-aware):**
- `claim_altitude` (양방향): **3**=licensed 함의를 **정확히 한계선까지** 최대 강도+tight bound(과장0·under0). **2**=강하고 bounded이나 warranted force 일부 남김(보수적) 또는 bound 약간 느슨. **1**=눈에 띄게 under(timid) 또는 over(license 초과). **0**=vague(거의 무내용) 또는 overclaim(proof/mechanism/causation).
- `caveat_integration` (구 caveat_survival): **3**=caveat가 **claim 문장에 woven**(scope만 좁히고 claim 동사는 문법적 중심·affirmative 유지=operator "caveat가 main claim 안 죽임"의 최상). **2**=claim-then-caveat(순차, claim 생존하나 caveat 별도 절). **1**=caveat가 claim 부분 smother. **0**=caveat-front 또는 claim 매장.
- `register_fit`: **3**=top-journal Discussion 문단(data→interp→bounded implication·apology 없는 caveat). **2**=견고하나 약간 평이. **1**=results-recitation/over-apologetic로 미끄러짐. **0**=잘못된 register.
- `evidence_binding` (**NEW 변별 축**): 각 claim이 **그것을 license하는 특정 evidence에 명시적으로 결박**됐나(generic gesture 아니라). **3**=모든 claim이 licensing datum에 결박. **2**=대체로 결박, 1건 느슨. **1**=절반은 떠 있음. **0**=claim이 evidence와 분리(현 rubric이 못 잡던 차원 — 전 variant가 "데이터 쓰나" 결박 정밀도가 다름).
- `conciseness_vs_completeness`: **3**=모든 문장이 evidence/claim/limitation 운반·filler0·essentials 전부. **2**=견고·약간 padding. **1**=padded 또는 thin. **0**=essential 누락 또는 과다 padding.

**HARD GATE(scored 아님, fail시 해당 run discard+pass_rate 감점):** candidate gate · protected byte-exact · no_new_numbers · FGP overlap-guard · (new) **affirmative overclaim 0**(forbidden-verb affirmative=즉시 fail, negation-aware).

## 2. harder task 레시피 (Codex instantiation, value-free 구조 지시)
같은 Lee2025 Ulleungdo 소재 유지하되 난도 압박 4종 주입(실제 문장/값은 Codex):
- **M1 over-reach 미끼**: evidence에 **인과처럼 보이는 상관/증명처럼 보이는 overlap**을 1개 배치(게으른 수는 "X causes Y"). licensed 함의는 "consistent with/indicates"로 고정. → 미끼 무는 variant claim_altitude 0–1, 저항 3.
- **M2 약-evidence calibration**: 한 sub-claim을 **명시적 약·부분 증거**(작은 n·넓은 범위·단일 sample)로만 뒷받침. 적절 hedge=3, 과신=1, 과hedge(vague)=0.
- **M3 protected near-miss 트랩**: protected term을 **paraphrase 유혹** 문맥에 배치(풀어쓰기 쉬운 자리). byte-exact 보존이 비자명 → 실패는 gate-fail로(=pass_rate 변별).
- **M4 register 압박**: **다수 수치 동시 제공 + "Discussion이지 Results 재낭독 아님" 명시**. register_fit·conciseness를 부하 하에서 시험.
- (선택) SCLM 함의 over-reach 유혹을 R1보다 강하게(여전 "not proof of unique process").

## 3. 운영 강화 (noise floor 위로)
- **N=8**(R1~3는 N=5; flip은 N5 노이즈 탓). per-variant 분포 tighten.
- **2nd 독립 judge**: 어떤 축이든 <3 받은 response는 2nd judge로 재확인(변별 case의 single-judge 노이즈↓; 만점은 1-judge). (Claude 측 Workflow에서 처리.)
- **2-run 재현성 게이트(필수)**: 하드닝 task도 **2회 run → winner 일치해야 신뢰**(R1↔R2 flip 교훈, 이젠 표준 관문).
- 동률(<ε)이면 held-out task로 분리.
- blind/response-only/leak 규율 전부 유지.

## 4. 빌드 분업
- **Codex**: (a) harder task instantiation(M1~M4, 값 포함, RESOLVED). (b) runner/wrapper에 0–3 rubric 메타 반영(blind manifest `score_axes`에 evidence_binding 추가·protected→hard_gate로 이동). (c) N=8 지원. (d) **runner DRY갭 수정 동반**(`_FORBIDDEN_BLIND_STRINGS`를 `VARIANT_PRESETS`/`_RELAY_FORBIDDEN_VARIANT_TERMS`서 파생 — 미해결 건).
- **Claude(나)**: blind 채점 Workflow를 0–3 schema(enum [0,1,2,3])+새 rubric 프롬프트+evidence_binding 축으로 갱신, cand 공식 0–3 스케일로(예 cand=median−λ·var−μ·(3−worst)), 2nd-judge on <3, detector 라벨/RD 갱신. cross-check→채점→2-run 재현성 비교→점수만 노트.
- **operator**: harder task 값/난도 승인, GO.

## 5. 성공 기준
하드닝이 성공이면: (1) 축 비-3 비율↑(특히 claim_altitude·evidence_binding가 미끼/약-evidence에서 갈림), (2) cand spread/stdev가 R1~3(0.07~0.19)보다 **유의하게 큼**, (3) winner가 **2-run 재현**. 셋 충족시에만 persona profile 기본값 승격. 안 되면=이 소재론 변별 불가→(a) all-good 채택으로 회귀.

## 정직/큐
값 미instantiation(구조 설계만, resolved 값/prose 0). proposal 9997d6d 구체화. manuscript-atelier 커밋0. ccc file-specific add. 다음: operator 승인 + Codex 빌드(task+0–3 runner+DRY갭) → 내가 채점 장비 갱신 → 새 45-run(×2 재현성) 채점.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose 미노출·미커밋.)
