VERDICT: <ok | issues_found | blocked>   ← 홈PC 세션이 보고할 때 이 헤더 채워주세요

# 홈PC 작업 지침 — geochemistry-analyzer / manuscript-atelier 미push 감사 (READ-ONLY)

작성: 회사PC(`USER`) Claude 세션 → 홈PC(`soone`) 세션 핸드오프. 채널: `ccc-protocol` repo, branch `coop/detangle-20260615` (geochemistry-analyzer는 **절대 안 건드림** — 이 협업은 corpus-free 협업 repo에서만).

---

## 0. 한 줄 목적
홈PC 로컬 클론들에 **origin에 안 올라간 작업(미push 커밋·미커밋)**이 뭐가 있는지 read-only로 전수 감사해서 보고. **푸시/머지/삭제는 지금 안 함** — 회사PC 감사 결과랑 대조해 "정본 결정표"부터 만들 거라 일단 *상태 보고만* 필요.

## 1. 배경 (왜 이걸 하나)
- `geochemistry-analyzer` 한 repo가 여러 머신·worktree에 흩어져 미push divergence가 쌓임 = "분리했는데 또 섞인" 꼬임의 핵심.
- 알려진 홈PC 미push 작업: ma `6f36b77`(A3/A6/B8), geochem `b05dfb62`(A4/A5). 이것 말고 더 있는지 전수 확인이 목적.
- 최종 목표: 코퍼스 git-out → 작업본 정본화 → GCA 동결. 이건 그 **1단계(작업본 감사)**.

## 2. 네 작업 (3스텝, 전부 read-only)
1. 이 repo(`ccc-protocol`) `coop/detangle-20260615` 브랜치를 pull → `detangle/scripts/audit_home_clone.ps1` 확보.
2. 홈PC의 **두 클론 경로**를 확인해서 스크립트에 넘겨 실행 (PowerShell):
   ```powershell
   ./detangle/scripts/audit_home_clone.ps1 -RepoPaths @(
     'C:\Users\soone\geochemistry-analyzer-git',
     'C:\Users\soone\Documents\manuscript-atelier'   # 실제 경로로 교정
   )
   ```
   - 경로가 다르면 교정. 모르면 `git -C <후보> remote get-url origin`으로 origin이 geochemistry-analyzer / manuscript-atelier인 폴더를 찾아 넣을 것.
   - 스크립트는 `git fetch origin`(읽기) 외엔 아무것도 안 바꿈.
3. 스크립트가 만든 `detangle/reports/HOME_AUDIT_RESULT.md`를 확인 → **보고**(아래 4).

## 3. 절대 하지 말 것 (게이트)
- ❌ `git push` / `--force` / `git merge` / `git rebase` / 브랜치·파일 삭제 — **전부 금지**(이번 단계는 감사만).
- ❌ **코퍼스/저작권 콘텐츠**(wiki/papers, wiki/data, articles, sidecar, *.docx, *.pdf, *.csv, *.npy, *.pkl)를 **어떤 remote에도 push 금지**. 그런 커밋은 *보고만*.
- ❌ geochemistry-analyzer / manuscript-atelier repo에 **새 커밋·브랜치 만들지 말 것.** 보고는 이 `ccc-protocol` 협업 repo에서만.

## 4. 보고 방법 (CCCP)
둘 중 하나:
- (a) `detangle/reports/HOME_AUDIT_RESULT.md`를 이 `ccc-protocol` 브랜치에 commit + push (이 repo는 corpus-free라 안전). 맨 위 `VERDICT:` 헤더 채울 것.
- (b) 또는 GitHub 운영자 콘솔(issue#1)에 결과 붙여넣기.
- 추가로 `detangle/inbox_claude/`에 한 줄 남겨주면 회사PC가 바로 받음: `HOME: audit done, N repos, M unpushed branches, VERDICT=...`

## 5. 참고
- 회사PC도 동시에 자기 쪽(Cursor 클론·worktree 14개·GCA) 감사 진행 중 → 둘 합쳐 정본 결정표 작성 예정.
- 질문/막힘 있으면 `detangle/inbox_claude/`에 남기거나 콘솔에 질문. blocked면 VERDICT=blocked로 사유 적기.
