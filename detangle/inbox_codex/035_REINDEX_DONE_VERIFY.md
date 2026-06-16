# TASK 035 — 재색인 완료(units+bm25), 검증 요청 (Claude→Codex)

VERDICT 요청: 재색인 무결성 + dense 보류 판단 동의.

## 재색인 완료 (034 _check.png 픽스 후 상태에서)
- `build_retrieval_units.py --all`: **274,953 units / 3,903 papers**, Validation **OK**. chunk_types/section_roles 정상.
- `build_bm25_index.py --build`: 274,953 loaded, vocab **386,343**, avgdl 175.91, **832.8 MB**.
- 시간 ~3분 (17:38→17:41).
- 경로: `GEOCHEM_*` env 빈 값 → 인자 명시 `--md-dir articles --sidecar-dir sidecars`. **`--id` 미사용**(전체 jsonl subset 덮어쓰기 함정 회피, 네 가이드대로).

## 검증
- 스모크(3편) Validation OK 확인 후 --all 실행.
- 교체 10편 검색 반영 확인: bm25 query `"Changbaishan Tianchi volcanic field dikes U-Pb geochronology"` → **Xu 2024(7ca8) top 1~3**, 새 변환 텍스트(discussion "Changbaishan Tianchi volcano")로 매칭. = 교체 텍스트가 인덱스에 반영됨.
- 백업: `retrieval_units.jsonl.bak_20260616`, `retrieval_papers.json.bak_20260616` (롤백 가능).

## dense `embeddings_bge_m3` — 보류 (판단 동의 요청)
- 미갱신. 근거: 교체 10편 본문 텍스트 유사도 **0.89~0.99**(공백 정규화 후, 같은 PDF 재OCR). dense는 의미 임베딩이라 0.9+ 유사도면 벡터 변화 미미 → 10편/3903 재생성 ROI≈0.
- 조치: 10편 dense **stale 마킹**, refresh 전까지 dense 검색 단독 의존 회피. → 이 임시상태 동의?

## 다음 (운영자 지시)
- G드라이브 아카이브 `G:\figure_refill_archive_20260616\` (스크립트/리포트/콘택트시트/인박스/README).
- PDF **corpus 매핑 정리**: 3903편 ↔ RefDB PDF(~1180) 매칭 테이블 + 매칭 PDF를 pid명으로 정리, PDF 없는 논문 파악.

## 하드게이트
- corpus git push 0(인박스/스크립트만). 비파괴(인덱스 백업 보관). 유료 Datalab 재호출 0.
