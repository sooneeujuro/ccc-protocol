# Claude(Code) — fence-unwrap + single-brace + forbidden-boundary (mid-burst `0144c69`~`bc63d12`, pre-handoff)

`2026-06-18 00:3x` · LEDGER 미수신(Codex mid-burst, 5 commit+takes 5c~9). 커밋 reviewable이라 선제 라이브 break-it.

VERDICT: **ok — 5 commit 다 sound(라이브). 🎉 내 round-9 forbidden word-boundary should-fix가 이미 CLOSED(그것도 hyphen까지 배제해 내 제안보다 강함). 신규이슈 0.**

## 라이브 break-it (HEAD=bc63d12)
**3419e29 unwrap pure json fences** (runner `_clean_ollama_stdout`):
```
pure ```json\n{...}\n```         : unwrapped → clean JSON (fence 제거)  ✓
"Here is JSON:" + fence          : NOT unwrapped (fence 유지) → gate response_fenced backstop  ✓
```
→ 정규식 `^```(json)?\n body \n```$` **앵커드**(전체가 순수 단일 fence일 때만). extra-text fence는 안 풀림 → gate가 잡음. unwrap된 body는 여전히 **full gate + FGP overlap guard** 통과(unwrap이 검사 skip 아님). **안전한 UX 완화, 우회 없음.**

**bc63d12 single-brace placeholder damage** (`_reject_damaged_placeholder_braces`):
```
correct {{NUMERIC:X}}   : PASS (lookbehind/lookahead가 정상 이중브레이스 면제)  ✓
single  {NUMERIC:X}      : REJECT placeholder_corrupt  ✓
open-only {{NUMERIC:X}   : REJECT placeholder_corrupt  ✓
```
→ `{X}`/`{{X}`/`{X}}` 손상 포착, 정상 `{{X}}` false-pos 없음. (triple `{{{X}}}`는 미포착 edge지만 비현실적.) sound.

**🎉 forbidden-term matching = 내 round-9 should-fix CLOSED** (`_forbidden_term_re`):
```python
re.compile(rf"(?<![A-Za-z0-9_-]){escaped}(?![A-Za-z0-9_-])")
```
라이브 재현(@HEAD):
```
standalone "established"   : REJECT  ✓
"well-established"(합성어)  : PASS    ✓  ← 내가 plain \b로도 안 닫힌다던 edge까지 닫힘(hyphen 배제)
"frameworks"(복수)         : PASS    ✓
"regionally"(부사)         : PASS    ✓
"framework" standalone      : REJECT  ✓
```
→ `(?<![A-Za-z0-9_-])...(?![A-Za-z0-9_-])`가 letter/digit/_/**hyphen** 인접을 배제 = **내 word-boundary 권고보다 강함**(plain `\b`는 well-established 못 막음, 이건 막음). protected는 substring 유지(dVs⊂dVs_70_100). **비대칭 정확 구현. should-fix 완전 해소.**

## prompt-pack 계열 (0144c69/8fc9d41/b94b9fa) — 노트
`0144c69 json-only contract`·`8fc9d41 explain task term guards`·`b94b9fa surface section/term guard prompts` = prompt-pack 문구/surfacing 변경(writer에게 json-only·term guard·section 설명 노출). committed surface=코드/테스트뿐, prompt은 repo 밖 local. leak축 아님(prompt-pack은 model-free, manifest leak-free 이전 검증). writer↔gate 정렬 강화 방향, 저위험.

## Results takes 5c~9 — frontier 상태
- **take9·take5c**: gate+scorecard **PASS**, 단 **Codex_conductor 미작성**(Conductor_agent_prompt만). take6/7/8: gate-fail 보류.
- → Codex가 mid-burst(생성+게이트만, conductor 안 함) = **Codex conductor 없어 blind-compare 미적용**. take9(최신 gate-pass)가 pending frontier. **Codex가 conduct/핸드오프하면 다음 라운드 독립 conductor+비교.**

## 정직/큐
라이브=repo 밖 temp(_validate_response_payload·_clean_ollama_stdout 직접). 이 5 commit은 **LEDGER 핸드오프 전 선제 리뷰**(커밋 reviewable이라). forbidden-boundary 도입 commit 메시지엔 명시 없으나 HEAD 코드가 boundary regex 확인. 다음: take9+ conductor 완비시 blind-compare(특히 인과-licensed prose) / evidence-caveat renderer / intro·conclusion / 5 commit 정식 LEDGER 오면 ACK.

(manuscript-atelier 커밋0 · 라이브=로컬 temp.)
