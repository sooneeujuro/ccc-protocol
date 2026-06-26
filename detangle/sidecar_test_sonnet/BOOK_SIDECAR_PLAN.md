# 책(book) sidecar 전략 — DRAFT v0
작성: 메인 세션(Claude Code, 1M Opus), 2026-06-25. 용도: CODEX 검토/pressure-test 핑퐁.
원칙: 정확도≫속도·비용 / 로컬 Gemma $0 / 정본 미수정(staging) / 환각방지 내장.

## 0. 핵심: 책 ≠ 논문 (왜 논문 스키마 못 씀)
- 논문 sidecar v2.2 = `variables_reported:[{raw_label,id,unit,phase,kind}]` = "이 논문이 **보고하는** 측정변수 인벤토리". 용도: "X 변수 데이터 있는 논문 찾기".
- 책은 측정을 보고하지 않음. **컴파일/설명/교육.** 가치 = (a) 레퍼런스 값·상수, (b) 방법 설명, (c) 개념 커버리지.
- 사용자(원희) 검색 의도: "δ34S 해석법?", "87Rb 붕괴상수?", "noble gas 물 용해도 설명" → **topic/method/reference 중심**이어야.

## 1. 먼저: "책" 15권은 사실 2종류 (★중요 결정포인트)
- **진짜 교과서(big, book-schema 대상)**: Faure&Mensing(927p), Seafloor Hydrothermal(478), IUPAC Solubility(401), Burnard(390), Clark&Fritz(343), Ozima&Podosek(302), TEOS-10(207), Rudnick&Gao(64), Cook(536·완료)
- **짧은 챕터/사실상 논문(small)**: Karlstrom(24), Taran(14), McCollom(11), German(10), Ryan(9), Klein(7), McDermott(5)
  → 얘넨 **그냥 논문 sidecar 스키마(variables_reported)** 쓰는 게 맞을 듯. book-schema 오버킬.

## 2. 단위: 챕터별 (책 통째 sidecar ❌)
- 927p를 sidecar 1개 = 검색 무용. 챕터/주요 절이 자연 단위.
- 세그먼트: MD heading(`#`) + (가능하면) TOC 탐지. `{N}---`는 **페이지 마커지 챕터 경계 아님** — heading 기반으로 챕터 잡아야.

## 3. 스키마 제안 (챕터별)
```
{
  book_id, chapter_id, chapter_title, page_range,
  content_type: explanation | reference_table | method | derivation | case_study,
  topics: [...],            # "Rb-Sr isochron", "sulfur isotope fractionation"
  isotope_systems: [...],   # "Rb-Sr","U-Pb","δ34S","He-Ne-Ar"
  methods: [...],           # "TIMS","SIMS","isochron regression"
  reference_data: [...],    # "87Rb decay constant 표","seawater 87Sr/86Sr" — FLAG+page만, 값은 use-time 본문읽기
  key_equations: [...],
  summary: "1-2문장"
}
```

## 4. 추출: 로컬 Gemma($0), 챕터 청킹, truncation 금지
- gemma4:12b, **think:false** (논문서 검증: recall 85%>77%, precision 77%>73%, ~17s/편, CoT는 인벤토리 완전성 오히려 해침).
- 챕터 단위 추출, 긴 챕터는 sub-chunk 후 병합. **MAXCHARS로 뒤 자르지 말 것**(논문서 거부된 안 — 중요내용 유실).
- ⚠️ **핵심 원칙(논문서 비싸게 배움)**: 측정/레퍼런스 **"값"은 추출해서 믿지 말 것**(Haiku가 46% 비측정을 measured로 환각한 전례). `reference_data`는 **"있다 + page"만** 인벤토리화, 실제 숫자는 use-time 본문읽기. = 논문의 provenance 분리와 동일 철학.
- ollama: 반복 hard-kill 금지(GPU degrade→재부팅만 복구), 직렬만, parallel-2는 16GB서 OK.

## 5. 검색 연동
- 책 model = **챕터청크 BGE+BM25**(논문과 동형; 기존 책corpus는 BGE만이었음 → BM25 추가).
- retrieval_units = 챕터. sidecar 메타(topics/methods/isotope_systems)로 필터.

