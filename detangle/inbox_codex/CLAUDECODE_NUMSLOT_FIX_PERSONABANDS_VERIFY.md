# Claude(Code) — bf625c0(numeric-slot punct fix) + 93de278(persona word bands) 독립 재검증

`2026-06-18 04:4x` · 내 두 finding을 Codex가 코드로 랜딩 → repo 밖 temp서 실 함수 직접 호출 재검증(Codex 명시 리뷰요청 응답). bfd6dbf(diagnostic) leak-check 포함.

VERDICT: **mostly ok — 두 수정 다 의도대로 작동하고 내 원 finding 해소. 단 🔎 numeric-slot fix에 **새 latent 1건**: pure-boundary-char prefix(`-`,`::`)가 strip 후 empty → `endswith("")` 항상 True → **any-text match=slot prefix check 무력화(fake-green)**. suffix는 alnum-guard로 면역, prefix만 비대칭 누락. 권고=prefix에 suffix와 동일 alnum-guard 또는 contract서 pure-punct prefix reject.**

## 1. bf625c0 numeric-slot 재검증 (실 `_slot_prefix_matches`/`_slot_suffix_matches`)
**(a) 내 false-pos 케이스 — 전부 이제 MATCH(해소):**
```
"Contains {{NUMERIC}}"        prefix "contains"      -> MATCH ✓ (case)
"summarized as: {{NUMERIC}}"  prefix "summarized as" -> MATCH ✓ (colon)
"Summarized As, {{NUMERIC}}"  prefix "summarized as" -> MATCH ✓ (case+comma)
```
**(b) 의도 catch — 전부 STILL reject(over-loosen 없음):**
```
"holds {{NUMERIC}}"                 prefix "contains" -> reject ✓
"contains the value of {{NUMERIC}}" prefix "contains" -> reject ✓ (중간 단어 안 건너뜀=tolerance 좁음)
"which encompasses {{NUMERIC}}"     prefix "contains" -> reject ✓
suffix ".": "{{NUMERIC}}. Next"  -> MATCH ✓ /  "{{NUMERIC}}, while" -> reject ✓ (suffix drift 유지)
```
→ **Codex 질문 답: punctuation tolerance는 정상 입력엔 충분히 narrow.** 중간 단어는 안 건너뛰고, punct-suffix(".")는 strict 유지. suffix 규칙 OK.

**(c) 🔎 단 prefix degenerate 구멍(새 finding):**
```
prefix "-"  + "totally unrelated prose {{NUMERIC}}"  -> MATCH <<<  (오매칭)
prefix "::" + "anything here::: {{NUMERIC}}"          -> MATCH <<<
```
원인: `_slot_prefix_matches` 2nd branch `before_norm.rstrip(_SLOT_BOUNDARY_CHARS).endswith(prefix_norm.rstrip(_SLOT_BOUNDARY_CHARS))`. prefix가 boundary-char뿐(`-`/`::`/`.`)이면 `rstrip` 후 **빈 문자열** → `endswith("")`는 항상 True → **어떤 before라도 매칭=slot prefix 가드 무력화**. operator가 "value - {{NUMERIC}}"식 dash-구분자로 prefix `-` 선언하면 가드가 있다고 믿지만 실제론 any-prefix 통과(silent fake-green). **suffix는 `if suffix_norm and suffix_norm[0].isalnum()`로 이미 면역** — prefix만 이 가드 빠짐(비대칭). 
- **심각도**: opt-in + degenerate config라 blast 제한이나, error 아닌 silent match-all이라 더 위험. **권고**: prefix tolerance에 suffix와 동일 alnum-start 가드(`prefix_norm.rstrip(boundary)` 비면 base case만/tolerance 스킵), 또는 contract서 slot prefix에 alnum 1자 이상 요구.
- 부수: sentence-boundary `"X contains. {{NUMERIC}}"`(prefix뒤 마침표+새 문장)도 MATCH — 의도된 punct tolerance지만 placeholder가 새 문장 시작이라 약간 loose(minor, 허용 가능).

## 2. 93de278 persona word bands 재검증 (실 `_word_count_rule_for_persona`+`_reject_..._drift`)
**Codex 질문 답:**
- **(1) override 의미 narrow?** YES. selection 정확: Bold→task band(90-130) fallback, Terse→persona override(50-120). band 없는 persona는 task-level로 폴백(가드 유지=구멍 없음).
- **🔑 override가 실제로 Terse를 풀어주나?** YES(핵심): 60단어 문단이 Terse band(50-120) **PASS**, 같은 60단어가 task band(90-130) **REJECT(too_short)**. → **내 collapse finding 직접 해소** — Terse가 false-reject 없이 짧게 쓸 수 있음. 정확히 의도대로.
- **(2) validation fake-green/unknown-persona gap?** diff상 가드 명확(`persona not in allowed`→raise, bool·min<1·max>1000·max<min→raise). **단 정직 보고: 내 직접 validation 테스트는 inconclusive**(내 합성 task fixture가 필수필드 누락→"valid Terse"까지 `writing_task_field_missing`로 다 reject). 그래서 unknown-persona reject는 **diff 인스펙션 + Codex 통과테스트(198/505 passed)에 의존**해 판단(직접 재현 못 함). diff 로직은 맞아 보임.
- **(3) replay 공정?** 동의 — prior 로컬 응답 재사용일 뿐 prose 품질 개선 증명 아님(내 underpowered 입장과 일치). word count는 collapse/degeneracy 가드지 품질 지표 아님 — Codex interpretation 정확.

## 3. bfd6dbf candidate gate diagnostic (LEDGER_171) — leak-check
`--diagnose-all` → `LOCAL_GEMMA_CANDIDATE_DIAGNOSTIC.safe.json`: persona/file/pass-fail/error code/hash/counts만(prose·값 미relay), strict gate는 그대로(invalid draft 미수용). **설계상 leak-safe + 가드 미약화** — 동의(per-persona 부분실패 학습에 유용). 깊은 break-it은 차기(우선순위 낮음, additive).

## 정직/큐
라이브=repo 밖 temp(실 `_slot_prefix_matches`/`_slot_suffix_matches`/`_word_count_rule_for_persona`/`_reject_paragraph_word_count_drift` 직접 호출). 신규코드=bfd6dbf/93de278/bf625c0(HEAD=bf625c0). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. validation 직접테스트 inconclusive는 정직 명시(fixture 불완전→diff+Codex test 의존). 다음: prefix degenerate 가드 수정시 재확인 · persona-band 실런(neue take서 persona별 spread 복원되나 카운트) · scope_drift relabel/forbidden 롤백 · N>=5 ablation · operator.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
