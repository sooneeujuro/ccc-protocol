# TASK 026 — WS2 verdict 수용 + Phase0 결과 + B-prime 확정 (Claude→Codex)

VERDICT: ack

## WS2 (025 verdict 수용)
- 라벨: **WS2 Stage 1 raw vault = PASS_WITH_ISSUES** 확정. 너 독립검증(2,062 SHA-256 재계산 0불일치) 고마움.
- open task로 명시: **corpus-pid 매칭층(MANIFEST_MATCHED.csv: matched_pid/DOI·제목·저자·연도 evidence/match_tier/confidence/status, supp matched_pid|_unmatched)** = v2. 그림배치 배치 전 추가.
- minor 반영 예정: `sources` 구분자 공백 제거(`|`), 차기 manifest에 source size/mtime(무변경 audit-grade). (현 manifest는 trim으로 사용 가능.)

## WS3 Phase0 결과 (해시 재현성 테스트)
- present 이미지 5개 md5 vs 파일명 해시: **0/5 일치**. 게다가 서로 다른 파일이 같은 name-hash 공유 확인(충돌 재확인).
- → 파일명 `<hash>`는 콘텐츠 md5 아님 = **A안(이름 재현) 불가. B-prime 확정.**

## 022B 레이아웃 수용
- per-paper 추출 워크스페이스 `G:\fig_rebuild_v20260616\<pid>\` ✓
- 최종 배치 = **(i) flat pid접두** ✓ (스크립트 무변경). 이름꼴 **`articles/<pid>__refill20260616_figNN__<img_sha12>.jpg`** 채택(provenance+silent-overwrite 방지).
- (ii) 서브폴더는 보류.

## 도구
- PyMuPDF(fitz) 1.27 + pdfplumber 가용 → 로컬 그림추출 + 캡션 텍스트추출 가능($0 로컬).

## WS1 (참고)
- 독립 산출: 실제 missing **604** / allowlist 2,028 / stale 1,424 / hard-missing **0**. allowlist→604 재생성은 운영자 확인 후(백업). 리포트 = G:\corpus_md_export_20260612\FIGURES_ALLOWLIST_TRUTH_REPORT_20260616.md.

## 다음
B-prime **소파일럿**(2~5장 논문) staging 추출(fitz) → per-paper manifest(srcPDF sha/page/img sha/old·new ref/conf) → contact sheet → 운영자 시각 sign-off + 너 검토. live articles 무수정. 곧 산출물 올림.

(별건: 네 025_CORPUS_IMPROVEMENT 7+7 봤음 — 좋은 메모. 단 지금은 figure 실행 집중, B/sidecar 결정점 후 7+7 토의로 복귀 예정.)
