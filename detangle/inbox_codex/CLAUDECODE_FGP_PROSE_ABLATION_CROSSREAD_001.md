# Claude(Code) — FGP prose ablation 교차-read (Claude run + Codex run)

`2026-06-17` · Claude run `…T105243Z`(intro) + Codex run `…T105027Z`(discussion)

두 독립 단일표본 교차 읽기. drafts/raw FGP = 로컬만, 미커밋. 이 노트는 합성 소견.

## 공통 (두 런 다)
- 파이프라인 실 FGP source 물고 end-to-end, **가드 전부 통과**(phrase corpus required·prompt boundary·전체-string overlap, 5251 phrase, 누수0).
- FGP-routed가 baseline보다 **약간 더 구조적/논문형**으로 읽힘(directional, dramatic 아님). 두 작성자가 독립적으로 같은 방향.

## 🎯 진짜 payoff = register drift 발견 (두 런·두 task·두 작성자에서 반복)
운영자가 Codex 출력에서 잡은 것: FGP-routed가 **"logic-coach/메타-코멘트 말투"**로 샘 — 논증을 *enact*하지 않고 *설명*함.
- Codex(discussion) 강한 사례: "The strongest discussion claim is also the narrowest one…", "the defensible sentence is therefore…", "Framed this way, the paragraph can…". = 논문 본문이 아니라 writer가 자기 논리구조를 해설.
- Claude(intro) **약한 사례지만 같은 모드**: "We frame this explicitly as a test of separability rather than a claim that it holds…" — "we frame this explicitly as"가 메타-플레이버.
- **핵심**: 같은 실패모드가 *두 작성자·두 섹션(intro/discussion)*에서 반복 → 한 사람 버릇이 아니라 **라우팅(structure_first/rubric/critique enum)이 '구조를 명시하라'고 밀면서 surface가 메타-해설로 기우는 체계적 효과.** FGP는 *논리 모양*을 잡아주지만 *도메인 register*는 안 눌러줌.

## ⚠️ 내 이전 주장 정정 (fake-green 자기점검)
직전에 "두 런 작성편향이 *반대 방향*이라 합치면 교락 일부 상쇄"라 했는데 **틀림.** Codex도 나도 *조건을 알면서* 둘 다 씀 → 작성편향은 **같은 방향**(둘 다 FGP를 더 잘 쓰려는 쪽). 두 런 합치기 = **작성자·task 넘은 replication**(효과가 우연만은 아닐 신호) ✅ 이지만 **de-confound는 아님.** 진짜 인과엔 여전히 condition-blind writer 또는 외부모델이 둘 다 작성 필요.

## 종합 (정직)
- **신뢰도 올라간 것**: 라우팅이 evidence-role 분리·반증가능 구조를 더 명시하게 만든다 — 2/2 replication.
- **여전히 미해결**: (a) 인과(작성편향 같은방향 잔존) (b) FGP 카드 *내용* 효과(설계상 raw 차단으로 미측정) (c) **register drift = 라우팅의 새 부작용.**

## 다음 개선점 (운영자+Codex와 수렴)
FGP가 *구조*는 잡았으나 surface가 "논리 코치"여서 도메인 논문 register로 다시 눌러야 함. 후보:
1. **register gate**(post-hoc): "the X should…", "the defensible sentence is…", "framed this way…", "we frame this explicitly as…" 류 메타-해설 문장을 플래그/리라이트. asymmetric_fgp_routing의 prose_vocab_gate를 메타-코멘트까지 확장.
2. **FGP-as-Critique 안전변형**: 카드가 구조/critique를 inform하되 최종 surface는 도메인 register로 강제(메타-해설 금지 규칙 포함).
3. de-confound 런: condition-blind writer 또는 외부 모델 1개가 baseline·FGP 둘 다 작성.

(read-only 합성 · drafts/FGP 미커밋 · 로컬 보고서 각 런 폴더.)
