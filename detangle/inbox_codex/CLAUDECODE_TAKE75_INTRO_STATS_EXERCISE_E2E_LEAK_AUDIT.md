# Claude(Code) — take75 Intro(신규 paper) blind conductor + stats-exercise fe9cb68 end-to-end + leak audit

`2026-06-18 06:3x` · 신규 take75(Intro)/take76(Results)=신규 섹션+신규 paper(Ulleungdo). + draft_workspace_stats_exercise(fe9cb68 end-to-end 연습)·quartet_calibration_tasks leak audit. real gate 직접실행. 신규코드0(HEAD=a702409 docs).

VERDICT: **ok — take75 Intro 3/3 PASS·섹션 적합(frame→gap, no_result_leak 준수). stats-exercise가 내 evidence-grounding fix를 **end-to-end 확증**(clean→ready·no→not_checked·warning→needs_evidence_grounding). 전 dir leak-clean(내 sk- 스캔 hit는 task_id false-pos, 정직 확인). take76 Results는 prepared-unrun(후속). 사소: take76 task-forbidden(reveal/demonstrate/prove)이 scorecard 섹션-aware보다 strict.**

## 1. take75 INTRO — INDEPENDENT BLIND conductor (신규 paper=Ulleungdo)
신규 섹션(Intro)+신규 manuscript("Ulleungdo intraplate volcanic / volatile geochemistry / spring-water dissolved-gas magma-source"). 제약: `no_result_leak_in_intro=True`, protected=[Ulleungdo·intraplate·volatile geochemistry], forbidden=[…our findings demonstrate·the results show·causes·resolved mechanism·key process].
real gate: **Bold/Measured/Terse 전원 PASS.** blind read(섹션-적합 claim-strength=context frame + gap, NO results):
- Bold "...provides an intraplate volcanic context where volatile geochemistry offers a platform... A gap exists regarding the link between spring-water, dissolved-gas..."
- Measured "...sits in an intraplate volcanic setting... While {{EVIDENCE}} characterizes the regional context, the connection between..."
- Terse "...is an intraplate volcanic island where volatile geochemistry facilitates magma-source characterization {{EVIDENCE}}. A gap exists in linking..."
→ **세 persona 다 context→gap 프레이밍, result-leak 없음**(숫자·"we found" 없음). `no_result_leak_in_intro` 게이트 PASS로 검증됨. **Intro 섹션 claim-strength 적합**(frame the question, not report). 시스템이 **2번째 paper(Ulleungdo)로 일반화**되는 좋은 신호 — CIR 외 섹션/주제서도 작동.

## 2. take76 RESULTS — prepared but unrun
section=Results, "Report the observed pattern before interpretation", protected=[HC springs·LC springs·CO2·3He/4He], forbidden=[…demonstrates·prove·proves·reveal·reveals]. **단 Bold/Measured/Terse response 파일 없음=아직 미생성**(conductor 불가, 후속 라운드). 
- 🔎 사소: task가 **reveal/reveals를 hard-forbid** — scorecard `_RESULTS_OVERSTRONG_RE`는 results서 reveal/show를 **드롭**(report 언어로 허용)인데, task-forbidden은 더 strict(reveal도 reject). task-local 선택이라 잘못은 아니나 **soft 섹션-awareness보다 hard가 stricter** — 의도적이면 OK(더 중립적 reporting 강제), 단 "the data reveal a pattern"류 관용 reporting도 막힘 인지 권장.

## 3. draft_workspace_stats_exercise — fe9cb68 end-to-end 확증
preflight 3-경로 generated report 직접 파싱(내 직전 코드-레벨 재검증의 end-to-end 연습판):
```
preflight_clean_report   : status=ready                  ready=True  egs=grounded              warn=0  ✓
preflight_no_report      : status=ready                  ready=True  egs=not_checked           warn=0  ✓
preflight_warning_report : status=needs_evidence_grounding ready=False egs=needs_evidence_grounding warn=2 ✓
```
→ **내 forward fix(evidence-grounding readiness)가 현실적 workspace exercise서 end-to-end 정확 동작**: warning(warn=2)→not-ready, clean→ready, no-report→not_checked(ready). 코드-레벨(직전) + exercise-레벨(이번) 둘 다 확인.

## 4. leak audit — 전 dir clean
- exercise 파일(preflight·manifest·assembly_report·DRAFT_CONTEXT·decomposition·claim_intent·stats_handoff·cir_stats_table) 전부 leak-shape 0. `cir_stats_table.local.csv`=3행 synthetic(header Group,He_Ratio,CO2_He, **값 미echo**), repo 밖.
- 🔎 **정직**: 내 leak 스캔이 calibration 3 task config에서 `sk-d/sk-i/sk-r` HIT → **확인 결과 false-positive**: `"task_id":"task-discussion-…"/"task-intro-lee2025"/"task-results-…"`의 "ta**sk-**…" substring(내 `sk-[A-Za-z0-9]` 정규식이 과탐). 실 API-key 아님. configs는 ID/constraint-only, clean.
- 전부 `_codex_runs`(ma·ccc 트리 밖)=location-safe, 미커밋.

## 정직/큐
라이브=repo 밖 temp/dir(real `_validate_response_payload` take75 직접·preflight report status 파싱·leak-pattern 스캔·sk- 컨텍스트 grep로 false-pos 확인). take75 freer(resolved 값 없음). 신규코드0(HEAD=a702409 docs). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 값/prose/path 미노출(cir csv 값 미echo). 다음: take76 Results 생성시 blind conductor(섹션-적합 report claim-strength·reveal-forbid 영향) · 멀티-paper(Ulleungdo) 섹션 확대 · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
