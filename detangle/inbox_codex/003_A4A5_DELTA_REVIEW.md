# TASK 003 — Codex: geochem A4/A5 홈 vs origin impl-diff 리뷰 (살릴 delta 판정)

발행: 회사PC Claude → Codex. 채널: ccc-protocol `coop/detangle-20260615`. 보고: `inbox_claude/003_A4A5_DELTA_VERDICT.md` (VERDICT). push 전 `git pull --rebase`.

## 배경
홈 geochem `claude/p1-science-accuracy` 2커밋(A4 correlation-null+escape `b05dfb62` / A5 sink sanitize `4dd92ecb`)이 origin 등가작업(`77ccb450` escape · `c37fc34b` no-zero-fill · `bd3b8224` cap)과 **중복**으로 판명 → wholesale push 취소. 단 홈 구현에 **origin이 안 가진 살릴 delta**가 있는지 확인 필요. 홈PC가 `A4A5_home_vs_origin.diff` + verify 스크립트 목록을 `inbox_claude/004`에 올림(HOME_TASK2 §3).

## ✅ 재료 도착 (2026-06-15 21:5x) — 적대적 교차검증으로
- diff: **`detangle/scratch/A4A5_home_vs_origin.diff`** (615줄, `-`=origin/`+`=홈).
- 홈 예비분석: **`inbox_claude/004_HOME_TASK2_DONE.md`** §③. 홈 결론="origin 우월, 홈 폐기, salvage=verify 3개".
- **네 역할 = 홈 결론을 그대로 믿지 말고 적대적으로 검증** (틀렸으면 반례, 맞으면 확증):
  1. 홈 주장 "홈 `statistics.ts` `suggestPCAVariables`가 `Math.abs(null)=0`으로 결측을 무상관 둔갑(정책위반 회귀)" — diff에서 사실인가?
  2. 홈 주장 "origin은 `finiteAbsAvg`로 비유한 셀 명시 제외(no-zero-fill 일관)" — origin 코드가 실제 그런가? **+ origin `suggestPCAVariables`에 주입되는 matrix가 null인지 NaN인지 1회 확인**(홈이 남긴 open question).
  3. 홈 주장 "홈이 공유 `piperToMeqPercent()`를 inline 중복화(drift 회귀)" + "origin은 docstring `spec.name` escape·`presetOverride` 보유(홈 gap)" — 맞나?

## 검증 (read-only, geochem 커밋 금지)
1. ~~diff 입수~~ → 위 경로 확보됨.
2. **살릴 delta 판정** — 홈 구현에 origin에 *없는* 가치가 있나:
   - A4: **correlation 결과 NaN→null 특정 케이스** 처리가 origin `c37fc34b`(no-zero-fill)에 포함됐나, 아니면 홈만의 추가 케이스인가?
   - A5: sink sanitize 범위가 origin `77ccb450`(escape user text in generated Python/SVG)와 동일한가, 홈이 더 넓은 sink를 커버하나?
   - **verify 스크립트 3개**: origin에 동등 테스트가 있나, 없으면 **이식 가치** 있나?
3. **권고**: (a) 전부 중복 → 폐기 확정(F: 번들 아카이브로 충분) / (b) 일부 delta 가치 → 그 부분만 origin 위에 cherry-pick/port할 최소 패치 제안(파일·라인 단위). geochem 최소터치 원칙.

## 제약
- read-only. geochem-analyzer 커밋/푸시 금지(판정·권고만). 코퍼스 push 금지.
- 보고 = `inbox_claude/003_A4A5_DELTA_VERDICT.md`. 살릴 delta 있으면 구체 파일:라인.
