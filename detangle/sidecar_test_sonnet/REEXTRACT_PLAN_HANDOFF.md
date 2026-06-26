# 재추출 지침 (HANDOFF, 2026-06-25, 컨텍스트 압축 직전)
운영자 최종 지시 4개 + 검증된 상태. 압축 후 이 문서대로 실행.

## 운영자 지시 (확정)
1. **조금이라도 입력 잘린 논문(>95000자) 전부 재추출.**
2. **청킹 반드시 포함** (안 잘리게) — "꼭 확인".
3. **버그픽스 적용 확인.**
4. **parallel-2(워커 2개)로 실행.**
입력 = **정본 corpus_20260624\articles** (옛 0612 아님!). 스키마 **보존**(변경 금지).

## ✅ 상태 (2026-06-25 ~12시, 전부 완료 + 가동중)
| 항목 | 상태 |
|---|---|
| 버그픽스 | ✅ IN (num_ctx 49152/16384, JSON raw_decode, classification/extraction_meta str-guard). py_compile OK. |
| 청킹 | ✅ **구현+검증** = `extract_chunked()`(L88~109). 검증: Huth(231k자) 단일컷 6변수→청킹 59변수(꼬리 δ18O/Δ17O/δD/δ13C/Mg/Ca 복구). Passey e2e: 2청크, 23변수, Haiku verbatim 전부 보존. |
| parallel-2 | ✅ **검증** = 2동시 88k자 ctx49152 OOM無, ~1.9배. bat workers=2. |
| 입력 0624 | ✅ pid 97.8%(3861/3948) 0624 직접매칭. ARTS=0624 우선+0612 fallback(L14-15). e2e서 0624 읽기 확인. |
| reuse-selective | ✅ 격리 done 2161 분류: **재사용 1199(안 잘림→canonical staging 복사) / 재추출 962(잘림)**. (reuse_prep.py) |

### ▶ 가동중 (RUNNING)
- 런치: `loop_gemma_v2.bat` WMI detached PID 61280, parallel-2, 입력 0624, 청킹, → `sidecars_v22_canonical`.
- **todo ~2748편**(962 잘린done + 1787 미추출), ETA ~12-14h. $0.
- **모니터(압축 후)**: `loop_canonical.log`(헤더 버퍼링 주의) / `PROD_PROGRESS.json`(25편마다 갱신) / `COMPLETE_GATE.json`(게이트). canonical staging 개수 증가 = 정상(시드 1200, 목표 ~3948-no_md).
- **남은 일**: ①114편 정본전용(0624에만, SIDE base無)은 이 런에 미포함 → article-driven Gemma-only 별도 ②완료후 canonical staging 검증→정본 sidecar로 승격 ③52 Sonnet 독립병합 ④index(BM25+BGE).

## 입력 잘림 정확 카운트 (검증됨, char 기준 len>95000)
- 정본 0624: **1707/3978편(42%) 잘림** (median 125k자, max 2.24M자; >250k 대량컷 71편)
- 0612: 1948/3903(49%)
- ※ 95000 = **글자수**(byte 아님; 한글논문 ~190KB+)

## 재추출 대상 (정본 0624)
- (a) 입력 잘림 len>95000 = **1707편** (반드시, 청킹으로)
- (b) 미추출(정본인데 valid sidecar 없음)
- (c) 이전 err/no_md
- **reuse**: done 2161(격리) 중 **안 잘린(≤95000) + 정본 매칭**되는 것 → 정본 paper로 re-key (인벤토리 노이즈는 inherent ~85%라 reuse OK)

## 청킹 구현 스펙 (gemma_production.py 수정)
- `MAXCHARS` 컷 제거 또는 청킹 분기:
  - `if len(md) <= CHUNK(~88000)`: 기존대로 1콜
  - `else`: 문단/페이지마커 경계로 청크 분할(없으면 char-window + 약간 overlap) → 각 청크 Gemma 추출 → **variables_reported = 청크들 union + dedup**(id 우선, 없으면 norm raw_label) / classification·made_new = 청크1 또는 다수결
- 검증: 롱페이퍼(faure pt1 등 >95000자) 1편 돌려 **꼬리쪽 변수 잡히나** 확인.

## 실행 순서 (post-compaction)
1. 청킹 구현 → py_compile → 롱페이퍼 1편 검증(꼬리 변수 OK)
2. gemma_production 입력경로 0624로, 런처 bat workers=2로
3. 재추출 todo 리스트(a+b+c) 생성, reuse분 re-key
4. WMI 루프 기동(parallel-2), prod2.log + check_complete 게이트로 미처리0까지
5. fail율 + 청킹 효과(롱페이퍼 변수 완전성) 확인

## 핵심 사실 (압축 후 필독)
- 스키마 **보존**: classification.type + made_new_measurements + variables_reported. 변경 금지.
- done 2161 격리 = `corpus_md_export_20260612\sidecars_v22_QUARANTINE_oldinput_20260625` (902 구config·parallel + 1259 신config·serial).
- 52 Sonnet 독립보존 = `corpus_md_export_20260612\sonnet52_independent`.
- ollama: **hard-kill 금지**(degrade→재부팅만 복구), 직렬 or parallel-2만, think:false.
- ★**경보성 숫자 즉답 금지** — 측정법 sanity-check 먼저(파일명매칭·exact-hash·1run-LLM비교 = artifact 3대장). 이 세션 6번 거짓경보냄.
- Gemma 인벤토리 inherent 노이즈 ~85%(holdout 검증·수용). 재추출이 "더 정확"한 거 아님 — 잘린 것만 고치는 게 목적.

## 파일 경로
- 추출기: `detangle/sidecar_test_sonnet/gemma_production.py`
- 게이트/루프: `check_complete.py` / `loop_gemma_v2.bat`(workers 2로 수정)
- 정본 입력: `G:\corpus_20260624\articles`
- Haiku base(merge): `C:\Users\USER\corpus_md_export_20260612\sidecars`
- 잘림 카운트 스크립트: `count_truncated.py`
