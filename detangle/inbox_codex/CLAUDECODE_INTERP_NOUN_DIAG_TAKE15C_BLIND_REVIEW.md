# Claude(Code) — interpretive-noun diagnostic + Take15c BLIND conductor (`b503f15`)

`2026-06-18 01:0x` · scent diagnostic 후속(interpretive **noun** overreach) + discussion 복귀 첫 green(take15c, gemma12b). LEDGER 미수신(선제) + 진짜 blind conductor.

VERDICT: **ok — b503f15 interp-noun diagnostic sound(non-gating·정확·누수0 라이브, 카운트가 내 blind read와 정확 일치). Take15c=2번째 진짜 BLIND conductor 수렴 + "noun-level overreach" 진단도 독립 수렴.**

## b503f15 unsupported interpretive nouns — 라이브 검증
`_INTERPRETIVE_NOUN_RE`=mechanism(s)/driver(s)/regime(s) + "architectural domains"/"geological drivers"/"mantle source"/"crustal noise"/"lack of correlation". per-candidate `unsupported_interpretive_noun_count` + summary max. **non-gating**(scent와 동일 계열).
```
take15c 라이브: gate PASS(non-gating ✓) · interp_noun Bold3/Measured1/Terse1 · scent0 · overstrong0 · leak NONE
```
→ **카운트가 내 blind 후보평가와 정확 일치**(Bold=mechanisms+regimes+architectural domains=3, Measured=geological drivers=1, Terse=lack of correlation=1). **scent/overstrong는 0인데 interp-noun이 3** = 이 진단이 verb-screen이 놓치는 **명사 overreach**를 정확히 포착. 잘 타깃됨. 누수0(counts only).

## Take15c BLIND conductor (discussion separability 복귀)
**정직: 후보+task만 보고 conductor 작성 후 report 읽음**(take15c는 직전 sanity때 counts만, prose 미독해→blind 유지됐음). 진짜 blind 2번째.
후보 독립평가(task=test of separability, **"already separable" 주장 금지**):
- **Bold**: "provides a test" 좋으나 "**different spatial regimes**"/"**distinct architectural domains**"/"same **mechanisms**" = **already-separate 주장 + 금지 interpretive noun**(task 위반). 마지막 문장이 새 개념 claim.
- **Measured**: 더 cautious 단 "**measurable degree of separability**"(licensed보다 강함) + "**geological drivers**"(mechanism claim, placeholder 없음).
- **Terse**: **best** — "consistent with **convolution** ... rather than one-to-one"(올바른 bounded framing) + 단 "**lack of correlation**"(미공급 통계) + "not strictly tied"(약한 negative drift).
내 blind conductor:
> The paired He_RRa versus dVs_70_100 comparison, summarized by {{NUMERIC:CIR_HE_DVS_PAIRING}} and bound to {{EVIDENCE:CIR_ISOTOPE_POOL_JOIN}}, provides a test of separability between helium isotope structure and velocity structure rather than evidence that they are already separable. Across the domain model {{EVIDENCE:CIR_DOMAIN_MODEL}} and its coverage balance {{NUMERIC:CIR_DOMAIN_BALANCE}}, the observations are consistent with convolution of the chemical and seismic signatures rather than a one-to-one correspondence. While {{CAVEAT:SMALL_N_SOUTH}} limits inference for the southern and vent-distance subsets, the comparison indicates where the two structures can be tested for separability rather than assumed resolved.

| 축 | 나(blind) | Codex draft |
|---|---|---|
| "provides a test of separability" | ✓ | ✓ |
| already-separable/resolved 거부 | "rather than already separable/assumed resolved" | "Rather than resolving whether separable" |
| convolution framing | ✓ | ✓ |
| domain context가 일반화 제한 | ✓ | ✓ |
| {{CAVEAT}} provisional | ✓ | ✓ |
| interpretive noun(mechanism/regime/driver) | 전부 제거 | 전부 제거 + "spatial check rather than a mechanism" |
| 후보평가(Bold overclaim/Measured 강함/Terse best) | ✓ | **동일** |
→ **2번째 진짜 BLIND 수렴**(take14에 이어). 구조·claim-strength·noun-strip 동일. (차이: Codex가 optional vent-distance placeholder 사용, 나는 미사용 — 둘 다 bounded.)

## 🎯 진단도 독립 수렴 — "noun-level overreach"
Codex report "Interpretation": *"main remaining quality gap is **noun-level overreach**: even when verbs are calibrated, the model can smuggle unsupported interpretation through nouns such as drivers/mechanisms/domains... next prompt adjustment should target unsupported interpretive nouns, not only verb strength."* = **내가 본 것과 정확히 동일**. b503f15가 이걸 operationalize. **verb-ladder 정렬돼도 noun으로 새는 게 다음 frontier**라는 데 독립 합의.

## 권고 — interpretive noun 처리 (내 Q4=B 연장)
mechanism/driver/regime는 **task-의존**(mechanism을 다루는 task면 정당). 따라서 **global hard-gate 금지** → **(a) global diagnostic(b503f15, 지금처럼) + (b) 이 noun을 금지하는 task는 per-task `forbidden_terms`에 선언**(boundary-aware 강제, 이미 있음). 즉 noun overreach도 verb처럼 "diagnostic + 필요시 task-local forbidden" 분업. global denylist로 굳히지 말 것(separability task엔 "mechanism" 금지지만 mechanism-task엔 정당).

## 정직/큐
라이브=repo 밖 temp(take15c copy 재계산·counts only로 blind 보존했다가 conductor 후 report). take15/15b=array-id 실패 보류(정상). take16(discussion) 진행중. 다음: take16+ blind conductor / interpretive-noun을 forbidden_terms로 선언한 run(가드 작동 확인) / evidence-caveat renderer / intro·conclusion.

(manuscript-atelier 커밋0 · 라이브=로컬 temp.)
