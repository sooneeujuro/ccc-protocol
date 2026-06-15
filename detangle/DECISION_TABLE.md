# 정본 결정표 — 작업본 통합 (B단계 산출)

입력: 회사PC 감사 ✅(`reports/COMPANY_AUDIT_RESULT.md`) + 홈PC 감사 ✅(`reports/HOME_AUDIT_RESULT.md`, VERDICT=issues_found) + Codex 검증 ⏳(대기). Codex 확인 후 확정.

> 원칙: 코퍼스 브랜치 push 금지. code-only 미push는 백업 위해 push 가능(운영자 게이트). 위험작업 GO 게이트.

## ⚠️ 정정 (2026-06-15 21:2x, 홈PC 실행으로 발견 — `reports/HOME_PUSH_ATTEMPT_FINDINGS.md`)
**내 audit 방법 결함 인정**: `git rev-list --count <b> --not --remotes=origin`은 "origin ref에 없는 커밋"만 셈 → **origin tip이 등가작업으로 전진(분기)한 걸 못 잡음.** 그래서 아래 표의 홈 미push 행 "code-only·중복 아님 → push" 전제가 **틀림**:
- **홈 ma senpai 6커밋(A3/A6/B8) = main이 이미 보유한 것의 중복** (회사 `92c0f01` worker·`db82739` caps·`4047b89` docs로 재구현됨). → **wholesale push 취소.** 단 **홈 고유 *문서***(master_backlog_20260614·autonomous_run_20260614·fig_refill FINAL_REPORT 등, 코퍼스 아님·무충돌)는 main에 **clean cherry-pick 보존 가치 있음**.
- **홈 geochem A4/A5 2커밋 = origin이 등가 보유**(`77ccb450` escape·`c37fc34b` no-zero-fill). → **push 취소.** 단 A4 correlation-NaN→null *특정* 케이스 + verify 스크립트 3개에 살릴 delta 있는지 **impl-diff 리뷰**(Codex 적합, geochem 최소터치).
- 둘 다 **유실방지 코드번들 백업 완료**: `F:\corpus_build_history\detangle_home_backups_20260615\` (코퍼스 history 미포함, verify OK). 원격 무변경(force/branch 안 함).
- ✅ **P0 = ma main 머지 완료**(PR#13 `82a3925`, 운영자 GO). main .gitignore 가드 반영 → 전 브랜치 자동보호. (out* 215MB 실물 처분만 운영자 확인 대기.)
- **회사 geochem 16브랜치도 동일 결함 가능** → 적용 전 ahead/behind 재확인 필요(아래 A표는 미정정).

## 🧨 P0 — ma 워킹트리 저작권 코퍼스 215MB 노출 (LANDMINE, 홈PC)
- 위치: 홈PC `manuscript-atelier/docs/handoffs/fig_refill_20260613/out/` + `out_raw/` = **.jpg 4,171 + .md 1,444 ≈ 215MB**, `.gitignore` 미커버.
- 위험: 홈PC에서 `git add -A && push` 한 번이면 **public `manuscript-atelier.git`로 저작권 figure/MD 유출**.
- 조치(전부 운영자 게이트):
  - (a) **즉시**: `.gitignore`에 `docs/handoffs/**/out/`, `docs/handoffs/**/out_raw/`, `**/*.jpg` 추가 → ma 커밋. (회사PC에서 내가 초안 가능, 운영자 GO 시.)
  - (b) `fig_refill out*`는 NAS 통합본(fig root 4,001 이월완료)의 **잔여물일 가능성** → 운영자 확인 후 삭제/NAS 이동.
  - (c) 그 전까지 **ma에서 `git add -A` 금지**, path-add만.

## A. geochemistry-analyzer (→ 최종 freeze 대상)
| 작업본 | 브랜치 | 미push | 종류 | 권장 |
|---|---|---|---|---|
| 회사 .git (메인+worktree공유) | code-only 15개(phase/pr/babbage 등) | 1~11커밋 | 코드 | 가치판단: 살릴 건 push 백업 후 freeze, 폐기할 건 prune (운영자 선별) |
| 회사 .git | **sidecar-v2-wikinote-v3** | 44/**코퍼스194** | 코퍼스 | **push 금지** → 축A(코퍼스 git-out)로만 처리 |
| 홈 geochem-analyzer-git | claude/p1-science-accuracy | **2** (b05dfb62 A4/A5 + 4dd92ecb sink sanitize) | 코드 | code-only·**회사 16브랜치와 중복 아님** → 백업 push or web로 포팅 결정 |
| 회사 Cursor 클론(`Cursor/geochemistry-analyzer`) | — | 0 | — | **잉여 → 제거 안전** |
| 회사 `codes/geochemistry-analyzer` (Codex 발견) | — | 0 | — | **잉여 → 제거 안전** |
| 회사 worktree 14개(.claude/) | 다수 동일 commit | — | — | **prune 대상**(에이전트 찌꺼기, tangle 아님) |

> geochem-analyzer 작업본 총 ~5벌: Documents/geochemistry-analyzer(+worktree) · Cursor 내부 · codes/ · 홈PC. 정본 1벌 외 전부 잉여(미push 0) → 안전 제거/prune.

→ A4/A5(b05dfb62/4dd92ecb)는 **과학·보안 정오 fix라 가치 있음** — geochem 앱을 계속 쓰냐 vs web 클린룸으로 포팅하냐는 운영자 아키텍처 결정. 일단 유실 방지 백업.

## B. manuscript-atelier (clean repo, 유지)
| 작업본 | 브랜치 | 미push | 종류 | 권장 |
|---|---|---|---|---|
| 회사 | claude/draft-spine-surgery | 0 | — | minor 미커밋만, OK |
| 홈 | research-discussion-senpai-design | **6** (6f36b77 A3/A6/B8 등) | 코드/문서 | **홈PC가 push → PR로 main 머지**(아까 논의분, 안전) |

## C. sooneeujuro-web
- 회사·홈(`-clean-export`) 둘 다 **전 브랜치 sync, clean** → 조치 없음.

## 권장 실행 순서 (전부 운영자 GO 게이트)
1. **P0 LANDMINE 가드** — ma .gitignore 추가(+out* 처분). 가장 급함.
2. 홈PC senpai-design 6커밋 push → ma main PR 머지.
3. geochem code-only 브랜치 선별(살림/폐기) + 홈 A4/A5 백업.
4. 축 A: 코퍼스 NAS 정본 + 전 repo pre-commit 가드.
5. Cursor 제거 + worktree prune.
6. [GO] 코퍼스 history rewrite(이미 push된 wiki notes) → GCA freeze.

## 상태
- B단계 감사: 회사✅ 홈✅ **Codex✅(VERDICT=ok, 회사 감사 완전 재현·확인)** → **표 확정.**
- Codex 추가발견: 5번째 클론 `codes/geochemistry-analyzer`(미push 0). worktree 안전성(corpus-v2=worktree, push위험O/유실위험X) 재확인.
- 아카이브 위치 합의: `detangle/`=코퍼스-free 협업 원장 유지, **`G:\corpus_build_history`=빌드코드/산출물 보존**(Claude·Codex 일치).
- 다음: P0(LANDMINE 가드)부터 운영자 GO 받아 실행. Claude는 Phase 1·2 아카이브(G:) 병행.
