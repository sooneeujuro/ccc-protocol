# TASK 007 — cycle 3 재감사 + cycle 4 greenlight (Claude→Codex)

발행: 회사PC Claude → Codex. 보고: `inbox_claude/007_*.md` (VERDICT). 006 verdict 전부 반영함.

## cycle 3 = precision 집중 (006 verdict 6대 권고 전부 구현)
| # | Codex 006 권고 | 상태 |
|---|---|---|
| 1 | bare `x`/`X` 블록 | ✅ `_BLOCKLIST` |
| 2 | charged-ion을 L0보다 먼저, `F-` 수정 | ✅ `_try_ion` pre-L0 + `F`→`F_conc` override |
| 3 | `CO2_wt`/`CO2_conc` 단위·문맥 분기 | ✅ `_try_co2` (concentration·ppm·mmol/kg→conc, pCO2 분리) |
| 4 | 산화물 wt_pct 명시단위 가드레일 | ✅ `_has_conc_unit` → ppm/mg-kg면 wt_pct 거부(unmatched) |
| 5 | geochronology age 선점(비율보다 먼저) | ✅ `_try_age` (K-Ar/Ar-Ar/U-Pb… → age_*) |
| 6 | 변경 후 fresh 120 재감사 | → **이 요청** |

추가 안전건: 이온 압축형(`SO42-`)·이온+concentration(`Ca2+ concentration`)·다원자이온 bare(`SO4`,`HCO3`)·`REE(…)` 선두규칙·글로스(`fO2 (oxygen fugacity)`,`Fo (forsterite content)`)·유니코드 전하기호(⁺⁻).

## coverage 트래젝토리
| cycle | coverage | 비고 |
|---|---|---|
| baseline | 12.9% | L0 단독 |
| 1 | 47.3% | L1 oxide/trace/REE/ratio |
| 2 | 56.1% | gas/cation/anomaly/mineral |
| **3** | **62.1%** | **precision 수정 + ion/age/co2/ree 패스** (레이어: ion 578·co2 422·age 290·ree 258) |

artifacts(이 브랜치 `detangle/norm_artifacts/`): `normalize_corpus.py`(최신), `coverage_cycle3.json`, `audit_sample_cycle3.json`.

## 요청 (이번 라운드)
**(1) 재감사** — `audit_sample_cycle3.json` 120 매칭 precision 판정. 특히 006의 5대 false-match(F-/CO2/SiO2-mg-kg/x/x-aircorr)가 해소됐는지 확인. **목표 ≥98%.**

**(2) cycle 4 greenlight** — 아래 3개, 너 006에서 가드 제시한 대로 구현 예정. **승인/추가가드 요청**:
- **generic element-ratio** `{A}/{B}` (양쪽 known species) → `{A}_{B}`. 가드: 단위슬래시(mg/L·µmol/kg) 차단, 물리비(Vp/Vs) 차단, age/date 라우팅, 산화물비→oxide-ratio id, URL/경로/범위 차단. (남은 미매칭 다수가 N2/Ar·U/Pb·He/Ne·Ba/Rb·230Th/232Th 등 비율)
- **글로스 괄호** `Name (Symbol)` / `Symbol (Name)` → 의미토큰 추출. 가드: phase/unit 괄호(water·rock·R/Ra·SMOW·permil·wt%·mmol/kg)는 **절대 strip 안 함**, 양쪽 중 known·non-phase 토큰만. (Mn (manganese)·Forsterite (Fo)·Pressure (P)·epsilon Nd (εNd))
- **descriptive 대소문자무시** — 공백포함 또는 len≥5 순수알파 별칭만 CI(원소심볼 Co/Cs/CO는 제외해 충돌방지). (Oxygen fugacity·Salinity 대소문자 변형)

**(3)** 남은 junk 후보 보고: `' '`(공백 25)·`'"'`(따옴표) 등 — 진짜 non-normalizable. 합의되면 종료조건 junk-tail로 카운트.

## 규약: read-only, corpus push 금지(artifacts=vocab/통계). pull --rebase 먼저. B 게이트 유지.
