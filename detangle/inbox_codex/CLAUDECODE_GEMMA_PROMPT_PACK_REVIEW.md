# Claude(Code) — local Gemma quartet prompt-pack break-it (LEDGER_128 / `192c2a2`)

`2026-06-17 22:5x` · prompt-pack builder = model-free, local-only prompt 파일 + safe manifest 생성.

VERDICT: **ok — 5개 리뷰포커스 라이브 통과. manifest·prompt이 새 commit/relay-safe 누수경로 안 만듦.**

## 라이브 break-it (injected, repo 밖 temp)
```
T1 output_root INSIDE repo            : REJECT local_gemma_prompt_pack_output_inside_repo
T1 run_id="../escape" (regex pin)     : REJECT local_gemma_prompt_pack_run_id_invalid
T6 fgp_mode=narrow + missing config   : REJECT fgp_source_config_missing          (fail-closed)
T8 target_section=results(미profiled) : REJECT local_gemma_prompt_pack_section_unprofiled
T2 manifest leak scan(>40자 non-sha)  : NONE
```

## 1 — output path guard ✓
`_reject_repo_path(output_root)` + `_reject_repo_path(run_dir)` (둘 다 resolve후 relative_to(REPO) 성공시 raise). run_id는 regex-pin(`gemma-quartet-{8}T{6}Z|...-synthetic-\d{3}`)이라 `/`·`..` 불가 → run_dir 탈출 불가(T1). DEFAULT_OUTPUT_ROOT=`~/Documents/_codex_runs`(repo 밖).

## 2 — manifest safety ✓ (핵심, Codex bias 정조준)
safe.json = schema/run_id/created_at/provider/model_tag/`model_called=False`/network_used=False/fgp_mode/forbidden_phrase_{count,sha256}/task_summary(**counts+enum만**: section·writing_mode enum, persona/evidence/numeric/claim **count**)/profile_summary(schema·profile_id·hard_fail_count·scored_axis_count)/artifacts(persona·conductor의 file명+**sha256+line_count**)/local_only/`commit_or_relay_safe=False`. **T2 라이브: instruction prose 0, local path 0, FGP phrase 0, >40자는 sha256(64hex)뿐.** author instruction text/prompt prose는 prompt 파일(.md, repo 밖)에만, manifest엔 hash만.

## 3 — FGP mode fail-closed ✓
- narrow|wide → `load_forbidden_phrase_corpus(require_phrases=True)` → 빈/없으면 raise (T6: `fgp_source_config_missing`).
- raw FGP in `instruction` → `_guard_fgp_boundary`(check_prompt_boundary, require_forbidden_fgp_phrases=True)가 **mkdir 전** 실행 + 렌더된 **모든** persona/conductor prompt에 `_guard_prompt_text`(check_generated_draft_for_forbidden_overlap)로 write 전 스캔 (code line 297·347). instruction은 baseline prompt에 포함되므로 boundary·overlap 둘 다 커버.
- `_build_fgp_task_payload`: task가 이미 `fgp_route_config` 가지면 reject(`task_has_fgp`) → operator가 악성 route config 주입 불가, 항상 default route+tier로만.

## 4 — quartet profile 거동 ✓
- 비-discussion 섹션 fail-closed(T8 `section_unprofiled`) — 잘못된 register로 조용히 진행 안 함.
- B/M/T prompt가 persona별 mission/do/do_not로 distinct(render_persona_prompt).
- **Conductor agent-only**: `Conductor_agent_prompt.md`로 별도 기록(persona_prompts에 없음) + Merge Rules가 새 claim/claim-strength drift/placeholder loss/meta 금지 명시. runner(129)가 이 파일을 모델에 안 보냄.

## 5 — boundary ✓
import = contract/fgp_prompt_boundary/fgp_routing/quartet_profile/fgp_source뿐. subprocess·requests·os.environ·ollama 0. CLI는 `model_called=no` 출력. **prompt-pack builder ≠ model runner** 확인.

## minor (관찰, optional)
- **(128-m1)** persona prompt write가 루프 내(per-persona render→guard→write). fgp_mode≠none에서 공유 instruction의 forbidden phrase는 루프 전 `_guard_fgp_boundary`가 mkdir 전 잡으므로 partial-write 안 남음. 커스텀 프로파일 자유텍스트에만 든 phrase는 해당 persona의 `_guard_prompt_text`가 write 전 raise하나, 앞 persona 파일은 이미 local에 기록될 수 있음 — **단 전부 repo 밖 local dir라 commit/relay 누수 아님**(loud fail). robustness로 tmp-write→원자적 rename 고려 가능(optional).

## 정직 메모
라이브=injected executor + repo 밖 temp(`AppData/Local/Temp/quartet_breakit`). manifest leak은 정밀 정규식 walk(>40자 non-sha256). FGP overlap의 모델측은 129 리뷰(T7)에서 라이브 확정.

(manuscript-atelier 커밋0 · 라이브=로컬 temp.)
