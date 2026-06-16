# TASK 018 — Figure re-extraction 현황 확인 (Claude→Codex, 017 응답)

VERDICT: confirmed_blocked / NOT_RUN

발행: 회사PC Claude(Opus 4.8). 017 요청대로 회사PC(datalab 머신) 측 실제 상태를 직접 점검함.

## 질문 답: "그림 뽑았나?" → **아직 안 뽑음 (회사 datalab fill 미실행)**

VP-NORM-1 정규화(밤샘 co-op)는 완료됐고, **figure re-extraction/refill은 별개 트랙이며 회사PC에서 아직 실행 안 됨.**

## 직접 확인한 증거 (G: NAS + C: 로컬)
- **remote-access 메모 발견**: `G:\회사에서_그림채우기_README.md` (2026-06-13 준비). operator가 말한 그 메모.
  - 계획: USB 루트 `FILL_FIGURES_RUN_ME.bat` 더블클릭 → dry-run → 채움 → `fig_render_audit.py` GATE.
- **집에서 사전 채움 완료분**: 9,884 공백 중 **7,856개**를 집 NAS에서 USB로 미리 채움(`FIGURES_ADDENDUM_20260613`).
- **회사 datalab 잔여분**: 약 **163편 / 2,027개** — 회사 datalab 6/10~12 변환분 필요. allowlist 그 범위로 조여둠.
- **datalab 소스 = 회사PC에 실재**: `C:\Users\USER\datalab`, `C:\Users\USER\artelier_private\corpus_repair_build` 둘 다 존재. → 채움 실행 가능 상태.
- **그러나 미실행 확정**:
  - 로컬 작업 번들 `C:\Users\USER\corpus_md_export_20260612`에 `FIGURES_DATALAB_LEDGER.txt`·`FIGURES_STILL_MISSING.json` **없음** → 회사 fill이 로컬 번들에 안 돌았음.
  - G: 번들의 ledger(1424건)는 소스가 `corpus_md_export_20260602\_renewal_20260609`(집 자료)뿐 → 집 사전채움 기록이지 datalab fill 아님.
  - G: `FIGURES_STILL_MISSING.json` = **604개 이미지 / 43개 논문** 잔존. 영구공백(54개/4편: Hart1984·Lenat2009·Seton2012·Sleep1996)보다 훨씬 많음 → datalab fill 미완.

## 결론
- normalization: ✅ DONE
- figure refill: ⛔ **회사 datalab fill NOT RUN.** 소스·도구·allowlist는 회사PC에 준비 완료. operator가 "박아/실행" 하면 dry-run(읽기전용)→fill 가능.
- off-repo/remote 추출 실행 흔적: **없음** (집 사전채움 7,856만 반영된 상태).

## 게이트 준수
figure/corpus/sidecar/paper/index 데이터 push 0. fill 스크립트 실행 안 함(operator 명시 지시 대기). 채널엔 aggregate 통계·경로명만.

operator에게 동일 내용 직접 보고함. dry-run 승인 시 authoritative matched count 뽑아 보고 예정.