## 6. 검증 (과적합 방지)
- holdout 챕터 ~6-8개(Faure Rb-Sr장, Ozima He장, Clark&Fritz 지하수장, IUPAC 데이터표장 등) → 답안지 만들어 Gemma recall/precision 측정. dev/holdout 분리. 지표 꺾이면 정지(과적합 방지).

## 7. CODEX가 깨부술 것 (pressure-test 포인트)
1. **small 7권을 paper-schema로** 보내는 거 맞나? 경계는?
2. `reference_data`: **flag-only(내 주장, 환각방지) vs 값까지 추출**? 트레이드오프?
3. `topics/methods`: free-text vs **controlled vocab**(논문 variable_aliases와 정렬해 cross-corpus 검색)?
4. **챕터 경계 탐지** 신뢰도 — heading 없는 컴파일(IUPAC 데이터표, TEOS 방정식집)은 어떻게 자르나?
5. **book-level 요약 sidecar**도 따로(책 1줄 소개 + 전체 TOC)? 챕터 sidecar만으론 "이 책 뭐임" 답 못 함.
6. 검색 통합: 책 챕터청크를 논문 index와 **합칠지 분리할지**(원희 한 번에 검색 vs 책/논문 따로).
```
파일: detangle/sidecar_test_sonnet/BOOK_SIDECAR_PLAN.md
```

---
# v1 — CODEX 핑퐁 수렴 (2026-06-25, 메인세션 확정)

CODEX `BOOK_SIDECAR_PROPOSAL_codex.md` 검토 후 수용/조정. VERDICT: keep_direction_but_tighten.

## 수용 (CODEX 구조 채택)
1. small/book 분류: page-count ❌ → **function classifier**. hard boundary = `reports_new_measurements_or_primary_case_data`. 애매하면 `book_lite`.
2. reference_data: **typed flag** = `{reference_kind, label_raw, label_norm, locator, value_extracted:false}`. 값 추출 v0 금지(v1 quarantine).
3. topics/methods/isotope_systems: **raw + norm 이중**. norm은 normalization_confidence(exact|alias|fuzzy|none).
4. 분절: **segment_type**(chapter|section|reference_table_group|equation_block|page_window) + **segment_method**(toc|heading|pattern|table_dense|fixed_window) + **segment_confidence**(high|med|low). low → production 금지/review queue. tiered tier1→4.
5. book-level: **book_manifest_v0**(결정론적·필수) + book_summary(생성·optional·저신뢰).
6. index: 물리 **분리**, query **federated**(source_type facet), **source_role**(primary_evidence|review_context|textbook_explanation|reference_data_locator|method_background).
7. version quartet(schema/segment_schema/normalizer/prompt) + **md_quality** gate(ok|heading_weak|table_weak|ocr_suspect|page_markers_only) + edition-aware book_id.
   schema 본체 = CODEX 제안서 §"최소 v0 수정안" 그대로 채택(book_sidecar_chapter_v0 + book_manifest_v0).

## 메인세션 가드레일 (15권 과설계·Gemma신뢰도 방지)
A. **normalizer 경량**: 새 vocab 구축 금지. 기존 논문 `variable_aliases`에 exact/alias만 매핑, 미스 → norm=[](raw가 recall). 15권 규모엔 충분.
B. **Gemma 필드 우선순위**: 세그먼트당 전필드 일괄 X(논문서 CoT/과필드 = 완전성↓ 검증됨). 결정론적(segment_*) 먼저 → content_type·topics_raw·reference_kind+locator(고가치) → norm·equation·summary(2차). think:false.
C. **segmenter도 과설계 금지**: tier1(heading) + 스팟체크 먼저, tier2-4는 필요시. 분절 confidence는 필수.

## 즉시 실행 (CODEX 7.6 dry-run — CPU, GPU 무관, Gemma 도는 지금 가능)
books_v5_out 17폴더 대상:
1. **segmenter dry-run**: 각 MD를 segment_type/method/confidence로 분절 → segment 통계 + low-confidence 목록.
2. **book_manifest_v0** 생성(결정론적: title/edition/page/segment_count/md_quality).
3. **md_quality gate** 평가.
→ GPU 비면(논문 model 뒤) Gemma 추출만 남게. 분절 결과 = 다음 핑퐁 라운드(CODEX 검토).
