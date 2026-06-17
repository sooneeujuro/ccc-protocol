# Claude(Code) — section profiles + math-delimiter gate + Results Take1 (LEDGER_136: `be32698`+`001c302`)

`2026-06-17 23:5x` · 5-section 확장(overfit 대응) + 내 직전 residual 패치 + 첫 비-discussion(results) Take.

VERDICT: **ok — 내 math-delimiter residual CLOSED(라이브). 5-section value-pin 유지·results가 인과금지(내 causal경고 잠복 유지). Results Take1=6연속 conductor 강수렴인데 이번엔 *다른 섹션* → overfit 우려 상당부분 해소. 신규 발견 1(scorecard overstrong이 section-blind).**

## 001c302 — 내 residual CLOSED (라이브)
`if "\\" in paragraph or "$" in paragraph` → bare `$dV_s$` **REJECT** ✓, 공백 `$ {{..}} $` **REJECT** ✓ (지난 라운드 둘 다 닫힘), clean 산문 PASS(false-pos 없음). contract의 "no math delimiters"가 이제 gate에서 강제됨. **이 도메인 산문에 bare `$` 불요라 안전.**

## be32698 — 5-section 확장 (라이브)
- default가 intro/methods/results/discussion/conclusion 5개, 각 function/preferred_sequence/forbidden_moves. **validates ✓ · value-pin 유지**(hard_fail gate drop→reject 라이브). 
- **results forbidden_moves = explaining_mechanism / turning_pattern_into_causality / adding_regional_implications** → results도 **인과 금지**. 즉 **5섹션 전부 인과 비-license** → 내 🔭 causal-gate 무조건성 경고는 **여전히 잠복**(이 5섹션엔 안 터짐). 경고는 *미래 인과-licensed task*에만 유효 — 그런 task 생기면 #1 감시점 유지.
- 안전/최소: 섹션별 forbidden(intro=result-leak·methods=interpretation·conclusion=new-evidence·results=mechanism/causality)이 적절. minimal section-function control. ok.

## Results Take1 frontier conductor — 6연속 수렴, 이번엔 *다른 섹션*
task=results(observed pattern only·인과/mechanism/implication 금지, 금지어 supports/motivates/framework/cause/drive/prove/establish). 후보 전부 구조 clean(placeholder 3·exact id):
- **Bold**: "**reveals** a spatial pattern" + "effect"(약간 해석적) + evidence array 1개만(cir_velocity 누락).
- **Measured**: **best** — "summarized in/describes a spatial distribution" 순수 관찰·overstrong 0·전 binding.
- **Terse**: 안전하나 과압축(skeletal note).

내 독립 conductor (results, local-review prose):
> The comparison between helium isotope structure and seismic velocity anomalies is summarized by {{NUMERIC:CIR_PRIMARY_EFFECT}}. The observed spatial pattern, evaluated against {{EVIDENCE:CIR_DOMAIN_MODEL}}, describes the distribution and contrast across the dataset, with any unresolved model dependence remaining subject to {{CAVEAT:MODEL_DEPENDENCE}}.

| 축 | 나 | Codex |
|---|---|---|
| spine | Measured | Measured |
| {{NUMERIC}} summarized + {{EVIDENCE}} evaluated | ✓ | ✓ |
| pattern 기술·mechanism 없음 | ✓ | ✓ |
| caveat 끝 {{CAVEAT}} | ✓ | ✓ |
| Bold "reveals" 평가 | overstrong(단 아래 nuance) | "too strong for placeholder-only" |
| Measured=best/Terse=skeletal | ✓ | ✓ |
→ **6연속 강수렴(take1/3/6/10+discussion진단 + 이번 results). 이번은 *섹션이 다름* → 수렴이 discussion-only 기계 overfit이 아니라 접근법 일반화임을 시사**(단 여전히 동일 task-family/dataset이라 완전일반화는 다양 claim/data 필요).

## 🆕 신규 발견 — scorecard overstrong이 section-blind
`_OVERSTRONG_RE`(demonstrate/reveal/establish/prove)가 **섹션 무관**. discussion에선 "reveals=해석 overclaim"이 맞지만, **fully-fed results에선 "reveals/shows a pattern"은 직접관찰 L4-licensed**(정당). 이번 Bold "reveals"가 overstrong=1로 잡힌 건 **underfed(placeholder뿐이라 실제 관찰 없음)라 우연히 맞은 것**(=Codex의 "too strong for placeholder-only"와 상보) — 휴리스틱이 results-licensing을 이해해서가 아님. **richer results(실데이터)로 가면 정당 L4를 over-flag** → verb scoring을 **section-aware**로(results는 직접관찰 L4 허용, discussion은 해석 L4 불허) 권장.

## LEDGER_136 4문항
1. be32698: 위(validates·value-pin·results 인과금지).
2. 5 profiles 안전/최소? **YES** (각 function/sequence/forbidden, value-pin, minimal).
3. Results Take1이 right failure mode(safe but underfed)? **YES** — 기계 일반화+implication 억제 성공, placeholder뿐이라 skeletal. + 위 scorecard section-blind nuance.
4. richer Results(real stats/data) vs Intro/Conclusion 먼저? **richer Results 우선 권장** — numeric/evidence **binding**을 실제로 exercise(=내가 추적한 ID-binding seam + M3 stats-ledger)하고 evidence→draft 전체 사슬을 검증, section-aware verb scoring 필요여부도 드러남. **단 실값은 stats-ledger ID-binding(stats_run:* / bound numeric id) 경유여야**(raw 숫자 prompt 투입 금지, no-fabrication 유지). Intro/Conclusion smoke는 싸니 병행 OK.

## 정직/큐
라이브=repo 밖 temp(_validate 직접·default profile 검증·results_take1 copy). 후보·conductor repo 밖 local·raw FGP 미노출. 미완 신규: `quartet_results_take2`(synthetic-002, 미완)·`stats_fact_probe`(23:55, 신규 — results↔real stats 연결?, 핸드오프前) → 완성/핸드오프시 본다. 다음: richer-results(stats-binding) Take / 인과-licensed task(causal gate 검증) / section-aware scorer / stats_fact_probe break-it.

(manuscript-atelier 커밋0 · 라이브=로컬 temp.)
