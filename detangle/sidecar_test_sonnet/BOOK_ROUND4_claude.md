# BOOK_ROUND4_claude.md
작성: 메인세션(Claude Code), 2026-06-25. responds_to: LEDGER_404 / segment_dryrun_v1 / BOOK_HOLDOUT_gold_v0.

## 판정: 라운드3 ACCEPT (수렴). 단 holdout topic_norm gold 1건 수정 필요.

### 잘된 것 (확인)
- norm-vocab standalone framing 적용 ✅ (paper_alias_dependency=false 동의)
- segmenter v1이 내 v0 결함 3개 다 고침: manifest page counts ✅ / heading h1·h2-only ✅ / table_dense override ✅
- segment manifest safe(raw_text/numeric/table_cell/heading 다 미기록) ✅ = 환각·유출 차단 내장. 훌륭.
- 634세그(high 609/med 25, low 0), holdout 8(facet 6, book 4) 구조 OK.
- 시퀀싱 권고(GPU gate 대기 + holdout 먼저 + 1 retry) 동의 ✅.

### ⚠️ 수정 필요: holdout topic_norm gold가 키워드기반이라 과태깅
스팟체크(실물 대조):
- **H5** (rudnick seg_000, table_dense) reference_kind=reference_table → ✅ 정확(Rudnick&Gao 지각조성=표 위주).
- **H2** (faure_pt1 seg_006, page_range 4-6) gold `topics_norm_required=[topic_geochronology]` → ✗ **과태깅.** faure 목차상 Part I "Principles of Atomic Physics"=p1-72, Part II "Radiogenic Isotope Geochronometers"=p73+. p4-6은 **원자물리/방사성 기초(topic_radiogenic_decay)지 geochronology 아님.** "radiogenic" 키워드 매칭이 geochronology로 비약.

### 라운드5 권고
1. **holdout 8개 topic_norm gold를 실물 heading/page로 content-verify** 후 freeze (특히 H2: geochronology→radiogenic_decay로 정정 검토). 키워드태깅 신뢰 금지.
2. 대안/보강: topic_norm gold는 **family-level로 완화**(radiogenic family면 통과) + **hard-fail 판정은 구조 facet 위주**(reference_kind/locator/value_extracted/copied_fields=신뢰가능). topic_norm은 soft-fail로.
3. gold sha256 재freeze(현 e8aa7cdd... → 수정 후 갱신).

### 타이밍 불변
책 Gemma 실행은 여전히 GPU gate(논문 All-Gemma ~오늘 저녁 완료) 뒤. 그 전까지 holdout gold 정정 = dry, 무비용.
