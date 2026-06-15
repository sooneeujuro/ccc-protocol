VERDICT: issues_found

# 홈PC 실행 시도 결과 — 두 diverged 브랜치 = 중복/superseded (DECISION_TABLE 전제 깨짐)

작성: 홈PC(`soone`) Claude. 운영자 "다 하셈" GO 받아 LAPTOP_CONTINUATION 실행 중 발견. read 단계가 아니라 **실제 push 시도에서 분기 노출**.

## TL;DR
- ✅ **P0 LANDMINE 가드 = ma `main`에 머지 완료** (PR #13 → `82a3925`). main .gitignore에 가드 반영 확인 → 모든 브랜치/머지 자동 보호. **LANDMINE은 main 차원에서 닫힘.**
- 🛑 **senpai-design 6커밋 push 보류** + 🛑 **geochem A4/A5 push 보류** — 둘 다 **origin이 등가작업 이미 보유(분기·중복)**. force 안 함, diverged-branch push 안 함.
- 💾 둘 다 **유실 방지 코드전용 번들로 F: 백업**(`F:\corpus_build_history\detangle_home_backups_20260615\`).
- ⚠️ **audit 방법 결함 발견**(아래 §3) — `--not --remotes=origin`은 분기를 못 잡음.

## 1. ma senpai-design — 7↔12 분기, A6/B8 중복
- 공통조상 `60b1c88`. 로컬 7커밋(홈 6 + 내 P0 gitignore) ↔ 원격 12커밋.
- **origin/main(`40155af`)이 회사 12커밋을 이미 머지**(`git merge-base --is-ancestor 171eb10 origin/main` = true). `origin/main..origin/senpai = 0` → 원격 senpai는 이미 main에 흡수됨.
- 홈 `6f36b77`(A3/A6/B8)이 회사가 main에 이미 넣은 것과 **같은 파일 재구현**:
  - A6 `job_handler.py` ↔ 회사 `92c0f01 fix(worker): reject wrong-typed input_summary + clamp top_k`
  - B8 `caps.ts` ↔ 회사 `db82739 fix(orchestra): measure summary caps in jsonb::text bytes`
  - A3 runbook 문서 ↔ 회사 `4047b89 docs(orchestra) drift fix` + `ee6666c error_code canonicalize`
- → **홈 코드(A3/A6/B8)는 main이 이미 가진 것의 중복.** wholesale push 시 분기/충돌/중복구현.
- **홈 고유(main에 없음·코퍼스 아님·충돌 없음)**: `docs/handoffs/master_backlog_20260614.md`, `autonomous_run_20260614/`(RUN_STATE+codex_verdicts+work/*.py), `fig_refill_20260613/FINAL_REPORT.md`, `hybrid_rrf_discussion_20260613/{EXPERIMENT,OPEN_QUESTION}.md`, `reader_ux_20260614/RUN_STATE.md`. → **선별 보존 가치 있음**(clean cherry-pick 가능, GO 시 Claude가 처리).

## 2. geochem p1-science-accuracy — 2↔6 분기, A4/A5 중복
- 로컬 2커밋(b05dfb62 A4 correlation-null+escape / 4dd92ecb A5 sink sanitize) ↔ origin/p1-science-accuracy 6커밋. FF 불가.
- origin 6커밋이 내 A4/A5와 **같은 파일 3개**(python-export.ts/statistics.ts/ternary-piper-export.ts) 건드림:
  - A5 ↔ 회사 `77ccb450 fix(security): escape user text in generated Python/SVG export libs`
  - A4 ↔ 회사 `c37fc34b fix(science): missing values excluded, never zero-filled` + `bd3b8224 cap all inputs`
- → **홈 A4/A5도 origin이 등가/인접 작업 이미 보유.** DECISION_TABLE의 "회사 16브랜치와 중복 아님"은 **분기 미탐지로 인한 오판**. (단 내 A4=correlation NaN→null *특정* 케이스 + verify 스크립트 3개는 origin의 no-zero-fill과 *다른 결*일 수 있음 → 살릴 delta 있는지 impl-diff 리뷰 필요. iron rule상 geochem 추가터치 최소화 권장 = Codex 리뷰 적합.)

## 3. ⚠️ audit 방법 결함 (정본 결정표 정정 필요)
- `git rev-list --count <branch> --not --remotes=origin`은 "어느 origin ref에도 없는 커밋"만 셈 → **공유 브랜치의 origin tip이 전진(분기)한 걸 못 잡음.** 그래서 홈 감사가 "code-only N커밋, push 안전"으로 본 두 브랜치가 실제론 둘 다 diverged+duplicate.
- **권고**: `audit_home_clone.ps1`에 브랜치별 `git rev-list --left-right --count <local>...<origin counterpart>` (ahead/behind) + `merge-base --is-ancestor` FF판정 추가. 그래야 "push 안전 여부"가 정확.

## 4. 백업 (유실 방지, 완료)
- `F:\corpus_build_history\detangle_home_backups_20260615\`
  - `geochem_p1-science-accuracy_home_A4A5.bundle` (22KB, 2커밋 코드델타, verify OK)
  - `ma_senpai-design_home_7commits.bundle` (136KB, 7커밋 코드/문서, 코퍼스 없음, verify OK)
- 범위 번들(`origin..local`)이라 **코퍼스 history 미포함**. 원격 무변경(force/branch 안 만듦) → GCA freeze 목표와 정합.
- 복원: 해당 repo clone에서 `git fetch <bundle>`.

## 5. 결정 필요 (운영자/Codex)
1. **ma 홈 고유 문서**(master_backlog 등, §1) → main에 clean cherry-pick 보존? (Claude가 GO 시 즉시, 코드 무관·무충돌)
2. **ma 홈 A3/A6/B8 코드** → main이 이미 보유 = **폐기 확정?** (아니면 어느 impl이 우월한지 리뷰)
3. **geochem A4/A5** → origin 등가작업과 impl-diff 리뷰해서 살릴 delta(correlation-null 케이스/verify 스크립트) 있는지 판정. 일단 번들 백업됨. iron rule상 geochem 최소터치.
4. **DECISION_TABLE 정정** — A·B 표의 "push 안전" 행 분기 반영(이 리포트 기준).

## 노트북 환경
- **노트북 SSD = F:** (문서 전반의 `G:\corpus_*`는 회사PC 기준). 노트북 G:는 별개 사진 드라이브(월식/Share). 자동화가 G: 가정하면 노트북에선 어긋남.
