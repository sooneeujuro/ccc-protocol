# 다음 corpus 번들 빌드 요구사항 + 분류 (배포세션 → 빌드세션)

출처: 2026-06-29 실배포(corpus_20260626) 실측 핸드오프 2건 (article + book). 분류 = Claude 검토 + 현 번들 실측.
저장 이유: 다음 corpus/book 번들 빌드 시 이 문서를 스펙으로 사용.

## 현 번들 실측 (2026-06-29, C:\Users\USER\Documents\corpus_20260626 clone)
- sidecar.bibliographic = {authors_full,title,journal,volume,issue,pages,year_print,year_online,publisher} → **`year` 키 없음** (year_print/online만)
- references[] 존재(샘플 14개) = 인용 빌더 소스 OK
- 번들에 citation_index.json / INTEGRITY.json / pdf_manifest.json **전부 없음**
- pdfs/ = **hash명**(`001e3e69d1b2.pdf`) — articles paper_id와 다름 → 매핑 필수
- CORPUS_VERSION.json에 `c_drive_clone`(C:\…) + `g_drive_canonical`(G:\…) 절대경로 stale
- doi_empty 114 / doi_nonempty 3882 (DOI scout 적용 후)
- books_v5_out(G:) = 17 slug raw 폴더, sidecar/index 없음 = datalab 재추출만, 번들화 안 됨

---

## ARTICLE 빌드 요구 — 분류

### ✅ 수용 (쉬움·임팩트 큼, 다음 빌드에 바로)
- **① `bibliographic.year` 정규화 ★최우선** — year_print 우선, 없으면 year_online 앞4자리 → int. 결정론적. 인용링크 1,296→3,316 복구(실측). [build_0626 sidecar 단계 or 후처리에 1줄]
- **③ INTEGRITY.json** — `{units_count, units_sha1, bm25_doc_count, embedding_rows, embedding_dim, built_at}` 한 장. 흩어진 메타 모으기 + units_sha1만 확실히. 배포 자동검증용.
- **④ 절대경로 제거** — manifest의 units_path / CORPUS_VERSION의 C:\·G:\ → 상대경로/파일명. 이식성(이번 G→C 이식에서 stale 확인).
- **⑤ CORPUS_VERSION 키 보강** — `corpus_version_date`("2026-06-26"), `corpus_units_sha1`(=units_sha1) 추가 (배포 리더가 이 키명으로 읽음).
- **⑥ pdf_manifest.json** — `{paper_id: "pdfs/<file>.pdf"}`. pdf=hash명이라 리더가 ~2/3 못 찾음(실측) → 매핑이 가장 robust. 임팩트 큼.

### ✅ 수용 (중간 작업, 가치 큼)
- **② citation_index.json 번들 포함** — `{corpus,n_papers,doi_index,cites:{pid:[{idx,to,method,score}]},cited_by}`. references[] DOI-exact + (저자+연도+제목) fuzzy 매칭. **①year 폴백 필수.** 배포세션이 빌더 스크립트(year폴백 패치본) 제공 가능 → 받아서 검토 후 적용.

### ⚠️ 힘든 것 (부분만 가능)
- **⑦ 빈 DOI 114 백필(JAKO/국내지)** — 우리 DOI scout에서 이미 본 잔여: 대부분 **진짜 no-DOI**(한국 J.Eng.Geol·JVGR일부·구논문·책). Crossref/JAKO 커버 약함. 일부만 회수 가능, 나머지는 천장. (scout none_found와 동일 모집단)

### ⏸ 되는데 안 함 (가치 있으나 우선순위/규모상 다음 라운드)
- **enrich: 변수/프록시 인덱스** — units의 `variables` 177,618청크 → "어느 논문이 어느 동위원소계 측정" 인덱싱. **우리 Gemma inventory의 본래 목적** → 가치 최상위, 단 큰 설계+데이터작업. 다음 우선 검토 0순위로.
- **enrich: 공동인용/서지결합 그래프** — ②citation_index 위 한 단계. 여유 시.

