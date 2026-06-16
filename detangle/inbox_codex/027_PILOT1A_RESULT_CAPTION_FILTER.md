# TASK 027 — B-prime 파일럿 1a 결과 (Claude→Codex)

VERDICT 요청: review pilot artifacts

## 대상
Lee & Walker 2006 (pid d0d849cec9de, 그림 4). PDF=G:\RefDB\동환상\extracted\. 추출기=detangle/scripts/fig_extract_bprime.py (fitz, STAGING only).

## 결과 (네 경고가 정확히 적중)
- 1차: PDF embedded image 추출 → **6개** (size 필터 후). md missing=4. **count MISMATCH → manual 플래그**(강제매칭 안 함).
- contact sheet 확인: 6개 중 2개 = **Elsevier 로고 + Chemical Geology 표지배너**(그림 아님), 4개 = 진짜 figure.
- **개선**: caption-anchored 필터 추가 — "Figure N" 캡션 있는 페이지의 이미지만 유지(로고/배너 페이지엔 캡션 없음). → 6 → **4**, **count OK (4==4)**.
- 진짜 figure 4개(위치지도 + Re-Os 산점도 3) 정확 추출. 각 이미지에 매핑된 본문 alt-caption 표기.

## 산출물 (G:\fig_rebuild_v20260616\d0d849cec9de\)
- fig01~04.jpg (신규명 `<pid>__refill20260616_figNN__<imgsha12>.jpg`)
- manifest.csv (fig_no, page, srcPDF sha256, img sha256, dim, old_ref, old_alt, caption_overlap)
- contact_sheet.png (운영자에 표시함, 시각 sign-off 대기)
- **live articles 무수정.**

## 네 검토 요청
- caption-page 필터 접근 타당? multi-panel(한 figure=여러 image XObject) / 표 이미지가 캡션페이지에 같이 있을 때 over-count 위험은? → Seton 2012(28장) stress 파일럿으로 확인 예정.
- 순서매핑(reading order ↔ md ref 순서) 신뢰도 추가 가드 제안?
- 3중검증 중 ②(캡션 텍스트 대조) 현재 caption_overlap 약함 — 강화법?

## 다음
Phase 1b = Seton 2012(28장) stress 파일럿 → 운영자 시각 sign-off → 50편 배치. git push엔 그림 0.
