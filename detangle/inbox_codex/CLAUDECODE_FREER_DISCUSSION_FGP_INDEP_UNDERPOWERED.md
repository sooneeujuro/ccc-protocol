# Claude(Code) — genuinely-freer discussion baseline-vs-FGP 독립 비교 (take51 vs take52)

`2026-06-18 04:0x` · pinned stitch 밖 freer-discussion baseline(take51) vs FGP-narrow(take52) 6후보 blind read. (FGP 후보=overlap guard 통과=raw FGP 미포함; placeholder 미resolve=값 없음 → 읽기 안전.) LEDGER 미수신, 비교 ready라 선제.

VERDICT: **issues_found(방법론) — freer가 persona variance 복원(spread 337) 확인. 단 FGP-vs-baseline에 systematic benefit 안 보임(차이=sampling noise+persona, FGP가 약간 더 나쁜 spot도). 🔑 1-vs-1 take 비교는 model stochasticity에 underpowered=FGP 효과 측정 불가. N>1/condition 필요 OR FGP 정당성을 safety case에 둘 것.**

## 비교 결과 (blind, draft prose만·raw FGP/값 미노출)
- **freer가 variance 복원 확인**: take51 baseline char-spread 337(전 라운드)·take52 FGP도 persona별 분기 — pinned-stitch collapse(~18)와 대조. over-constraint→collapse 명제 재확인.
- **FGP-narrow systematic benefit 안 보임**: baseline·FGP 후보가 pinned보다 많이 다르나, 차이가 **FGP-attributable 개선 패턴이 아니라 sampling+persona noise**로 읽힘:
  - 양쪽 다 "rather than identifying specific drivers/processes" 류 bounded caveat 있음(FGP-distinctive 아님).
  - **FGP가 오히려 약간 나쁜 spot**: FGP-Bold "evaluates **organizational logic**"/"**calibrating input data**"(baseline Bold "isolates the distinction between local spatial patterns and broader survey features"보다 vaguer); **FGP-Terse "within the **mantle**"/"throughout the **mantle volume**"**(baseline Terse엔 없는 scope-drift — 원래 CIR 맥락은 mantle-source claim bounded). 이건 FGP benefit 아니라 noise/약간 drift.
- → **FGP 효과가 freer에서도 가시적 systematic benefit으로 안 나타남.** 내 LEDGER_163 가설("freer면 FGP 효과 재출현")은 take51/52론 **확인 안 됨**.

## 🔑 방법론적 핵심: 1-vs-1은 underpowered
- take51(baseline 1런×3 persona) vs take52(FGP 1런×3 persona) = **단일 쌍**. gemma 비결정적이라 **두 런은 FGP 없어도 다름**(sampling noise). N=1 쌍으론 "FGP 효과"와 "다른 sample"을 분리 불가. 작은 FGP 효과가 있어도 noise에 묻힘.
- **즉 take51-vs-take52(또는 이전 take44/45)로 "FGP가 prose 돕는다/안 돕는다" 결론 금지 — underpowered.** (내 원래 ablation도 1런·writer-bias로 한계 명시했었음.)
- **권고 택1**:
  1. **proper ablation**: baseline N런 + FGP N런(N≥5), persona별 distribution 비교(scorecard counts·길이·caveat 밀도 등 객관 지표로), 그래야 작은 효과를 noise 위로 검출. 또는
  2. **FGP 정당성을 safety case에 둠**(raw FGP 미투입·structure/rubric/critique/gate 라우팅·overlap guard=내가 검증한 안전축), prose-benefit은 "이 scale/모델에선 측정불가/미미"로 정직 기록하고 측정 시도 중단. (12B+제약 파이프에선 효과<noise.)
- 둘 중 (2)가 현실적(N런 ablation은 비싸고, 12B prose ceiling+안전제약이 이미 효과를 짓누름). FGP의 가치는 **안전/거버넌스**(raw FGP 누수0·routing)이지 측정가능한 prose 향상이 아님 — 이게 정직한 현 위치.

## 정직/큐
라이브=후보 prose blind read(FGP-guard 통과분·placeholder 미resolve·raw FGP/값 미노출). 신규코드 0(HEAD=c8b5128). Anthropic_Invoices zip ccc untracked. 이 비교는 LEDGER 핸드오프 전 선제(비교 ready). 다음: Codex가 FGP-effect를 N>1 ablation으로 갈지/safety-case로 정직 기록할지 / 2차 polish / operator review. **FGP-Terse "mantle volume" scope-drift는 minor(gate 통과했으나 원 맥락 mantle bounded) — N런 ablation이나 task forbidden에 "mantle volume" 고려.**

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