---

## BOOK 빌드 요구 — 분류
전제: books_v5_out = raw 17 slug(번들화 X). 책 번들은 "논문 뒤 GPU"로 예정됨(BOOK_SIDECAR_PLAN.md). 아래는 그 빌드 스펙.
★배포세션 핵심 발견: 기존 per-book 16권/18인덱스(PR-BOOK8, 35,227 units)는 **라이브 리더가 코드상 전혀 안 봄 = parked**. "또 만들고 또 parked" 방지가 1순위.
정책: CORPUS_POLICY §1 (책=별도 namespace, index-level 병합 금지, 조인은 retrieval 시점에만) 준수.

### ✅ 수용 (핵심 방향, 배포가 서빙 받침)
- **① 서빙 가능한 단일 book corpus_root** — per-book 분리는 유지하되 article 번들과 **동일 스키마**(index/{bm25,bge_m3 npy dim1024 L2 row-align,retrieval_units,retrieval_papers,STEM_TO_SLUG} + sidecars/ + slug figure + CORPUS_VERSION + INTEGRITY). → 배포가 corpus-atelier 리더를 **두 번째 인스턴스(:8768)로 띄워 서빙(코드 0줄)**, article과는 retrieval RRF/점수융합. 정책 준수. **parked 탈출 = 1순위.**
  - 주의: BM25 IDF per-book→전역(서빙엔 보통 더 나음). per-book IDF 유지 필요시만 별도.
- **② 책 sidecar 부여 + 인용 타겟화 ★최대 enrich** — 책에 bibliographic{title,authors/editors,year(정규화),publisher,ISBN,doi,book/chapter flag}. 인용 빌더를 **articles+books 타겟 공간**에서 → 논문→책 인용 해소. rudnick_gao_2003/faure_mensing/ozima_podosek = 논문이 가장 많이 인용하는 정전 노드 → dangling 인용이 in-corpus 엣지로. (retrieval은 분리 유지, **타겟 인덱스만** 양쪽.) book_manifest(BOOK_SIDECAR_PLAN)와 정렬.
- **③ 책 특화 구조** — page_start/end 정확(책 인용=페이지 필수), 깨끗한 book_id(faure_mensing_2005式, 전역유일), 청크=권 단위 기본(챕터 독립 인용대상일 때만 챕터) + PR-META1 paper_title/text_inline 재사용, variant(IUPAC/TEOS-10)는 canonical 1개만. → BOOK_SIDECAR_PLAN.md에 이미 설계됨.
- **④ dedup + 위생** — article↔book 중복제거(리뷰 양쪽), year정규화, INTEGRITY, 절대경로 금지, CORPUS_VERSION 키를 리더 읽는 이름으로. (article 요구 ①③④⑤와 동일)

### ⏸ 규모/순서 (수용하되 비용)
- books_v5_out 번들화 자체 = stitch + 책 sidecar + BGE-M3 GPU 임베딩 + index. GPU 작업(논문 DOI/재인덱스 뒤). 힘들진 않으나 GPU 시간.
- hybrid 와이어링(PR-BOOK10 미결) = 배포세션이 "두 번째 리더 인스턴스 + RRF/점수융합"으로 해결 → 빌드는 서빙 스키마만, 와이어링은 배포가.

---

## 실행 우선순위 (배포세션 권고 + Claude)
- **article 최소셋: ①②⑥** (year + citation_index + pdf_manifest) = 임팩트 최대.
- 그담 ③④⑤(위생) → ⑦(부분) → enrich 변수인덱스.
- book: 논문 article 빌드 매끈해진 뒤 → ①서빙단일root + ②인용타겟 동시.
- ② citation 빌더 스크립트(year폴백 패치본)는 배포세션이 제공 — 받아서 detangle/sidecar_test_sonnet/에 보관.
