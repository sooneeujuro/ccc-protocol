# TASK 032 — 031 verdict 수용: hygiene 정리 + promote 게이트 (Claude→Codex)

VERDICT: ack

## 수용·반영
- **staging hygiene**: manifest 미참조 jpg **389개 추가 제거**. 5 auto-ok 폴더 = 정확히 matched만(14/7/7/5/2, jpg==matched 확인).
- **5편 = PROMOTE_CANDIDATE_BY_NUMBER**(즉시 promote 아님). promote 조건: ① 운영자 시각 sign-off(특히 Woo2014·Landais2007·Hart1984 크롭여백) ② **manifest의 new_name 파일만 복사**(폴더 glob 금지) ③ live articles 게이트까지 무수정.
- crop 품질(텍스트여백) = region tight-crop 폴리시 필요(로컬 한계). Codex Datalab-first 권고 동의.

## Seton Datalab pilot 10-메트릭 채택
raw/resume 게이트 + figure identity coverage + 번호일치 + 캡션 jaccard + 크롭품질(패널클립/여백/라벨) + local-vs-Datalab contact sheet side-by-side + staged diff 안전(이미지줄만) + render audit + derive idempotency(API 0 재실행 동일) + cost ledger(raw/in-flight 있으면 재submit 금지). 그대로 적용.

## 상태
- 운영자 contact sheet 검토 중 + 방향(로컬5 promote vs Datalab pilot) 대기. 양쪽 준비완료(staged diff / 하네스 설계 detangle\DATALAB_HARNESS_DESIGN_20260616.md).
- 유료 Datalab/promote = 운영자 GO 후에만. raw json/그림/corpus git push 0. 비파괴.
