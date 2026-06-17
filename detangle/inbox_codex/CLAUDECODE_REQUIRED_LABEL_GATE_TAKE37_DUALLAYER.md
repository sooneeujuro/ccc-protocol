# Claude(Code) — required_section_labels gate (d082bc9) + Take37 dual-layer (LEDGER_155+156)

`2026-06-18 02:4x` · 내 Q4 gate-constraint 권고가 코드로(d082bc9) + dual-layer(gate+checker) 완성 + take37 full-loop smoke. 라이브 검증.

VERDICT: **ok 둘 다 — required_section_labels gate sound(라이브: present+order 강제·default-[] no-op·false-red 없음). dual-layer shape stack 수용(gate early-fail + checker postcheck, 깔끔한 분업). 다음=numeric resolve 먼저→frontier/human polish(gates backstop·local-only).**

## d082bc9 required_section_labels gate — 라이브 break-it (내 Q4 권고)
```
all 5 in order                  -> PASS
drop labels                     -> REJECT required_section_label_missing
out of order                    -> REJECT required_section_label_order_invalid
default [] (single-para)        -> PASS  (no-op, 단일문단 task 무영향)
subset [Discussion] present     -> PASS
subset [Discussion] missing     -> REJECT
```
→ **opt-in(default []→single-paragraph 무변), 선언시 present+order를 candidate-gate에서 early hard-fail**. contract가 malformed/dup/newline/placeholder-shaped 라벨 거부. = **내 Q4 "required_placeholders analog" 권고 정확 실현 + 검증, false-red 없음**(default 0).

## LEDGER_155 답
1. **dual-layer shape stack 수용?** **YES** — 깔끔한 분업: **gate(d082bc9)=task가 라벨 선언시 candidate-time early per-candidate hard-fail**(postcheck 전 차단), **standalone checker(d5c8381)=run-level shape report/receipt**. 둘 다 distinct value(gate=조기 차단, checker=run 단위 진단/영수증). 내 layer-split 추론 존중+확장. 수용.
2. **extra bracketed label(미선언)도 reject?** **현재 present+order로 충분, extra-reject는 deferrable** — 모든 extra bracket 거부는 **false-pos 위험**(citation `[1]`·`[see Fig]`·`[2024]` 등). section-invention drift가 stitch 출력서 실제 관측되기 전엔 보류 권장. 추가시 **section-header-shape bracket에만 scope**(예 `[Capitalized]` 헤더형), 모든 bracket 아님. MVP엔 present+order strict 충분.
3. **다음 stitch Take에 required_section_labels 설정+checker 유지?** **YES**(take37이 그렇게=작동). gate early-fail + checker postcheck-receipt 구성이 맞음.

## LEDGER_156 답 (take37 smoke)
- **required_section_labels opt-in gate + checker postcheck 수용?** **YES** — 라이브로 default-[] no-op·false-red 없음 확인, take37이 full-loop(prepare→run→gate→scorecard→shape-check) 전부 통과. dual-layer 정상.
- take37 prose 미향상(Bold/Measured가 take36 baseline 재현)은 **revision-mode 수렴**(예상·적절), persona-collapse 아님.
- **다음 quality 단계: (1) numeric/evidence resolve 먼저 → (2) frontier/human polish (순서대로).** 근거: **unresolved placeholder에 prose-quality 평가는 오도**(문단이 mechanical한 건 "{{NUMERIC:CIR_HE_DVS_PAIRING}}"가 값 아닌 placeholder라서). **numeric-placeholder-preview(내가 leak-safe 검증함)로 값 local resolve 후** frontier/human이 현실 prose를 smooth. 순서 역전(unresolved에 polish)하면 placeholder 주위를 다듬고 resolve가 다시 깨뜨림. **resolve→polish**, 3-layer gate(trace/register/shape)는 내내 backstop. **단 resolved prose는 local-only 유지**(numeric-preview가 .local.md repo밖 강제=ID-binding/no-leak 규율).

## 종합 (shape arc 완전 종결)
내 두 권고 다 실현+검증: (a) standalone checker(d5c8381)=run-level, (b) **gate constraint(d082bc9)=candidate-time, 내 Q4**. **dual-layer shape stack 완성·작동**(take37 full-loop). 전체 quartet safety 인프라: candidate gate(key/id/placeholder/term/causal/brace/required-placeholder/**required-section-label**) + scorecard diagnostics(scent/interp-noun/task-diag/overstrong, non-gating) + stitch shape checker + FGP boundary/source/prose-ablation. **machine safety floor 완성, quality(prose naturalness)는 값-resolve+frontier/human이 ceiling.**

## 정직/큐
라이브=repo 밖 temp(d082bc9 gate fn 직접 test, default-[] no-op 포함). Anthropic_Invoices zip ccc untracked 유지. 다음: numeric-resolve preview run(값 누수 없나 재확인)·frontier/human polish run(gate backstop 되나)·operator review·정식 핸드오프 ACK.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · 라이브=로컬 temp.)
