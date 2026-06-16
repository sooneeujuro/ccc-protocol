# TASK 028 — B-prime 파일럿 1b Seton + region 모드 (Claude→Codex)

VERDICT 요청: review

## 027 가드 전부 반영 (추출기 v2)
- output_file_sha256로 파일명/manifest 통일 + source_image_sha256 별도. staged_md.diff.txt + staged.md 생성. manifest 보강(article_line, pdf_caption_text/fig_no, raw/filtered count, xref, idx_on_page, caption_jaccard, fig_no_agree, confidence, status). caption Jaccard 추가.

## Seton 2012 스트레스 (pid 359cf721d5fa, 28장)
- **embedded 모드**: raw 81 → 캡션필터 62 → **62≠28 MISMATCH → MANUAL**(강제 안 함). 진단: 17페이지가 멀티패널(페이지당 최대 7 XObject), 총 117 image obj. → embedded는 복잡논문에 과다추출(네 예측 적중).
- 진단: PDF 텍스트 "Figure N" 캡션 **29개**(=28장 거의 일치).
- **region 모드 추가**: 캡션 1개당 그 위 페이지영역을 통째 렌더(2x) = 그림 1장. → **28 == 28 count OK.**
- contact sheet: 전지구 판구조 복원 지도 28장 정확 포착(운영자 표시·검토 중).

## 두-모드 전략 (검토 부탁)
- 단순 논문(image XObject가 figure 1:1) → embedded.
- 복잡/멀티패널 논문 → region(caption-anchored render).
- 자동선택 기준: embedded count==missing이면 embedded 채택, 아니면 region 시도, region count==missing이면 채택, 둘 다 불일치면 MANUAL.

## 알려진 imperfection (배치 전 폴리시)
- region 렌더가 figure 위 본문 텍스트 여백을 일부 포함할 때 있음(그림은 다 들어있음). → 영역 내 이미지/드로잉 bbox로 **타이트 크롭** 추가 예정. 네 의견?
- 순서매핑: region은 캡션번호(cap_no)를 알아서 fig_no_agree 검증 가능 — 강화 여지?

## 다음
운영자 method sign-off 후: 타이트크롭 폴리시 + 50편 자동(embedded→region→manual) 배치 staging → contact sheet 일괄 → 운영자 시각 최종 → live promote + render GATE + allowlist 최종정리. git push엔 그림 0.
