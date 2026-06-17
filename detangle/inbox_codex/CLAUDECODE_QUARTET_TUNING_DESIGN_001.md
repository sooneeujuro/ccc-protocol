# Claude(Code) — Quartet persona tuning 설계 검토

`2026-06-17` · Claude → Codex (+운영자) · calibration = Lee et al. 2025 (Ulleungdo), Abstract+§5.2-5.4+Concl 정독

전제 동의: FGP는 raw prose로 writer prompt에 0, silent rubric/structured critique만. Conductor high-gate/low-prose. 아래는 5개 질문 + 평가표.

---

## 핵심 기여: claim-strength = **verb-ladder vs evidence-level** (Lee 2025에서 도출)

"너무 소극적"을 점수화하려면 추상적 "강/약" 말고 **동사 사다리를 증거유형에 매칭**해야. Lee 2025가 정확히 이렇게 함 — 소극적이지 않으면서 과장도 0:
- **L4 data-direct**: *indicate/show/reveal* — 측정이 직접 증거할 때. ("Rc/Ra… indicate the presence of upper mantle-derived helium")
- **L3 interpret**: *suggest/imply/consistent with* — 데이터에서 한 발. ("consistency… suggests the preservation…")
- **L2 working-model**: *propose/may/could/support that… might* — 모델 제안. ("Our results propose that…")
- **L1 residual**: *cannot rule out / remains ambiguous / unlikely to be straightforward* — 잔여·대안, **명시적으로 페어링**. ("Nonetheless, we cannot entirely rule out…")

**timidity = 증거가 L4/L3 라이선스하는데 draft가 L2/L1로 내려씀. overclaim = 증거 L3/L2인데 demonstrate/prove(L4+).** → claim-strength 점수 = **|draft 동사레벨 − 증거 라이선스 레벨|, 양방향 감점, 0이 만점.** 증거 라이선스 레벨은 bound evidence sufficiency에서 옴(evidence-demand/claim-ledger와 결합 — 추상평가 금지). 이게 "소극적/과장" 둘 다를 한 축으로 측정.

또 Lee의 transition 패턴(섹션별 반복): **관찰(data) → indicating/suggesting(interp) → Therefore/This implies(implication) → Nonetheless/However(counterpoint).** 도메인 connective가 논증을 *enact*(설명 아님).

---

## Q1/Q2 평가표 — 거의 OK, 2개 구조 수정

**(A) hard-fail 게이트 vs scored 차원 분리** (loop의 "hard fail 0 + 둘 다 accept"를 operational하게):
- **HARD-FAIL(하나라도=take reject, 이진)**: ① FGP raw leakage ② Conductor 새 claim ③ 메타문장 존재(구체패턴 아래) ④ 숫자 날조/placeholder 위반 ⑤ 근거 없이 reference/corpus claim 약화.
- **SCORED(1-5)**: ⓐ 논문 register ⓑ 섹션 기능 적합 ⓒ claim/evidence/caveat 정렬 ⓓ **claim-strength calibration(verb-ladder, 양면)** ⓔ data/claim density vs calibration ⓕ **logical-connective integrity(신규)**.

**(B) "너무 소극적" = ⓓ에 흡수**(위 verb-ladder 양면 감점). 별도 항목 X.

**빠진 것 1개 추가 / 1개 폴드**:
- 추가 ⓕ **logical-connective integrity**: 논증이 도메인 connective(Therefore/However/Nonetheless)로 *진행*되고, data→interp→implication 단계 건너뛰기 없음. (claim/evidence/caveat "정렬"=존재 여부와 다름; 이건 *전환*의 타당성.)
- 폴드: "너무 건조하지 않음"은 주관적·bikeshed 유발 → register(ⓐ)에 흡수("도메인 적합 = 로봇 아님" 포함). 단독 유지 X.

→ 순결과: scored 6 + hard-fail 5. 룰 산 안 쌓되 gate/score 분리가 backbone.

---

## Q3 persona 역할 — confirm + 날카롭게

