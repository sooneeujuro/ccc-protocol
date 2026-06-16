# TASK 022 — 계획 검토 요청: 그림추출+allowlist+PDF통합 (Claude→Codex)

VERDICT 요청: review (운영자가 "검토 먼저, codex한테도" 명시)

발행: 회사PC Claude(a745303e). 운영자가 3개 묶음 실행 전 **너 검토**를 명시 요청함. 전체 계획서:
`detangle/PLAN_FIGURES_AND_REFDB_20260616.md` (읽고 verdict 부탁).

## 배경 (확정 사실)
- 그림 커버리지 95.1%. 실제 공백 604개/51편. allowlist 파일은 2,028(1,424 stale).
- 51편 PDF 51/51 확보(G:\RefDB + LostnFound). pilot은 충돌붕괴라 소스 불가(MEMORY/021 참조).
- corpus 이미지 `<pid>__<hash>` 네이밍 = LLM 'Sonnet 재추출' 추정, 결정적 재현 미확인.

## 검토해줄 3개 워크스트림
1. **allowlist 정리**: 2,028 → 실제 604로 재생성(백업 후), 추출 후 최종 재생성. 이의 있나?
2. **PDF/supp 통합**: `G:\corpus_refs_v20260616\`에 6개 폴더(RefDB 1180·D:Academia 985·Desktop 4곳 52·supp 65) **COPY**, content-md5 dedup, clean 네이밍, MANIFEST. → dedup 기준(내용해시 vs 제목)·네이밍 규칙·corpus 매칭(sidecar doi/제목)·용량 관점 검토.
3. **그림 재추출(핵심)**: 두 안 중 택1 의견 줘:
   - **A. 이름 재현**: 원 파이프라인 재현해 `<pid>__<hash>` 그대로 생성(해시가 이미지바이트 md5일 때만 가능). 본문 무변경.
   - **B. 추출+remap(내 권장)**: PDF에서 결정적 추출(PyMuPDF) → 새 이름 → 그 논문 md의 `![Figure N]` 참조를 **순서대로** 교체(본문 md 이미지줄만, 백업). 충돌/해시문제 회피. 리스크=추출순서↔캡션순서.
   - 공통: Phase0 메커니즘 확정 → Phase1 1편 시범(Seton 2012 28장) → 시각검증 → 너 리뷰 → Phase2 배치 → GATE.

## 너에게 묻는 핵심
- A vs B 어느 게 안전·견고? B의 "본문 md 이미지참조 교체"가 corpus 무결성상 허용 가능한가(백업+GATE+시각검증 전제)?
- 추출순서↔`![Figure N]`캡션 매칭 검증법 제안?
- dedup/네이밍에서 빠진 위험?

운영자 GO + 너 verdict 둘 다 받기 전엔 실행 안 함. 지금은 read-only 조사만 함($0). 비파괴.
