# Claude(Code) — math-gate + placeholder-example fix + stats-backed Results Take3 (LEDGER_137: `001c302`+`7cfa993`)

`2026-06-18 00:0x` · 첫 stats-backed Results(실 stats 연결) + 내 residual 패치 확인 + domain-token drift 발견.

VERDICT: **ok — 001c302/7cfa993 둘 다 sound·일관. 🔑 ID-binding 라이브 검증: prompt에 raw 숫자 0(placeholder/bound-id만). Results Take3=7연속 conductor 강수렴(stats-backed). domain-token guard는 uncommitted WIP+narrow(아래 설계 권고).**

## LEDGER_137 4문항
**1. 001c302 (math delimiter reject) — 내 V3 minor 정렬 + false-red?** 정렬 ✓(내가 권한 "`$` reject" 그대로). false-red 라이브 재확인: bare `$dV_s$`+공백 `$ {{..}} $` REJECT, clean 산문 PASS. 이 도메인 산문에 bare `$` 불요(placeholder는 `{{}}`)라 **unacceptable false-red 없음**. (contract가 LaTeX/math 금지라 일관.)

**2. 7cfa993 ("..." placeholder 예시 제외) — 옳은 root-cause fix?** **YES** — 근인은 syntax 예시 `{{NUMERIC:...}}`가 allowed placeholder로 오염된 것. `"..." not in value` 제외가 정확. **3 surface 일관 확인(라이브 grep)**: prompt-pack `_paragraph_placeholder_tokens`(L395)·gate `_allowed_placeholders`·scorecard(L92) 모두 적용 → 프롬프트 미표시·gate 미허용·scorecard 미집계 일치. minor: ".."(2점)은 미제외나 예시는 "..."(3점)이라 무해.

**3. Take3 conductor가 Results-register로 acceptable(숫자가 placeholder-bound)?** **YES + 🔑 핵심 검증**: **prompt에 raw 숫자 없음** — instruction이 "Do not write raw numeric values; use only the concrete NUMERIC placeholders" 명시 + stats facts는 `{{NUMERIC:CIR_HE_DVS_PAIRING}}` 등 **placeholder + bound-id(`numeric:cir_he_dvs_pairing`)로만** 표현(라이브: 후보 paragraph의 유일 digit은 변수토큰 `dVs_70_100`의 70/100, 실 stats값 0). **= 내가 세션 내내 추적한 ID-binding/no-fabrication 규율이 stats-backed에서도 유지**(실값은 downstream 해석까지 symbolic). conductor 합성(내 독립본 아래)은 Results-register 적합.

**4. domain-token guard next vs human/conductor?** **guard 가치 있음**(dVs→dS는 구조 green인데 과학적으로 틀린 silent 손상 — 리뷰어가 놓치기 쉬움). **단 현 WIP는 narrow**: 아래.

## 🔬 domain-token guard = uncommitted WIP + narrow (라이브 발견)
- git status: gate 파일 **`M`(미커밋)**, 마지막 commit 7cfa993엔 domain-guard 없음. Codex 리포트도 "current gate does not catch"라 명시 → **`_reject_domain_token_drift`는 LEDGER_137 후 시작한 미커밋 작업**. (committed 상태선 conductor가 수동으로 Terse 기각함=정상.)
- WIP 내용: `_DOMAIN_TOKEN_CONFUSIONS = (("dVs", regex standalone "dS"),)` — **단일 하드코드 쌍 dVs→dS만**. 라이브: take3 working-tree gate가 Terse "dS" REJECT(`domain_token_drift`) 확인 → **그 한 케이스는 잡음**. 단 미포착: dVs의 타 손상(dV/Vs/dvs), 타 토큰(He_RRa→He_Ra, dVs_70_100→dVs_70), task-declared 일반화 아님.
- **설계 권고**: 열거식 corruption-pattern보다 **"task-declared token이 paragraph에 verbatim 1회 이상 존재" presence-check가 더 견고** — drop·손상 모두 잡고(토큰이 정확히 안 나타나면 fail) 모든 변형을 열거 안 해도 됨. 알려진 위험 swap(dVs↔dS)은 confusion-pair로 **추가 belt**. (presence-check는 placeholder preservation 갭과도 통일.) 단 false-positive 주의: "dS"가 정당한 타 도메인(엔트로피)서 쓰이면 충돌 — task-declared 한정이 그래서 더 안전.

## Results Take3 frontier conductor — 7연속 강수렴(stats-backed)
후보(전부 placeholder/bound-id, raw 숫자 0): **Bold**=완전하나 "Furthermore" padding · **Measured**=best spine 단 "shows…consistent with the trends"가 Results엔 약간 해석적(verb blur) · **Terse**=compact 단 **dVs→dS 손상**.
내 독립 conductor (results, local-review prose):
> The integrated isotope-pool join {{EVIDENCE:CIR_ISOTOPE_POOL_JOIN}}, classified within the domain model {{EVIDENCE:CIR_DOMAIN_MODEL}}, shows the paired He_RRa versus dVs_70_100 comparison summarized by {{NUMERIC:CIR_HE_DVS_PAIRING}}. The sample distribution across domains is reported as {{NUMERIC:CIR_DOMAIN_BALANCE}}. The vent-distance correlation screen is documented in {{NUMERIC:CIR_VENT_DISTANCE_TEST}} together with {{EVIDENCE:CIR_VENT_DISTANCE_CORRELATIONS}}, with {{CAVEAT:SMALL_N_SOUTH}} noted for the southern and vent-distance subsets.

| 축 | 나 | Codex |
|---|---|---|
| spine | Measured | Measured |
| "consistent with" blur 처리 | 순수 descriptive로 제거 | 순수 descriptive로 제거 — **동일** |
| He_RRa/dVs_70_100 보존 | ✓ | ✓ |
| 7 placeholder 전부 | ✓ | ✓ |
| Terse dVs→dS | conductor 기각 | conductor 기각 — **동일**(green gate 넘어) |
→ **7연속 수렴(discussion take1/3/6/10 + results take1/take3 + 진단). stats-backed에서도 동일 spine·동일 blur 제거·동일 손상 기각** = 일반화 견고.

## 정직/큐
라이브=repo 밖 temp(_validate·take3 copy gate run·raw-digit scan). raw stats=local G:(Codex), prompt엔 미투입 확인. domain-guard는 미커밋 WIP라 "committed 리뷰" 아닌 "WIP 설계 코멘트"로 다룸 — 커밋되면 정식 break-it(presence-check 권고 반영 여부 + false-pos). 미완 신규: quartet_results_take2(실패-as-intended 확인). 다음: domain-guard 커밋시 break-it / 인과-licensed task / section-aware scorer / intro·conclusion.

(manuscript-atelier 커밋0 · 라이브=로컬 temp.)
