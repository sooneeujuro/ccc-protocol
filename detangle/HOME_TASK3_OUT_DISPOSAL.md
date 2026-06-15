# 홈PC TASK3 — fig_refill out* 215MB 실물 처분 (확인 후 삭제, 저작권)

발행: 회사PC Claude(maestro) → 홈PC. 채널 `coop/detangle-20260615`. 보고: `inbox_claude/005_OUT_DISPOSAL_DONE.md`. push 전 `git pull --rebase`.

## 배경
P0 LANDMINE(`reports/HOME_AUDIT_RESULT.md` §LANDMINE)의 **실물**. gitignore 가드는 ma `main`에 머지됨(PR#13) → **commit/유출 위험은 이미 닫힘**. 이 태스크는 *디스크 실물 215MB 정리*(+LANDMINE 물리 제거). **긴급 아님**, 단 저작권 자료라 **확인 후** 처분.

## 대상 (홈PC `manuscript-atelier` 워킹트리, untracked)
```
docs/handoffs/fig_refill_20260613/out/      (jpg ~1,529, ~88MB)
docs/handoffs/fig_refill_20260613/out_raw/  (jpg ~2,642 + md ~1,444 + png 4, ~127MB)
```
= ≈215MB, 논문 figure 이미지 + paper MD (Elsevier 등 저작권 파생).

## 절차 (확인 → 삭제 or 보존)
1. **이월/재현 확인** (read-only):
   - `fig_refill_20260613/ledger.tsv` · `refill_manifest.json` · `judge_result_final.json` 으로 out*가 **어디로 ingest됐는지** 확인.
   - 메모리/핸드오프상 "fig root 4,001 이월 완료" 상태와 대조 — 이 out*가 그 소스/잔여물인가?
   - (가능하면) NAS 코퍼스에 동일 figure가 이미 있는지.
2. **이월·재현 확인됨 → 삭제**:
   ```
   # 백업 불필요(이미 NAS/corpus에 있음). 단 삭제 전 한 번 더 경로 확인.
   Remove-Item -Recurse -Force docs/handoffs/fig_refill_20260613/out
   Remove-Item -Recurse -Force docs/handoffs/fig_refill_20260613/out_raw
   ```
   → 215MB 회수, LANDMINE 실물 제거. gitignore 이미 main이라 재유입 0.
3. **확인 안 됨/애매 → 삭제 금지, 보존**: NAS 올라오면 staging 이동 후 삭제. 그 전까진 그대로 두되 `git add -A` 금지(가드가 막지만 습관).

## 철칙
- **확인 없이 blind 삭제 금지** — 저작권 자료라 유일본이면 복구 불가.
- 다른 untracked(codex_verdicts·done_markers·로그 등)는 이 태스크 범위 아님(건드리지 말 것).
- 코퍼스 remote push 금지.

## 보고
`inbox_claude/005_OUT_DISPOSAL_DONE.md` 에 VERDICT + (삭제했나/보존했나 + 근거: 어느 ledger/상태로 이월 확인했는지, 회수 용량).
