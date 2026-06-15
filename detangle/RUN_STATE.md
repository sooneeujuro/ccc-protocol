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
- [확정] **정본 결정표** → `DECISION_TABLE.md`. Codex VERDICT=ok로 회사감사 확인 + 5번째 클론(codes/) 발견. 🧨 P0=ma LANDMINE 215MB 가드.
- [착수] Claude Phase 1·2(역대 빌드코드·산출물 아카이브) → `G:\corpus_build_history`(Claude·Codex 합의). 비파괴.

## 알려진 미push (감사로 확정 필요)
- ma `6f36b77` (A3/A6/B8) — 홈PC.
- geochem `b05dfb62` (A4/A5) — 홈PC.
- geochem-corpus-v2 worktree: sidecar-v2-wikinote-v3 44커밋 (회사PC, 같은 .git이라 유실위험 없음).

## 로그
- 2026-06-15 19:4x — 브랜치 생성 + 홈PC 핸드오프 작성(Claude/회사PC).
- 2026-06-15 20:27 — 홈PC(`soone`) Claude 감사 완료. read-only 스크립트 3 repo 실행 → `reports/HOME_AUDIT_RESULT.md` + `inbox_claude/002_HOME_AUDIT_DONE.md`. 최고 발견=ma untracked 코퍼스 노출(§LANDMINE).
