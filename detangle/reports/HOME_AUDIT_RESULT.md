VERDICT: issues_found

# 홈PC 미push 감사 (read-only)
- 생성: 2026-06-15 20:27:26  | machine: GALAXYBOOKHJ / soone
- 감사자: Claude (Opus 4.8). read-only — fetch(읽기) 외 working tree/원격 무변경. push/commit/delete 없음.

## 요약 (operator + Codex용)

| repo | 미push 커밋 | 워킹트리 | 코퍼스 위험 |
|---|---|---|---|
| geochemistry-analyzer-git | **2** (claude/p1-science-accuracy) | clean | code-only — 없음 |
| manuscript-atelier | **6** (claude/research-discussion-senpai-design) | **dirty (대량 untracked)** | ⚠️ **있음 — 아래 §LANDMINE** |
| sooneeujuro-web-clean-export | 0 (27개 브랜치 전부 sync) | clean | 없음 |

**홈PC 결론 3줄**
1. **geochem**: 미push 2커밋 = 내(Claude) A4/A5 작업 `b05dfb62`(correlation null + injection escape) + `4dd92ecb`(전 sink sanitize). **code-only, 코퍼스 무관**. 처분=operator 게이트(iron rule상 geochem 코디 금지 — 인벤토리로만 보고). 회사컴의 16개 geochem 미push 브랜치와 **중복 아님**(홈은 이 1브랜치 2커밋뿐).
2. **manuscript-atelier**: 미push 6커밋은 code/docs-only(안전). 그러나 ⚠️ **워킹트리에 untracked 저작권 코퍼스 ≈215MB가 노출**돼 있음(§LANDMINE). gitignore 미커버 → `git add -A` 한 번이면 공개 remote로 push되는 사고 위험. **이번 감사 최고 우선순위 발견.**
3. **web**: 27 브랜치(claude/web-* + codex/figure-*) 전부 origin과 동기화·clean. 홈PC에서 detangle 대상 아님.

## §LANDMINE — ma 워킹트리 untracked 저작권 코퍼스 (push 금지)

스크립트 corpusRegex는 **커밋된 파일만** 스캔 → untracked는 못 잡음. 수동 read-only 확인 결과:

- `docs/handoffs/fig_refill_20260613/out/` — **.jpg 1,529 (88.3MB)**
- `docs/handoffs/fig_refill_20260613/out_raw/` — **.jpg 2,642 + .md 1,444 + .png 4 (127.3MB)**
- 합계 **.jpg 4,171 + .png 4 + .md 1,444 ≈ 215MB** = 논문 추출 figure 이미지 + paper MD = **저작권 코퍼스**.
- 그 외 untracked(코퍼스 아님, 로그류): `codex_verdicts/` *.md 340+, `overnight_agent_exchange/` *.md 163, `fig_refill_20260613/` 산출 json/tsv/py, `done_markers/` *.done 1,481.

**위험**: `git check-ignore` 확인 = **NOT ignored**. .gitignore의 handoff 관련 룰은 `figures/raw_TIFF/` 뿐 → `docs/handoffs/**` 전부 노출. 누가 `git add -A && push` 하면 4,171 figure + 1,444 MD가 public github(`manuscript-atelier.git`)로 유출.

**권고(전부 비파괴, operator 게이트)**:
- (a) `.gitignore`에 `docs/handoffs/**/out/`, `docs/handoffs/**/out_raw/`, `*.jpg` 등 추가 — **단 이건 ma 커밋이라 iron rule상 내가 못 함**. operator 또는 detangle 라이브게이트에서.
- (b) 또는 fig_refill 산출 코퍼스를 NAS staging으로 이동(이미 NAS에 통합본 있음 — 메모리상 fig root 4,001 이월 완료라 **이 out*는 그 소스 잔여물일 가능성** → operator 확인 후 삭제/이동 가능).
- (c) 그 전까지: **ma에서 `git add -A` 절대 금지**. 커밋은 항상 명시적 path-add만.

