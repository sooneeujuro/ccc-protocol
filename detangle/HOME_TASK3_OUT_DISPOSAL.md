# 홈PC TASK3 — fig_refill out* 215MB **격리**(삭제 아님, 비-git 이동)

발행: 회사PC Claude(maestro) → 홈PC. 채널 `coop/detangle-20260615`. 보고: `inbox_claude/005_OUT_DISPOSAL_DONE.md`. push 전 `git pull --rebase`.

## 배경 + 방침
P0 LANDMINE(`reports/HOME_AUDIT_RESULT.md` §LANDMINE)의 **실물**. gitignore 가드는 ma `main`에 머지됨(PR#13) → **commit/유출 위험은 이미 닫힘**. **운영자 결정: 삭제 말고 격리(비-git 위치로 이동).** 저작권+이월 불확실 데이터라 비가역 삭제 대신 **가역 격리** — 워킹트리에서 빼서 위험0, 데이터는 보존, 215MB 회수.

## 대상 (홈PC `manuscript-atelier` 워킹트리, untracked)
```
docs/handoffs/fig_refill_20260613/out/      (jpg ~1,529, ~88MB)
docs/handoffs/fig_refill_20260613/out_raw/  (jpg ~2,642 + md ~1,444 + png 4, ~127MB)
```
= ≈215MB, 논문 figure 이미지 + paper MD (Elsevier 등 저작권 파생).

## 절차 (격리 = 비-git 위치로 이동, 삭제 없음)
1. **격리 폴더 생성** (repo 밖, 비-git, 노트북 F: SSD):
   ```
   New-Item -ItemType Directory -Force F:\corpus_quarantine\fig_refill_out_20260613
   ```
   (F:\corpus_build_history\ 옆에 두면 백업류와 한곳. 경로는 적절히 조정 OK — *repo 밖 비-git*이기만.)
2. **이동(Move, 복사 아님)**:
   ```
   Move-Item docs/handoffs/fig_refill_20260613/out      F:\corpus_quarantine\fig_refill_out_20260613\out
   Move-Item docs/handoffs/fig_refill_20260613/out_raw  F:\corpus_quarantine\fig_refill_out_20260613\out_raw
   ```
   → 워킹트리에서 빠짐(commit위험0), 데이터 보존(가역), 215MB 회수. F:→F:면 즉시.
3. **확인** : `git status`에서 out*/out_raw 사라졌는지 + 격리폴더에 jpg/md 수 맞는지(≈4,171 jpg + 1,444 md).
4. **나중(NAS up 시, 별개)**: ledger로 이월 확인 → 이미 NAS에 있으면 격리본 삭제, 아니면 NAS 코퍼스로 이동. (지금은 격리까지만.)

## 철칙
- **삭제 안 함 — 이동(Move)만.** 가역 보장.
- 다른 untracked(codex_verdicts·done_markers·로그 등)는 이 태스크 범위 아님(건드리지 말 것).
- 코퍼스 remote push 금지.

## 보고
`inbox_claude/005_OUT_DISPOSAL_DONE.md` 에 VERDICT + 격리 위치 경로 + 옮긴 파일 수/용량 + `git status` 깨끗 확인.
