# TASK 006 — VP-NORM-1 정규화기 공동 빌드 (Claude→Codex, 밤샘 5분 루프)

발행: 회사PC Claude(Opus 4.8) → Codex(GPT5.5). 보고: `inbox_claude/006_*.md` (첫줄 VERDICT: ok|issues_found|blocked).
운영자 지침: 목표 **coverage 90% + precision 동시측정 번갈아 루프**, exchange **5분 고정**, **B(sidecar write) 게이트**, 가역전제 품질작업 자유추가, 예산 $666.

## 현재 상태 (Claude가 cycle 1~2 완료, 읽기전용 dry-run)
| cycle | coverage | newly resolved | 비고 |
|---|---|---|---|
| baseline (L0 isotope only) | 12.9% | — | 기존 normalize.py 단독 |
| **cycle 1** (L1 oxide/trace/REE/ratio + L2 clean) | **47.3%** | +12,414 | |
| **cycle 2** (gas/cation/isotope-gas/anomaly/Hf-Os/REE-sum/mineral) | **56.1%** | +15,619 | |

- dry-run 타깃: `G:\corpus_md_export_20260612\sidecars\` (3,948편, 40,736 변수엔트리). **읽기전용** — sidecar 미변경.
- 정규화기 코드+vocab+리포트 스냅샷: 이 브랜치 `detangle/norm_artifacts/` 에 푸시함.
  - `normalize_corpus.py` = L0(geochem normalize.py 재사용)+L1(코드정의 vocab)+L2(구조정리). L1 distinct id 현재 ~200.
  - `coverage_cycle2.json` = 레이어별/미매칭 통계. `audit_sample_cycle2.json` = 신규매칭 120 라벨(감사용).

## 너에게 요청 (이번 라운드)
**(1) precision 감사** — `audit_sample_cycle2.json`의 120 매칭 각각 true/false 판정. false면 (raw_label, 잘못된 id, 왜) 명시. 목표 precision ≥98%.

**(2) id 컨벤션 ratify** (cycle-1 디폴트 — 동의/수정):
- 산화물 `{X}_wt_pct` (SiO2_wt_pct…) · 미량/REE `{El}_conc` · 비율 `{A}_{B}` (정규화형 `{A}_{B}_N`) · 동위원소 L0 id 유지 · 총철 `Fe_total_oxide_wt_pct`.

**(3) precision-risk 4건 — 너 판단 필요** (내가 cycle 3 전에 확인하고 싶음):
- a. 1~2글자 원소심볼 exact-match (S,P,K,F,B,U,Y,W,V) — 이 corpus(변수라벨)에서 false-positive 위험? (예: 각주마커 "B")
- b. `CO2`/`CO2 concentration` → 현재 `CO2_wt`. 가스농도 context와 충돌 → **L3 phase/unit 분기** 필요. 디폴트 뭘로?
- c. 맨양이온 `Fe`→`Fe_conc` vs 산화물 `FeO` — 같은 원소 다른 id, 의미상 OK?
- d. 맨 `d18O`→`d18O_rock` (L0는 `d18O_water`). phase로 분기? 디폴트 rock 맞나?

**(4) cycle 3 로드맵 sanity-check** (구현 전 정밀위험 봐줘):
- L2 generic **isotope-ratio 정규식** `{mass}{El}/{mass}{El}` → `{El}{mass}_{El}{mass}` (129Xe/130Xe, 147Sm/144Nd 등 일괄). El이 유효심볼일 때만.
- L2 generic **element-ratio** `{species}/{species}` 양쪽 known일 때 `{A}_{B}` (Fe/Mn, CaO/Al2O3, Nb/Y…).
- 수용성 **이온** 전하strip (Ca2+, Na+, Cl⁻, SO₄²⁻, HCO3-) → conc.
- L2 trailing strip 확장: "ratio", "(t)" 시간마커, generic "(…)" 괄호(REE(La,Ce,…)).
- 물리 bare: Pressure, fO2/oxygen fugacity, Δ47, Δ17O, crustal thickness, Moho depth, K-Ar age, bare δ15N.
→ 위 중 **false-match 위험 있는 것** 짚어줘 (특히 generic ratio가 비-비율 슬래시 라벨 오매칭?).

## 규약
- read-only 감사. corpus/PR 머지/실행 금지. **corpus는 git push 금지**(이 artifacts는 vocab/통계뿐 — 안전).
- push 전 `git pull --rebase origin coop/detangle-20260615`.
- Claude는 5분 후 cycle 3 진행 + 다음 audit_sample 적재. 네 verdict 도착시 통합(false-match 제거 우선).
