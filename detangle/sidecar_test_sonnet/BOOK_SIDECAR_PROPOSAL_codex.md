# BOOK_SIDECAR_PROPOSAL_codex.md

작성: Codex, 2026-06-25
대상: `BOOK_SIDECAR_PLAN.md` DRAFT v0 독립 압박 검토
범위: 책 corpus/sidecar/model 전략. 새 설계안이 아니라 DRAFT v0의 빈틈, 대안, 리스크 검토.

## 총평

VERDICT: keep_direction_but_tighten_boundaries

초안의 큰 방향은 맞다. 책은 논문처럼 "보고한 측정변수"를 찾는 자산이 아니라, reference/explanation/method/derivation/case coverage를 찾는 자산이다. 그래서 책 전용 sidecar가 필요하다는 판단은 통과.

다만 v0 그대로 가면 위험한 지점이 있다. 가장 큰 리스크는 다음 4개다.

1. "small book = paper schema"를 page count로 결정하면 오분류가 난다.
2. reference_data flag-only는 맞지만, 너무 약하게 잡으면 reference book의 본질을 못 살린다.
3. topics/methods free-text만 쓰면 논문 alias/index와 연결이 끊긴다.
4. chapter boundary가 실패하면 sidecar 품질 전체가 무너진다. 이건 모델 문제가 아니라 segmentation 문제다.

권고: v0는 book chapter sidecar + book manifest + segment confidence를 먼저 고정하고, value extraction은 quarantined v1로 미룬다.

## 1. small 7권을 paper-schema로 보낼지

찬성:
- 짧은 chapter/paper-like 문서는 book schema가 과하다.
- original measurement나 article-like methods/results가 있으면 `variables_reported` 인벤토리가 검색에 더 직접적으로 유용하다.
- 기존 논문 sidecar/index 파이프를 재사용할 수 있다.

반대/리스크:
- page count는 schema 경계가 아니다. 짧아도 review chapter, encyclopedia entry, handbook section이면 paper schema가 틀린다.
- "short chapter = paper"로 보내면 book 자산의 핵심인 explanation/reference coverage를 잃는다.
- 반대로 긴 chapter 안에도 original data/case-study 성격 단위가 섞일 수 있다.

대안:
- page count가 아니라 document function classifier를 둔다.
- 판정 기준은 `original_research_like`, `review_or_educational`, `reference_table_like`, `method_protocol_like`.
- paper schema는 `original_research_like=true`일 때만 사용한다.
- 애매한 짧은 문서는 `book_lite`로 둔다: book schema의 축약판이지만 `variables_reported`는 optional.

권고:
- "small 7권 = paper schema"는 보류.
- "small 7권 = function classifier 후 paper_schema 또는 book_lite"로 바꾸는 게 안전하다.
- hard boundary는 page count가 아니라 `reports_new_measurements_or_primary_case_data`.

## 2. reference_data: flag-only vs 값 추출

찬성(flag-only):
- 초안의 환각방지 논리는 강하다. 논문 sidecar에서 배운 교훈과 맞다.
- exact value는 책/표/상수에서 가장 위험한 필드다. 모델이 숫자를 한번 틀리면 검색 필터 전체가 거짓 권위가 된다.
- 정본 미수정/staging 원칙과 잘 맞는다.

반대/리스크:
- IUPAC/TEOS 같은 reference-heavy book은 "값이 있다"만으로는 사용성이 낮을 수 있다.
- flag-only가 너무 헐거우면 모든 table chapter가 같은 의미로 뭉개진다.
- retrieval이 "어느 책 어느 페이지에 뭔가 있음"까지만 말하고, 실제 constant/equation identity를 못 가리면 책 corpus의 장점이 반감된다.

대안:
- v0: flag-only 유지. 단, flag의 타입을 세분화한다.
  - `reference_kind`: constant | solubility_table | isotope_ratio_reference | equation | conversion | calibration | standard
  - `locator`: page_range / section_id / table_id_candidate / equation_id_candidate
  - `value_extracted`: false
- v1: 값 후보는 별도 quarantined artifact로만 허용한다.
  - `reference_value_candidate`
  - `verified=false`
  - search/index default에서 제외
  - deterministic parser 또는 human/use-time read로만 승격

권고:
- v0는 값 추출 금지.
- 하지만 `reference_data`를 단순 문자열 배열로 두면 약하다. `reference_kind + locator + value_extracted=false` 구조로 바꿔야 한다.

## 3. topics/methods: free-text vs controlled vocab

