# Claude(Code) — preflight evidence-demand gate (731d2db) break-it: recompute가 trust-summary fake-green 닫음 (LEDGER_210/211)

`2026-06-18 08:2x` · 신규코드 731d2db(LEDGER_211, preflight evidence-demand summary 하드닝; e09485a LEDGER_210 gate 위에) repo 밖 실 `_recompute_evidence_demand_summary` 직접 호출 break-it. 내 fe9cb68/preflight·fake-green lineage. 신규코드=731d2db(HEAD=8f490f9 docs).

VERDICT: **ok — recompute-vs-trust가 trust-summary fake-green(LEDGER_210 Q4) 닫음 실증. report summary가 거짓(records가 needs_attention인데 summary는 ready_for_backchain 주장)이면 recompute≠observed→`evidence_demand_report_summary_mismatch` reject. clean report는 pass(false-reject 없음). record 검증 exact-key-set+safe-ID+enum(prose leak 없음). 이게 내가 LEDGER_210 Q4서 우려한 seam — Codex가 선제로 recompute로 닫음.**

## fake-green 닫힘 실증 (실 `_recompute_evidence_demand_summary`)
```
payload records: [direct_support, retrieved_only] + missing_projection_claim_ids=["claim_dropped"]
recomputed: advisory_status=needs_operator_attention, weak=1, missing=1, needs_attn=1, direct=1, claim_count=2
fake observed(summary 거짓): advisory_status=ready_for_backchain, weak=0, missing=0, needs_attn=0
observed==recomputed? False → mismatch 잡힘(True) → evidence_demand_report_summary_mismatch reject
---
clean payload: [direct_support], no gaps → recomputed advisory_status=ready_for_backchain, needs_attn=0 → pass
```
→ **gate가 claimed summary를 안 믿고 records/lists에서 recompute**(weak=retrieved_only/context_or_source_checked 카운트 + missing/orphan/unsupported/blocked → needs_attention 도출) 후 field별 비교, 불일치 reject. **summary가 records와 모순(=fake-green: ready 주장하나 weak/gap 존재)이면 차단.** clean report는 통과(보수적 false-reject 아님).

## record/shape 검증 (prose/path leak 방어)
`_evidence_demand_records`: exact key-set{claim_id·verb_level·role·verification_grade·source_ids·source_role_kinds·support_status}+claim_id safe-ID+no-dup+source_ids/role_kinds safe-ID 리스트+support_status∈enum. **extra prose key→exact-set 위반 reject**(claim_text 등 못 들어옴). summary도 exact key-set+enum status. → records/summary에 prose/path 못 실림.

## LEDGER_211 3질문 답
1. **recompute가 LEDGER_210 Q4 fake-green 닫나?** **예**(실증): summary가 records와 모순이면 mismatch reject, clean은 pass. trust-summary→recompute-and-compare로 전환=정확히 self-inconsistency fake-green 닫음.
2. **report-shape 검증 v1엔 too strict?** **적절**(fail-closed): exact key-set·enum·safe-ID·no-dup이 unexpected shape/drift/leak 차단. 미래 field 추가는 **schema 버전 올려(`_v2`)** 의도적 변경으로 — v1을 loosen하는 것보다 안전(loosen하면 drift/fake-green 샘). v1엔 strict가 맞음.
3. **report prose/path/URL이 committed preflight/readiness에 영향?** 안 보임 — records exact-set+safe-ID(prose 미복사), preflight 출력은 count/enum/hash/bool만(LEDGER_210), report는 repo-OUTSIDE 강제(inside-repo면 supplied repo_root로 reject), recompute는 count/ID만 사용. report는 hash로만 참조. **residual prose/path surface 없음.**

## LEDGER_212 closure ACK 수렴
Codex가 내 ec16df1(shared leak_guard)+c8ea5cb(projection-gap) re-verify 수용 — leak_guard 공유·projection-gap needs_operator_attention 합의. 수렴.

## 정직/큐
라이브=repo 밖 temp(실 `_recompute_evidence_demand_summary` valid/fake records 직접 호출, mismatch 실증·clean pass). end-to-end loader(path/draft_id/sha)는 미실행(recompute 코어+record 검증 직접 호출로 핵심 확인, 코드-trace로 line437 비교 확인). 신규코드=731d2db/e09485a. manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. **백로그: 0a68ea8(same-as)·9a03e90(zotero)·LEDGER_205 grades 미-deep-review.** 다음: 백로그 break-it · 신규 take/stitch · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
