# 밤샘 brief (메인세션, 2026-06-25 ~04:10) — 아침에 볼 것

## 1. CODEX 라운드2 검토 결과 (3종 다 정독)
CODEX 산출 `BOOK_GEMMA_PROMPT_codex.md` / `BOOK_NORM_VOCAB_codex.md` / `BOOK_HOLDOUT_codex.md` = **프로덕션급, 3종 다 수용(ACCEPT).**
- Gemma 프롬프트: think:false, 세그먼트당 1콜, 값추출 금지, model이 norm id 못 지어냄(allowed_norm_ids만), fail-closed 검증 — 환각방지 완벽.
- norm-vocab: 41 id 경량(isotope 14/method 15/topic 12), family-level.
- holdout: contract 검증(prose 아님), H1-H8 facet, hard/soft fail 규칙.

### ★ 내가 corpus로 검증한 것 (CODEX가 못 한 것)
1. **논문 normalizer/alias layer 부재 확정**: `find` 0개, retrieval_papers에 variable_aliases 키 없음(paper-level facet만). 논문 sidecar id는 Gemma 자유형("delta_18O"). → **CODEX의 "기존 논문 alias 정렬"은 정렬 대상이 없음.** 단 CODEX §6(index 물리분리+federated)대로면 id-join 불필요 → 책 vocab는 **standalone 책 facet로 OK**, cross-corpus join은 v0 밖. framing만 수정.
2. **Gemma 프롬프트 dev-test 필요**: 규칙 엄격 → gemma4:12b가 거절 많이 당할 수 있음(yield↓). 전량 전에 holdout로 거절률 측정 + 거절시 1회 retry 권고.

## 2. ⚠️ Gemma 논문 sidecar QA (gate라 점검)
- **데이터 손실 0** — staging의 "빈" 400편은 `variables_measured`(구 Haiku 키)에 보존, `variables_reported`(신)만 없음 = Gemma 미처리/실패분.
- **실제 실패율 ~13%** (prod.log: 950 처리 중 fail 122). 실패분은 Haiku 구데이터(46% measured 환각 문제)로 남음.
- **원인 미상**: MD 크기 상관 약함(실패 median 101KB vs 정상 90KB, 전 구간 ~27%아니라 prod 카운터로는 13%). 긴논문/ollama degrade/JSON 파싱 중 하나. 재현=GPU 필요 → 아침에 실패 1편 재run으로 확인.
- **권고**: (a) 본run 끝나고 **haiku-only 400 + fail분 2차 패스 재처리**(idempotent라 staging에 있으면 skip → 명시 타겟 필요). (b) 실패 원인 못 잡으면 청킹 도입 고려.

## 3. segmentation dry-run (책)
- 12권 textbook → heading 분절 high-conf. 5권(IUPAC pt1/pt2·karlstrom·rudnick=table-dense, mcdermott=작음) → reference_table_group 필요.
- v0 결함(라운드2 수정): pages_est=0(v5 페이지마커 regex 미스), heading 과다(서브섹션 → 챕터는 h1/h2), table-dense가 heading보다 우선.

## 아침 결정거리
1. Gemma 실패 ~13% 원인규명 + haiku-only 400 2차패스 (논문 model 전에 채울지/나중에).
2. 책: segmenter v1 개선(table-dense override, h1/h2 챕터) + holdout 8세그 인스턴스화 + Gemma 프롬프트 dev-test.
3. norm-vocab는 standalone 책 facet로 확정(cross-corpus는 미래).