찬성(free-text):
- 책은 표현이 넓고 교육적이라 controlled vocab만 쓰면 recall이 떨어진다.
- Gemma가 책 장의 주제를 자연어로 잘 요약할 가능성이 높다.

반대/리스크:
- free-text만 두면 cross-corpus 검색이 깨진다.
- 같은 개념이 표기 변형으로 분산된다.
- 논문 sidecar의 `variables_reported.id` / alias 체계와 연결되지 않아, "논문+책 같이 찾기"에서 후처리가 필요해진다.

대안:
- dual field를 둔다.
  - `topics_raw`: model text
  - `topics_norm`: controlled/alias-normalized ids
  - `methods_raw`
  - `methods_norm`
  - `isotope_systems_norm`
- controlled vocab은 처음부터 완벽히 만들지 말고, paper alias registry와 공유 가능한 핵심 축만 둔다.
- normalization confidence를 둔다: exact | alias | fuzzy | none.

권고:
- free-text only는 반대.
- controlled-only도 반대.
- v0는 raw + normalized dual로 가야 한다. raw는 recall, norm은 cross-corpus filter를 책임진다.

## 4. chapter boundary 탐지

찬성(heading/TOC 기반):
- heading이 있는 textbook에는 자연스럽고 검증 가능하다.
- chapter 단위 sidecar는 책 통째 sidecar보다 훨씬 검색 가능하다.

반대/리스크:
- heading 없는 handbook/data book/equation book에서 바로 깨진다.
- page marker는 chapter marker가 아니다. 초안이 이 점을 짚은 건 맞지만, 대안이 아직 약하다.
- segmentation 실패는 모델 품질보다 더 치명적이다. 잘못 자른 chunk의 sidecar는 아무리 잘 추출해도 잘못된 단위의 metadata가 된다.

대안:
- segmentation strategy를 tiered로 둔다.
  - tier1: explicit TOC/heading
  - tier2: repeated section title/page pattern
  - tier3: table/equation dense logical sections
  - tier4: fixed page-window with overlap
- 모든 segment에 `segment_method`와 `segment_confidence`를 붙인다.
- low-confidence segment는 production 승격 금지 또는 별도 review queue.
- IUPAC/TEOS류는 "chapter"가 아니라 `reference_section`/`table_family`/`equation_block` 단위를 허용해야 한다.

권고:
- `chapter_id`라는 이름만 쓰면 위험하다. v0 schema에 `segment_type`을 추가해야 한다.
- `segment_type`: chapter | section | reference_table_group | equation_block | page_window.
- `segment_confidence` 없이는 전수 production 금지.

## 5. book-level 요약 sidecar

찬성:
- 꼭 필요하다. chapter sidecar만으로는 "이 책이 무엇인지" 답할 수 없다.
- routing/search UI에서 source-level context가 필요하다.
- edition/version/coverage/facet summary는 chapter sidecar와 다른 레벨이다.

반대/리스크:
- generated summary를 권위 있게 쓰면 책 전체를 hallucinated synopsis로 덮을 수 있다.
- book-level summary가 너무 강하면 chapter retrieval을 누르고 잘못된 broad match를 만든다.

대안:
- `book_manifest`와 `book_summary`를 분리한다.
- `book_manifest`: deterministic/structural.
  - book_id, title, author/editor, edition/year if known, page_count, segment_count, segment_methods, coverage_norm counts
- `book_summary`: optional generated 1-2 sentence, search boost 낮게.

권고:
- book-level sidecar는 yes.
- 단, v0 필수는 `book_manifest`; generated summary는 optional/low-trust.

## 6. 책 청크를 논문 index와 합칠지 분리할지

합치기 찬성:
- 사용자는 한 번에 묻고 싶어 한다.
- 책 explanation과 논문 primary evidence를 같은 query에서 보는 UX는 좋다.

합치기 반대/리스크:
- 책은 broad educational match가 많아서 논문 primary evidence를 밀어낼 수 있다.
- score calibration이 다르다. chapter chunk와 paper abstract/body chunk를 같은 BM25/BGE score로 섞으면 랭킹이 왜곡된다.
- "값/상수/방법 설명"과 "측정 보고 논문"은 answer role이 다르다.

대안:
- physical index는 분리, query surface는 federated.
- source_type facet: paper | book_chapter | book_reference | book_manifest.
- result mixer는 per-source quota 또는 intent router 사용.
- default answer UI는 "papers"와 "books/reference"를 나란히 보여준다.

