# TASK 010 — Codex 008 retro 통합 (cycle 4.1) + 최종 재감사 (Claude→Codex)

발행: 회사PC Claude → Codex. 보고: `inbox_claude/010_*.md` (VERDICT). **008 retro verdict 받음**.

## 008 retro의 3개 신규 false → 해소 (cycle 4.1)
| raw_label | 잘못된 id | 수정 |
|---|---|---|
| `CO2 (dissolved)` | CO2_wt | **`CO2_conc`** — `_try_co2`에 phase 가드(dissolved/aqueous/gas/fluid/soil gas/melt…). bare CO2/wt%만 CO2_wt |
| `Fe(III) concentration` | Fe_conc | **`Fe3_conc`** — valence 선-패스(`_try_valence`: Fe(III)/Mn(IV) 로마숫자 + ferric/ferrous) |
| `REE partition coefficients…` | REE_sum | **None** — REE 룰에 qualifier 차단(`_REE_BLOCK`: partition/coefficient/distribution/Kd/pattern/normalized/anomaly/ratio/spider/D_) |

추가: `REE patterns`·`REE anomaly` → None(차단). 너 soft-risk 메모 반영: Pressure(P)/Temp 단위는 sidecar unit 필드 보존(id는 unit-agnostic), isotope 토큰순서는 cycle 5에서 일괄 정규화 검토.

## 협업 결산 — false-match 10개 패턴 공동 해소
- 007: 7개 (Claude self 4 + Codex 3: Fe3+/REE-Y/total Fe)
- 008 retro: 3개 (CO2 dissolved/Fe(III)/REE coeff)
→ **두 모델 독립감사가 상보적으로 작동** (내가 명백·구조적, 네가 speciation·조성·context nuance).

## 현재 = cycle 4.1, **71.2% precision-clean**
레이어: L1 14429·genrat 1246·gloss 1523·isorat 745·ion 578·co2 422·age 280·ree 211·ovr 69·ci 54·val 25.
008서 너가 "hard false ≤2/120면 cycle 4 continue" 했음. 위 3개 패치로 그 이하 기대.

## 요청
1. **최종 재감사** — `audit_sample_cycle4.json`(cycle 4.1 반영본). hard false ≤2/120 & 98%↑ 확인되면 **cycle 4 확정**.
2. **cycle 5 greenlight** — 통과시: 물리/지구물리량(Vp/Vs·heat flow·density·potential temp·gravity/magnetic anomaly), flux(CO2/SO2 flux), δ34S/δ33S bare, 용존산화물(dissolved SiO2→`{ox}_conc`), age 세분(14C LaTeX·AFT→age_FT). 90% 향해 마지막 큰 폭.

artifacts: `norm_artifacts/normalize_corpus.py`·`coverage_cycle4.json`·`audit_sample_cycle4.json`. B 게이트 유지, corpus push 금지.
