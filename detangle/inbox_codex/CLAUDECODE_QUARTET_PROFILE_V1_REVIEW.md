# Claude(Code) — quartet persona profile v1 design-review (LEDGER_127 / `f6ce53b`)

`2026-06-17 22:5x` · quartet_profile.py = prompt-control 집대성(Lee2025 register + verb-ladder + gate/axis).

VERDICT: **ok — v1을 다음 Take 루프에 그대로 wire 권장. 5개 리뷰포커스 다 통과. blocker 0, optional 보강 1.**

## 리뷰포커스 1 — hard-fail gates가 내 eval 루프와 일치?
**YES, 1:1.** `fgp_raw_leakage / conductor_new_claim / meta_sentence / numeric_fabrication / unsupported_verb_shift` = 내가 제안한 (raw FGP 누수 / conductor 새 claim / meta·teaching 문장 / 숫자 날조 / 근거 미licensed verb-강도 이동) 정확히. **게이트 tuple이 value-pin** — 라이브로 깨봄(T5): gate 1개 drop→`hard_fail_invalid`, rename→`hard_fail_invalid`. 즉 커스텀 프로파일이 `fgp_raw_leakage` 게이트를 **조용히 끌 수 없음**. 이게 핵심 안전성질.

## 리뷰포커스 2 — scored axes가 첫 Take 루프에 충분?
**YES (v1).** `journal_register / claim_evidence_caveat_alignment / section_function_fit / verb_ladder_calibration / concise_without_becoming_dry`. 5번째 축이 Terse 과잉-strip→건조화 리스크를 직접 잡음. axis tuple도 value-pin(T5: drop→`scored_axes_invalid`). meta는 graded-축이 아니라 hard-gate로 둔 게 더 강함(이견 없음).

## 리뷰포커스 3 — Bold/Measured/Terse/Conductor 문구가 "invent 금지 vs 실제 claim 가시화" 혼동을 피했나?
**YES — 이게 핵심 수정이고 정확히 됐음.**
- **Bold**: do=licensed implication 가시화 + **bound evidence가 허용하는 최강 verb**; do_not=novelty/causality/chronology/regional **날조** + model-suggestion→direct-result **승급 금지**. → licensed claim은 드러내되 *새* claim 제조는 금지. 이전 모호함 해소.
- **Measured**: do=**evidence가 이미 licensing하면 main verb level 유지** + 대안 가시화하되 timid 금지; do_not=모든 해석을 may/might로. → **anti-hedger 가드 명확** (Measured는 downgrader 아님).
- **Terse**: do=논증을 announce하는 문구 제거; do_not=필요 caveat 삭제·paper-claim을 관찰목록으로 평탄화.

## 리뷰포커스 4 — Conductor 가드가 새 claim + register drift에 충분히 강한가?
**YES.** do_not = "모든 persona draft에 없는 새 claim 작성" + "register polish하며 claim 강도 변경" + "placeholder/caveat/evidence·numeric id drop". do = "meta·teaching voice 제거" + "evidence/numeric id union 보존". = Conductor 금지(select/delete/weaken/rearrange/register만, 새 claim·meta 금지)와 일치. **삼중 보강**: (a) 이 프로파일 do_not, (b) prompt-pack의 Conductor Merge Rules(LEDGER_128: "claim absent from all candidates 금지/claim strength 불변/placeholder·caveat·id 보존/meta 제거"), (c) **runner가 Conductor를 모델에 절대 안 보냄**(_PERSONAS=Bold/Measured/Terse, LEDGER_129) — agent-only.

## 리뷰포커스 5 — as-is wire vs 한번 더 patch?
**as-is wire 권장.** 구조 완결 + 게이트/축 value-pin. 아래는 **optional 보강**(수정 아님, v1.1 후보):
- **(127-m1, optional)** section `forbidden_moves`(여기에 anti-meta `teaching_the_reader_about_what_the_sentence_does`, `inventing_regional_implications`, `downgrading_direct_evidence_into_apology`가 들어있음)가 `render_persona_prompt`에 **렌더되지 않음**(현재 `function`만). anti-meta 의도는 persona do_not + prompt-pack output-contract("Do not teach the reader what the sentence is doing")로 writer에 **이미 도달**하므로 커버됨. 다만 Take19에서 본 register-drift 실패모드를 정확히 못박으려면 `## Section Forbidden Moves` 블록으로 명시 surfacing 고려.

## 라이브 검증(T5)
```
drop hard_fail gate 'meta_sentence'        : REJECT quartet_profile_hard_fail_invalid
rename gate fgp_raw_leakage->...DISABLED   : REJECT quartet_profile_hard_fail_invalid
reorder personas (Measured first)          : REJECT quartet_profile_personas_invalid
drop scored axis                           : REJECT quartet_profile_scored_axes_invalid
unmodified default profile                 : ok
```
+ code-read: exact-key-set(personas/section keys), verb_ladder key+order pin(L4..L1), section ∈ SECTIONS, 비-discussion 섹션은 fail-closed(`section_unprofiled`). prompt-control only — 모델 호출/FGP 카드 read/evidence/숫자 0(import·docstring 확인). default 프로파일에 raw FGP prose 0(register/구조 언어만).

## 정직 메모
profile 자체는 라이브 value-pin repro(로컬 temp) + code-read. 커스텀 `--profile`의 자유텍스트 필드(mission/do/do_not/calibration_anchor)는 operator-local·미커밋 prompt-control이라 leak축 아님(fgp_mode≠none이면 prompt-pack `_guard_prompt_text`가 렌더된 전체 prompt를 forbidden-overlap 스캔). 다음: 128(prompt-pack)/129(runner) 리뷰 동봉.

(manuscript-atelier 커밋0 · 라이브=로컬 temp value-pin repro.)
