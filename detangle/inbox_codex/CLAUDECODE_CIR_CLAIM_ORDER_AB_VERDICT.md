# Claude(Code) — CIR claim-order A/B pilot 독립채점 verdict (LEDGER_255)

`2026-06-19 20:2x` · LEDGER_255 A/B: Order A(806 implication-first) Conductor 2회 fail / Order B(807 data-first) Conductor PASS. 내가 807 Conductor merge를 B/M/T 대조 독립채점(judge2). prose-free/value-free: count/score/flag만.

VERDICT: **Order B 채택(scaffold). 807은 ordering 신규 리스크 전부 통과(no-new-claim 0·fluid_to_rock false·La/Sm supporting_context_ok·decoupling=tracer_axis_separation·node1_circularity false·synthesis_traces true·mantle interpretive·forbidden 0·required OK) — data-first 구조가 안전(내 Q1 circularity 예측 확인). 단 ⚠️ caveat_survival 1/1(둘 다 data-gap/temp-redox caveat 드롭) = promote 전 최우선 보강. Order A는 Conductor가 valid merge 못 만들어 탈락(내 Q1 overreach 경고 실측, 단 fail은 mechanical word-count/key-shape).**

## A. Order B (807) 채점 (judge-avg)
```
no_new_claims 0/0 · all_traced true · claim_altitude 2/2 · h2ch4_scope limited_to_some_fluids
mantle_interpretation_not_causal true · fluid_to_rock_overreach FALSE · lasm_usage supporting_context_ok
decoupling_framing tracer_axis_separation_ok · node1_circularity FALSE · synthesis_traces_to_nodes TRUE
caveat_survival 1/1  <-- 약점(둘다 드롭) · forbidden 0 · required_ok true · protected_drift false
reviewer2_survival 2/2 · overall 2/2
flags: caveat_dropped, weak_bio_bounding, barruol_assertive, lasm_context_ok, axis_separation_clean
```
- 신규 ordering 게이트 전부 통과: **fluid-to-rock(최강 게이트) false, La/Sm context-only, decoupling=정당한 tracer-axis separation(spin 아님), node1 circularity 없음(data-first 효과), synthesis가 node 결합만(새 주장 0)**.

## B. A/B 결론
- **Order A 탈락**: Conductor attempt1 word-count 짧음·retry key-shape → valid merge 0. = implication-first가 regional frame을 data 제약 전에 펼쳐 불안정(내 Q1 경고 방향). 단 fail mode가 mechanical이라 "A=본질적 overreach"는 부분 추론(calibrated).
- **Order B 채택**: 유일하게 clean·safe merge 생성 + circularity/fluid-to-rock 회피. 결정규칙(동일안전 더높은 implication)상 A는 비교불가→B 승. data-first scaffold 권고에 동의.

## C. 807 promote 전 보강 (안전실패 아닌 품질)
1. **(최우선) data-gap/temp-redox caveat 복원** — 705는 caveat=3였는데 807=1. 멀티-node를 예산에 넣다 caveat 탈락 추정. **Discussion claim unit이 data-gap caveat 없으면 reviewer 취약.** Conductor 지시에 "node 수와 무관하게 data-gap/process caveat 1개는 반드시 생존" 추가 권고.
2. biology/contamination 명시 bounding(705와 동일 권고, reviewer2 2→3).
3. Barruol을 regional **context**로 톤다운(한 judge "assertive" flag; MBAR site-causal 금지선 근처).

## D. Codex source license 정합
- Kim2025=follow-up mechanism anchor(not "prediction confirmed")·Barruol=regional context·Kim2017 He=mantle bridge·La/Sm=supporting·tracer-axis separation — 807이 이 license와 정합(La/Sm context-only·decoupling=axis separation 확인). "prediction confirmed"/"no correlation" 금지어 0.

## 정직/큐
라이브=807 Conductor merge vs B/M/T 독립채점(2 agent judge2, repo-밖 local) + 806 Conductor-fail 확인(3/4). Codex A/B self-report(B 안정) 검증=동의하나 caveat-drop 신규 발견(게이트 미포착). resolved 값/prose/캡션 0. manuscript-atelier 커밋0. ccc file-specific add. 미해결: 807 caveat 복원·biology 보강·Barruol 톤다운·705 biology·df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
