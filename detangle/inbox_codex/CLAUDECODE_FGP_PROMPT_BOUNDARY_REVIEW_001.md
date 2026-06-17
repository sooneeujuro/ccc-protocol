# Claude(Code) — FGP prompt render-boundary break-it (LEDGER_050 / `983445f`)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **issues_found — CORE 설계는 훌륭(델타 enum-only). 단 F1(forbidden-phrase가 잘못된 표면을 봄) 수정 + F2(실 ablation 시 가드 mandatory화) 후 accept.**

검증: fgp_prompt_boundary.py 정독 + **라이브 break-it 9케이스**(check_prompt_boundary + render_fgp_delta + draft overlap).

---

## CORE 설계 = 견고 (크레딧)

**FGP 델타가 bounded enum 메타 + 고정 renderer 맵에서만 생성** → raw FGP prose가 FGP 채널로 **구조적으로 진입 불가**. 라이브로 델타 출력 확인: schema/model_amplitude_tier(enum)/llm_critique_blocker_allowed(bool)/routes(target_role·writing_persona·fgp_route enum + `bounded_control`=FGP_ROUTE_RENDERERS 맵 상수)/posthoc_gate_order(enum). **자유 텍스트 0.** 이게 내가 권한 allowlist/recompute 원칙을 렌더 경계에 정확히 적용한 것.

라이브 거부 확인(전부 의도대로):
- `fgp_prompt = baseline + delta` recompute-`==` → 프롬프트에 prose 덧붙이면 `fgp_prompt_delta_drift` ✅
- baseline recompute-`==` → `fgp_prompt_baseline_drift` ✅
- route_config canonical(`raw != to_payload(validate(raw))`) → extra-key prose `fgp_prompt_route_not_canonical` ✅
- task-pair 포괄 비교(task_id·fgp_route_config 외 전 필드) → `fgp_prompt_task_mismatch` ✅
- draft overlap: exact-phrase `fgp_draft_forbidden_phrase_overlap` ✅, 8+단어 shingle ✅

---

## F1 (확정, major) — forbidden-phrase가 *delta*만 스캔, prose가 실제 들어가는 *instruction*은 안 봄

`check_prompt_boundary`의 forbidden-phrase 체크가 **`expected_delta`에만** 적용됨(186-187: `_count_forbidden_phrase_hits(expected_delta, ...)`). 그런데:
- **delta는 이미 enum-only** → forbidden phrase가 거기 들어갈 일이 없음 → 이 체크는 거의 redundant.
- **정작 prose가 들어갈 수 있는 곳 = `instruction`**(author 자유텍스트, render_baseline_prompt가 그대로 프롬프트에 박음, line 120). 이건 LLM이 실제로 보는 writer 프롬프트의 일부.
- **라이브 확인**: FGP 카드 문장을 instruction에 넣고(baseline·fgp 둘 다 동일), 그 문장을 `forbidden_fgp_phrases`로 줘도 → **`check_prompt_boundary` 통과(OK)**. baseline drift도 안 뜸(instruction은 "expected"라서).

즉 "writer 프롬프트에 raw FGP 금지"라는 이 경계의 목적에서, **실제 누수 표면(instruction 등 baseline 자유필드)을 가드가 안 봄.** delta-가드(핵심)는 건전하나, optional phrase-가드가 이미 안전한 표면을 겨누고 있음.

**Fix**: forbidden-phrase 스캔을 **전체 FGP 프롬프트(baseline+delta) 또는 최소한 instruction**에 적용. (target_journal 등 다른 baseline 자유필드도 같은 클래스 — 전체 프롬프트 스캔이 깔끔.)

---

## F2 (forward, 실 ablation accept 조건) — optional 가드를 mandatory로

`forbidden_fgp_phrases`와 `check_generated_draft_for_forbidden_overlap`는 **optional·분리**. 이 커밋은 LLM 안 부르니 지금은 OK. **하지만 진짜 prose ablation을 열 때**:
- 출력 draft가 생기면 **draft-overlap 체크 mandatory** + FGP 카드 코퍼스(로컬) 실제 공급.
- 프롬프트 phrase-스캔도 **전체 프롬프트에 mandatory**(F1).
- 이 둘이 안 걸리면, verbatim FGP echo의 유일한 구조적 backstop이 꺼진 채 ablation이 돎.

## F3 (calibration note, 버그 아님)
shingle backstop = **8+ 연속단어** verbatim(min_words 기본 8, 튜너블). 7단어 이하 verbatim 조각은 통과 — "verbatim/near-verbatim" backstop으론 합리적. semantic paraphrase는 못 잡음(Codex 명시, process/human 가드). 운영자가 민감도 알고 있을 것.

---

## Codex 7 break-it 항목 답
1 델타 prose → R1 REJECT ✅ / 2 route extra·dup·free-text → R3 REJECT ✅ / 3 baseline drift → R2 REJECT ✅ / 4 task mismatch → R4 REJECT ✅ / 5 **hidden/unpinned string channel → 찾음 = instruction(F1)** / 6 draft overlap exact+shingle → D1 ✅, 8+단어 동작 확인 / 7 너무 좁나? → 아니, 실 ablation 모양에 맞음(같은 task, FGP는 델타로). 단 F1·F2 보완 필요.

## 다음
F1 수정(phrase 스캔을 전체 프롬프트로) + F2를 실-ablation accept 조건으로 명문화 → 내가 재검증 → 그 다음 첫 real prose ablation. **지금 ablation 금지.** 지도 트랙 "prompt-boundary built, F1 수정 대기"로.

(read-only · manuscript-atelier push0 · 머지0 · raw FGP 커밋0. 라이브=로컬 `.scratch/bnd-gate/`.)
