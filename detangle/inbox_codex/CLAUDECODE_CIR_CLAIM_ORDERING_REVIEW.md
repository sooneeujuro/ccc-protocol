# Claude(Code) — CIR claim-ordering / reverse-outline 독립검토 (LEDGER_254)

`2026-06-19 19:4x` · LEDGER_254: CIR Discussion을 4 claim-node 순서로 확장(reverse-outline). 다음 B/M/T run 전 ordering 로직 검토 요청. **데이터 없는 argument-architecture 검토**(claim 구조/altitude/순서 논리만, resolved 값 0). 4질문 직답.

VERDICT: **순서 자체는 건강. implication-maximizing이 too-interpretive 아님 — 단 node1(regional mantle frame=Kim2017)이 '우리 claim 아닌 기존 외부 context'로 분명히 frame될 때만(이게 안전 hinge). decoupling은 두 order 다 H2/CH4·He 뒤=논리적으로 맞음. 다음 run 최강 게이트=fluid-to-rock petrogenesis overreach(node4+synthesis의 새 attack surface; 운영자 rock=context only). 다음 run=A/B 둘 다(검증장비+싼 run, 결정기준=동일-or-낮은 overreach에서 더 높은 implication).**

## Q1. implication-maximizing이 too-interpretive인가? → 아니오(조건부)
- 핵심: implication-max의 **node1 = "regional mantle heterogeneity frame(Kim2017)"은 기존 외부 context**지 이 논문 claim 아님. Discussion을 established context로 열고→데이터→해석→synthesis로 가는 건 정당하고 종종 강한 구조.
- **안전 hinge = node1 framing**: "Kim2017이 CIR mantle heterogeneity를 established → 우리 fluid He가 이와 align[관찰]"이면 OK. "mantle이 heterogeneous하니까 우리 데이터가 X를 보여야"면 circular(narrative-fitting). → node1을 **외부 frame, 우리 결론 아님**으로 명시하면 too-interpretive 아님.
- 잔여 리스크는 **optical**: 큰 frame으로 열면 reviewer가 "결론부터 깔고 데이터를 맞췄다"로 읽을 수 있음. conservative data-first는 이 optics에 더 강함(데이터→bottom-up→synthesis last, narrative-fitting 공격 어려움). 단 implication이 덜 살 수 있음. → Q4의 A/B로 실측 권고.

## Q2. decoupling node는 H2/CH4 diagnostic 앞? 뒤? → 반드시 뒤 (두 order 다 이미 맞음)
- decoupling(node3)은 **H2/CH4 tracer와 He tracer 사이의 관계**. 두 대상을 다 소개한 뒤에야 "decouple한다" 주장 가능. → H2/CH4 AND He 둘 다 제시 후에 와야.
- implication-max: He(2)→H2/CH4(3)→decoupling(4) ✓. conservative: H2/CH4(1)→He(2)→...→decoupling(4) ✓. **두 order 다 decoupling을 양쪽 뒤에 둠=논리적으로 정확.** 변경 불요.
- ⚠️ decoupling framing 주의: "weak correlation이 feature다"는 spin(null result 미화)으로 공격받음. **"부분 decoupling은 두 tracer가 서로 다른 reservoir/process(hydrothermal gas-generation vs mantle source)를 sample하면 *예상되는* 것"**으로 frame해야 strength가 됨. 이 해석적 정당화가 node3/5의 안전선.

## Q3. 다음 run 최강 게이트는? → fluid-to-rock petrogenesis overreach (+ 기존 2개 유지)
- 3 후보 중: causality overreach·all-site abiotic-H2 overreach는 take01 게이트에 이미 인코딩(705 통과). = 검증된 가드, 유지.
- **새 attack surface = node4(Kim2017 mantle heterogeneity alignment) + node5(two-layer architecture synthesis)**. node4는 fluid He를 rock-based mantle heterogeneity와 비교 → **fluid 데이터가 rock/petrogenesis claim으로 넘어가는 유혹**. 운영자가 "rock=context only"라 명시했으므로 이게 **이번 확장의 가장 위험한 신규 overreach**.
- → **최강 게이트 = fluid-to-rock petrogenesis overreach**: fluid 데이터로 rock/petrogenesis 단정 금지(Kim2017은 *비교 context*지 derived rock claim 아님). forbidden 후보: "fluids prove/require [rock/petrogenesis/source-rock]", "fluid He demonstrates mantle [composition/lithology]", Kim2017을 우리 결과로 흡수하는 표현.
- 동시에 **node5 synthesis 게이트**: "two-layer volatile architecture"는 **interpretive로 유지**("may record"/"is consistent with" not "records"/"is"/"establishes"). synthesis가 node1-4를 결합만 하고 새 주장 안 만들어야(Conductor no-new-claim과 동일).
- 기존 causality(node2 MBAR)·all-site abiotic(node1) 게이트는 그대로 유지(빼지 말 것).

## Q4. implication-max / conservative / A/B? → A/B 둘 다
- 검증된 장비 + 싼 run이 있으니 **순서를 추측 말고 실측**(좋은 장비 ethos). 두 order로 B/M/T+Conductor 돌려 내가 둘 다 채점.
- **결정 기준(명시)**: implication-max가 conservative 대비 (a)claim_altitude/implication 더 높고 (b)overreach/circularity 플래그가 동일-or-더 낮으면 → implication-max 채택. (a)는 높은데 (b)도 높으면(circularity·rock-overreach 증가) → conservative 채택. 즉 **"동일 안전에서 더 높은 implication"**이 선택 규칙.
- A/B 채점축: claim_altitude_two_sided·node별 caveat survival·**fluid-to-rock overreach**·causality·all-site-abiotic·decoupling-as-spin·synthesis no-new-claim·reviewer-2 survival. + node1 framing이 external-context인지(circularity 체크).

## 정직/큐
라이브=claim-ordering 로직 독립검토(데이터 값 0, argument 구조/순서/안전선만). 운영자 입력(데이터/G:\) 미접근. resolved 값/prose/캡션 0. manuscript-atelier 커밋0. ccc file-specific add. 다음=Codex A/B run(2 order)→내가 둘 다 채점(fluid-to-rock 게이트 최강+기존 가드 유지). 미해결: A/B run·705 biology 보강·df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
