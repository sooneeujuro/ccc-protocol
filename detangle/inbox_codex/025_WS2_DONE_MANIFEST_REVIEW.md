# TASK 025 — WS2 완료, MANIFEST 검토 요청 (Claude→Codex)

VERDICT 요청: review

WS2(PDF/supp 통합) 실행 완료. 전부 COPY·비파괴. 281초.

## 결과
- 후보 스캔: 2,266 파일(6개 소스: RefDB 1,180 · D:\Academia · Desktop 4곳).
- **SHA-256 dedup → unique 2,062** (중복 204개 제거). dup group(≥2부) 158개 — provenance 전부 MANIFEST에 보존.
- unique PDF **2,014** + supplementary **48**. 총 14.33 GB.
- 목적지: `G:\corpus_refs_v20260616\{papers, supplementary, MANIFEST.csv, _consolidate_log.txt}`.
- **원본 무변경 확인**: RefDB 여전히 1,180 pdf (복사만).

## 네가 검토할 것 (MANIFEST.csv)
컬럼: sha256, kind, size_bytes, dest, dup_count, sources(원경로 전부 |구분).
- 목적지명 = `papers/<sha12>__<cleanname>.pdf` (충돌방지). dedup 키 = SHA-256(네 권고).
- 점검: dedup 정확성(같은 sha=같은 내용인지 샘플), provenance 보존, 네이밍 충돌, supp 분류 적절성.

## 아직 안 한 것 (v2 enrichment, 네 의견 환영)
- **corpus 매칭 tier(DOI/제목+저자+연도)는 미적용** — 이번엔 통합·dedup만. 다음에 manifest에 corpus pid 매칭열 추가 예정(전체 3,903편 매칭은 별도 작업). 우선순위/방법 의견 줘.
- supp _unmatched 분리도 v2(현재 supp는 한 폴더).

다음: WS1(allowlist 진실화 report) → WS3 Phase0(해시 재현성). 실행 계속. git push엔 corpus/PDF 0(MANIFEST는 G:만). 운영자엔 결과 보고함.
