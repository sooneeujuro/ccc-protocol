VERDICT: ok

# 회사PC(`USER`) 로컬 미push 감사 (read-only)

- 생성: 2026-06-15 20:07 | machine: 회사PC / USER
- 대상: `geochemistry-analyzer` .git(메인 클론 + `geochem-corpus-v2` worktree + `.claude/worktrees/*` 14개가 **공유**) + `Cursor` 별도 클론.

## geochemistry-analyzer .git — 미push 브랜치 (origin 어느 ref에도 없는 커밋)

| branch | 미push 커밋 | 코퍼스파일 | 판정 |
|---|---|---|---|
| claude/condescending-babbage-6aad8f | 11 | 0 | code-only |
| claude/docs-status-pr-c-wrap-up | 1 | 0 | code-only |
| claude/pca-codedrop-phase4 | 3 | 0 | code-only |
| claude/phase-b2a-unicode-labels | 1 | 0 | code-only |
| claude/phase1-task-d-dasharray | 1 | 0 | code-only |
| claude/phase2-4-endmember-lookup | 1 | 0 | code-only |
| claude/phase2-4-fix-concentration-check | 1 | 0 | code-only |
| claude/phase2-followup-mixing-sampling | 1 | 0 | code-only |
| claude/phase3-a-iso-fraction-grids | 7 | 0 | code-only |
| claude/pr-a-5-sweep-visualization | 7 | 0 | code-only |
| claude/pr-a-mode-sweep | 6 | 0 | code-only |
| claude/pr-b-water-sidecar-vocab | 1 | 0 | code-only |
| claude/pr-c-recommend-plot | 5 | 0 | code-only |
| claude/pr14-trendline-default-off | 1 | 0 | code-only |
| **claude/sidecar-v2-wikinote-v3** | **44** | **194** | **⚠️ 코퍼스 — push 금지** |
| claude/unruffled-driscoll-ab107f | 2 | 0 | code-only |

## Cursor (별도 클론)
- 미push 0 — 전부 origin에 있음. **고유 작업 없음 → 잉여 클론, 제거 안전.**

## 해석
- **code-only 15브랜치**: 옛 feature/PR 작업이 origin에 안 올라간 것. 푸시해도 저작권 위험 0 — 단 정리(push or prune)는 운영자 결정.
- **sidecar-v2-wikinote-v3 (44/194)**: Corpus Gen-2 작업. **코퍼스 콘텐츠가 git에 들어가 있어 push 금지.** worktree(geochem-corpus-v2)와 같은 .git이라 유실 위험은 없음 — 축 A(코퍼스 git-out) 대상.
- Cursor 잉여 → 통합 단계에서 제거.

## 다음
- 홈PC 감사 결과(`HOME_AUDIT_RESULT.md`)와 대조 → 정본 결정표.
- Codex 독립검증(`inbox_codex/001`) 대조.
