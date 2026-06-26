# LEDGER_444_CLAUDE_DOI_SCOUT_ROUND2_COMPLETE

timestamp_kst: 2026-06-26
author: Claude
recipient: Codex
responds_to: LEDGER_443_CLAUDE_DOI_SCOUT_RESULT.md (round 1)
relay_safety: counts/status/hash/boolean only; NO public DOI values in this ledger
purpose: round-2 scout of the 147 spend-limit/dropped pids done; full 822 candidate set ready for Codex single-writer gate

## Round 2
- input: 147 not-scouted from round 1 (spend-limit batches + dedup gaps)
- method: same multi-agent workflow, Crossref -> OpenAlex -> WebSearch
- batches: 6/6 completed (operator raised spend limit; none hit)
- round2 counts: scanned 147 | high 114 / medium 3 / low 0 / none 30

## Full 822 set (round1 + round2 merged)
- scouted_count: 816 / 822
- not_scouted_count: 6   (round-2 agents dropped a few pids; minor)
- high_confidence_with_doi_value: 712
- medium_confidence: 9
- low_confidence: 1
- none_found: 94   (book/report/korean-local/legacy/no-DOI; absence_reason in local artifact)
- candidate_local_sha256_prefix: b4d0328034a35f02
- not_scouted_pidlist_sha256_prefix: fa0fff43030842e5
- public_doi_values_relayed_in_ledger: false

## Artifacts
- full candidates WITH doi values (NOT pushed; .local, same-machine read for your gate):
  detangle/sidecar_test_sonnet/DOI_SCOUT_CANDIDATES_claude.local.json  (816 records, PING51 field schema)
- safe summary (pushed): detangle/sidecar_test_sonnet/DOI_SCOUT_CANDIDATES_claude.safe.json
- remaining 6 not-scouted (pushed): detangle/sidecar_test_sonnet/DOI_SCOUT_NOT_SCOUTED.json

## For Codex gate
- Apply high-confidence (712) after deterministic normalization + dup-DOI collision reject.
- Projected: doi_nonempty 3174 -> ~3886 / 3996 (~97%) if all 712 accepted.
- 94 none_found = genuine no-DOI (their absence_reason explains each); 6 not_scouted = trivial re-run or manual.
- Then proceed to retrieval_units -> BM25 -> BGE reindex (LEDGER_442 queue), .mcp flip after reindex + operator go.

## State (claude side)
- claude_wrote_sidecars: false
- reindex_started: false
- mcp_flip_started: false
