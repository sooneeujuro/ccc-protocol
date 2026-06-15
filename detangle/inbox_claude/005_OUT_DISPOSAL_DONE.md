VERDICT: ok

# 홈PC TASK3 완료 — fig_refill out* 215MB 격리(MOVE, 삭제 아님)

실행: 홈PC(`soone`) Claude. 운영자 GO("옮겨=격리"). read 단계 아님, 실물 이동.

## 결과: 가역 격리 성공, 무손실

**격리 위치 (repo 밖, 비-git, F: SSD):**
`F:\corpus_quarantine\fig_refill_out_20260613\{out, out_raw}`

**이동 전/후 카운트 정확히 일치 (무손실):**
| 폴더 | 파일 | jpg | md | png | 용량 |
|---|---|---|---|---|---|
| out | 1,529 | 1,529 | 0 | 0 | 88.3MB |
| out_raw | 4,090 | 2,642 | 1,444 | 4 | 127.3MB |
| **합계** | **5,619** | **4,171** | **1,444** | **4** | **215.6MB** |

DST 카운트 = SRC 카운트 (Move-Item, 복사 아님). C:→F: 크로스드라이브 이동.

## 검증
- ✅ 원본 위치 `docs/handoffs/fig_refill_20260613/{out,out_raw}` 둘 다 제거됨(Test-Path False).
- ✅ `git status`에서 out/out_raw 사라짐 (워킹트리 commit위험 0).
- ✅ **삭제 아님 — F: 격리본 보존, 가역.** (NAS up 시 ledger 대조 → 이미 NAS에 있으면 격리본 삭제, 아니면 NAS 코퍼스로 이동. 지금은 격리까지만.)
- ✅ 범위밖 untracked(codex_verdicts·done_markers·ledger·로그 등 72항목) **그대로 — 안 건드림**.
- ✅ `fig_refill_20260613/FINAL_REPORT.md`(PR#14로 보존된 tracked 문서) 그대로.
- ✅ 홈 ma 브랜치/HEAD 무변경(`claude/research-discussion-senpai-design @ 4f9b6ce`, **커밋 0**). geochem 무관.
- ✅ F: 여유 128.5GB (215MB 격리 후에도 충분).

## 철칙 준수
삭제 0(이동만) · 코퍼스 remote push 0 · 범위밖 untracked 무접촉 · geochem 무관.

→ P0 LANDMINE 실물까지 정리 완료: gitignore 가드(main PR#13) + 215MB 워킹트리에서 격리. **commit위험·디스크 둘 다 해소.**
