VERDICT: issues_found

# 홈PC TASK2 완료 — 문서 보존 PR + A3/A6/B8 폐기 + A4/A5 impl-diff

실행: 홈PC(`soone`) Claude. 운영자 "다" GO. 채널 `coop/detangle-20260615`.

## ① 홈 고유 문서 → ma main (완료, PR 열림)
- 깨끗한 worktree(origin/main 기반) `docs/home-detangle-records` → **289 files 전부 `docs/handoffs/` md/py/log, 코드·코퍼스 0** (검증: docs/handoffs 밖 0, .ts/jpg/png/csv/npy/pkl 0).
- 커밋 `600f9f2` → **PR #14** (https://github.com/sooneeujuro/manuscript-atelier/pull/14). 머지 클릭은 운영자/maestro.
- 포함: master_backlog_20260614.md · autonomous_run_20260614/(RUN_STATE+codex_verdicts+work/*.py) · fig_refill_20260613/FINAL_REPORT.md · hybrid_rrf_discussion_20260613/{EXPERIMENT,OPEN_QUESTION}.md · reader_ux_20260614/RUN_STATE.md.
- A3/A6/B8 **코드 변경은 경로선택으로 제외**(docs/handoffs만 checkout).

## ② A3/A6/B8 코드 = 폐기 확정 ✅
- main이 `92c0f01`(A6 worker)·`db82739`(B8 caps)·`4047b89`(A3 docs)로 이미 보유. 추가 작업 0. 코드 아카이브 = F: 번들. 

## ③ geochem A4/A5 impl-diff (read-only, 커밋 0) — Codex 판정 요청
- diff 파일: **`detangle/scratch/A4A5_home_vs_origin.diff`** (615줄, `-`=origin / `+`=홈, secret 0).
- 홈 고유 verify 스크립트(origin 없음): `scripts/verify_{correlation_null,export_sanitize,generator_sinks}.mjs`.

### ⚠️ 핵심 결론: **origin이 대체로 동급~우월. 홈 코드엔 잠재 회귀 있음.** 살릴 delta는 적음.

**A4 — statistics.ts (origin 우월, 홈 채택 비권장)**
- 홈: `calculateCorrelationMatrix` → `number|null`(명시적 null). 깔끔하지만,
- 홈 `suggestPCAVariables`는 `finiteAbsAvg` 없이 **plain `Math.abs(corr)` 합산** → 셀이 null이면 JS가 `Math.abs(null)=0`으로 강제 → **"결측을 0(무상관)으로 둔갑" 정책위반 재유입(잠재버그)**.
- origin: `calculateCorrelationMatrix`는 NaN 보존(JSON→null 동일효과) + `suggestPCAVariables`에 **`finiteAbsAvg`로 비유한 셀 명시적 제외**(그룹탐색·정렬·PCA검증 전부). → **origin이 no-zero-fill을 일관되게 더 견고히 구현.**
- 권고: **origin 유지**, 홈 statistics.ts 폐기. (단 Codex가 origin 쪽도 `suggestPCAVariables`에 어떤 matrix(null/NaN)가 실제 주입되는지 1회 확인.)

**A5 — python-export.ts / ternary-piper-export.ts (혼재, 대체로 origin 동급+)**
- 둘 다 generated-Python injection escape 구현하나 방식 다름:
  - 홈: 공유모듈 `export-sanitize.ts`(`safeColor/pyStr/safeLinestyle/pyDocSafe`)를 다수 sink에 적용(중앙집중, 깔끔).
  - origin: 로컬 `pyQuote()` + inline escape. **docstring `spec.name` escape**(홈은 raw로 둠=홈 gap) + **`options.presetOverride` 지원**(홈은 제거=기능 누락) 보유.
  - ⚠️ **홈 회귀**: ternary-piper의 공유 `piperToMeqPercent()`(Python·SVG preview 공용, drift 방지용 추출)를 **홈이 다시 inline 중복화**. origin이 더 나음.
- 권고: **origin 코드 유지**. 홈의 유일한 실질가치 = (a) 중앙집중 sanitizer 모듈은 리팩터 취향(신규 커버리지 아님), (b) **verify 스크립트 3개 = origin에 없는 테스트** → origin 구현 검증용으로 **포팅 고려**.

### 살릴 delta 요약
| 항목 | 판정 |
|---|---|
| A4 statistics.ts | origin 우월, 홈 폐기 (홈 null→0 강제 잠재버그) |
| A5 export sanitize 코드 | origin 동급+, 홈 폐기 (piperToMeqPercent 중복화 회귀) |
| verify_*.mjs 3개 | **유일한 salvage 후보** — origin 구현 테스트로 포팅 가능 |

## 제약 준수
- geochem **diff만 추출**(커밋/푸시 0). 코퍼스 push 0. main 보존 = **문서 only**(코드 제외). worktree 정리 예정.

→ Codex `inbox_codex/003` 수행: 위 판정 교차검증 + verify 스크립트 포팅 가치 결정.
