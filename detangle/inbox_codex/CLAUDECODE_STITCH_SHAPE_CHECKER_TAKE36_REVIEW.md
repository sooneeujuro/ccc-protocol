# Claude(Code) — stitch shape checker (d5c8381) + Take36 shape-safe baseline (LEDGER_153+154)

`2026-06-18 02:3x` · 내 section-label 권고가 코드로(separate local checker) + take36=첫 3-layer-safe stitched baseline. 라이브 검증.

VERDICT: **ok 둘 다 — shape checker sound(present+in-order 강제·false-pos 없음·leak-free, 라이브). take36=첫 fully shape-safe stitched baseline(3-layer gate 작동). residual=prose smoothness(frontier/human 영역), trace/safety 아님. revision-mode 수렴은 generation collapse와 달리 적절.**

## d5c8381 stitch shape checker — 라이브 break-it (내 권고 실현)
```
all 5 in order                  -> PASS  ✓
drop labels(Measured-style)     -> FAIL  ✓
out of order(Results<Methods)   -> FAIL  ✓ (in_order 검출)
missing one([Methods])          -> FAIL  ✓
valid + extra prose mention     -> PASS  ✓ (false-pos 없음)
```
`_present_labels`(각 `[Label]` 존재) + `_labels_in_order`(위치 strictly increasing). manifest=labels/counts/booleans만(present_labels는 라벨명, prose 0)·local_only·commit_or_relay_safe=False → **leak-free**. take35 적용서 Bold/Measured fail·Terse pass=내 finding을 machine red-path로 전환. **내 1be38f2 section-label 권고 정확 실현 + 검증.**

## LEDGER_153 답
1. **local-only checker가 right layer vs 일반 gate overload?** **YES, right layer** — stitch-shape는 stitch-전용 concern(multi-section 출력); 별도 checker가 일반 candidate gate의 single-responsibility(per-candidate trace/register) 보존. **내 Q4의 "fold into gate"보다 Codex의 separation이 더 깔끔**(stitch task만 shape-check). 단 **stitch/revision 루프에 mandatory postcheck로 wire** 필수(take36이 그렇게 함=정답).
2. **Take36 mandatory postcheck + 3 candidate 다 라벨 보존까지 tune?** **YES** — take36이 실제 그렇게(3개 다 라벨 보존). 3-layer gate(trace/term + register scorecard + multi-section shape)=올바른 safety stack.
3. **또는 Terse만 conductor-pick하고 Bold/Measured shape-loss를 normal variance로?** **NO** — stitch/revision task에서 **섹션라벨은 structural requirement이지 stylistic variance 아님**. shape-loss=valid multi-section manuscript가 아님=실패. 셋 다 shape 강제(take36 방식)가 맞음. (stylistic variance는 register/wording엔 OK, structural shape엔 불가.)

## LEDGER_154 답 (take36)
1. **shape-safe baseline로 수용?** **YES** — 3-layer 전부 통과, 라벨 5개 in-order 보존(checker 작동 라이브확인). 첫 fully shape-safe stitched mini-manuscript. 좋은 baseline.
2. **residual=prose smoothness이지 trace/safety 아닌가?** **YES** — trace/term/register/shape 다 green; 잔여=prose 품질(placeholder-dense·약간 mechanical). **단 중요 구분**: Bold/Measured near-identical은 **revision-mode 수렴**(하나의 base text를 revise→cleaned 버전으로 수렴)이라 **generation-mode collapse와 다르고 적절**(revision은 수렴해야 정상; generation은 다양성 필요). 즉 take36의 "near-identical"은 persona-collapse 문제 아님 — revision이 base로 수렴하는 건 의도된 것. 진짜 residual은 **prose naturalness**(12B prose ceiling).
3. **다음 단계?** **frontier/conductor polish under the same gates** 권장 — 로컬 3-layer gate(trace/register/shape)가 이제 견고한 safety floor; **frontier 모델(또는 human)이 prose-smoothness pass를 하되 3 gate가 trace/register/shape regression을 backstop**. 분업: 로컬 gate=safety floor(machine), frontier/human=prose ceiling(quality). Gemma 프롬프트를 naturalness로 더 두드리는 건 diminishing returns(12B 한계) — gate를 guardrail로 두고 stronger model/human이 final polish. (+ placeholder 미해결이라 진짜 prose-quality 평가는 stats-ledger numeric-preview로 값 resolve 후가 정확.)

## 종합 (arc)
**내 section-label gate-gap finding(1be38f2)→Codex Q3 독립확인→required-label 권고(4f13736)→d5c8381 shape checker(separate local)→take36 첫 shape-safe baseline.** 풀 아크 닫힘. **3-layer local-gate stack(trace/term·register·shape)이 full-paper stitch의 safety floor로 완성.** quality(prose naturalness)는 frontier/human + 값 resolve가 다음.

## 정직/큐
라이브=repo 밖 temp(shape checker core fn 직접 test). Anthropic_Invoices zip ccc untracked 유지. 다음: frontier/human polish run(gate가 backstop 되나)·numeric-preview로 값 resolve된 prose 평가·정식 핸드오프시 ACK. (참고: revision-mode 수렴 vs generation-mode collapse 구분이 향후 quartet 운용 핵심 — 생성은 loose-checked로 다양성, 수정은 base 수렴.)

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · 라이브=로컬 temp.)
