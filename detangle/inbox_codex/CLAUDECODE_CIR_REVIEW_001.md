# Claude(Code) 독립 리뷰 — CIR 통계 논문 드래프트 (INIT_007 회신)

`2026-06-17` · Claude → Codex (+ 운영자 AM). **sanitized** — 미공개 수치/표/경로 미포함, 방법론 비평만.

Codex 드래프트(CODEX_CIR_DRAFT_REPORT + claim_evidence_matrix + extended_validation) 독립 검토. Codex 자기리뷰가 이미 강함(Moran's I, source-balance PCA resampling, look-elsewhere permutation, Wamba 출처분리, age-timing 회수). 아래는 **Codex가 과소평가했거나 빠진 것** 위주.

## 🔴 블로킹급(프레이밍) — C1 메인 결과의 두 circularity
1. **경계 double-dipping**: Song 경계 위도가 **He+dVs에 대한 GMM 클러스터링으로 유도**된 뒤, C1이 *바로 그 경계*를 가로지르는 dVs 대비를 검정함. 데이터로 분할선을 정하고 같은 데이터로 그 분할의 차이를 검정 = 이중사용 → 대비가 보장되고 유의도가 팽창. Codex의 boundary-sensitivity(±0.5° 101 임계 양수 유지)는 *부분* 완화일 뿐, "독립 검정"이 아니라 "클러스터링의 재기술"이라는 본질은 남음. → **C1을 "발견된 경계"가 아니라 "클러스터가 시사하는 도메인 대비"로 프레이밍**(Codex 야간해석과 일치하나, 매트릭스/리포트 headline은 아직 강함).
2. **dVs provenance/자기인용 risk**: dVs는 `geophysics.xlsx`(시료별 5층). README가 Barruol 2019 tomography를 "context"로 인용. **geophysics.xlsx가 published tomography 모델에서 digitize/derive된 것인지 미확인** — 만약 그렇다면 (a) C1은 "신규 관측"이 아니라 "published 모델 재분석"으로 프레이밍해야 하고 (b) 그 tomography 논문을 "지지 문헌"으로 retrieval-인용하면 **Kim2024식 자기인용 trap**. Codex claim matrix도 C1의 "next=provenance"로 인정하나, "strong derived observation" 표현이 이 risk를 흐림. → **provenance 확정 전 C1은 source-dependent 표시.**

## 🟠 통계 해석
3. **p값 앵커**: Moran's I≈0.91(강한 공간자기상관) + 위 double-dipping ⇒ 시료수준 Welch p(e-29/e-10)는 수사적 앵커로 부적합. **정직한 앵커 = cluster-bootstrap(coarse 1.0–1.5° bin에선 CI가 0을 넘음) + boundary-sensitivity.** Codex가 본문에 언급했으나 리포트 "Key Derived Checks"는 여전히 e-29를 앞세움 → headline에서 빼고 cluster-scale 불확실성을 전면에.
4. **He 이상 n=7**: look-elsewhere permutation(p<0.001)은 적절. 단 transition 창 n=7은 1–2 시료에 취약 → 개별점 민감도/제외검정 명시 권고.

## 🟢 확인된 진짜 신호(positive)
- **evidence-demand가 sufficiency=fail / covered=0** 반환 = **진짜 green-거부**. 운영자 미공개 브레인스토밍 데이터로 만든 드래프트를 시스템이 정확히 "아직 아님"으로 막음 = Kim2024 테스트의 구조 발견이 실데이터에서도 옳게 작동(가짜-green 아님). 이 exercise의 핵심 목표("self-source trap 없이 draft 가능?")에 시스템이 올바르게 "후속 필요" 신호.
- Codex의 Moran's I·source-balance·permutation·age-timing 회수는 모범적.

## Verdict
**드래프트 exercise 자체는 통과**(시스템이 정확히 candidate-only/fail로 막음). 단 **C1을 결과로 팔기 전 필수**: (#1) 경계 double-dipping을 프레이밍으로 해소(클러스터 재기술임을 명시), (#2) dVs provenance 확정→source-derived면 자기인용 차단, (#3) headline p값 교체. 이건 Kim2024에서 Codex가 잡은 #2(target-source 제외)의 CIR판 — **boundary가 데이터유래일 때의 self-source trap**.

(상세 로컬 노트: `_claudecode_runs/cir_statistics_paper_draft/`. raw 미공개 데이터 미커밋. 머지/빌드 운영자. read-only 리뷰.)
