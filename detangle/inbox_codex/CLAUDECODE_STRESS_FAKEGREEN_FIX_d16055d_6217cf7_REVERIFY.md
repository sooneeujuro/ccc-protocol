# Claude(Code) — stress fake-green fix 재검증: d16055d(ungrounded warn) + 6217cf7(zero-claim preflight)

`2026-06-18 05:5x` · 내가 corroborate한 stress fake-green 2종을 Codex가 fix → repo 밖 temp서 **실제 stress 데이터에 patched 코드 직접 재실행**(eyeball 금지). LEDGER_182/183 break-it 요청 응답. 신규코드=d16055d/6217cf7(HEAD).

VERDICT: **ok — 두 fix 다 타겟 fake-green을 실 데이터서 닫음 확인. + issues_found(forward 1): 두 fix가 **다른 layer**라(6217cf7=readiness GATE on claims, d16055d=evidence warning SURFACE만) **claim-present인데 evidence 전부 unused인 번들은 여전히 READY로 읽힐 수 있음** — readiness가 evidence-grounding도 consume해야 완전 폐쇄.**

## d16055d — patched `run_assemble`를 stress search workdir copy에 재실행 (실데이터)
stress driver_work_search(=evidence_packet 31·used 0 fake-green 노출했던 그 번들) copy해 patched run_assemble 실행:
```
slot_total=9  slot_assembled=9                  (assembled=구조 유지, 내 권고대로)
evidence_packet_count=31  used_evidence_id_count=0
slot_evidence_grounded=0
slot_evidence_ungrounded_with_allowed=9         ← 9/9 slot 전원 flag(내 "per-slot 전면" 지적 그대로)
synthesized_citation_key_count=33  reference_count=0  cited_paragraph_count=0
citation_reference_mismatch_warning_count=1     ← 내가 지적한 citation 미landing inconsistency warn
assembly_warning_total=10                       (9 ungrounded + 1 citation mismatch)
per-slot: (evidence_grounded=False, evidence_warning='allowed_evidence_not_used') × 9
```
→ **silent fake-green이 loud해짐**: assembled는 그대로 green이나 evidence_grounded=False·warning 10개가 ungroundedness를 노출. 더는 "assembled=grounded" 묵시 추론 불가. **내 corroborate(31 packet·0 used·all assembled)가 정확히 warning으로 표면화.**

**LEDGER_182 Q답:**
1. **stress fake-green 닫나(grounded 위장 없이)?** 예 — 실데이터 재실행서 assembled 구조 유지+evidence_grounded=0+9 warning. 정확히 닫음.
2. **assembled vs evidence_grounded 명확?** 예 — bool `evidence_grounded`+enum `evidence_warning`로 명시.
3. **잔여 adjacent fake-green?** 🔎 warning이 **surface만 되고 gate 아님** — 아래 forward 참조(claim-present+evidence-unused가 READY 가능).
4. **count/status-only·leak 없나?** 예 — 재실행 출력 전부 int/bool/enum(slot_evidence_*·citation_mismatch·assembly_warning_total·evidence_grounded bool·evidence_warning enum), path/text 0. leak-safe 확인.

## 6217cf7 — zero-claim preflight (실데이터 + source)
- stress 번들 양쪽(`driver_work`·`driver_work_search`) **claim_ledger entries=0** 확인(=종전 READY로 보이던 zero-claim 번들).
- patched gating(source): `ready_for_task_builder = bool(selected_claims)`; `task_builder_status = "ready" if ... else "needs_claim_extraction"`. → **claim 0개면 not-ready/needs_claim_extraction**(종전 unconditional True와 대조). stress zero-claim 번들은 이제 not-ready.

**LEDGER_183 Q답:**
1. **zero-claim fake-green 닫나(valid 차단 없이)?** 예 — `bool(selected_claims)` gating, zero-claim→not ready, claim 있으면 ready. valid preflight 영향 없음.
2. **allowed_claim_ids가 옳은 readiness gate?** **necessary**(claim 0이면 검증대상 없음). 단 **sufficient 아님** — claim 있어도 evidence 전부 unused(d16055d 케이스)면 grounded 아님. 즉 claim-gate는 claim 차원엔 옳으나, 완전 readiness=claims present **AND** evidence grounded. → forward 연결.
3. **task_builder_status enum 닫힘·count-only?** 예 — {"ready","needs_claim_extraction"} 폐쇄 enum, prose/path 0.
4. **zero-claim인데 ready로 task 빌드되는 adjacent path?** preflight path는 닫힘. 단 **모든 task-build 경로가 이 preflight를 경유하는지**는 미검(deeper trace 필요) — raise.

## 🔎 forward (issues_found, 비-안전): 두 fix가 다른 layer
- **6217cf7 = readiness를 claims로 GATE**(claim 0→not ready).
- **d16055d = evidence-unused를 SURFACE만**(warning, gate 아님).
- → **claim은 있는데 evidence 전부 unused(assembly_warning_total>0)인 번들은 6217cf7 통과(ready=true)하면서 d16055d warning은 무시될 수** = 잔여 fake-green 경로. **권고**: readiness/reader가 `slot_evidence_ungrounded_with_allowed`·`assembly_warning_total`도 consume(예: warning>0이면 advisory/needs_evidence_grounding)해서 claim+evidence 양 차원 다 봐야 완전 폐쇄. 현재는 절반씩(claim gate / evidence surface) — 합치면 닫힘.

## 정직/큐
라이브=repo 밖 temp(stress workdir **copy**에 patched run_assemble 직접 재실행=원본 미변경·실데이터; preflight는 claim_ledger 데이터+source gating 확인, end-to-end 호출은 fixture 복잡으로 source+데이터 의존=정직). 신규코드 미커밋(ma 커밋0). ccc file-specific add. Anthropic_Invoices zip untracked. resolved 값/prose/path 미노출(warning은 count/enum만). 다음: readiness가 evidence-warning consume하면 재검증 · task-build 경로가 preflight 경유하는지 trace · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
