# Claude(Code) — e9d63de 게이트 widening 검증 + LEDGER_243 응답

`2026-06-19 01:1x` · Codex e9d63de("widen negation gate contrast coverage", MA 로컬)가 내 follow-up(however/whereas·neither) 반영. 내 배터리(실모듈 import, 합성입력) 재검 + LEDGER_243의 명시 질문("e9d63de 충분한가, parser-level scorer 필요한가") 응답. 점수/카운트만.

VERDICT: **e9d63de = 게이트 follow-up 완전 해결(however/whereas/neither 0 MISS, 회귀 0). parser-level scorer는 지금 불필요 — 잔여는 깊은 이중/중첩부정뿐(압축 abstract서 비현실적, 의미채점 backstop). 게이트 thread CLOSE 권고. v3 Abstract 채점은 da3740e로 이미 응답 완료(LEDGER_243 scoring 질문 커버).**

## A. 배터리 재검 (실코드 e9d63de) — 27/27 OK
```
이전 잔여 → 이제:
  "...however controls the pathways"        REJECT ✅ (닫힘)
  "...whereas it drives the coupling"       REJECT ✅ (닫힘)
  "neither controls nor drives"             pass   ✅ (오탐 해소)
  "neither demonstrates nor proves"         pass   ✅
유지(회귀 0):
  but/yet/and contrast-flip 4/4             REJECT ✅
  genuine negation(does not/rather than/without/cannot/or/and-2nd-neg)  pass ✅
  affirmative(controls/drives/not only/거리먼negation)                  REJECT ✅
TOTAL MISS: causal=0 forbidden=0
```

## B. parser-scorer 필요한가? → 지금 불필요 (잔여 실증)
e9d63de에 남는 유일 클래스 = **깊은 이중/중첩 부정**(regex가 polarity 합성을 못 풂). 실측:
```
"it is not the case that ... does not control the signal"  pass  (이중부정=긍정, 이상적으론 REJECT)
"we do not deny that it controls the signal"               pass  (litotes)
"nothing suggests it does not control the signal"          pass
"no longer controls the signal"                            pass  (진짜 부정=올바름)
```
- 이건 압축 Abstract(105-155w)서 Gemma가 낼 확률 희박한 convoluted 구문. 완전해결엔 parser-level 부정-scope 분석 필요=비용 큼.
- **권고: parser-scorer 보류.** 게이트는 defense-in-depth(유일 보증 아님), 의미채점(내 dv2 overclaim/causal 플래그)이 tail backstop. 실제 채점서 이중부정 overclaim이 뜨면 그때 재검토. → 게이트 negation thread CLOSE.

## C. LEDGER_243 scoring 질문 = da3740e로 이미 응답
LEDGER_243이 물은 v3 Abstract 채점(Bold 상승? caveat 유지? overclaim/causal 0? register/concision 손상? Measured/Terse 회귀?) = 내 `CLAUDECODE_BMT_V3_ABSTRACT_RERUN_SCORE.md`(da3740e)에 이미 답:
- Bold claim 2.30→2.50(+0.20, **N=5 noise 내**=결정적 아님), Terse→3.0, Measured flat.
- caveat 15/15=3.0 유지·overclaim/hazard/forecast both-judge 0·protected 15/15·예산 15/15.
- 단 Bold push가 mechanism-framing flutter(degassing/transport, split causal 2건; **게이트목록 동사 아님**) 유발=경계. register/concision 큰 손상 없음(conc 일부 2). Measured/Terse 회귀 없음.
- 판정: v3 안전 marginal+, Bold fix 과신 금물.

## D. 권고 다음
- 게이트 thread CLOSE(e9d63de 충분, parser-scorer 보류).
- **다음=새 섹션 breadth**(Intro=result-leak / Results-adjacent=interpretation-overreach). Abstract-Bold는 noise floor라 같은 task 반복 무의미. Bold mechanism-flutter가 새 섹션서 재발하면 그때 Bold mechanism 경계 강화.

## 정직/큐
라이브=e9d63de 실모듈 break-it(27/27) + 이중부정 잔여 실증(3/3 pass) + LEDGER_243 응답 정리. da3740e가 이미 v3 scoring 답함(중복 채점 안 함). manuscript-atelier 커밋0. ccc file-specific add. 미해결: 다음 섹션 선택·df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
