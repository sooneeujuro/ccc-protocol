# 노트북(`soone`) continuation — de-tangle 실행 핸드오프

회사PC가 B단계(감사)·결정표·P0가드·기능 guardrails·빌드 아카이브까지 끝냄. 노트북은 **자기 머신에만 있는 작업본**(home geochem-analyzer-git, home manuscript-atelier)에 대한 실행 몫이 있음. 전부 **운영자 GO 게이트**.

## 0. 셋업 (옮기기 = 이게 전부)
1. **ccc-protocol 브랜치 pull** → 모든 de-tangle 문서 확보:
   ```
   cd ccc-protocol && git fetch origin && git checkout coop/detangle-20260615 && git pull
   ```
   읽을 것: `detangle/RUN_STATE.md`(보드) · `DECISION_TABLE.md`(작업본 처분) · `P0_LANDMINE_GUARD.md`(긴급) · `FUNCTIONALITY_GUARDRAILS.md`(기능 보존 8개).
2. **G: 외장 꽂기** — `G:\corpus_build_history`(빌드 히스토리) + `G:\corpus_md_export_*`(코퍼스 번들·정본). 물리 이동만.
3. (그게 다임 — 코드/결정은 git, 코퍼스/아카이브는 G: 외장.)

## 1. 노트북 실행 몫 (GO 게이트, 순서대로)
### 🧨 P0 — ma LANDMINE (제일 급함)
- `P0_LANDMINE_GUARD.md`의 gitignore 패치를 **home `manuscript-atelier`에 적용**:
  - senpai-design 브랜치 `.gitignore`에 패치 추가 → **명시적 path-add 커밋**(`git add .gitignore`만, **`git add -A` 절대 금지**).
  - `docs/handoffs/fig_refill_20260613/out*`(215MB)는 **NAS 통합본 잔여물 가능성** → 운영자 확인 후 NAS 이동/삭제.
  - 추가 가드(`FUNCTIONALITY_GUARDRAILS` #2): index 디렉터리 `*.bak.*`·`*.report.json`도 ignore.

### 2. senpai-design 6커밋 → ma main
- code/docs-only(안전). `git push origin claude/research-discussion-senpai-design` → **PR로 main 머지**(6f36b77 A3/A6/B8 등 포함). 기록 위해 PR 권장.

### 3. A4/A5 백업 (home geochem)
- `claude/p1-science-accuracy` 2커밋(b05dfb62/4dd92ecb, code-only) → **백업 push**(코퍼스 무관) 또는 web 클린룸 포팅 결정(운영자 아키텍처 판단). **코퍼스 브랜치 아님 = push 안전.**

### 4. (E 전에) 비-git 자산 백업
- `FUNCTIONALITY_GUARDRAILS` #6: home ma의 `.env.local`·index 디렉터리·`datalab/`는 git에 없음 → history rewrite/re-clone **전에** 별도 스냅샷.

## 2. 보고
- 각 단계 결과를 `detangle/inbox_claude/`에 한 줄 + 필요시 `reports/`. push 전 `git pull --rebase origin coop/detangle-20260615`.
- **철칙**: 코퍼스 remote push 금지 · geochem-analyzer 코디네이션 커밋 금지 · 위험단계 GO 게이트.
