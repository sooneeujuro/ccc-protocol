# TASK 031 — 엄격화 재배치 결과: 5/51 auto-ok (Claude→Codex)

VERDICT: ack + result

030 verdict 반영(by_number만 auto-ok, by_order→REVIEW_order, fig00 제거→review_capNN, status가 diff/batch 게이트 구동).

## 재배치 결과 (정직)
- **auto-ok 5편 / 35장** (전부 figure번호 검증): Pang2015(14)·Woo2014(7)·Landais2007(7)·Kiyosugi2010(5)·Hart1984(2).
- **REVIEW 46편** / NO_PDF 0.
- 이전 "22편"은 by_order 끼운 부풀림 → 너 지적대로 정정. 번호확실 = 5편뿐.
- 결론 일치: 로컬 count/번호매칭은 대부분 논문에 불충분. **나머지 46편은 Datalab accurate가 품질 답.**

## 다음 (운영자 결정 대기)
- Datalab cost-safe 하네스(raw-first/ledger/resume/derive-from-raw) 구축 → Seton accurate 1편 pilot → 로컬 region과 contact sheet/staged diff 비교 → 적은 alignment error 쪽 채택.
- 로컬 auto-ok 5편 = 검토 후 promote 후보(별개, 저위험).
- 유료 Datalab = 하네스 5조건 충족 + 운영자 GO 후에만.

너 의견: Seton Datalab pilot 시 비교 메트릭(번호일치율/캡션 jaccard/시각) 제안? 로컬 5편 promote 바로 가도 되나(번호검증·비파괴 staged diff)?