권고:
- v0에서 물리 통합은 반대.
- separate index + federated search + unified UI가 안전하다.
- 나중에 score calibration을 검증한 뒤 통합 여부를 재평가한다.

## 7. 추가 빈틈

### 7.1 schema versioning / migration

책 sidecar는 v0에서 바로 흔들릴 가능성이 크다. `schema_version`, `segment_schema_version`, `normalizer_version`, `prompt_version`을 명시하지 않으면 나중에 재추출과 비교가 어렵다.

권고: 모든 sidecar에 version quartet을 넣는다.

### 7.2 edition/version identity

책은 edition 차이가 크다. 같은 title이라도 edition/page/table이 달라질 수 있다.

권고: `book_id`는 title slug가 아니라 edition-aware id여야 한다. page locator는 edition에 종속된다는 사실을 manifest에 명시한다.

### 7.3 OCR/MD 품질 gate

책은 OCR/heading/table 손상이 sidecar 품질을 크게 좌우한다. 모델 추출 전에 MD 품질 gate가 필요하다.

권고: `md_quality`: ok | heading_weak | table_weak | ocr_suspect | page_markers_only.

### 7.4 equations/tables are not normal prose

reference/equation books는 prose summary보다 table/equation locator가 더 중요하다.

권고: `key_equations`도 값/식 본문을 추출하지 말고 `equation_present + locator + topic_norm` 중심으로 둔다. equation text extraction은 quarantined v1.

### 7.5 validation answer sheet가 과적합될 위험

holdout 6-8개는 좋지만, answer sheet가 free-text topic 위주면 precision/recall 평가가 흐려진다.

권고: holdout은 facet별 gold로 쪼갠다.
- segment boundary
- topic_norm
- method_norm
- reference_kind
- locator presence
- false value extraction count

### 7.6 GPU scheduling

논문 Gemma production 뒤에 책 Gemma가 직렬로 붙으면, book sidecar 실험은 stale context가 되기 쉽다.

권고: book sidecar는 model execution보다 먼저 schema/segmentation dry-run을 끝내야 한다. GPU가 비기기 전까지는 segmentation + manifest + tiny synthetic sidecar validation만 한다.

### 7.7 retrieval role labels

책 result는 "evidence"가 아니라 "background/reference/explanation"인 경우가 많다. 논문 result와 같은 evidence label로 보여주면 논증에서 오용된다.

권고: retrieval unit에 `source_role`: primary_evidence | review_context | textbook_explanation | reference_data_locator | method_background.

## 최소 v0 수정안

초안 schema를 크게 바꾸지 않고도 v0 안전성을 올리는 최소 변경:

```json
{
  "schema": "book_sidecar_chapter_v0",
  "book_id": "...",
  "book_manifest_id": "...",
  "segment_id": "...",
  "segment_type": "chapter|section|reference_table_group|equation_block|page_window",
  "segment_method": "toc|heading|pattern|table_dense|fixed_window",
  "segment_confidence": "high|medium|low",
  "page_range": "...",
  "content_type": ["explanation", "reference_table"],
  "topics_raw": [],
  "topics_norm": [],
  "methods_raw": [],
  "methods_norm": [],
  "isotope_systems_raw": [],
  "isotope_systems_norm": [],
  "reference_data": [
    {
      "reference_kind": "constant|table|equation|standard|calibration",
      "label_raw": "...",
      "label_norm": "...",
      "locator": "...",
      "value_extracted": false
    }
  ],
  "summary": "...",
  "md_quality": "ok|heading_weak|table_weak|ocr_suspect|page_markers_only"
}
```

Book-level:

```json
{
  "schema": "book_manifest_v0",
  "book_id": "...",
  "edition_key": "...",
  "page_count": 0,
  "segment_count": 0,
  "segment_confidence_counts": {},
  "coverage_norm_counts": {},
  "md_quality": "...",
  "generated_summary_present": false
}
```

## Final Recommendation

1. Accept book-specific sidecar.
2. Reject page-count-only small/book split.
3. Keep reference values out of v0 sidecar.
4. Strengthen reference_data from string flag to typed locator flag.
5. Add raw+normalized dual fields for topics/methods/isotope systems.
6. Add segment_type/method/confidence before any full extraction.
7. Add book_manifest_v0.
8. Keep paper and book physical indexes separate in v0; federate at query/UI layer.
9. Do schema/segmentation dry-run before waiting on GPU model execution.

If these changes land, the plan is safe enough for a staged Gemma book-sidecar pilot.
