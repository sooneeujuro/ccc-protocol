# Corpus sidecar 필드 — 중요도×취약도 발견 (2026-06-15~16, 회사PC 전수 스캔)

> 이 문서가 보존하는 것: verification 정책(ma PR#15)에 **안 들어가는** corpus-품질 발견들 — 전수 통계 + 스키마 버그.
> verification/정규화/certification 설계는 ma PR#15 `corpus_verification_policy_v0.md`에 있음(중복 안 함). 여긴 그 *근거 수치*와 *별개 결함*.
> 스캔: `datalab/sidecars_v2` 3,948편 read-only. 코퍼스 본문 미포함(통계만).

## 전수 fragility 실측 (3,948 sidecars; Haiku 3,388 / Sonnet-4.5 560)
| 필드 | 중요도 | fragile(실측) |
|---|---|---|
| **variables_measured `id`** | ★★★ | 🔴 **73%** = `raw_label_only` (29,796/40,627) → 정규화 깨짐. **VP-NORM-1로 $0 수정**(PR#15 §0.5) |
| **instruments `category`** | ★★★ | 🟠 **스키마 enum 갭 + 비정규 누수**(아래 ★) |
| cited-vs-measured (귀속) | ★★★ | 🟠 추론필요 → **VP-CVM-1 lazy**(PR#15) |
| labs (vs 소속 혼동) | ★★ | 🟡 empty 13% |
| doi | ★★ | 🟡 **52% 없음** |
| standards | ★★ | 🟡 33% 없음 |
| classification | ★★ | 🟡 16% "other" |
| geography coords | ★ | 🟢 20%(대개 진짜 없음) |
| conclusions 완결성 | ★★ | 🟢 5% truncated + 3% no-section (파이프라인, 별개) |
| string-encoded 잔재 | — | 🟢 1편 (수리 거의완료) |

## ★ 별개 결함 #1 — instrument `category` enum 갭 (스키마 버그, PR#15와 무관)
- 스키마 `sidecar_v2.1` 의 instrument category enum 22종에 **`tims`(열이온화MS — Sr/Nd/Os/Pb 동위원소용, 지화학 최빈기기)가 빠짐.**
- 결과: TIMS가 갈 곳 없어 **`noble_gas_ms`로 오분류**(실측 예: Wang 2018 N-TIMS). → **`noble_gas_ms` 1,490개 의심**(상당수 미분류 TIMS 가능, 스팟확인 필요).
- 비정규 누수 ~50종(enum 밖 자유텍스트): `la-icp-ms`(24)·`ion_microprobe`(3→sims)·`electron_microprobe`(2→epma)·`nanoSIMS`(1→sims)·`mc_icp_ms`(→icp_ms)·`thermal_ionization_mass_spectrometry`(→tims)·`xanes`·`seismic` 등.
- **조치(별개 트랙, $0)**: ① 스키마 enum에 `tims`(+필요시 `mc_icp_ms`,`xanes`) 추가 ② category 정규화 매핑(비정규→canonical). VP-NORM류로 확장 가능. **단 스키마 변경이라 drift-contract(extract script+validator 임베드본 동기) 지켜야 함.**

## ★ 별개 결함 #2 — 편찬/리뷰 논문 (체계적 오염)
- 리뷰/편찬 논문은 남의 데이터를 대량 표로 모음 → Haiku가 통째로 measured로 기록 가능(이전 broad-403 부류). 논리가 paper-type 구분을 안 함.
- VP-CVM-1(per-variable lazy 판정)이 케이스별로는 잡지만, **paper-type 사전탐지**가 있으면 우선순위·일괄처리에 유용. (별도 탐지 후보)

## 검증 우선순위 (종합)
1. **VP-NORM-1 정규화**(변수 id 73% + 기기 category) — $0, 최대효과, PR#15 §0.5 전제
2. **VP-CVM-1 lazy verification** — 읽는김에, ~$0, PR#15
3. 편찬논문 탐지 + instrument enum 스키마 수정 (별개 $0 트랙)
4. conclusions 완결성 — 파이프라인(재추출 무관, 별개)

> 의미: corpus 최대 결함 두 개(변수 id 73%, 기기 category)가 **$0 결정적 수정**. 비싼 모델은 cited-vs-measured 추론에만. 전수 재추출($755) 불요.
