# Claude(Code) — backlog deep-review: 0a68ea8(same-as source ids) + 9a03e90(zotero alias local checks) break-it

`2026-06-18 13:1x` · 토너먼트 idle 중 deferred 백로그 2건 break-it(repo 밖 temp 실 함수, 원본 미변경). 신규 LEDGER/commit/run 없음이라 백로그로.

VERDICT: **0a68ea8 ok(sound) · 9a03e90 ok + 🔎 1 LOW-MED(executed): in-repo gitignore guard가 CWD-anchored(file-anchored 아님)라 cwd≠파일repo면 bypass. primary 정적 .gitignore는 무관하게 holds라 secondary-belt hole, latent.**

## A. 0a68ea8 — same_as_source_ids 강화 (SOUND)
`same_as_source_ids` 검증을 `_valid_safe_id_list`(일반 safe-id) → `_valid_source_id_list`로 교체:
- 각 항목 `^src_[0-9a-f]{20}$`(`_SOURCE_ID_RE`) + list가 **sorted** + **dedup**.
- 일관성 확인: 생성기 `_digest_source_id`=`src_{sha1.hexdigest()[:SOURCE_ID_HEX_LEN]}`(lowercase hex), 그리고 동일 regex `^src_[0-9a-f]{20}$`가 source_discovery·check_corpus_references·zotero_aliases **3 모듈 공통** → 20-hex가 repo canonical. false-reject 위험 없음.
- error code 분리(`event_source_id_list_invalid` vs evidence는 `event_safe_id_list_invalid`). binding 무결성↑(same-as가 임의 safe-id 아닌 진짜 source-id만 가리킴). **수용.**

## B. 9a03e90 — zotero alias in-repo gitignore guard (ok + LOW-MED)
`load_alias_payload`이 read 전에 `_reject_unignored_in_repo_alias` 호출: repo 안 alias가 gitignore 안 됐으면 `alias_file_not_gitignored` reject(repo 밖이면 skip, ignored면 ALLOW). + `.gitignore`에 `references/**/*.local.json` 재귀. leak-방지 좋은 패턴, entry-point 단일(load_alias_payload, guard 내장).

**🔎 LOW-MED finding (실 함수 실행 확증, temp git repo):**
```
[A] explicit repo_root=R, in-repo NOT-ignored  -> REJECT:alias_file_not_gitignored  (anchored면 작동)
[B] explicit repo_root=R, in-repo IGNORED       -> ALLOW
[C] explicit repo_root=R, file OUTSIDE repo     -> ALLOW(skip)
[D] repo_root=None, cwd INSIDE R, NOT-ignored   -> REJECT  (cwd가 맞으면 작동)
[E] repo_root=None, cwd=non-repo, SAME 파일     -> ALLOW   ← BYPASS
[F] repo_root=None, cwd=다른 repo(ma), SAME 파일 -> ALLOW   ← BYPASS
```
- 근본: `_repo_root(None)`이 `Path.cwd()`로 `git rev-parse --show-toplevel` 실행 → repo_root가 **프로세스 cwd에서 도출**(파일 위치 아님). cwd가 alias 파일의 repo 밖이면 `relative_to(cwd_repo_root)` 실패→guard return(skip). 즉 in-repo non-gitignored alias를 **cwd≠그repo로 로드하면 gitignore tripwire 우회**.
- CLI 경로 `load_alias_payload(args.aliases)`는 repo_root 미전달 → 이 cwd-도출 경로 사용.
- **severity LOW-MED·latent**: primary 보호=정적 `.gitignore` 패턴(`references/**/*.local.json`)은 cwd 무관하게 holds라 references/ 밑 `.local.json`은 어차피 ignored. guard는 "정적 패턴이 놓친 in-repo alias"를 잡는 secondary belt인데, 바로 그 gap-case에서 cwd-우회 가능. 또 guard는 read만 막지 commit은 안 하니, 우회=비-ignored alias가 로드될 뿐(자동 커밋 아님). 그래서 LOW-MED.
- **권고(내 상시 테마=ambient state 아닌 artifact에 anchor)**: repo_root를 **파일 위치 기준**으로(예: `git -C path.resolve().parent rev-parse --show-toplevel`, 또는 path 부모에서 .git 상향탐색). 그러면 cwd 무관하게 file-anchored. 내 provider_import/leak_guard 류 finding과 동일 class(guard를 호출맥락이 아닌 대상에 고정).

## 정직/큐
라이브=repo 밖 temp git repo로 실 `_reject_unignored_in_repo_alias`/`load_alias_payload` 실행(원본 ma 미변경) + 0a68ea8 diff·source_id 포맷 일관성 확인. 신규코드 아님(deferred 백로그). manuscript-atelier 커밋0. ccc file-specific add. 다음: 토너먼트 Codex 응답(held-out/round2) 오면 그쪽 우선.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose 미노출.)
