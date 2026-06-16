# TASK 036 — PDF/supp 수집 + 660 DOI provenance 판별 (Claude→Codex)

VERDICT 요청: DOI provenance 매칭 로직 + 187 신규 판정 타당성 검토.

## 1. 재색인 (035 후속) — 완료
- units 274,953/3,903 + bm25 832MB, 쿼리검증 OK. dense 보류(stale 마킹). 인덱스 백업 보관.

## 2. PDF/supp G드라이브 정리 — 완료 (운영자 "corpus명으로 복사")
- **PDF 3,665편 / 12.8GB → `G:\corpus_pdfs\<corpus_md_stem>.pdf`** (corpus 1:1).
- **supp 41편 / 211MB → `G:\corpus_supplementary\<corpus_md_stem>\`** (확정분만; 모호 9·corpus밖 13 제외).
- 소스: RefDB(동환상 875/홍씨 299/LostnFound 6) + **WonheeLee(논문 2774 + References 750)** = 메인.
- 매칭률: corpus 3,852편 중 **3,665(95.1%) PDF 확보**, 187편은 원본 PDF 없음(진짜 갭).

## 3. 660 corpus-밖 PDF 판별 — DOI provenance로 확정
**중요 교훈**: 처음에 파일명 정규화 fuzzy로 "신규 후보 660"이라 과대추정함. raw 파일명(`1-s2.0-…`, uuid, 홍씨\김동환 100% raw)이 corpus와 파일명 매칭 실패해 신규로 잡힌 것. 운영자 지적("변환 기록 안 보여?")으로 **sidecar provenance**를 발견:
- `sidecars\<PDF stem>.json` 에 `doi`, `bibliographic.title`, `provenance.md_file` 존재.
- corpus 전체 sidecar에서 DOI 1,840개 수집 → 660 PDF 첫 페이지 DOI(fitz 텍스트 추출, vision 불필요)와 대조.

결과 (`DOI_PROVENANCE_MATCH.json`):
- **DOI 중복 209** (raw명 → corpus DOI 정확 일치) + **제목 중복 255** = **중복 464 (70%)**
- **진짜 신규 187** (DOI 확인, corpus DOI에 없음) — 일부 책/thesis/리포트 포함, 저널논문은 더 적음
- 미정 9 (스캔 이미지, 텍스트 없음)

→ 660의 70%는 신규 아님(파일명만 다른 기존 논문). 진짜 편입 후보 = 187(운영자 결정: 리스트만 보존, 편입은 별도 — Datalab 변환비용).

## 검증 요청
1. DOI provenance 매칭 타당? (파일명 fuzzy → sidecar DOI 전환이 옳은가)
2. 제목 중복 255 (DOI 없이 title norm[:50])의 false positive 위험?
3. 187 신규 중 비-논문(책/thesis) 분리 필요?

## 산출물 (커밋됨, corpus 본문 아님 = 메타/스크립트만)
- scripts: pdf_corpus_map / supp_corpus_map / corpus_gap_report / pdf_orphan_classify / sidecar_provenance_check / doi_provenance_match / fig_md_textdiff
- maps: PDF_CORPUS_MAP / SUPP_CORPUS_MAP / CORPUS_GAP_REPORT / DOI_PROVENANCE_MATCH .json

## 하드게이트
- corpus 본문·그림·raw json·index **git push 0** (스크립트/매핑 메타만). 비파괴(전 백업 보관). 유료 Datalab 재호출 0.
