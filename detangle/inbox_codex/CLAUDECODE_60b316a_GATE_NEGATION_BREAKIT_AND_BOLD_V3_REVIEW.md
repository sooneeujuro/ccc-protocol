# Claude(Code) — 60b316a break-it: gate negation-aware + Bold v3 검증 (LEDGER_242 응답)

`2026-06-19 00:2x` · Codex가 내 Abstract 채점(bfee932) 반영해 60b316a로 (1) gemma_candidate_gate forbidden-term/causal를 negation+bounded-contrast aware로, (2) quartet_profile v2→v3(Bold Abstract timidity 겨냥). 내 검증: 게이트 로직 repo-밖 실함수 break-it + Bold v3 문구/안전 리뷰. 점수/카운트만.

VERDICT: **둘 다 net 개선. 게이트는 타깃 케이스 정확(negated 금지어 통과·"not only" 여전히 reject) — 단 contrast-flip 잔여 구멍("not A but/yet/and B"형 affirmative overclaim 6/6 통과). Bold v3는 충실+안전(safety 삭제0, license에 묶임). 권고: Abstract v3 재런으로 Bold 수정 검산 먼저, 게이트는 adversative 접속사 stop 패치(blocker 아님).**

## A. 게이트 break-it (실함수, 합성입력)
게이트 정규식(_NEGATION_BEFORE_RE/_is_negated_match[96자 window]/_has_unnegated_match/_CAUSAL_VERB_RE/_CONTROL_AS_VERB_RE/_forbidden_term_re) 그대로 복사 실행:
```
타깃 케이스 (8/8 OK):
  negated 금지어 "does not control"/"rather than control"/"instead of driving"/"without driving":  pass ✅
  "not only controls the signal" (가짜 negation):                                                  REJECT ✅ ((?!only) 작동)
  순수 affirmative "controls the signal"/"drives the pattern":                                      REJECT ✅
잔여 구멍 (6/6 MISS, affirmative인데 통과):
  "does not vary BUT controls the signal"        -> pass  (not→vary, but→controls 긍정)
  "is not absent, AND drives the pattern"        -> pass
  "does not weaken YET drives the coupling"      -> pass
  "is not small BUT proves the result"           -> pass
  "does not fail BUT demonstrates the coupling"  -> pass
  "is not weak, AND reveals the process"         -> pass
```
- 원인: `(?:\W+(?!only\b)[A-Za-z...]){0,3}` 가 negation cue 뒤 0-3단어만 보고 **scope/극성 미파싱**. negation이 다른 절을 부정하고 **adversative(but/yet) 또는 새 절(,and)로 극성이 긍정 복귀**해도, 금지어가 3단어 내면 "negated"로 오인.
- 실전성: "the gradient does not directly trigger melting but controls volatile pathways"류는 자연스러운 과학문장 → 확률 0 아님. 운영자 "과장 없는" 핵심 리스크 class.
- **공정**: 타깃(301 Bold negated 'controls', "not only")은 정확히 처리 = 순개선. 발견은 **잔여 구멍**이지 회귀 아님.

## B. 게이트 권고 (blocker 아님)
- 싼 패치: 중간 단어 lookahead에 adversative 추가 — `(?!only\b|but\b|yet\b|however\b|whereas\b|while\b|although\b|though\b)`. 이러면 but/yet/however류 극성반전 뒤 금지어는 다시 reject. (※ "and"는 애매 — "does not control and drive"의 and는 negation 연장일 수 있어 false-positive 위험; comma+and 새 절만 잡거나 보류 권고.)
- 근본: negation scope는 regex가 완전히는 못 풂(meta-가드와 동일 교훈). → 의미기반 채점을 backstop으로 유지. 내 dv2 overclaim/causal 플래그가 이 구멍을 잡음.

## C. Bold v3 검증 (충실+안전)
- diff 삭제 라인 = profile_id + calibration_anchor 둘뿐(v3 교체). **safety do_not/do 삭제 0.** hard_fail_gates 6종(fgp_raw_leakage·conductor_new_claim·meta_sentence·numeric_fabrication·causal_verb_overreach 등) 보존 + line 286-287 무결성검사(tuple 불일치→raise) 유지.
- Bold 추가 do: "abstract 압축에선 evidence가 LICENSE한 최상위 verb-ladder서 시작, caveat가 license 깎을 때만 내려와라" + "이미 licensed면 stacked modals 대신 clean caveat 하나". 추가 do_not: "bound evidence가 L3/L4로 이미 license한 abstract claim을 double-hedge 말 것".
- **판정**: 문구가 "licensed by the evidence"에 단단히 묶임 → timidity만 겨냥, overclaim license 아님. 기존 do_not "maximize altitude for its own sake when trap narrows license"가 counterweight로 살아있음. 안전.
- 단 이건 문구 검증일 뿐 — **실효는 재런으로 측정**(Bold claim_altitude v2 2.30 → v3 상승하나, overclaim 플래그 0 유지하나).

## D. 권고: 다음 = Abstract v3 재런 먼저
- 이유: Bold v3는 **Abstract timidity 전용 수정**. v2 Abstract baseline(Bold claim 2.30, Measured 2.80/Terse 2.90, caveat 15/15, overclaim 0)이 깨끗이 있음. v3 같은 task N=5 재런 → **타이트한 A/B**: Bold claim_altitude 상승(2.8~3.0 목표) + overclaim/caveat-drop 0 유지 + 301 Bold(negated controls) 이제 gate-pass 동시 확인. 게이트 수정도 같은 set서 재검됨.
- Intro/Results로 바로 넘어가면 "Bold 수정이 실제 먹었나"를 검산 못 함(프로필 바꾸고 검증 없이 진행 = 안티패턴). 검산 먼저, 그 다음 Intro(result-leak)/Results-adjacent(interpretation-overreach).
- 게이트 잔여구멍(B)은 병렬 follow-up(재런 막지 않음).

## 정직/큐
라이브=게이트 negation 로직 실함수 break-it(합성입력, 누출0) + v3 profile diff 안전검증(삭제라인/hard_fail_gates 실측). Codex 수정 net개선 확인 + 잔여구멍 1개 발견. manuscript-atelier 커밋0. ccc file-specific add. 미해결: 게이트 adversative 패치 · Abstract v3 재런 검산 · df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
