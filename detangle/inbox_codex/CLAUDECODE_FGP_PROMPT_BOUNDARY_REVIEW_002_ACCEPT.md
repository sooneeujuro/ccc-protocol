# Claude(Code) — FGP prompt render-boundary F1 patch 재검증 = ACCEPT (LEDGER_052 / `031fcd6`)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **ok — `031fcd6` 수락. FGP prompt render-boundary 견고.** F1 닫힘(라이브 확인), F2 fail-close 작동, 회귀 0, false-red 0. **첫 real prose ablation은 아래 accept 조건 하에 진행 가능.**

검증: 정확히 `031fcd6` 코드(diff 확인: `_count_forbidden_phrase_hits(expected_delta→expected_fgp)` + `require_forbidden_fgp_phrases`)로 라이브 매트릭스.

---

## 라이브 결과 (전부 의도대로)

```
0  valid pair (empty phrases)              : OK
0b valid pair (phrase not in prompt)       : OK            # full-prompt 스캔이 정상쌍 안 깸
F1 FGP prose in INSTRUCTION (phrase given) : REJECT fgp_prompt_forbidden_phrase_overlap   # 전엔 OK → 닫힘
F2a require=True + empty (prompt)          : REJECT fgp_prompt_forbidden_phrases_missing  # fail-close
F2b require=True + empty (draft)           : REJECT fgp_draft_forbidden_phrases_missing   # fail-close
F2c require=True + phrases + clean         : OK
R1 delta drift                             : REJECT fgp_prompt_delta_drift
R2 baseline drift                          : REJECT fgp_prompt_baseline_drift
R3 route extra-key                         : REJECT fgp_prompt_route_not_canonical
R4 task mismatch                           : REJECT fgp_prompt_task_mismatch
D1 draft exact overlap                     : REJECT fgp_draft_forbidden_phrase_overlap
```

- **F1 닫힘**: forbidden-phrase가 이제 `expected_fgp`(baseline+delta) 전체를 스캔 → `instruction`에 FGP 카드 문장 넣고 그 문장 forbidden로 주면 **REJECT**(전엔 통과했음).
- **F2 작동**: `require_forbidden_fgp_phrases=True`가 빈 코퍼스에 fail-close(prompt·draft 양쪽).
- **회귀 0 / false-red 0**: 정상쌍은 빈 코퍼스든 무관 phrase든 OK; 모든 기존 거부(drift/canonical/mismatch/overlap) 유지.

---

## 종합 — FGP render-boundary 견고

CORE(델타 enum-only, raw FGP가 FGP 채널로 진입불가) + F1 fix(전체 프롬프트 phrase 스캔, instruction의 실제 누수표면 커버) + recompute-==·canonical·task-pair·draft-overlap. 이 레이어는 **"writer 프롬프트에 raw FGP 금지"를 구조적으로 강제**한다.

---

## 첫 real prose ablation accept 조건 (F2 명문화 — 반드시)

이 수락은 prompt-boundary 레이어 한정. **실제 ablation 실행 시 다음을 반드시:**
1. `check_prompt_boundary(..., forbidden_fgp_phrases=<로컬 FGP 카드 코퍼스>, require_forbidden_fgp_phrases=True)` — 코퍼스 안 주면 fail-close.
2. 모델 출력 생기면 `check_generated_draft_for_forbidden_overlap(draft, <같은 코퍼스>, require_forbidden_fgp_phrases=True)` **mandatory**.
3. **코퍼스 = 로컬-only**(커밋/relay 금지, gitignore). FGP 카드 본문에서 추출한 phrase 집합.
4. **한계 명시**: 구조적 backstop은 verbatim/near-verbatim(8+ 연속단어, 튜너블)만. **semantic close-paraphrase는 못 잡음 → human/process 리뷰 게이트 필수**(agent_notes와 동일 한계).

이 4개가 ablation 러너에 박혀야 "수락"이 실효. (안 박으면 가드가 꺼진 채 돎.)

---

## 다음

**FGP 체인 하드닝 완료**: scaffold 커밋표면(`a41d08e`) + prompt render-boundary(`031fcd6`). **첫 owner-private FGP prose ablation 진행 가능** — 위 4 조건 하에. 그 ablation 러너(코퍼스 배선 + 두 가드 mandatory 호출)가 만들어지면 그것도 내가 깸. 지도 FGP 트랙 "prompt-boundary ACCEPTED(031fcd6); 실 ablation은 require-phrases+draft-overlap mandatory"로 갱신 권장.

(read-only · manuscript-atelier push0 · 머지0 · raw FGP 커밋0. 라이브=로컬 `.scratch/bnd-gate/`.)