---
## repo: `C:\Users\soone\geochemistry-analyzer-git`
- fetch OK
- origin: https://github.com/sooneeujuro/geochemistry-analyzer.git
- HEAD: 4dd92ecb on 'claude/p1-science-accuracy'

### 브랜치별 미push 커밋 (origin 어느 ref에도 없는 것)

| branch | 미push 커밋수 | 코퍼스 건드림? |
|---|---|---|
| claude/fix-es5-build | 0 | code-only |
| claude/p1-science-accuracy | 2 | code-only |
| main | 0 | code-only |

### 미push 커밋 상세

#### claude/p1-science-accuracy — 미push 커밋 
```
4dd92ecb 2026-06-15 17:04:48 +0900 fix(security): sanitize ALL generated-Python sinks in matplotlib/ternary/piper exports b05dfb62 2026-06-14 06:41:53 +0900 fix(science+security): correlation null for non-computable cells + export injection escape
```

### 작업트리 미커밋
- clean

### worktree 목록
```
C:/Users/soone/geochemistry-analyzer-git 4dd92ecb [claude/p1-science-accuracy]
```

---
## repo: `C:\Users\soone\Documents\manuscript-atelier`
- fetch OK
- origin: https://github.com/sooneeujuro/manuscript-atelier.git
- HEAD: c898e15 on 'claude/research-discussion-senpai-design'

### 브랜치별 미push 커밋 (origin 어느 ref에도 없는 것)

| branch | 미push 커밋수 | 코퍼스 건드림? |
|---|---|---|
| claude/corpus-reader-integration | 0 | code-only |
| claude/fix-pnpm-builds | 0 | code-only |
| claude/p2b-gateway-tighten | 0 | code-only |
| claude/research-discussion-senpai-design | 6 | code-only |
| main | 0 | code-only |
| pr7-review | 0 | code-only |

### 미push 커밋 상세

#### claude/research-discussion-senpai-design — 미push 커밋 
```
c898e15 2026-06-15 06:06:07 +0900 docs(handoff): company-computer corpus-fix snapshot memo (USB corpus_fixes_20260615) a9c73c0 2026-06-15 04:20:50 +0900 board: move recovered paper MDs off-board to NAS staging (fix audit cost false-positive) 9ef3a90 2026-06-14 17:27:26 +0900 A2: recover German (datalab reconvert + neighbour-bleed trim) and Lee_S.C (clean review MD) to staging 49fd5c5 2026-06-14 07:22:09 +0900 board: restructure RUN_STATE.md as the Codex-heartbeat channel; drop stray prose ACKs 6f36b77 2026-06-14 06:54:55 +0900 fix(harness): autonomous run 2026-06-14 — A3 doc-drift + A6 worker caps + B8 cap-basis unify 56503e8 2026-06-14 05:44:46 +0900 docs(handoff): master backlog + hybrid NO + reader UX/fig-refill records (Fable→Opus 인수)
```

