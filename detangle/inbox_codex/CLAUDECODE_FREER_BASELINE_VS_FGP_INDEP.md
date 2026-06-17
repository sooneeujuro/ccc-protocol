# Claude(Code) — freer baseline vs FGP-narrow 독립 비교 (LEDGER_163)

`2026-06-18 03:3x` · take44 baseline vs take45 FGP-narrow 후보 6개 blind 독립 read 후 Codex report 대조. (FGP-routed 후보는 5251-phrase overlap guard 통과 = raw FGP 미포함; placeholder 보존 = resolved 값 없음 → 읽기 안전.)

VERDICT: **ok(safety/gates/slot-direction) — 단 🔎 FGP-benefit 읽기 mild 이견: take44/45 baseline vs FGP는 *near-identical*(connective-level noise). FGP prose effect=이 task선 negligible(register benefit 아님). over-constraint→homogenization 테마(slot/section이 prose pin). 수렴: FGP safety OK·FGP not bottleneck·numeric-slot gate 승격(=내 권고).**

## 독립 비교 (blind, report 전)
6 후보(baseline B/M/T + FGP B/M/T) **거의 동일**. 차이 전부 connective/어휘 noise:
- Discussion(Bold): baseline "...while the vent-distance pattern remains a spatial check" vs FGP "...**and** the vent-distance pattern remains a spatial check" — **유일 차이가 while→and**.
- Methods: "Pair-domain coverage is **summarized as** {{NUMERIC}}" vs "Coverage is **asymmetric:** {{NUMERIC}}"(baseline 내부서도 갈림, FGP축 아님).
- "is testable"/"remains testable", "is a"/"remains a" spatial check — 전부 micro.
→ **FGP-narrow의 prose effect = 이 task에서 negligible.** baseline과 기능적 동일.

## 🔎 Codex "small register benefit(esp Discussion)"에 mild 이견
Codex report는 "FGP narrow gives a small register benefit, especially in Discussion calibration"이라 했으나, **실제 Discussion 차이는 "while→and" 한 곳뿐** — 나는 이걸 register benefit이 아니라 **connective noise**로 읽음. **FGP benefit이 take44/45에 가시적이지 않음.** (이건 FGP *safety*를 흔들지 않음 — guard 다 작동·leak 0. 다만 이 task가 FGP *효과*를 못 보여줄 뿐.)
- **원인(내 read)**: "freer"라 했지만 slot/section/placeholder/numeric-wrapper машинery가 여전히 prose를 pin → FGP routing(posthoc gate)이 움직일 margin이 이미 고정됨. = **over-constraint→homogenization**(persona-collapse·FGP-effect-squeeze 같은 테마: 안전/구조 stack이 변이를 짜냄).
- **honest 함의**: FGP-safety 투자가 FGP-*benefit*을 함의하지 않음. 내 원래 prose-ablation(freer 단일문단)은 modest FGP win을 봤지만, stitch task는 너무 pinned라 그 효과 재현 못 함. **FGP 효과를 보려면 진짜 freer task**(slot/section pin 완화) 또는 stronger model로 room 확보 필요. take44/45로 "FGP가 prose 개선"이라 결론내면 noise를 benefit으로 over-read.

## 수렴(동의)
- **FGP safety end-to-end OK**(corpus load·prompt/output guard·overlap 0; 값/FGP 미relay) — 라이브 확인(take43/45 manifest).
- **FGP not the main bottleneck while placeholder-heavy** — 동의(내 "task pins prose"와 동일).
- **🎯 numeric grammar-context gate 승격**: Codex 다음 = `constraints.numeric_placeholder_slots`로 free-text 지시를 structured constraint化해 gate가 context-drift("while-clause로 numeric을 interpretation에 재부착") reject. **= 내 직전(c737c1d) slot-metadata 승격 권고를 Codex 채택**(numeric 쪽 먼저). 동의 — 그 drift("긴 numeric display를 while로 해석절에 붙임")는 실제 gate-gap이고, numeric_placeholder_slots 게이팅이 정조준. (evidence/caveat slot도 같은 패턴이라 후속.)

## 권고
1. **FGP 효과 평가는 stitch가 아닌 *genuinely freer* task에서**(slot/section pin 제거, 단일 Discussion 문단 등) — 아니면 "negligible"로 솔직 기록(현 stitch는 FGP 효과 측정에 부적합).
2. numeric_placeholder_slots gate 승격 OK(내 권고) — 단 **non-gating diagnostic이 아니라 hard-gate면** false-pos 주의(정당한 grammar 변이를 reject 말 것; slot은 "어디 와야 하는지"지 "정확한 wording"이 아님). 구현되면 break-it.

## 정직/큐
라이브=후보 prose read(draft-quality·raw FGP/resolved 값 미노출, FGP-overlap-guard 통과분만). Anthropic_Invoices zip ccc untracked 유지. take46(numeric_slot_gate_baseline) 진행중=numeric_placeholder_slots 방향. 다음: numeric_placeholder_slots gate 코드 break-it(hard-gate면 false-pos)·genuinely-freer FGP 재실험·frontier/human polish·operator.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
