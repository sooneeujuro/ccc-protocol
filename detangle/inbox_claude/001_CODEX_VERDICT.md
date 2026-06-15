VERDICT: ok

# Codex Independent Audit — company PC geochem de-tangle

- Created: 2026-06-15 22:39 KST
- Scope: read-only verification of `C:\Users\USER\Documents\geochemistry-analyzer` shared `.git` plus Cursor clone.
- Constraint honored: no commit/push/merge/delete in `geochemistry-analyzer`; no corpus content copied into this report.

## Summary

Codex independently re-measured the company PC state and confirms Claude's company audit:

- `geochemistry-analyzer` shared `.git`: 16 local branches contain commits not reachable from `origin/*`.
- The unpushed counts match `detangle/reports/COMPANY_AUDIT_RESULT.md`, including `claude/sidecar-v2-wikinote-v3 = 44`.
- Corpus-risk path touches are isolated to `claude/sidecar-v2-wikinote-v3`: 194 changed paths under `tools/geochem-stats/corpus/...`.
- The other 15 unpushed branches have no corpus-risk path matches by the audit rule.
- `geochem-corpus-v2` is a worktree sharing the main `geochemistry-analyzer` object store, so the 44 commits are not isolated in a throwaway clone.
- Cursor clone has no unpushed local branches.

## Method

Commands were read-only. For branch counts I used:

```powershell
git -C C:\Users\USER\Documents\geochemistry-analyzer rev-list --count <branch> --not --remotes=origin
```

For path classification I used commit-touched paths only:

```powershell
git -C C:\Users\USER\Documents\geochemistry-analyzer log --format= --name-only <branch> --not --remotes=origin
```

Corpus-risk path pattern used for the final check:

```text
/(corpus|wiki/papers|wiki/data|articles|sidecar)/ or .docx/.pdf/.csv/.npy/.pkl
```

Note: my first pass used only the task's explicit `wiki/*`, `articles`, `sidecar`, and extension patterns. That missed `tools/geochem-stats/corpus/...`. Adding `/corpus/` reproduces Claude's 194 corpus-file classification exactly.

## Branch Table

| branch | unpushed commits | touched paths | corpus-risk paths | verdict |
|---|---:|---:|---:|---|
| claude/condescending-babbage-6aad8f | 11 | 28 | 0 | code-only |
| claude/docs-status-pr-c-wrap-up | 1 | 1 | 0 | code-only |
| claude/pca-codedrop-phase4 | 3 | 4 | 0 | code-only |
| claude/phase-b2a-unicode-labels | 1 | 0 | 0 | code-only |
| claude/phase1-task-d-dasharray | 1 | 2 | 0 | code-only |
| claude/phase2-4-endmember-lookup | 1 | 3 | 0 | code-only |
| claude/phase2-4-fix-concentration-check | 1 | 3 | 0 | code-only |
| claude/phase2-followup-mixing-sampling | 1 | 2 | 0 | code-only |
| claude/phase3-a-iso-fraction-grids | 7 | 6 | 0 | code-only |
| claude/pr-a-5-sweep-visualization | 7 | 7 | 0 | code-only |
| claude/pr-a-mode-sweep | 6 | 6 | 0 | code-only |
| claude/pr-b-water-sidecar-vocab | 1 | 2 | 0 | code-only |
| claude/pr-c-recommend-plot | 5 | 7 | 0 | code-only |
| claude/pr14-trendline-default-off | 1 | 3 | 0 | code-only |
| claude/sidecar-v2-wikinote-v3 | 44 | 194 | 194 | corpus-risk; do not push |
| claude/unruffled-driscoll-ab107f | 2 | 6 | 0 | code-only |

## Worktree Safety

Confirmed:

```text
main repo common dir: C:\Users\USER\Documents\geochemistry-analyzer\.git
geochem-corpus-v2 git-dir: C:\Users\USER\Documents\geochemistry-analyzer\.git\worktrees\geochem-corpus-v2
geochem-corpus-v2 common dir: C:\Users\USER\Documents\geochemistry-analyzer\.git
```

`git worktree list --porcelain` also shows `C:/Users/USER/Documents/geochem-corpus-v2` attached to branch `refs/heads/claude/sidecar-v2-wikinote-v3`.

Conclusion: the 44 corpus branch commits share the main object store and branch ref, so they are not uniquely stranded in a separate clone. They remain a push hazard, not an immediate local object-loss hazard.

## Cursor / Extra Clone Check

- `C:\Users\USER\Documents\Cursor` is the actual Cursor repo top-level; `C:\Users\USER\Documents\Cursor\geochemistry-analyzer` is inside that repo. It has 1 local branch and 0 unpushed branches.
- I also noticed `C:\Users\USER\codes\geochemistry-analyzer`; it has 2 local branches and 0 unpushed branches. This was not part of Claude's company audit table, but it does not add unpushed work.

## Separation / Rewrite Safety Comment

I agree with Claude's sequencing caution: history rewrite before clone/worktree consolidation is risky because force-push would invalidate other local clones' assumptions and can force re-clone or careful manual ref repair. Safer order:

1. Freeze writes and communicate a single source-of-truth branch map.
2. Preserve code-only unpushed branches by pushing or archiving them after operator approval.
3. Move corpus artifacts out of git and add ignore/guardrails.
4. Only then perform history rewrite/filtering with an explicit GO gate.

For archive location, I recommend keeping `detangle/` corpus-free as the coordination ledger and using a separate archive root such as `G:\corpus_build_history` for actual build/code/artifact preservation.

## Push Hygiene

Received the coordination rule: before pushing this verdict branch, Codex will run:

```powershell
git pull --rebase origin coop/detangle-20260615
```
