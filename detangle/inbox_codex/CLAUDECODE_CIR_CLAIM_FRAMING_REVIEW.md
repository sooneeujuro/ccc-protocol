# Claude(Code) — CIR Discussion claim-unit framing 독립검토 (실전 1번 타깃)

`2026-06-19 11:4x` · 운영자가 장비검증 arc 종료→첫 실전: G:\260518_CIR_Statistics 기반 Discussion claim unit. Codex가 곧 claim packet(컬럼/요약) 추출 예정, 나는 (1)framing 안전성 (2)verb-ladder 독립검토. **이 노트는 데이터 값 0, claim 구조/altitude만**(packet 받기 전 단계). 점수/구조만.

VERDICT: **framing 안전·잘 calibrated(L3 comparative). Codex의 "consistent with / more consistent with abiotic than biological·contamination"·"mixed > single endmember more natural"는 옳은 rung — 너무 소극도 과장도 아님. 단 2개 over-reach 리스크 경계: (a) mantle "둘 다 필요/required"=necessity claim은 L4 과장이니 comparative 유지, (b) 소절 제목 "Abiotic H2 generation"이 bald fact=제목만 L4 → "Evidence for ..." 권고. abiotic claim의 최종 altitude는 packet의 discriminator에 의존(아래 D).**

## A. Claim 1 — Abiotic H2 (온누리/온나래/온바다/미래2/처음/다음/마루)
- 과학적 근거 OK: MOR 열수계 abiotic H2(초염기성 serpentinization, 또는 mafic 고온 water-rock FeO 산화)는 확립된 과정.
- **핵심 안전장치 = discriminator 명시**: H2 농도 단독으로는 abiotic vs biotic 구분 불가(둘 다 H2 생성). 그래서 Codex의 **comparative**("biological·shallow contamination보다 abiotic water-rock reaction과 more consistent")가 bare "consistent with"보다 우수 — 단순 양립이 아니라 경쟁가설 대비 더 지지됨을 말함. 이게 "강한데 과장 아닌" 핵심.
- verb-ladder: "consistent with"=L3, "more consistent with X than Y"=L3 discriminating. 적절. "demonstrates/proves abiotic"=L4 금지. "may be related"=L2 too timid.

## B. Claim 2 — Mixed mantle (3He/4He + 지진파속도)
- 두 독립 proxy 수렴(He isotope + seismic) = 강점. mixed-source claim 합리적.
- ⚠️ **necessity 경계**: 운영자 "둘 다 필요(required)"는 necessity claim = 단일소스 대안 전부 배제해야 성립(어려움). Codex가 "more natural/more consistent"로 softening한 게 맞음. **comparative 유지**("단일 endmember보다 MORB-like + asthenospheric 2-component와 more consistent"), absolute "requires/needed" 회피.
- ⚠️ **velocity 해석 비순환**: 저속도→asthenospheric은 조성뿐 아니라 온도/melt에도 의존. "velocity가 조성을 증명"이 아니라 "velocity가 asthenospheric influence와 consistent"로 bind. 즉 seismic은 corroboration이지 단독 증명 아님.

## C. Claim 3 — 암석/petrology = supporting context only
- **옳은 판단**: 데이터가 터프한 곳서 주도적 big claim 안 만들고 context로 두는 것=좋은 절제(over-reach 회피). 유지.

## D. abiotic altitude의 packet 의존성 (task 3 준비)
packet에 뭐가 들었나로 rung이 갈림:
- **H2 농도만** → "consistent with abiotic" + 경쟁가설(biological·contamination·magmatic) 명시적 bounding에서 멈춤(현 framing).
- **+ discriminator(δD-H2, H2/CH4 또는 CH4 systematics, 유체온도, host-rock, 농도가 biological 상한 초과 등)** → "more consistent with abiotic than ..."로 한 칸 firm하게 license 가능.
- **site 이질성**: 7개 site가 균일 abiotic-consistent인지 spread 확인. 일부 다르면 "across these sites" 일반화 말고 "at most/several sites"로. → packet 받으면 per-site 분포 체크.

## E. 🎯 reviewer-2 attack surface (claim unit이 견뎌야 할 공격)
미리 방어하게 설계 권고:
1. abiotic: "biology 배제했나? sediment-hosted/magmatic CO2-H2는? shallow seawater contamination은?" → claim이 이들을 명시적으로 bounding해야(Codex framing이 이미 일부 함).
2. mantle: "3He/4He range가 MORB 변동폭(8±1 Ra) 내면 mixed 불필요. 단일 heterogeneous source로 설명 안 되나?" → packet의 He isotope spread가 MORB 밖임을 보여야 mixed claim 성립.
3. seismic 순환성(B 참조).
4. 제목 bald assertion(F).

## F. 제목
- "Abiotic H2 generation and mixed mantle volatile influence along the CIR" — body는 "consistent with"인데 제목이 abiotic을 fact로 단정 = 제목만 altitude 높음. 권고: **"Evidence for abiotic H2 generation and mixed mantle volatile influence along the CIR"** 또는 "...: evidence from CIR vent fluids". 제목은 약간 더 assertive 허용되나 claim과 정합 유지.

## G. 다음 (task 3·4)
- Codex가 claim packet(컬럼/요약, prose-free/value는 로컬) 주면: B/M/T + Conductor v3 장비로 실제 Discussion claim unit 생성→내가 독립 채점(dv2 + claim_altitude_two_sided + protected/unit 보존 + no-new-claim Conductor + reviewer-2 survival). section=Discussion rubric.
- **ccc note는 count-only/prose-free/resolved value 0** 유지(운영자 task 4). claim 구조·altitude·flag만.

## 정직/큐
라이브=claim framing 독립검토(데이터 값 0, claim 구조/verb-ladder만, packet 전 단계). 운영자 입력(packet) 받기 전 데이터 미접근. resolved 값/prose/캡션 0. manuscript-atelier 커밋0. ccc file-specific add. 미해결: Codex claim packet 대기→장비 run→채점 · df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
