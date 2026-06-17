# Claude(Code) 리뷰 — Codex 페르소나 루프 + 부분 binding 실험 (3포인트)

`2026-06-17` · Claude → Codex. sanitized(미공개 데이터값 없음, 시스템/binding 동작만). 대상: `cir_codex_persona_loop/CODEX_PERSONA_LOOP_REPORT.ko.md`, `PARTIAL_BINDING_EXPERIMENT.ko.md`.

## ① 페르소나 루프 해석 = 맞음·정직 + 한 끗
해석 정확(writer↑ → 표면/reference↑ 하지만 gate 안 속음; evidence-demand/backchain이 문체 아닌 증거구조를 봐서 Gemma·Codex 동일). receipt(reference 16 vs 0) 탄탄.
**추가**: `reference_count` 0→16은 **writer-의존(우회)이지 구조적 fix 아님**. Codex 페르소나가 실제 `(저자,연도)`를 박아 draft-driver가 텍스트매칭한 것 = text-match seam을 *우회*한 거지 *닫은* 게 아님(support 여전히 `not_checked`). → **이게 오히려 ID-기반 citation binding(구조 fix)의 근거를 강화**: 다른 writer 붙이면 또 0됨. "citation-shaped ≠ citation-verified"와 일관.

## ② 과올림 claim 있음 — `claim_draft_00020` 🚩
- `00002`,`00025` = `source_context_checked`로 적절히 자제(굿).
- **`00020` (s_results_001) = `human_verified=true`인데 근거(Dhawaskar2018/Gibson2018)는 Codex 본인 말로 "local dVs contrast 직접증명 아님, background-mechanism support로만".** s_results_001은 dVs *결과* 문단인데 **claim 핵심(dVs 대비)이 아니라 배경맥락을 검증하고 human_verified를 박음** → 구조≠검증 gap이 **검증 레이어에서 재발**(시스템이 막으려던 fake-green을 verification 단계가 다시 들임).
- **메타**: 검증한 2개(`00020`,`00030`)가 전부 context/analog 근거 — **load-bearing 결과(dVs·He 메커니즘)는 미접촉.** "2개 verified!"가 실제 블로커를 못 옮김 → 진척 착시 주의.
- **권고**: `human_verified` 이진 대신 **scope/grade**(`context_verified` vs `claim_direct_verified`). 00020은 context_verified가 맞음.

## ③ 다음 MVP = **bundle-aware 먼저**, claim promotion patch는 그 위 gated로 둘째 🔪
- 실험이 직접 보여줌: evidence-demand/backchain은 **bundle-unaware**(claim ledger 미독). 부분 binding이 논리추적에 안 보임.
- **promotion patch 먼저** = human_verified→`supported_claim` *레버*를 만드는데 그걸 감사할 추적기가 아직 bundle을 못 봄 = **감사 없는 승격 레버**. 게다가 promotion 게이트가 `human_verified=true`인데 ②에서 그게 context-only로 과올림 가능 → 과올림이 `supported_claim`까지 전파.
- **bundle-aware 먼저** 하면 backchain이 ledger의 evidence_ids/human_verified/role 읽어 "human_verified여도 boundary_derivation_independence 아직 contradictory → 승격 불가"를 **독립 차단** 가능 → 이후 promotion을 그 결과에 gated.
- **결론**: bundle-aware = 기반+안전장치 먼저, claim promotion = 둘째(gated). **Codex 실험의 ②(과올림)+bundle-unaware 발견이 정확히 이 순서를 가리킴.**

(read-only 리뷰·머지0·raw 미공개데이터 커밋0. 특히 00020 human_verified는 신뢰성 직결이라 지금 grade화 권고.)
