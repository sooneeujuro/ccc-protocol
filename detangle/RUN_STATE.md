# RUN_STATE — Corpus/Repo de-tangle (2026-06-15)

protocol: CCCP (ccc-protocol). channel: this repo, branch `coop/detangle-20260615`. console: GitHub issue#1.
operator: sooneeujuro. agents: Claude(회사PC `USER`) 실행 / Codex 독립검증 / 홈PC(`soone`) 자기 클론 감사.

## 목표 (운영자 확정 2026-06-15)
geochemistry-analyzer 모노레포에서 코퍼스/CIR 콘텐츠가 git에 섞이고 작업본이 여러 머신·worktree에 흩어진 꼬임을 정리.
**최종 흐름:** B(작업본 감사) → 1·2(역대 빌드코드·산출물 아카이브) → 3(코퍼스 git-out + 가드) → [GO] 4(history rewrite) → 5(GCA 동결) → 그다음 B1 Sonnet 재추출(원래 숙제).

## 철칙
- **geochemistry-analyzer는 코디네이션으로 안 건드림.** 협업/보고는 ccc-protocol에서만.
- **코퍼스(article md/sidecar/index/wiki note)는 git 원격 push 절대 금지(저작권).**
- 위험단계(force-push·history rewrite·freeze·예산)는 운영자 GO 게이트. 그 전엔 비파괴(읽기+문서)만.

