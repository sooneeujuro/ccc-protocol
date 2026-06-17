# Claude(Code) — FGP portable local source R0 break-it (LEDGER_054 / `40a38b8`)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **ok — R0 ACCEPT (intended out-of-repo 모드 기준). 핵심 가드 라이브 확인.** 단 should-fix 1(R-a fail-open) + nit 2. should-fix는 *in-repo byte-copy 모드 의존 전*에 고치면 됨(그 모드는 권장X라 기본경로엔 영향 없음).

검증: fgp_source.py + check_fgp_source.py 정독 + **temp git repo로 라이브 보안 매트릭스**(R-a/R-c/R-e).

---

## 라이브 매트릭스 (핵심 가드 작동)

```
R-e1 relative ../../etc escape   : REJECT fgp_source_path_escape           # resolve+is_relative_to
0 in-repo untracked root inspect : OK ready
R-a in-repo TRACKED file inspect : REJECT fgp_source_root_contains_tracked_files   # 핵심
R-c .local.json NOT ignored      : REJECT fgp_source_phrase_corpus_not_ignored     # is_git_ignored fail-closed
R-c non-.local name              : REJECT fgp_source_phrase_corpus_not_local
R-c .local.jsonl ignored         : OK (wrote)
count-only status                : phrase_count=2, sha=set, 문구 누수=no
```

설계리뷰 반영 확인: **out-of-repo 절대경로 기본**(example `REPLACE_ME_OUT_OF_REPO...` + "Prefer out-of-repo absolute, do not commit real paths/raw") / **PHRASE_LAYER_DIRS=3rd-party만**(Plated/cards·handbook·Cooked·Chopped·Original, **Personal·writing 제외**=내 Q3) / **`.local.jsonl` corpus + checker count·hash만**(상태에 문구0) / **@eaDir(Synology) skip** / R-e 이중커버(config 상대escape + iter_phrase_files의 file escape).

---

## should-fix 1 (R-a fail-OPEN — 보안가드는 fail-closed여야)

`git_tracked_paths_under`가 git 명령 `returncode != 0`이면 **`[]` 반환**(line 298-300). 라이브 확인: repo_root가 non-git이면 `git ls-files` 실패 → `[]` → `inspect_fgp_source`가 tracked 0으로 보고 **통과**. 즉 **git 부재/깨짐 + root_inside_repo면 raw-FGP-in-repo 가드가 조용히 꺼짐.**

대조: `is_git_ignored`는 git 실패 시 `returncode != 0` → `False` → write 거부 = **fail-CLOSED**(올바름). 비대칭이 tell.

**Fix**: root_inside_repo인데 git 명령 실패(또는 git 부재)면 **fail-CLOSED**(`fgp_source_git_check_unavailable` raise), `[]`로 넘기지 말 것. **실무 확률은 낮음**(git repo엔 git 있음) + **기본 out-of-repo 모드는 root_inside_repo=False라 git 체크 자체를 안 함**(정상). 그래서 blocker 아님 — **in-repo byte-copy 모드(권장X) 의존 전에** 고치면 됨.

## nit 2
- **R-c config-load는 gitignore 미검증**: `load_fgp_source_config`가 phrase_corpus_path의 `.local.` infix만 보고 `is_git_ignored`는 안 봄(write_phrase_corpus_local만 봄). write 가드가 operative(fail-closed 확인)라 저위험. config-load에도 한 줄 추가하면 defense-in-depth.
- **symlink-root tracked**: `local/` 아래 symlink가 repo 밖을 가리키면 root가 밖으로 resolve→root_inside_repo=False→git 체크 skip. 그 symlink 자체가 tracked여도 안 잡힘. 저위험(링크는 content 아님 + gitignore가 local/ 덮음 + `git add -f` 필요).

---

## 통합 + 다음

R0는 **의도된 out-of-repo 모드 기준 견고** — 핵심 가드(R-a tracked탐지·R-c fail-closed·R-e escape·count-only) 전부 라이브 확인. should-fix(R-a fail-open)는 in-repo 모드 쓰기 전 처리.

**다음 = ablation runner**: `load_forbidden_phrase_corpus()` → `check_prompt_boundary(... require_forbidden_fgp_phrases=True)` + `check_generated_draft_for_forbidden_overlap(... require=True)` mandatory 배선. 그거 만들어지면 내가 깸(특히 두 가드가 *진짜* mandatory로 호출되는지 + empty-corpus fail-close + corpus가 committed 안 되는지). 지도 FGP 트랙 "source R0 ACCEPTED(40a38b8), R-a fail-open should-fix"로.

(read-only · manuscript-atelier push0 · 머지0 · raw FGP 커밋0. 라이브=temp git repo + 로컬 `.scratch/`.)
