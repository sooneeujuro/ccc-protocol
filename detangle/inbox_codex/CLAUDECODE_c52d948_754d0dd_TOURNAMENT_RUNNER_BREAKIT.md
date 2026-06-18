# Claude(Code) — c52d948(tournament runner) + 754d0dd(singleton persona filter) break-it

`2026-06-18 11:4x` · runner landing 직후 코드 break-it. 실 함수 정독 + 실제 run 디렉토리(gemma-tournament-20260618T111500Z) 구조 검사. **run 진행중(4/45, pid 54820 alive, scoring manifest 미생성)이라 채점은 미실시** — 이번은 코드/매니페스트 구조만. response prose 미열람(파일명/카운트만).

VERDICT: **ok(runner 수용) — BLIND/EXECUTION/REVEAL 경계 구조적 성립, scoring manifest response-only(내 권고 구현), de-blind self-check 완전, fake-green 없음. + LOW 2(forward, 블로커 아님). gate-change 754d0dd 건전(느슨화 아님).**

## A. 경계·response-only (operator point 1·2·4) — 통과
- **EXECUTION-only 입력**: `_load_execution_manifest`가 `schema==local_gemma_prompt_tournament_execution_v1` AND `blind_scoring_surface is False` 아니면 reject(`..execution_scope_invalid`). BLIND을 runner 입력으로 쓰면 거부. ✓
- **blind manifest leak guard**: `_load_blind_manifest`가 `"prompt_pack_dir" in json.dumps(payload)`면 reject(`..blind_manifest_leaky`). ✓
- **scoring_entry = response-only(내 refinement 구현됨)**: 필드 = `{blind_variant_id, persona, repetition, status, attempt_count, elapsed_ms, error_stage, error_code, response_file(상대), response_sha256, +int counts}`. **prompt_sha256/task_sha256/prompt_pack_manifest_sha256/prompt_pack_dir 전부 없음** = 내가 요청한 prompt-side 키 제거 정확 반영. ✓
- **de-blind self-check 완전**: `_FORBIDDEN_BLIND_STRINGS` 9개가 **실제 variant_id 전부와 일치**(licensed_max/caveat_survivor/test_framed/claim_then_caveat/woven_caveat/caveat_front/n_points/frame_bound/minimal_clause — M2가 `M2_woven_caveat`라 `woven_caveat` 정확). `_assert_scoring_manifest_is_blind`가 직렬화 스캔 후 hit 있으면 `..scoring_manifest_leaky` raise. ✓
- **gen-order grouping 차단**: scoring entries `sorted(by blind_variant_id)`. ✓
- **integrity**: `_cross_check_blind_entries`가 blind↔execution 의 blind_id 집합+persona/repetition/3 sha 일치 강제(불일치→`..blind_execution_mismatch`). ✓

## B. fake-green / recompute (내 상시 공격면) — 통과
- status="passed"는 **`gate_local_gemma_candidates`가 실제 실행돼 raise 안 했을 때만** 설정(trust-summary 아님, 실 게이트). gate 실패→`diagnose_*`로 진단 summary만.
- `passed_count/failed_count`는 entries에서 **재계산**(`sum(row["status"]=="passed")`), trusted summary 아님. ✓ recompute-vs-trust 통과.
- response 복사(`_copy_scoring_response`)는 **PASS 분기에서만** → scoring_blind.local엔 gate-통과(placeholder-bound·no_new_numbers-clean·FGP-overlap-clean) response만. fail은 response_file=None. ✓

## C. path-traversal / repo 격리 — 통과
- `_entry_prompt_pack_dir`: `raw.startswith("/")` or `"\\" in raw` reject → resolve → `relative_to(tournament_dir)`(escape면 `..escape`) → `_reject_repo_path`. `..`/abs(`C:/`는 join서 escape catch)/UNC(`\\`) 전부 막힘. ✓
- `_reject_repo_path`로 tournament_dir·prompt_pack 모두 repo 밖 강제. ✓

## D. timing/gate per-call (operator point 3) — 충족(+LOW 1)
per-entry: `elapsed_ms` + `attempts[]`(각 attempt elapsed_ms/status/error_stage/error_code) + `attempt_count`(retry) + `error_stage/error_code` + `gate_summary`(status·word/char/id counts). run-level: `started_at/completed_at/timeout_seconds/max_retries` + `timing_summary`(total·median·p90 entry/passed). breeding round 시간통계에 충분.
- **🔎 LOW#1(forward)**: per-call **절대 start/end 타임스탬프**는 미기록(run-level만 + per-call duration). 순차 실행이라 순서는 암시적 → 통계엔 무영향. forensic overlap/ordering 분석 원하면 per-entry `started_at/ended_at` 추가 권고. **블로커 아님.**

## E. gate-change 754d0dd 건전성 (느슨화 여부)
`_response_entries`가 hardcoded `["Bold","Measured","Terse"]` → `task.persona_set`로. **singleton pack(persona 1개)이 게이트 통과하려면 필수**. 느슨화 아님 — `task.persona_set`은 `_required_persona_set`(contract.py)이 **empty reject·non-string reject·unknown∉{Bold,Measured,Terse} reject·dup reject**로 검증. 즉 declared set과 order-sensitive exact-match 유지, 검증된 집합만 허용. ollama_quartet_runner도 대응(subset-in-canonical-order + empty reject). candidate_count/response_count의 hardcoded "3"→실측은 cosmetic(singleton=1 표시 정정). ✓

## F. LOW#2 (defense-in-depth)
`_assert_scoring_manifest_is_blind`는 9 variant label + 2 path token만 스캔, abs-path(`C:\`)·task-instruction prose는 미스캔. 단 scoring_entry 구성상 abs-path/prose가 들어갈 자리 없음(필드가 enum/상대경로/카운트뿐)이라 **현재 무누수** = defense-in-depth만. belt-and-suspenders로 abs-path 스캔 추가 고려(선택).

## G. run 상태 + 내 다음
- run 진행중: pid 54820(python) alive, scoring_blind.local 4/45, `LOCAL_GEMMA_TOURNAMENT_SCORING_BLIND.local.json` 미생성. **45 완료 후 채점.**
- 내 다음(scoring manifest 생성되면): (1) 독립 detector를 scoring manifest에 적용(de-blind/abs-path/금지키 cross-check) → (2) 통과시 scoring_blind.local의 gate-passed response를 **로컬에서만** 읽어 blind 채점(blind_id별 45개 독립 per-response: claim_altitude 양방향·caveat_survival·register·protected·conciseness, negation-aware) → (3) 완료 후 REVEAL로 variant 묶어 median/worst/var → persona별 winner(median−λvar−μ(2−worst)·pass_rate≥4/5·best-of 금지) → held-out. 점수/카운트만 보고, prose 미노출.

## 정직/큐
라이브=runner 실 코드 정독 + 실 run dir 구조검사(파일명/카운트, prose 미열람) + contract `_required_persona_set` 확인. 신규코드=c52d948/754d0dd. manuscript-atelier 커밋0. ccc detangle file-specific add. Anthropic_Invoices zip untracked. 다음: scoring manifest 생성 폴 → detector 적용 → blind 채점. 백로그(0a68ea8/9a03e90) deferred. (내 detector 토큰 woven→woven_caveat 보정 예정=내 도구, runner 무관.)

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값/prose 미노출.)
