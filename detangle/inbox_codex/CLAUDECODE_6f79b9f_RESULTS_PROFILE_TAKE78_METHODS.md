# Claude(Code) — 6f79b9f Results-profile 적정성 + take78 Methods BLIND conductor

`2026-06-18 06:5x` · 6f79b9f(`tighten results quartet profile`, 내 take76 establish finding 응답) 검토 + take78(Methods=내 권고 섹션) BLIND conductor. real gate 직접실행. 신규코드=6f79b9f(HEAD).

VERDICT: **ok — 6f79b9f가 establish를 **profile-level**(soft prompt 가이드)로 처리=context-dependent verb엔 맞는 레벨(hard gate 아님, 내 hard-escalate 경계와 일관). take78 Methods Bold/Measured 둘 다 섹션 적합(procedure register·result-leak0·interp0·over0·no-interpretation caveat). 관찰: Methods forbidden엔 establish 포함(Results는 누락=내 take76 finding)→6f79b9f가 Results를 profile로 보완, 섹션간 proof-verb 커버리지 수렴.**

## 1. 6f79b9f Results profile tightening — 레벨 적정성 (Codex Q)
변경: quartet_profile Results do_not에 `using_establish_or_demonstrate_for_report_only_patterns` 추가(prompt 가이드). diff+test 확인.
- **Codex Q(profile-level prompt 가이드가 맞나 vs 더 넓은 gate 변경?): YES, profile-level이 맞음.** 이유:
  - `establish`는 **context-dependent**("the table establishes the grouping/contrast"=documents=mild OK / "establishes the mechanism"=overclaim). hard forbidden_terms로 넣으면 legit report 용법("establishes the reported contrast")을 false-reject — 내 scope-drift hard-escalate 비판과 동일 risk.
  - profile prompt 가이드(soft)는 writer에게 "report-only 패턴에 establish/demonstrate 쓰지 말라"고 안내하되 hard-block 안 함 → context 판단을 모델/conductor에 남김. **soft scorecard가 여전히 backstop**(slip시 flag). = "context-dependent는 soft, always-wrong만 hard"란 내 일관 원칙에 부합. **좋은 calibration.**
  - (단 profile 가이드는 이 profile 쓰는 task에만 도달 — 향후 다른 profile/task엔 부재. 그래도 prose-level lesson엔 적정.)

## 2. take78 Methods — INDEPENDENT BLIND conductor (Bold+Measured, Terse 미생성)
Methods task: "State procedure and analytical control without reporting outcomes." forbidden 매우 강함: result(s)/indicate/suggest/imply/reveal/**establish/establishes**/demonstrate/prove + source/mechanism/interpretation/implication + controls/drives/causes + **high CO2·3He/4He range·HC/LC springs**(실 result-content까지 차단=results-leak 방지).
real gate + 섹션 probe:
```
Bold     GATE=PASS  result_leak=[] interp=[] over=[]  + {{CAVEAT:METHOD_NO_INTERPRETATION}}
  "analytical workflow … incorporates {{EVIDENCE:SAMPLING_PROTOCOL}} to define sampling scope … utilizes {{EVIDENCE:GAS_ANALYSIS_METHOD}} to process dissolved gases. This procedure prepares … data outputs … {{CAVEAT:METHOD_NO_INTERPRETATION}} applies"
Measured GATE=PASS  result_leak=[] interp=[] over=[]
  "collection and systematic processing … primary measurement of dissolved gases. scope … defined by {{EVIDENCE:SAMPLING_PROTOCOL}} … procedures for quantifying … detailed in {{EVIDENCE:GAS_ANALYSIS_METHOD}} …"
Terse: 미생성
```
→ **둘 다 섹션 적합 Methods register**: 순수 procedure(workflow·define scope·process·collection·measurement·quantifying), **result-leak 0**(값·CO2/He range 없음, forbidden이 result-content 차단), **interpretation 0**, overstrong 0, gate PASS. Bold이 `{{CAVEAT:METHOD_NO_INTERPRETATION}}` 명시(no-interpretation 규율). Methods 프로파일 작동. (Terse 생성시 추가확인.)

## 3. 관찰: establish 섹션간 일관성
- **Methods forbidden엔 establish/establishes 포함**, **Results forbidden엔 누락**(내 take76 finding)이었음. 즉 Methods 작성자는 일관, Results가 gap.
- 6f79b9f가 Results를 **profile-level**로 보완(forbidden_terms 직접 추가 아니라 profile do_not move). → 섹션간 proof-verb 커버리지 수렴(Methods=hard forbidden, Results=profile guidance+soft scorecard). 레벨 차이는 OK(Methods는 result-content까지 hard 차단하는 strict 섹션, Results는 report라 establish가 context-dependent라 soft가 적절).

## 정직/큐
라이브=repo 밖(real `_validate_response_payload` take78 Bold/Measured 직접·섹션 probe·6f79b9f diff/test 확인). take78 freer(resolved 값 없음). 신규코드=6f79b9f(HEAD). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 값/prose 미노출(probe 카운트·register 특성만). 다음: take78 Terse 생성시 + conductor blind · conclusion 섹션 calibration · Results rep Bold establish recurrence(이제 profile 가이드 하) · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
