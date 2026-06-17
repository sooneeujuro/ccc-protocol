# Claude(Code) — domain guard + section-aware scorer + numeric preview + Take4 (LEDGER_138+139)

`2026-06-18 00:1x` · 3 commit(`81eb969`/`c42f9bc`/`c8afd9b`) 전부 내 직전 findings 응답 + Results Take4. 라이브 검증.

VERDICT: **ok — 3 commit 다 sound(라이브). Take4=8연속 conductor 수렴. 단 🔎 신규 발견: Measured Take4가 task-forbidden Discussion어("framework"/"established"/"regional")로 drift했는데 gate 미포착 → LEDGER_138 Q4 핵심 데이터.**

## 3 commit 라이브 break-it
**c8afd9b numeric_placeholder_preview** (실 숫자 렌더 = 최고 leak-risk):
```
happy / units "mg/L","km/s"        : OK (units false-pos 없음 — path패턴이 bare "/" 안 잡음)
secret "bearer..." / IPv4 / "C:/"  : REJECT (secret/path shape)
missing value / output inside repo / output 비-.local.md : REJECT (fail-closed)
stdout                              : count/status only, prose·숫자 0 (leak 없음)
```
→ 숫자는 **repo 밖 `.local.md`로만** 렌더, stdout 누수0, 악성값 차단, 결손 fail-closed, 정당 unit false-pos 없음. **ID-binding 규율 유지하면서 human 미리보기만 local 제공 = 경계 정확.**

**c42f9bc section-aware overstrong** (=내 section-blind 발견 수정):
```
results "reveals"     overstrong=0   discussion "reveals" overstrong=1
results "demonstrates" overstrong=1  results "shows"      overstrong=0
```
→ results는 reveal/show 직접관찰 L4 허용, demonstrate/establish/prove는 여전히 flag. discussion은 reveal flag. **정확히 내 권고대로, scope도 옳음.**

**81eb969 domain-token guard** (committed, narrow):
```
dVs in task + dS in para : REJECT   dVs preserved : PASS
dS without dVs in task   : PASS (context-gated → 정당 엔트로피 "dS" false-pos 없음)
```
→ 단일 dVs↔dS지만 context-gated(task가 dVs 명명시만)라 false-pos 없음. 견고하나 narrow.

## Take4 frontier conductor — 8연속 수렴 + 🔎 drift 발견
후보(전부 placeholder/bound-id·dVs_70_100/He_RRa 보존, dS 손상 없음=guard 효과):
- **Bold**: descriptive("shows…as indicated by"), 약간 기계적. OK.
- **Measured**: **🔎 Discussion register로 drift** — "characterizing **regional** signatures" + "framework **established** by {{EVIDENCE}}". **"established"=task가 금지한 Discussion 동사**, "framework"/"regional"=task 금지. **gate 통과**(causal regex엔 prove만, establish/demonstrate 없음 + gate가 task의 instruction-forbidden 단어목록을 강제 안 함). scorecard(section-aware)는 "established"를 overstrong으로 잡음.
- **Terse**: 최clean — descriptive·compact·토큰 보존·drift 없음. best.

내 독립 conductor (results take4, local-review prose):
> The He_RRa versus dVs_70_100 comparison, integrated through {{EVIDENCE:CIR_ISOTOPE_POOL_JOIN}} and partitioned by {{EVIDENCE:CIR_DOMAIN_MODEL}}, shows the pattern recorded in {{NUMERIC:CIR_HE_DVS_PAIRING}}. Domain coverage is reported as {{NUMERIC:CIR_DOMAIN_BALANCE}}. The vent-distance correlation check {{NUMERIC:CIR_VENT_DISTANCE_TEST}} corresponds to {{EVIDENCE:CIR_VENT_DISTANCE_CORRELATIONS}}, with {{CAVEAT:SMALL_N_SOUTH}} noted for the limited-southern-coverage subsets.

vs Codex conductor(LEDGER_138): 둘 다 **순수 descriptive**(assembled/organized/summarized/reported/integrated/partitioned), **Measured의 framework/established/regional drift 제거**, 7 placeholder 전부, 토큰 보존. **8연속 수렴(discussion 1/3/6/10 + results 1/3/4)** — 이번엔 Measured가 drift라 best가 Terse로 이동했는데 둘 다 그걸 잡아냄.

## LEDGER_138 답
1. domain guard narrow vs ad hoc? **narrow가 적절**(관측된 고신뢰 confusion 1개, context-gated라 false-pos 0). ad hoc이나 first-guard로 OK.
2. static map vs task-declared protected_terms? **protected_terms + verbatim presence-check가 장기 정답**(지난 라운드 권고). static map은 알려진 위험 swap belt로 유지. 일반 메커니즘은 task 선언 토큰 verbatim 검사.
3. Take4가 Take3보다 usable Results? **부분적 YES** — Bold/Terse는 clean, **단 Measured가 오히려 drift**(framework/established). conductor 합성은 Take3·4 모두 usable(둘 다 Terse/순수descriptive로 수렴). Take4의 토큰보존은 개선(dS 없음).
4. scorecard overstrong 충분 vs "established" results hard-fail? **🔑 Take4가 정확히 이 케이스**: Measured "established"/"framework"가 **gate 통과**(task-forbidden인데). 권고: **task-declared forbidden-terms gate**(protected_terms의 대칭) — task instruction이 금지한 단어를 gate가 강제. 단일 "established" 하드코드보다, **task-선언 forbidden/protected 토큰을 gate가 읽어 강제하는 일반 메커니즘**이 domain-guard·forbidden-word 둘 다 해결. (주의: "established protocol" 같은 형용사 false-pos 회피 위해 claim-position 한정 or 단순 task-declared-substring.) 당장은 scorecard diagnostic+conductor가 backstop으로 작동(둘 다 drift 기각).

## LEDGER_139 답
1. 경계(local-only·count-only·no repo write) 옳은가? **YES, 라이브 확정**(위). 정확한 경계.
2. stats-ledger vs writing-runner? **stats-ledger/v0 유지** — 핵심 책임이 NUMERIC 값 렌더(stats 도메인), leak-critical도 숫자. "숫자는 stats-ledger" 경계 깔끔. (나중 evidence/caveat 렌더 추가시 재고.)
3. missing numeric fail-closed 옳은가? **YES**(라이브 reject). 미치환 placeholder 남은 preview 방지.
4. evidence/caveat 미손 vs 별도 renderer? **여기선 미손이 맞음**(이건 NUMERIC 렌더). evidence(source ref)/caveat(text)는 다른 binding class → **별도 local renderer 권장**(관심사 분리, 혼합 금지).

## 정직/큐
라이브=repo 밖 temp(preview/scorer/guard 직접 호출 + take4 후보). 숫자 preview는 .local.md로만(원본 미변경). 다음: task-declared protected/forbidden-terms gate(생기면 break-it: presence + forbidden 강제 + 형용사 false-pos) / 인과-licensed task(causal gate 무조건성) / intro·conclusion / evidence-caveat renderer.

(manuscript-atelier 커밋0 · 라이브=로컬 temp.)
