# Claude(Code) — gemma_repair_semantic_review_runner.py break-it (LEDGER_275, 7 케이스 요청)

`2026-06-20 00:5x` · LEDGER_275가 명시 요청한 7 break-it. executor 주입형이라 가짜 executor+canary로 모델 없이 repo-밖 실행. count/flag만.

VERDICT: **6/7 견고. malformed/invalid-status/non-bool-drift/count-mismatch/hash-drift 전부 REJECT, empty-queue=executor 호출 0·model_called False, safe-manifest canary 누출 0(notes/prose/abs-path 미포함, 실증). 1 발견(#2 fenced): runner end-to-end에선 fenced가 REJECT 안 되고 strip+accept됨 — _clean_ollama_stdout가 fence를 상류서 제거해 _load_review_response_payload의 response_fenced 체크가 unreachable. low severity(inner JSON 여전히 전체 검증), 단 intent 불일치+단위테스트 갭.**

## A. 7 케이스 실증 (가짜 executor)
```
#1 malformed JSON      -> REJECT response_json_invalid   OK
#2 fenced response     -> ACCEPT (clean 후 통과)         <- 발견(아래 B)
#3 invalid status      -> REJECT status_invalid          OK
   non-bool drift flag -> REJECT drift_flag_invalid      OK
#4 prompt hash drift   -> REJECT prompt_hash_mismatch    OK
#5 queue count mismatch-> REJECT queue_count_mismatch    OK
#6 safe-manifest leak  -> canary(notes/prose) 0·abs-path 0  OK (row keys=item_id/source_kind/source_label/prompt-file/sha/response-file/sha/review_status/drift_flags; notes 미포함)
#7 empty queue         -> executor 호출 0·model_called False  OK (no false model call)
valid pass/issues_found -> OK (정상 accept)
```

## B. 발견 #2: fenced reject가 runner 경로서 unreachable
- 정밀확인:
  - `_load_review_response_payload(fenced)` 직접호출 -> REJECT response_fenced (체크 작동)
  - `_clean_ollama_stdout(fenced)` -> fence 제거, inner JSON 반환
  - runner는 line 127 _clean_ollama_stdout → line 132 _load_review_response_payload 순서 → fence가 이미 제거돼 response_fenced 분기 안 탐 → fenced 응답이 cleaned 후 accept.
- 함의: Codex 단위테스트 #2가 validator를 직접 테스트하면 PASS(reject 확인)하지만, **end-to-end runner 동작은 'fenced strip+accept'**라 테스트가 실제 경로를 반영 못 함(test-coverage 갭). "fenced=reject"라고 믿으면 오해.
- severity LOW: cleaned JSON은 status/drift/notes 전체 재검됨=안전 hole 아님. 단 의도 정리 필요.
- 권고(택1): (a)fence 관용이 의도면 → response_fenced 체크는 runner서 dead code(방어 backstop으로 두되 #2 테스트를 end-to-end로 바꿔 'strip+accept' 검증). (b)fence 거부가 의도면 → fence 체크를 _clean_ollama_stdout 前으로 옮기거나 이 runner선 cleaner가 fence 안 벗기게. 메타교훈: validator-단위 PASS ≠ integration 동작(상류 cleaner가 입력 바꿈).

## C. 견고 확인 (읽기+실증)
- queue 검증: schema·local_only=True·commit_or_relay_safe=False·status∈{queued,empty}·count==len·item_id 정규식·source_kind∈{bmt,conductor}·source_label per-kind·prompt_file unsafe-relative(abs/'..') 거부·sha 64.
- safe manifest: schema/run-id/model-tag/counts/relative-name/hash/review_status/drift_flags/drift_counts만. **notes(reviewer 노트=prose 가능)는 .local 응답파일에만, manifest 제외**(canary 0 확인).
- empty→no model call, hash recheck, _reject_repo_path(_load_text).

## 정직/큐
라이브=semantic review runner 7케이스 실증 break-it(가짜 executor+canary, repo-밖) + fenced 메커니즘 정밀확인(direct reject vs runner accept). 모델 미실행. resolved 값/prose/캡션 0. manuscript-atelier 커밋0. ccc file-specific add. 미해결: fenced intent 정리(#2)·accepted repair 의미재채점(이 runner가 자동화 시작)·queue .as_posix·p3 polish·705 biology·df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
