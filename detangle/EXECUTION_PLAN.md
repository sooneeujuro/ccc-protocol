# de-tangle 실행계획 (GO-게이트, 검증된 명령 + gotcha)

회사PC Claude가 read-only 검증으로 각 GO단계의 실제 명령 + 함정을 미리 확정. 실행은 운영자 GO. (검증 2026-06-15 21:24)

## ⚠️ 클론 정리 — push-button 아님! (검증으로 발견)
"잉여 클론 미push 0"이라도 **막 지우면 안 됨** — 둘 다 비-git 자산 보유:

| 클론 | 미push | .env.local | 미커밋 | 처분 |
|---|---|---|---|---|
| `Documents/Cursor` | 0 | ⚠️ 있음 | **`ChatInterface.tsx`(MM, 고유작업?)** | 미커밋 검토(살림/버림) + .env.local 백업 **후** 삭제 |
| `codes/geochemistry-analyzer` | 0 | ⚠️ 있음(**메인엔 없음→유일본 가능**) | `?? mcp-server/` | .env.local **반드시 백업** + mcp-server 검토 후 삭제 |

> 메인 `Documents/geochemistry-analyzer`엔 `.env.local`이 없음 → 위 둘의 .env.local(Supabase URL/키 등)이 로컬 dev 설정의 유일본일 수 있음. **삭제 전 `.env.local` out-of-band 백업**(guardrail #6) + 미커밋 변경 검토 필수. 그 다음에야 `rm -rf`.

## worktree prune (geochem-analyzer 14개)
- 대부분 `.claude/worktrees/*` = Claude Code 에이전트 작업 잔재(여러 개 같은 commit). 안전.
- **유지**: `geochem-corpus-v2`(코퍼스 worktree, 작업본). 나머지 stale은:
  ```
  git -C C:/Users/USER/Documents/geochemistry-analyzer worktree prune   # 끊긴 것 정리
  git -C ... worktree remove <path>                                     # 살아있는 잔재 개별 제거
  ```
- prune은 비파괴(끊긴 참조만 정리). remove는 해당 worktree 브랜치 미push 없는지 확인 후.

## 코퍼스 history rewrite (E단계, 큰 GO)
범위 측정: geochem `.git` = **87M**. strip 대상 = 코퍼스 663파일.
```
git filter-repo \
  --path wiki/papers --path wiki/data --path paper1-CIR-volatiles \
  --path tools/geochem-stats/corpus \
  --invert-paths
```
- tracked 코퍼스: `wiki/papers`(630) + `wiki/data`(27) + `paper1-CIR-volatiles`(1) + `tools/geochem-stats/corpus`(5).
- **⚠️ 절대 strip 금지**: `tools/geochem-stats/index/variable-vocabulary.json`(빌드 static import, tracked). 위 --path에 corpus만 있고 index는 없으니 안전 — 단 실행 후 `git ls-files | grep variable-vocabulary` 로 잔존 확인.
- 루트 `figure_*.png/svg/tiff`는 **history에 없음**(tracked 0, untracked) → strip 불요.
- **순서**: 클론/worktree 통합·정리 → 비-git 자산 백업 → filter-repo → force-push → **전 클론(메인·Cursor·codes·홈PC) + worktree re-clone**. (force-push 전 `git bundle`로 풀백업 권장.)
- manuscript-atelier는 코퍼스 tracked=0이라 rewrite 대상 아님(가드만).

## GCA freeze (마지막)
- **commit-freeze만**(README에 DEPRECATED/FROZEN + 신규작업은 후속 repo로). **Vercel 배포 LIVE 유지**(guardrail #4 — manuscript .mcp.json이 호출).
- A4/A5(b05dfb62/4dd92ecb)는 freeze 전 백업/포팅 결정.

## 권장 GO 순서
Codex 가드검증 → 노트북 P0/senpai-push/A4A5백업 → repo 가드 적용 → **클론 .env.local·미커밋 백업 후** 클론정리+worktree prune → 비-git 자산 풀백업 → filter-repo + force-push + 전클론 re-clone → GCA freeze → B1 재추출.
