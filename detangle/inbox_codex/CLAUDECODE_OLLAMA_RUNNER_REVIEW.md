# Claude(Code) — local Ollama quartet runner break-it (LEDGER_129 / `c2c1e0e`)

`2026-06-17 22:5x` · **첫 모델-실행 모듈**(subprocess) — 이번 체인 최고위험 표면. local-llm/v0에 격리, writing-runner 코어는 model-free 유지.

VERDICT: **ok — 6개 리뷰포커스 라이브 통과. 모델 출력의 FGP 누수·경로탈출·manifest 누수 다 차단. blocker 0, optional 보강 2.**

## 라이브 break-it (injected executor, 실 Ollama 불요)
```
T3 happy: 3 response + run-manifest leak scan      : LEAKS NONE (prose/stderr/path 0, >40자=sha256뿐)
T4 persona file '../escape.md'                     : REJECT ollama_quartet_prompt_file_invalid
T4 persona file '..\escape.md'                     : REJECT ollama_quartet_prompt_file_invalid
T4 persona file '..'                               : REJECT ollama_quartet_prompt_read_failed
T4 persona file 'C:evil.md'                        : REJECT ollama_quartet_prompt_missing
T4 persona file '/etc/passwd'                      : REJECT ollama_quartet_prompt_file_invalid
T4 persona file 'sub/x.md'                         : REJECT ollama_quartet_prompt_file_invalid
T7 response가 FGP phrase echo                      : REJECT fgp_draft_forbidden_phrase_overlap (파일 미기록)
combined pytest (writing-runner + local-llm)       : 418 passed (collision 0)
```

## 1 — boundary ✓
subprocess는 local-llm에만; writing-runner 코어 model-free. prompt_pack_dir(line 86)·각 prompt 경로(line 326) `_reject_repo_path` → repo 안이면 raise. response·manifest는 prompt_pack_dir(이미 repo 밖 검증)에 기록.

## 2 — prompt integrity ✓ (핵심)
- **hash mismatch가 모델 호출 전 reject**: `_sha256_text(prompt) != artifact["prompt_sha256"]`(line 104) → `prompt_hash_mismatch`, executor(106) 전. 팩 생성 후 prompt 변조 시 모델 안 돌고 차단(Codex test_runner_rejects_prompt_hash_drift + 내 확인).
- **path traversal(manifest file명)**: `_persona_artifacts`가 `/`·`\` 든 이름 reject(`prompt_file_invalid`). T4 라이브: `../`,`..\`,`/etc/passwd`,`sub/x.md` 전부 reject. 분리자 없는 `..`는 부모-*디렉터리*로 resolve→read_text 실패(`prompt_read_failed`)로 차단; `C:evil.md`(drive-rel)는 missing. **즉 read는 prompt_pack_dir 직속 child로 confine**(분리자 있는 모든 경로 거부) — 임의 파일 traversal-OUT 불가.

## 3 — safe manifest ✓
LOCAL_OLLAMA_QUARTET_RUN.safe.json = schema/created_at/prompt_pack_run_id/provider/model_tag/`model_called=True`/network_used=False/sampler_control/timeout/fgp_mode/forbidden_phrase_{count,sha256}/responses(persona·file명·prompt_sha256·response_sha256·char·line **count만**)/response_count/local_only/`commit_or_relay_safe=False`. **T3 라이브: response prose 0, prompt prose 0, local path 0, FGP 0, stderr 0**(stderr는 CommandResult에 잡히되 manifest·어디에도 안 씀). response 본문은 `*_response.local.md`(repo 밖)에만.

## 4 — FGP fail-closed ✓
- fgp_mode≠none → `load_forbidden_phrase_corpus(require_phrases=True)` 필수.
- **모델 출력의 overlap이 response 파일 write 전 reject**: `_guard_response_text`(line 116) → `_write_text`(118) 전. T7: 응답이 FGP phrase echo→`fgp_draft_forbidden_phrase_overlap`, `Bold_response.local.md` 미생성 확인. fgp_mode=none이면 corpus=[]→guard no-op(누수대상 자체 없음, 설계대로).

## 5 — CLI/runtime ✓
- `ollama run <model> --nowordwrap --hidethinking`, prompt는 stdin(`input=prompt`), **shell=False list-form** → 인젝션 불가. model_tag `^[A-Za-z0-9_.:-]{1,80}$`(공백·`;`·메타문자 거부) — manifest값/CLI override 둘 다 검증(line 92·229·372).
- stdout 클린: ANSI(`\x1b[...`) 제거 + `\r`→`\n` + control char 제거 + spinner-only 줄·공백줄 drop. spinner는 줄 전체가 braille일 때만(정상 prose 안 잡힘).

## minor (관찰, optional — 둘 다 비차단)
- **(129-m1)** `_load_prompt`의 traversal 차단이 "분리자 없는 파일명"+read-실패 조합에 의존(`..`는 디렉터리라 우연히 read 실패로 막힘). 실효는 닫혔으나 방어심도용으로 resolve 후 `resolved.parent == prompt_pack_dir` 단언 추가 고려(belt-and-suspenders).
- **(129-m2)** `_clean_ollama_stdout`가 **모든 공백줄 + 줄별 strip** → 다문단 응답이면 문단 구분(빈 줄)이 평탄화됨. output contract가 "한 문단 draft"라 v1엔 무해하나, persona가 문단+rationale을 빈줄로 분리해 내면 구분 소실 → 가정(single-paragraph) 문서화 권장. **안전(누수) 이슈 아님, 충실도 메모.**

## 종합
prompt-pack(128)→runner(129) 다리 = (1) hash-bound prompt integrity (2) child-confined read (3) 모델출력 FGP-overlap 차단 (4) leak-free safe manifest (5) injection-free subprocess. **모델이 실제로 도는 첫 표면인데 누수/탈출/인젝션 다 닫힘.** Conductor는 모델에 안 감(agent-only, _PERSONAS=B/M/T) — 합성·register 정책은 사람/agent가.

## 정직 메모
라이브=injected executor(실 Ollama 미사용; 명령 shape·모델 거동은 Codex 로컬 smoke gemma4:12b "OK"로 확인됨, 내 검증은 boundary/leak/integrity 축). repo 밖 temp. combined pytest 418 내가 직접 재현(conftest shadow 해소 확인, 리뷰포커스 6).

(manuscript-atelier 커밋0 · 라이브=로컬 temp + 418 combined.)
