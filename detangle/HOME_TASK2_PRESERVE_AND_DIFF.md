# 홈PC TASK2 — 홈 고유 문서 보존(cherry-pick) + A4/A5 델타 추출 (운영자 GO="다")

발행: 회사PC Claude(maestro) → 홈PC. 채널: ccc-protocol `coop/detangle-20260615`. 보고: `inbox_claude/004_HOME_TASK2_DONE.md`. push 전 `git pull --rebase`.
재료가 홈PC에만 있어(senpai 분기 + F: 번들) 회사PC가 직접 못 함 → 노트북이 실행.

## 결정 (운영자 "다" GO)
1. **홈 고유 문서 → ma `main` 보존** (clean cherry-pick).
2. **A3/A6/B8 코드 = 폐기 확정** (main 이미 보유 + F: 번들 백업) — push/머지 안 함, 추가 작업 0.
3. **geochem A4/A5 = impl-diff 추출** → Codex가 살릴 delta 판정.

## 1. 홈 고유 문서 cherry-pick → ma main (코드 아님, 무충돌)
대상(senpai에만 있고 main에 없는 **문서/기록**, 코퍼스 아님):
- `docs/handoffs/master_backlog_20260614.md`
- `docs/handoffs/autonomous_run_20260614/` (RUN_STATE + codex_verdicts + work/*.py 중 **committed인 것**)
- `docs/handoffs/fig_refill_20260613/FINAL_REPORT.md` (FINAL_REPORT만 — out*/ledger 등 산출물·코퍼스 제외)
- `docs/handoffs/hybrid_rrf_discussion_20260613/{EXPERIMENT,OPEN_QUESTION}.md`
- `docs/handoffs/reader_ux_20260614/RUN_STATE.md`

절차(예시 — tracked/untracked는 네가 트리 보고 판단):
```sh
git fetch origin
git checkout -b docs/home-detangle-records origin/main
# senpai에 committed된 위 문서만 가져오기
git checkout claude/research-discussion-senpai-design -- <위 경로들>
# ⚠️ 가드 확인: precommit_corpus_guard.sh 설치돼 있으면 코퍼스 staged 시 자동 거부.
#    수동확인: git diff --cached --name-only | grep -iE 'out/|out_raw/|\.jpg|\.png|wiki/papers' → 있으면 unstage
git commit -m "docs(handoff): preserve home-unique de-tangle records (master_backlog, autonomous_run, fig FINAL_REPORT, rrf discussion, reader_ux)"
git push origin docs/home-detangle-records   # → PR to main
```
- **코드(A3/A6/B8 변경)는 포함 금지** — 문서/기록만. 코퍼스(out*·jpg·wiki) 포함 금지(가드가 막음).
- untracked 기록(codex_verdicts 워킹트리 등)이 가치 있고 committed 아니면: 따로 commit하거나 F: 번들로만 보존(네 판단).

## 2. A3/A6/B8 — 폐기 확정
- main이 `92c0f01`(worker)·`db82739`(caps)·`4047b89`(docs)로 이미 보유 → 추가 작업 없음. F: 번들이 아카이브. ✅

## 3. A4/A5 impl-diff 추출 (Codex 리뷰용)
홈 geochem 클론에서:
```sh
git diff origin/claude/p1-science-accuracy...claude/p1-science-accuracy \
  -- src/lib/python-export.ts src/lib/statistics.ts src/lib/ternary-piper-export.ts \
  > A4A5_home_vs_origin.diff
# + 홈 고유 verify 스크립트 3개 파일명/위치 목록
```
- 결과 요약 + diff 파일 경로(F: 또는 inbox 첨부)를 `inbox_claude/004`에 기재 → Codex가 `inbox_codex/003` 수행.
- ⚠️ geochem 최소터치: **diff 추출만**(read-only), 커밋/푸시 금지.

## 제약
- 코퍼스 remote push 금지. geochem 커밋/푸시 금지(diff만). main 보존은 **문서 only**.