## STATUS: B단계 진행 (작업본 미push 감사)
- [완료] 홈PC 핸드오프 패킷 작성 + **origin push 완료**(d31ba02) → `HOME_PC_AUDIT_TASK.md` + `scripts/audit_home_clone.ps1`. 홈PC 실행 대기.
- [완료] 회사PC 로컬 감사 → `reports/COMPANY_AUDIT_RESULT.md`. 결과: code-only 15브랜치 + 코퍼스 1브랜치(sidecar-v2-wikinote-v3 44/194, push금지) + Cursor 잉여(미push 0).
- [발행] Codex 독립검증 태스크 → `inbox_codex/001_INDEPENDENT_AUDIT.md`. 보고 대기(`inbox_claude/001_CODEX_VERDICT.md`).
- [완료] **홈PC 감사** → `reports/HOME_AUDIT_RESULT.md` (VERDICT=issues_found). 홈 미push: geochem p1-science-accuracy 2커밋(code-only) + ma senpai-design 6커밋(code/docs) + web 27브랜치 전부 sync. ⚠️ ma 워킹트리 untracked 저작권 코퍼스 ≈215MB 노출(§LANDMINE) — gitignore 미커버.
- [확정] **정본 결정표** → `DECISION_TABLE.md`. Codex VERDICT=ok로 회사감사 확인 + 5번째 클론(codes/) 발견.
- [작성] 🧨 **P0 LANDMINE 가드** → `P0_LANDMINE_GUARD.md` (gitignore 패치 + 적용지침). **실제 ma 커밋은 운영자 GO 게이트**.
- [완료] **Phase 1·2 아카이브** → `G:\corpus_build_history` (~6MiB, non-git). code 114 + outputs 116. 시크릿 누수 0(012 오탐 1건 수동복원). renewal_snapshot은 번들에 이미 있어 중복제외.
- [완료] **기능 보존 검증** → `FUNCTIONALITY_GUARDRAILS.md`. 작품 4개 다 작동(git-tracked 런타임 의존 0). A/B/D/E=git-only 무해, C(freeze)만 commit-freeze로 제한.
- [작성] **축 A corpus 가드** → `scripts/precommit_corpus_guard.sh` + `GUARD_DEPLOY.md`(repo별 gitignore). **Codex 검증 발행**(`inbox_codex/002`, 오차단 교차검증). 적용은 GO 게이트.
- [발행] **노트북 continuation** → `LAPTOP_CONTINUATION.md` (셋업=pull+G: / 실행 몫 P0·senpai push·A4A5).
- [✅완료] **P0 LANDMINE 가드 = ma `main` 머지** (홈PC, 운영자 "다 하셈" GO). PR #13 → `82a3925`. main .gitignore에 가드 반영 확인 → 모든 브랜치 자동 보호. **LANDMINE main 차원 closed.** (실물 out* 215MB 처분은 별개, 운영자 명시 확인 대기 — 삭제 안 함.)
- [🛑보고] **홈PC push 시도 → 두 브랜치 다 diverged+중복** → `reports/HOME_PUSH_ATTEMPT_FINDINGS.md` (VERDICT=issues_found). senpai 7↔12(A6/B8 main이 이미 보유) / geochem A4/A5 2↔6(origin이 등가 escape+no-zero-fill 보유). **DECISION_TABLE "push 안전/중복아님" 전제 깨짐.** force/diverged-push 안 함. 유실방지 코드번들 백업 → `F:\corpus_build_history\detangle_home_backups_20260615\`(geochem 22KB + ma 136KB, 코퍼스 history 미포함, verify OK).
- [⚠️결함] **audit 방법**: `--not --remotes=origin`은 분기 미탐지 → 결정표 정정 필요. `audit_home_clone.ps1`에 ahead/behind(`--left-right`) + FF판정 추가 권고.

## 다음 (운영자 GO 게이트) — 운영자 "다" GO (2026-06-15 21:3x)
1. ✅ P0 **완전 해소**: ma main 가드 머지(PR#13) + **out* 215MB 격리 완료**(홈PC, `F:\corpus_quarantine\fig_refill_out_20260613`, MOVE 무손실 5,619 files, `inbox_claude/005`). NAS up 시 ledger 대조 후 격리본 삭제/이동(별개·나중).
2. **[✅홈PC TASK2 완료]** (`inbox_claude/004_HOME_TASK2_DONE.md`):
   - ① 홈 고유 *문서* → **PR #14** `docs/home-detangle-records`(289 files, docs only, 코드·코퍼스 0). 머지 클릭=운영자.
   - ② A3/A6/B8 코드 = **폐기 확정** ✅ (main 보유 + F: 번들).
   - ③ A4/A5: **Codex VERDICT=issues_found**(`inbox_claude/003_A4A5_DELTA_VERDICT.md`) — 홈 결론 부분확증 + **반례**. A4 null→0 회귀 확인·piper 중복화 확인 → **홈 wholesale 폐기**(origin이 A4·piper구조·presetOverride·spec.name escape 우월). **단 홈 "salvage=verify뿐"은 너무 좁음**: ⚠️**origin 자체에 미수정 raw injection sink ~13곳**(python-export·ternary-piper-export, 사용자문자열 raw 보간) → 홈 A5 sink-hardening이 *진짜 보안 delta*. **salvage = (a) 최소 sink-hardening 패치(pyStr/safeColor 등 raw sink만) + (b) verify 스크립트 3개**(번들서 내용리뷰 후). geochem 커밋 0(diff/리뷰만).
3. ✅ **축 A 가드 Codex VERDICT=ok**(13/13 잡고 오차단 0, advisory 2건 반영). → repo별 가드 적용은 GO 게이트. 코퍼스 NAS 정본(NAS up 후).
4. Cursor·codes 잉여 제거 + worktree prune.
5. [GO] 코퍼스 history rewrite → GCA freeze.
6. 그 다음: 원래 숙제 B1 Sonnet 재추출.

## 알려진 미push (감사로 확정 필요)
- ma `6f36b77` (A3/A6/B8) — 홈PC. → **diverged: main이 A6(92c0f01)/B8(db82739) 이미 보유. 중복.** 번들 백업됨.
- geochem `b05dfb62`/`4dd92ecb` (A4/A5) — 홈PC. → **diverged: origin이 A5(77ccb450)/A4-인접(c37fc34b) 이미 보유. 중복.** 번들 백업됨.
- geochem-corpus-v2 worktree: sidecar-v2-wikinote-v3 44커밋 (회사PC, 같은 .git이라 유실위험 없음).

## 로그
- 2026-06-15 19:4x — 브랜치 생성 + 홈PC 핸드오프 작성(Claude/회사PC).
- 2026-06-15 20:27 — 홈PC(`soone`) Claude 감사 완료. read-only 스크립트 3 repo 실행 → `reports/HOME_AUDIT_RESULT.md` + `inbox_claude/002_HOME_AUDIT_DONE.md`. 최고 발견=ma untracked 코퍼스 노출(§LANDMINE).
- 2026-06-15 21:2x — 홈PC Claude, 운영자 "다 하셈" GO 실행. ✅P0 ma main 머지(PR#13). 🛑senpai/A4A5 push 시도→둘 다 diverged+중복 발견(`reports/HOME_PUSH_ATTEMPT_FINDINGS.md`), 번들 백업(F:). audit 방법 결함(분기 미탐) 보고. **노트북 SSD=F:**(문서 G:는 회사기준).
- 2026-06-15 21:5x — 홈PC Claude TASK2 완료. ①문서보존 PR#14(289 docs) ②A3/A6/B8 폐기확정 ③A4/A5 impl-diff(`scratch/A4A5_home_vs_origin.diff`)→origin 우월/홈 잠재회귀, salvage=verify 3개. geochem 커밋 0(diff만). `inbox_claude/004`.
- 2026-06-15 22:3x — Codex 003 VERDICT=issues_found: 홈 A4/A5 wholesale 폐기, **단 반례=origin에 미수정 raw injection sink ~13곳** → 보안 salvage 있음.
- 2026-06-15 22:5x — 홈PC Claude TASK3 완료: out* 215MB **격리**(MOVE, 삭제아님) → `F:\corpus_quarantine\fig_refill_out_20260613`. 무손실(5,619 files, DST=SRC), git status 깨끗, 범위밖 untracked·FINAL_REPORT 무접촉, 커밋 0. P0 실물까지 해소. `inbox_claude/005`.
- 2026-06-15 22:51 — 회사PC Claude, 운영자 GO("A"). **A5 sink-hardening 패치 구현 완료** → geochem 브랜치 `claude/harden-export-sinks`(`64c393ae`, 2파일: python-export·ternary-piper-export). pyQuote/pyStr/safeColor/pyDocSafe로 raw sink 무력화. origin presetOverride·spec.name escape·piperToMeqPercent 보존. **tsc clean + 주입테스트 통과**(code sink 전부 escape). p1=main에 이미 merge라 main PR 깨끗. **미push — deploy 게이트(운영자: push+PR#→Vercel redeploy).** salvage 잔여=verify 스크립트 3개(홈 F: 번들서 추출 후 포팅). +발견: geochem 워킹트리 untracked 코퍼스(wiki/papers/Fischer…·새 폴더) → 축A 가드 대상.
