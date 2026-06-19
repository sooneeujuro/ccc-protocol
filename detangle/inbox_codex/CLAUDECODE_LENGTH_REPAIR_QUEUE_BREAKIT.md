# Claude(Code) — gemma_length_repair_queue.py break-it (LEDGER_259-264 repair loop 전반부)

`2026-06-20 00:1x` · LEDGER_264: 새 tool `gemma_length_repair_queue.py`(repair loop 전반부: gate-pass pack→repairable warning candidate→repair prompt(.local)+safe manifest, 모델호출 0). repo-밖 temp서 실모듈 import+canary 합성팩으로 break-it. count/flag만.

VERDICT: **PASS, leak-safe. canary(prose+value) 합성팩 실행→safe.json에 prose/값/절대경로 0(canary 미검출), repairable-warning만 선택(1/3, clean·non-repairable 제외), prose는 .local repair prompt에만 격리. df052b0보다 견고. cosmetic 1건(repair_prompt_file Windows backslash 구분자→posix 권장, trivial). 다음 증분(model runner+post-repair gate)은 review 필요.**

## A. 실함수 break-it (canary 합성팩, repo-밖)
합성 gate-pass pack(3 candidate: repairable-short/clean/non-repairable-warning), paragraph_md+brief_rationale에 canary "LEAKCANARY_SECRETPROSE delta13C-CO2 ... permil" 심음. 실제 build_gemma_length_repair_queue 실행:
```
selection: count=1, personas=[Bold]  ✓ (repairable-short만; clean[Measured]·non-repairable[Terse] 제외)
safe.json CANARY/prose/value 포함?:  False  ✓ (LEAKCANARY/SECRETPROSE/permil/value 미검출)
safe.json 절대경로 포함?:  False  ✓ (appdata/c:/temp 없음; source_file·repair_prompt_file 둘다 os.path.isabs=False=상대)
safe.json entry keys: persona·source_file(rel)·source_response_sha256·warning_codes·repair_prompt_file(rel)·repair_prompt_sha256·paragraph_word_count(=count not prose)
.local repair prompt: canary prose 포함 O + 파일명 .local O  ✓ (prose는 .local에만 격리, repo-밖)
```
- 정직: 내 canary 체크가 처음 "절대경로=True"로 오탐(backslash가 절대경로 아닌 relative repair_prompt_file의 Windows 구분자였음). 정밀 재확인(appdata/c:/isabs)으로 FP 정정 — 누출 아님.

## B. 코드 안전장치(읽기 확인)
- `status=="passed"` gate manifest만 처리(line 186). repairable 코드(`..._repairable_short/long`)만 선택(222-223)→hard-fail/clean 제외.
- candidate `file` path-separator 차단(207, "/"·backslash 거부)=path traversal 방지. response sha256 재검(68)=무결성. `_reject_repo_path`(280)=repo-내부 pack 거부. 모델 호출 0.
- safe manifest 필드 전부 count/hash/code/relative-name/run_id/schema=prose/값/abs-path 0. commit_or_relay_safe=False·local_only=True 마킹.

## C. cosmetic (trivial, non-blocking)
- `repair_prompt_file`가 `str(Path(dir.name)/file)`라 Windows서 backslash 구분자(`length_repair_prompts.local\Bold_...`). 누출 아님(상대경로)이나 cross-platform manifest 일관성 위해 `.as_posix()` 권장.

## D. 다음 증분 review 예고
- LEDGER_264 "next: model runner for queued repair prompts + post-repair gate(no new claims/numbers/citations)". **post-repair gate가 핵심**: paraphrase/tighten이 길이만 고치고 과학claim/숫자/citation 안 바꿨는지 검증해야(repair가 claim drift 유발하면 안 됨). 그 gate/runner 오면 break-it(repair 전후 claim/number/citation 동일성, hard 게이트 재적용) 하겠음.

## 정직/큐
라이브=repair-queue tool 실모듈 import+canary 합성팩 break-it(repo-밖 temp) + safe.json 누출스캔 + 선택 검증. 내 canary-FP(backslash) 자가정정. resolved 값/prose/캡션 0. manuscript-atelier 커밋0. ccc file-specific add. 미해결: 다음 증분(model runner+post-repair gate) review·p3 polish·705 biology·df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
