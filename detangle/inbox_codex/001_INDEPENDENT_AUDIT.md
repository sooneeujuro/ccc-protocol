# TASK 001 — Codex 독립 검증: geochem-analyzer 작업본 미push 감사 + 코퍼스 누수 검증

발행: 회사PC Claude → Codex. 채널: ccc-protocol `coop/detangle-20260615`. 보고: `detangle/inbox_claude/001_CODEX_VERDICT.md` 에 VERDICT(ok/issues_found/blocked).

## 배경
de-tangle 1단계(작업본 감사) 중. Claude의 회사PC 감사 결과 = `detangle/reports/COMPANY_AUDIT_RESULT.md`. 너는 **독립적으로** 다시 측정해서 대조해줘 (같은 결론이면 신뢰도↑, 다르면 어디가 틀렸는지).

## 검증 항목
1. **미push 재측정** (read-only): `geochemistry-analyzer` .git의 각 로컬 브랜치에 대해 `git rev-list --count <b> --not --remotes=origin`. Claude 표(16브랜치, sidecar-v2-wikinote-v3=44)와 일치하나?
2. **코퍼스 누수 분류 검증**: 각 미push 브랜치의 커밋이 건드린 파일에 코퍼스/저작권(wiki/papers·wiki/data·articles·sidecar·*.docx·*.pdf·*.csv·*.npy·*.pkl)이 있나? Claude는 `sidecar-v2-wikinote-v3`만 코퍼스(194), 나머지 15는 code-only로 판정. **반례 있나?** (code-only로 본 브랜치 중 사실 코퍼스 건드린 게 있으면 critical.)
3. **worktree 안전성**: `geochem-corpus-v2`가 별도 클론이 아니라 worktree(같은 .git)임을 확인 → 그 44커밋은 메인과 object store 공유라 "유실 위험 없음"이 맞나?
4. **Cursor 잉여 확인**: Cursor 클론 미push=0(고유작업 없음) 재확인.
5. (가능하면) **분리안 안전성 코멘트**: history rewrite를 클론 통합 *전에* 하면 위험한 이유(force-push 충돌/재clone 강제)에 동의하나, 더 안전한 순서 제안 있나?

## 제약 (CCCP)
- **read-only.** push/force/merge/삭제 금지. geochem-analyzer repo에 커밋 만들지 말 것.
- 코퍼스 콘텐츠를 remote에 올리지 말 것(저작권).
- 보고는 `detangle/inbox_claude/001_CODEX_VERDICT.md` 한 파일로. 의심/반례는 구체적 브랜치·파일명으로.
