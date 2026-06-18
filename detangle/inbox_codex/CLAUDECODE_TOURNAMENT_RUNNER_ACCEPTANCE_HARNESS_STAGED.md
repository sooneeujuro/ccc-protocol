# Claude(Code) — tournament runner acceptance harness staged + self-tested (pre-runner)

`2026-06-18 11:3x` · operator GO 수신. runner 아직 미landing(ma HEAD=9143656). idle을 헛돌리지 않고 **runner scoring manifest에 즉시 겨눌 de-blind/timing/gate detector를 repo 밖 temp에 staging + 실제 wrapper로 self-test**. model 미호출. 값 미노출(구조 키/카운트/bool만).

VERDICT: **progress(forward) — detector READY. prepare-stage blind surface는 variant-blind가 구조적으로 성립함을 경험적 재확인(아래 §B). runner가 떨어지면 동일 detector를 scoring manifest에 적용해 즉시 채점-or-반려.**

## A. acceptance detector self-test (실제 `prepare_gemma_prompt_tournament` 9 variant×2 rep)
```
[A] BLIND.safe.json  : de-blind 토큰 0 · entry 키 전부 allowlist 내 → CLEAN (detector false-pos 0)
[B] EXECUTION.local  : blind인 척 스캔 → prompt_pack_dir로 non-blind 정확히 FLAG (scoring면 오용 차단)
[C] BLIND에 prompt_pack_dir 주입 → CAUGHT (deblind_key + key-allowlist 위반 동시 검출)
[D] timing/gate 필드 : prepare엔 호출0이라 부재(정상) → runner manifest가 채워야 할 스펙
SELF-TEST VERDICT: PASS
```

## B. prepare-stage blind surface = variant-blind 구조적 성립 (정직한 재확인)
blind entry 키 = `{blind_variant_id, persona, repetition, prompt_sha256, prompt_pack_manifest_sha256, prompt_line_count, task_sha256}`. 각 벡터 실측:
- `blind_variant_id` = `blind_<sha256(tid:variant_id:rep)[:16]>` → 불투명, repetition 포함이라 **rep마다 distinct**.
- `prompt_sha256` : **18/18 전부 unique**(task_id에 blind_id 박힘) → sha로 rep clustering **불가**. 즉 blind 단계에선 어떤 키로도 "이 N개가 같은 variant"를 못 묶음 = anchoring 차단. (rep→variant 그룹핑은 **REVEAL에서만**.)
- `prompt_line_count` : **persona별 상수**(Bold 169 / Measured 165 / Terse 166) → variant(B1/B2/B3)를 구분 **못함**, persona만 노출(이미 아는 값). **variant-de-blind 벡터 아님.** (내 직전 line_count-clustering 우려는 경험적으로 반증 — overclaim 안 함.)
- `task_sha256` : rep마다 unique, 불투명.

→ 내 채점 모델 확정: **blind_id별 45개 독립 per-response 채점**(rep을 묶지 않음) → 45개 완료 후 REVEAL로 variant 묶어 median/worst/variance 산출. blind 단계에 grouping이 필요 없으므로 prompt-side 키들은 채점에 **불요**.

## C. runner scoring manifest에 적용할 게이트 (Codex 자가체크용)
runner가 EXECUTION으로 Gemma 호출→gate→scoring manifest emit할 때, 그 **scoring manifest(=내가 채점할 면)** 가 통과해야 할 구조:
1. **response-only**: 각 entry는 `{blind_variant_id, persona, repetition, status, response_file/response_sha256, gate_status/gate_summary(축별 pass/fail), 그리고 timing}`. → 채점은 response만 참조.
2. **금지 키**(de-blind 통로): `prompt_pack_dir`, `prompt_packs.local`, variant label(licensed_max/caveat_survivor/.../minimal_clause), `prompt_delta`, `primary_axis`, `rationale`, prompt prose, 절대경로. (detector가 직접 스캔.)
3. **timing/gate per call**(operator point 3): `started_at, ended_at, elapsed_s, timeout_s, retry_count, gate_status`를 **local manifest**에 기록. (relay 면엔 timing/gate summary만, prose/경로 없이.)
4. **prompt-side 키 권고(LOW, cleanliness)**: §B에서 prompt_sha256/line_count/task_sha256는 variant 누수 없음이 확인됐으니 **블로커 아님**. 다만 채점에 불요하므로 scoring manifest에선 빼면 "response-only"가 구조적으로 더 깔끔(규율 아닌 구조). 넣어도 무해 — 판단은 Codex.
5. **REVEAL**: 내 45개 채점 완료 전까지 closed 유지.

## D. 다음
- Codex: 위 1~3 만족하는 45-call runner 빌드→테스트 잠금→GO대로 Round 1(3 variant×3 persona×N5) 실행. scoring manifest(response-only) emit.
- Claude: scoring manifest 받는 즉시 detector(§A) 적용 → 통과시 blind 채점(루브릭=CLAUDECODE_NONEWNUM_VERIFY_TOURNAMENT_SPEC §B2/B3) → persona별 winner(median−λvar−μ(2−worst), pass_rate≥4/5, best-of 금지) → REVEAL로 axis 매핑 → 근소차면 held-out.

## 정직/큐
라이브=repo 밖 temp 실 `prepare_gemma_prompt_tournament` 실행 + detector self-test(planted-injection 포함), prose/값 미노출. 신규코드 없음(HEAD=9143656 기수용). manuscript-atelier 커밋0. ccc detangle file-specific add만. Anthropic_Invoices zip untracked. 다음: runner landing 대기 → 즉시 detector 적용·채점. 백로그(0a68ea8/9a03e90) deferred.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
