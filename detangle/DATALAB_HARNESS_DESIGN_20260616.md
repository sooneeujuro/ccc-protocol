# Datalab 비용-안전 하네스 설계 (호출 전 스펙) — 2026-06-16 15:24

작성: Claude(a745303e). **설계만. 유료 호출 0. 운영자 GO + 하네스 구현 후에만 실행.**

## 그라운딩 (확인된 사실)
- Datalab = Marker API(datalab.to): PDF→markdown+이미지. `DATALAB_API_KEY`(.env). 기존 pilot이 이 출력(`NAS\datalab\pilot`).
- async: submit → request_check_url polling → 완료시 md+images 반환. 호출당 과금.

## 레이아웃 (git 밖, 논문데이터 push 금지)
```
G:\datalab_runs_v20260616\
  RUN_LEDGER.csv          # 인플라이트/완료 추적
  raw\<pid>.json(.tmp→atomic)   # Marker 원응답(파싱 전)
  derived\<pid>\{manifest.csv, staged.md, staged_md.diff.txt, contact_sheet.png, images\}
```

## RUN_LEDGER.csv 컬럼
pid, pdf_path, pdf_sha256, mode(accurate), page_range, request_id, check_url, submitted_at, state, raw_path, cost_est, note
- state: planned|submitted|polling|raw_saved|derived|failed|manual

## 파이프라인 (유료↔무료 분리)
1. **submit**(유료): raw\<pid>.json 없고 ledger에 미완 request 없을 때만. submit 직후 ledger에 request_id/check_url/submitted_at + state=submitted **먼저 기록**(원자적).
2. **poll**: check_url polling → 완료시 raw\<pid>.json.tmp 저장 후 atomic rename → state=raw_saved.
3. **derive**(무료, 무한 재실행): raw에서 md+images 파싱 → 그림을 articles 이름규칙으로 → 본문 ref 번호정렬 매핑(로컬과 동일 가드) → staged diff + contact sheet. state=derived.
4. **resume**: 죽으면 ledger 읽어 submitted/polling 상태는 check_url로 이어받음. **raw 있으면 submit 금지(API skip).** 증거 없이 재submit 금지.

## 비용 가드
- 1편 pilot(Seton) 먼저 → 비용/품질 확인 → 운영자 GO 후 배치.
- page_range로 제한 가능. accurate 모드(품질우선, 비용은 pilot/batch 크기로 통제).
- idempotency: raw 존재 = 재호출 안 함. derive 버그는 derive만 재실행(무료).

## 비교 메트릭 (Datalab vs 로컬 region, Seton)
- figure 번호일치율(by_number/real), 캡션 jaccard 평균, extra_unused, 시각(contact sheet 나란히).
- alignment error 적은 쪽 채택(가격 아닌 품질 기준).

## 게이트
유료 호출 = 하네스 구현(raw-first/ledger/resume/derive-from-raw) + 운영자 GO 후에만. raw json/그림/corpus git push 금지. 비파괴.
