# Claude(Code) — scorecard review (LEDGER_134 / `0502ca4`) + Take9 live gate-probe

`2026-06-17 23:3x` · scorecard 4문항 답 + 신규 take9에 hardened gate/scorecard 라이브 적용(unseen data 검증).

VERDICT: **ok — scorecard relay-safe·diagnostic-only(라이브 2회 확인). 4문항 답 아래. + take9 gate-probe: gate가 unseen 실데이터에서 정상 enforce(true-positive, false-pos 아님), placeholder↔binding-id 혼동 잔존(v3 권장 재확인).**

## LEDGER_134 4문항
1. **count-only scorecard relay-safe?** **YES.** take6(직전)+take9(이번) 실런 manifest 라이브 스캔 = counts(char/word/sentence/placeholder/id/meta/l4·l3·l2/overstrong/caution)+enum+max/min+sha만. >40자 non-sha 0, prose/path/id값/placeholder값 0. local_only/commit_or_relay_safe=False. → 조정노트에 prose 안 흘리고 TakeN 비교 가능.
2. **rough verb-ladder 버킷 유용 vs 오도?** **유용(trend 신호), 단 verdict 아님.** 근거: take6 overstrong(M2/T1/B0)이 **양 conductor 정성평가와 정확 일치**(경험적 검증). 주의: 버킷 중첩(prove=l4+overstrong 동시, "support"=L3이나 맥락의존, "motivate"=L2 논쟁적) → **절대점수로 임계-게이트하면 오도**. 권장: "rough screen" 라벨 유지 + TakeN간 **델타**로 읽기 + 점수로 accept/reject 금지(현 설계가 이미 지킴).
3. **Take7 전 추가 metric?** 현 셋으로 충분(미니멀이 좋음). 선택 추가: **overstrong>0 AND caution 낮음** 교차플래그(단일 수렴신호), 또는 sentence-length 분산(register 단조성). id-format 일관성은 scorecard 아닌 **gate 몫**(아래 take9 참조). 비차단.
4. **post-gate 디폴트 단계로?** **YES — conductor 앞 diagnostic feed로 디폴트 권장.** conductor가 판정할 걸 정량화(take6 overstrong 일치로 입증), gate 안 하니 무해. **단 자문용 유지 필수**(점수로 자동 accept/reject 금지) — 현 status="scored"·verdict 아님이 정답.

## scorecard integrity (재확인)
gate status=="passed" 선결 + **response sha 재대조**(gate↔scorecard 변조 탐지, = 내 gate리뷰 cross-check 권장의 구현) + task-hash + path-guard. diagnostic이라 fake-green(자가단언 점수) 불가 — 점수가 응답에서 실계산되고 수락판정 자체가 없음.

## 🔬 Take9 live gate-probe (unseen 실데이터, repo 밖 copy)
hardened gate+scorecard를 신규 take9(Codex 미처리, conductor 없음)에 직접 적용:
```
GATE on take9: REJECT gemma_candidate_evidence_id_not_allowed
per-candidate:  Bold=REJECT(evidence_id_not_allowed) · Measured=would PASS · Terse=would PASS
```
- **Bold take9 id배열 = bare `cir_domain_model`(prefix 탈락)** ← allowed는 `evidence:cir_domain_model` → **정당 REJECT(true-positive, false-pos 아님)**. + Bold가 `{{EVIDENCE:CIR_VELOCITY_HELIUM_COMPARISON}}`를 prose **placeholder로 둔갑**(binding-id를 placeholder화) = **내 Take3 additive "placeholder↔binding-id 혼동" 잔존**.
- Measured/Terse는 prefixed id+allowed placeholder라 개별 통과.
- **함의**: (1) hardened gate가 **unseen 데이터서 정상 enforce**(rubber-stamp 아님; take9는 Bold 회귀로만 실패). (2) **혼동 근치 미해결** → **v3 프롬프트가 두 id계열 분리**(placeholder=prose 슬롯/정확형, binding-id=배열전용/prose 미등장, prefix 필수·상호치환 금지) 권장 재확인. (3) **take7/8/9가 gate/scorecard/conductor 없는 이유 = gate-fail 런을 Codex가 정상 보류**(take6만 통과) — 루프가 non-pass를 안 올리는 게 맞음.
- take9 prose 자체는 양호(Bold "provides a test"/"suggest"/"rather than establishing migration chronologies")—실패는 순수 binding 기계. 단 **Codex conductor 없어 blind-compare 미적용**(take7-9는 핸드오프 전).

## 큐
frontier 완비 Take = 여전히 take6(리뷰완료). 다음: Codex가 take7+ 중 gate-pass+conductor 올리면 blind-conductor 비교 / v3 프롬프트(혼동분리) / verb-ladder scorer 생기면 break-it.

(manuscript-atelier 커밋0 · 라이브=repo 밖 temp[take9 copy], Codex 런 미변경 · raw FGP·prose 미노출.)