### 작업트리 미커밋
```
 M docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_060509.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/STOP
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_042113.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_042455.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_042956.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_043457.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_043957.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_044458.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_044959.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_045459.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_050000.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_050501.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_051001.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_051502.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_052002.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_052503.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_053004.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_053505.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_054006.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_054507.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_055007.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_055508.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_060008.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_061010.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_061511.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_062011.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_062512.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_063012.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_063513.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_064014.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_064514.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_065015.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_065516.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_070016.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_070517.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_071018.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_071519.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_103931.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_104439.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_104948.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_105455.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_105957.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_110458.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_110959.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_111501.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_112002.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_112503.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_113004.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_140825.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_141326.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_141828.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_142329.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_142831.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_143332.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_143833.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_144335.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_144838.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_145339.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_145841.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_150342.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_150844.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_151345.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_151846.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_152347.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_152849.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_153350.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_153852.md
?? docs/handoffs/autonomous_run_20260614/codex_verdicts/verdict_154353.md
?? docs/handoffs/autonomous_run_20260614/work/lazyverif_poc.py
?? docs/handoffs/fig_refill_20260613/RUN_STATE.md
?? docs/handoffs/fig_refill_20260613/codex_verdicts/
?? docs/handoffs/fig_refill_20260613/debug_calls.log
?? docs/handoffs/fig_refill_20260613/done_markers/
?? docs/handoffs/fig_refill_20260613/judge_manifest.json
?? docs/handoffs/fig_refill_20260613/judge_manifest_cap.json
?? docs/handoffs/fig_refill_20260613/judge_result_final.json
?? docs/handoffs/fig_refill_20260613/judge_result_pass1.json
?? docs/handoffs/fig_refill_20260613/judge_slots/
?? docs/handoffs/fig_refill_20260613/ledger.tsv
?? docs/handoffs/fig_refill_20260613/ledger_v1.tsv
?? docs/handoffs/fig_refill_20260613/ledger_v2_triples.bak.tsv
?? docs/handoffs/fig_refill_20260613/out/
?? docs/handoffs/fig_refill_20260613/out_raw/
?? docs/handoffs/fig_refill_20260613/phash_furniture.ps1
?? docs/handoffs/fig_refill_20260613/pilot_pids.json
?? docs/handoffs/fig_refill_20260613/pilot_report.md
?? docs/handoffs/fig_refill_20260613/pos_sample_12.txt
?? docs/handoffs/fig_refill_20260613/pos_verify_slots/
?? docs/handoffs/fig_refill_20260613/postproc.py
?? docs/handoffs/fig_refill_20260613/postproc_ledger.tsv
?? docs/handoffs/fig_refill_20260613/refill_manifest.json
?? docs/handoffs/fig_refill_20260613/refill_runner.py
?? docs/handoffs/fig_refill_20260613/visual_check_list.txt
?? docs/handoffs/geochem_triage.md
?? docs/handoffs/overnight_agent_exchange/
?? docs/handoffs/reader_ux_20260614/codex_verdicts/
```

### worktree 목록
```
C:/Users/soone/Documents/manuscript-atelier c898e15 [claude/research-discussion-senpai-design]
```

---
## repo: `C:\Users\soone\Documents\sooneeujuro-web-clean-export`
- fetch OK
- origin: https://github.com/sooneeujuro/sooneeujuro-web.git
- HEAD: d2cefb7 on 'main'

### 브랜치별 미push 커밋 (origin 어느 ref에도 없는 것)

| branch | 미push 커밋수 | 코퍼스 건드림? |
|---|---|---|
| claude/p1-science-accuracy | 0 | code-only |
| claude/web-classification-v6 | 0 | code-only |
| claude/web-codedrop-v9 | 0 | code-only |
| claude/web-cv-v5 | 0 | code-only |
| claude/web-deckcode-v11 | 0 | code-only |
| claude/web-figure-style-v26 | 0 | code-only |
| claude/web-fixtures-v4 | 0 | code-only |
| claude/web-mcp-figs-v21 | 0 | code-only |
| claude/web-mixing-mode-v12 | 0 | code-only |
| claude/web-mixing-smoke-v13 | 0 | code-only |
| claude/web-pca-v22 | 0 | code-only |
| claude/web-piper-v3 | 0 | code-only |
| claude/web-smoke-v14 | 0 | code-only |
| claude/web-stats-v10 | 0 | code-only |
| claude/web-style-v8 | 0 | code-only |
| claude/web-ternary-v7 | 0 | code-only |
| claude/web-uiwire-codedrop-v15 | 0 | code-only |
| claude/web-uiwire-homecards-v19 | 0 | code-only |
| claude/web-uiwire-share-v18 | 0 | code-only |
| claude/web-uiwire-stats-v16 | 0 | code-only |
| claude/web-uiwire-style-v17 | 0 | code-only |
| claude/web-workbench-v23 | 0 | code-only |
| claude/web-xlsx-import-v20 | 0 | code-only |
| claude/web-xlsx-stats-v20 | 0 | code-only |
| codex/figure-preset-restore-v27 | 0 | code-only |
| codex/figure-style-v1 | 0 | code-only |
| main | 0 | code-only |

### 미push 커밋 상세

### 작업트리 미커밋
- clean

### worktree 목록
```
C:/Users/soone/Documents/sooneeujuro-web-clean-export d2cefb7 [main]
```

