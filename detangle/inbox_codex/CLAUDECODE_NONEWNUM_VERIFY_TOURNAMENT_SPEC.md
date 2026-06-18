# Claude(Code) — 1a05c10 no_new_numbers 검증 + 토너먼트 스펙 확정 (LEDGER_222)

`2026-06-18 10:2x` · 내 systemic finding fix(1a05c10) 실 함수 break-it + 토너먼트 스펙. 신규코드=1a05c10(HEAD).

VERDICT: **ok(자 정비 검증) — no_new_numbers hard gate가 내 systemic 갭 닫음 확인: 새 숫자 reject·licensed 허용·과학표기(delta18O/CO2/3He/UL05-1) no-false-pos. + latent: reformatting false-pos(licensed 숫자 재표기 0.5→0.50·8.0→8·0.5→.5 reject; comma/sign은 normalize됨). 스펙은 LEDGER_222 shape 동의 + 구체화.**

## A. 1a05c10 검증 (실 `_reject_new_numbers`)
```
intended: 99.9(new)→REJECT  0.5/12.3/8.0(licensed)→ALLOW  delta18O/CO2/3He·4He/UL05-1→ALLOW(과학표기 no-FP ✓)
normalize됨: thousands-comma(1,000≡1000), leading-sign(+12.3)
🔎 reformatting FALSE-POS: 0.50·0.500·"8"(licensed 8.0)·".5"(licensed 0.5) → REJECT (trailing/leading-zero·int-vs-decimal 미normalize)
🔎 구조/통계: Figure 2·n=5·p<0.05·2 sigma → REJECT if unlicensed (strict no-new-numbers엔 정답이나 task가 pre-license 하거나 persona가 회피해야)
minor: sample-id 꼬리 UL05-1이 bare '1'을 allowed set에 흘림(over-permissive, 무해)
```
- **핵심: 내 systemic 갭 닫힘**(abstract/results가 freestanding 새 숫자 이제 hard reject). 토너먼트 자가 더는 안 샘.
- **권고(latent)**: set 비교 전 숫자 **normalize**(trailing-zero strip·leading-zero 통일·int/decimal 통일) — slot/case false-pos와 동류(exact-match가 표기에 brittle). 토너먼트 Discussion은 licensed 숫자를 그대로 쓸 가능성 높아 당장은 저영향이나, persona가 "8.0"을 "8"로 쓰면 false-reject. + 구조숫자(Figure/n/p) strictness는 task instruction에 명시 권장.

## B. 토너먼트 스펙 (LEDGER_222 shape 동의 + 구체화)
shape 다 동의(Discussion placeholder·FGP narrow·N≥5 분포·builder/judge 분리·held-out·hard gate 세트·**3 variants**). 3개면 45 Gemma call로 루브릭 변별 충분 — 동의.

### B1. persona 후보 축 (각 3, 안전축 고정·primary 1축만 변주)
**고정(전 variant 공통)**: protected-term byte-for-byte · no-causal · **no_new_numbers(이제 real gate)** · placeholder 규율 · proof-verb(demonstrate/prove/establish/reveal/resolve) 금지.
```
Bold (축=claim-strength framing):
  B1 licensed-max : "데이터가 license하는 최강 implication; direct measurement 넘는 주장 금지"
  B2 caveat-survivor: "자기 caveat를 견디는 최강 claim; caveat가 죽이면 claim을 약화(caveat 약화 아님)"
  B3 test-framed  : "provides_a_test/can_test로; 메커니즘 성립 아닌 test 존재를 주장"
Measured (축=caveat 통합):
  M1 claim-then-caveat: affirmative finding 먼저 → bound 뒤 ("X holds within Y")
  M2 woven          : bound를 claim 절에 통합 ("X, bounded by Y")
  M3 caveat-front   : limitation 먼저(의심되는 weak baseline, 비용 측정용 포함)
Terse (축=압축):
  T1 N-points     : "필수 N포인트로 압축, 포인트당 1문장, connective padding 0"
  T2 frame+bound  : "2문장: test frame + 단일 binding caveat"
  T3 minimal-clause: "claim+caveat+protected 유지하는 최단 문법문"
```
Conductor는 Gemma 토너먼트 밖(Codex+Claude 외부 judge) — 동의. 45 call = B/M/T만.

### B2. 루브릭 스코어카드 (런마다 → N 분포)
**HARD GATE(하나라도 fail→해당 런 discard, candidate pass-rate 감점)**: candidate gate PASS · protected pass · no_new_numbers pass · FGP overlap-guard pass(누수0).
**SCORED 축(0/1/2, semantic·negation-aware)**:
- `claim_altitude` **양방향**: 2=강하고-bounded(licensed-max·과장0) / 1=약간 under|over / **0=vague 또는 overclaim**(둘 다 감점 — vague 이기는 함정 차단).
- `caveat_survival`: 2=claim affirmative 생존+caveat가 bound만 / 1=약간 smother / 0=caveat-front·claim 死.
- `register_fit`(섹션): 2=적합 / 0=cross-register leak.
- `protected_preservation`: 2=전부 exact / 0=drift.
- `conciseness_vs_completeness`: 2=필수 다+padding0 / 0=padded|missing.
**negation-aware**: overstrong/scope는 **negation/disclaimer window(앞 not/without/rather-than/no)면 미카운트**(밤샘 false-pos 교훈).

### B3. 선정식 (반복가능성 = 핵심)
candidate(persona-variant)당 N=5:
- `pass_rate`(hard gate) — **≥4/5 아니면 탈락**.
- `score_dist`: median, worst-case(min), variance.
- `candidate_score = median − λ·variance − μ·(2 − worst_case)` (median 보상, variance·낮은 floor 벌점).
- persona별 승자 = candidate_score 최고 **AND** pass_rate≥4/5. **best-of 금지**(단일 lucky 런 승리 불가).
- 근소차/동률 → **held-out task** 재현 검증.

### B4. blind-scoring 안전 매니페스트 (Codex emit)
런마다: `{variant_id(blind hash), persona, run_n, gate_verdicts(축별 pass/fail), real-scorecard counts, paragraph}`.
- Discussion **placeholder-bound** → paragraph에 resolved 값 0 = relay 안전.
- **variant→prompt 매핑은 내 채점 완료까지 withhold**(blind). 채점 후 reveal→분포→선정.
- Codex pre-score 금지(anchoring). 채점=나(deterministic gate + semantic 축).
- (향후 resolved task면 paragraph withhold, counts만 relay = value-free.)

## 다음
1. **Codex**: 위 스펙으로 **토너먼트 wrapper**(variant-profile 재현 실행 + safe manifest emit) 빌드. P1=Discussion placeholder, 3 variants×3 persona×N5.
2. **Claude**: manifest 받으면 blind 채점→분포→persona별 winner→held-out 검증. + (선택) reformatting-normalize fix 재검.
3. 권고: 1a05c10 reformatting-normalize는 토너먼트와 병행(저우선, latent).

## 정직/큐
라이브=repo 밖 실 `_reject_new_numbers`/`_number_tokens` 직접 호출(합성 입력, 값 미노출). 신규코드=1a05c10. manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 다음: 토너먼트 wrapper 빌드시 spec 준수 재검 · reformatting-normalize · 백로그(0a68ea8/9a03e90) · operator.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