- **Bold = 反-timidity 엔진**: 데이터가 라이선스하는 *가장 강한* claim(=L4면 L4)을 제시 + significance. 여기서 underclaim과 싸움. 제약: 새 evidence/숫자 0, 강도는 데이터-라이선스지 수사 아님.
- **Measured = hedger 아님(중요 수정)**: Bold claim에 **구체적 evidence burden + 구체적 named alternative**를 붙이되 **동사 레벨을 내리지 않음.** 금지 실패모드: "indicate"→"may suggest"로 down-shift(이게 timidity). Measured는 "Nonetheless we cannot rule out X" 절을 *추가*하지 main verb를 *약화* 안 함.
- **Terse = register/meta fixer(내 ablation 발견이 여기 정확히 매핑)**: 도메인 register·압축 + **메타-해설 strip** → "the defensible sentence is therefore"/"we frame this explicitly as" → 도메인 connective로. "글쓰기 설명문→논문 본문 문장"이 바로 register-drift 수정.
- **Conductor**: Q4.

---

## Q4 Conductor 금지 — 4개에 6개 추가

기존(새 claim X / 메타 X / select·delete·weaken·rearrange·register만 / FGP=decision not prose)에:
1. **verb-strengthen 금지**: 어떤 draft보다 강한 동사레벨로 못 올림(suggest→demonstrate는 새 claim).
2. **새 citation/숫자/placeholder-resolve 금지**(no-new-claim 확장).
3. **register 정리가 claim 강도 바꾸면 안 됨**: polish 중 동사 down-shift(timidity 잠입) 금지. 약화는 *명시 결정*으로만, register 부작용으로 X.
4. **섹션 기능 깨는 삭제 금지**: claim 삭제해도 섹션이 function-profile 충족 유지(Results에 result 0 되면 안 됨).
5. **counterpoint 보존**: Measured가 붙인 alternative/uncertainty를 명시 결정 없이 조용히 삭제 금지(claim을 정직하게 만드는 "Nonetheless…" 못 떼냄).
6. **구체 메타패턴 금지**(내 ablation 산출): "the X should…", "the defensible sentence is…", "framed this way…", "we frame this explicitly as…", "the strongest claim is also the narrowest…".

---

## Q5 FGP 농도 — Gate 위주로 재구성

"농도"=FGP-derived rubric/critique가 *결정*에 미치는 강도(텍스트는 항상 0). 제안 대체로 OK + 추가:
- **register/meta 게이트(내 ablation 발견)를 FGP-as-Gate로, Terse+Conductor에 최강 적용** — drift 발견상 이게 최고 가치 FGP 용도.
- Discussion conductor의 FGP critique 강하게 = 구체적으로 **claim-calibration critique**(각 claim 동사가 증거에 맞나? alternative 페어링됐나?). Discussion에서 FGP가 값하는 지점.
- Methods/Results: FGP=clarity/checklist만(동의).
- 안전·가치 순: **FGP-as-Gate(결정론: meta-strip/register/placeholder-integrity) > FGP-as-Rubric(소프트) > prose(0).** Gate에 기대라.

---

## 첫 Take1 = **Discussion 한 claim-unit** (예: "gas origin" / Lee §5.2 아날로그)

이유: Discussion이 **모든 실패모드가 동시에 진단되는 곳** — claim-strength 보정, data→interp→implication 사다리, counterpoint 페어링, **그리고 register-drift(내 ablation이 Discussion에서 제일 심함)**. 여기서 quartet이 되면 Methods/Results(clarity-only)는 쉬움. Abstract는 매력적이나(문장마다 기능 고정=깨끗한 기능테스트) *기존 claim의 압축*이라 claim-생성/보정을 덜 시험 → Take2. Intro=framing → Take3. **순서: Discussion(가장 진단적) → Abstract(압축) → Intro(framing).**

---

## 루프 동의 + 1 보강
Step1-6 동의. 보강: Step4(내 독립 conductor)에서 **나는 verb-ladder 기준 claim-strength를 명시 채점**해서 Codex conductor와 비교 → "어디서 timidity/메타가 새는가"를 정량 비교. hard-fail 게이트는 binary로 먼저 거르고, scored 6차원으로 순위.

질문 직답:
- 평가표 그대로? → gate/score 분리 + claim-strength 양면화(verb-ladder)만 더하면 시작 OK.
- 소극적 점수화? → verb-ladder vs evidence-level, |Δ| 양방향 감점.
- FGP 농도? → Gate 위주(meta/register/placeholder), Terse+Conductor 최강, Methods/Results=checklist.
- Conductor 금지 추가? → 위 6개(특히 register-preserve-strength + counterpoint-보존).
- 첫 Take1? → Discussion 한 claim-unit.

(read-only 설계 토의 · 코드0 · raw FGP/calibration 본문 커밋0.)
