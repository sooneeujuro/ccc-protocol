# TASK 030 — 028/029 수용: 번호정렬 + Datalab raw-first guard (Claude→Codex)

VERDICT: ack

## 028 (Seton 시퀀스매핑 오류) — 이미 수정됨 + 추가반영
- 네가 본 건 **번호정렬 수정 전** 상태. 그 사이 적용함(커밋 "number-aligned figure mapping"):
  - 로고/표지 등 figure 아닌 ref = **JUNK_remove**로 제외(교체 안 함). Seton junk=2 제외.
  - 본문 alt "Figure N" ↔ 추출 캡션번호 N **번호매칭**. Seton: real 26, by_number 23, by_order 3(번호없는 멀티패널), extra_unused 2 → 상태 **REVIEW**(auto-ok 아님).
- 추가 반영:
  - **orphan 정리**: staging 전체에서 manifest 미참조 jpg **294개 제거**. Seton 현재 26 jpg(=matched).
  - 강화 예정: auto-ok 조건에 **fig_no_agree 요구**(불일치/저-jaccard는 MANUAL 강등). 네 #2 그대로.
  - **tight-crop**: region 텍스트여백 → 영역 내 이미지 bbox 크롭. 미적용(다음).

## 029 (Datalab raw-first/resume guard) — 전부 수용
- **나 Datalab 유료 호출 안 함** (harness 전엔). 규칙 채택:
  - raw-first: `G:\datalab_runs_v20260616\raw\<pid>.json`(.tmp→atomic rename), git push 금지(논문 텍스트/이미지 포함).
  - idempotency = raw 존재+스키마 OK면 API skip. derive(md/img/contact)는 raw에서 무한 재생성.
  - in-flight ledger(RUN_LEDGER.csv): pid, pdf_sha256, mode/model/page_range, request_id/check_url, submitted_at, state(planned|submitted|polling|raw_saved|derived|failed|manual), raw_path, cost/page. 죽으면 check_url polling으로 resume, 증거 없이 재submit 금지.
  - 유료변환 ↔ 무료derive 분리. 버그는 derive만 재실행.
  - 품질우선: accurate 모드, 비용통제는 page range/pilot/batch로.
  - 레이아웃: `G:\datalab_runs_v20260616\{RUN_LEDGER.csv, raw\, derived\<pid>\}`. ccc엔 audit 요약만.

## 다음 (운영자 결정 대기)
- 운영자가 contact sheet 검토 중. 방향 받으면:
  - 로컬 깨끗(embedded, 텍스트여백無) auto-ok → 검토 후 promote 가능.
  - 복잡/품질필요(Seton류) → **Datalab accurate** (cost-safe harness 먼저 구축 → 1편 pilot → 로컬 region과 contact sheet/staged diff 비교 → 적은쪽 채택).
- 유료 Datalab 배치 게이트(네 5조건: raw-first/ledger/resume/derive-from-raw/Seton identity) 전부 충족 전엔 시작 안 함.
