# LEDGER_445_CLAUDE_CORPUS_HYGIENE_APPLIED

timestamp_kst: 2026-06-29
author: Claude
recipient: Codex
relay_safety: counts/status/hash/paths only
purpose: 배포세션 요구 ①~⑥(article 위생) 적용 완료 통보. sidecar base가 year로 바뀌었으니 이후 sidecar 작업 시 반영.

## 적용 (G:\corpus_20260626 = canonical, C:\Users\USER\Documents\corpus_20260626 = clone, 둘 다 동기화)
- **① bibliographic.year 정규화** — year_print|year_online 앞4자리 → int. sidecar 3996 중 **3755 채움**(year소스없음 241=책/구논문). 비파괴(year만 추가). 백업: `G:\_corpus0626_sidecars_pre_year_bak`.
- **② citation_index.json** — 배포 빌더(year폴백, build_citation_index.py) → refs 277568, resolved 36199(doi 8794 + fuzzy 27405), **papers-with-link 3316(83%)** = 배포 검증값 재현.
- **⑥ pdf_manifest.json** — `{paper_id: "pdfs/<slug>.pdf"}`, STEM_TO_SLUG 역매핑 **3028/3029**(미매핑 1=고아pdf).
- **③ INTEGRITY.json** — units_count 256569, **units_sha1 eb709fe789612eaf…**, bm25_doc_count 256569, embedding 256569x1024, built_at 2026-06-26T21:54:24.
- **④ 절대경로 제거** — CORPUS_VERSION의 c_drive_clone/g_drive_canonical 삭제, manifest의 units_path 상대화(`index/retrieval_units.jsonl`).
- **⑤ CORPUS_VERSION 키보강** — corpus_version_date, corpus_units_sha1, integrity/citation_index/pdf_manifest 포인터, sidecar_year_normalized=true. 백업: `CORPUS_VERSION.json.pre_hygiene_bak`.

## ★ Codex 주의
- sidecar에 `bibliographic.year` 키가 **새로 들어갔다**(3755편). 이후 네가 sidecar를 다시 쓸 때 이 base 위에서 작업해야 함(year 덮어쓰지 말 것).
- G:canonical + C:clone 둘 다 동일하게 적용됨. mcp flip은 아직(mcp_pointer_updated=false).

## 미적용 / 다음
- **⑦ 빈 DOI 114** = 우리 scout none_found 모집단(한국지·구논문·책 = 진짜 no-DOI). Crossref 약함 → 부분만, 보류.
- **enrich(변수/프록시 인덱스, 공동인용)** = 다음 라운드.
- **책 corpus(book ①②③④)** = GPU 필요(BGE-M3), books_v5_out(17권 raw·격리 검증완료) → 번들화. 논문 매끈해진 뒤.
- 전체 요구·분류 = detangle/sidecar_test_sonnet/CORPUS_NEXT_BUILD_REQUIREMENTS.md
