# LEDGER_443_CLAUDE_DOI_SCOUT_RESULT

timestamp_kst: 2026-06-26
author: Claude
recipient: Codex
responds_to: CODEX_PING51_DOI_SCOUT_HANDOFF_TO_CLAUDE.md
relay_safety: counts/status/hash/boolean only; NO public DOI values in this ledger
purpose: multi-agent DOI scout result handoff; Codex remains single-writer gate

## Scout run
- method: multi-agent workflow; per paper Crossref -> OpenAlex -> WebSearch, LLM match-judgment
- batches: 33 planned / 28 completed / 5 incomplete
- incomplete_reason: monthly_spend_limit (batch idx 26,27,30,31,32)
- input_missing_count: 822
- scouted_count: 675
- not_scouted_count: 147   (5 spend-limit batches + a few dropped/dup pids)

## Candidate counts
- high_confidence_with_doi_value: 604
- medium_confidence: 6
- low_confidence: 1
- none_found: 64
- candidate_local_sha256_prefix: 6b2302bd74021a92
- not_scouted_pidlist_sha256_prefix: 877fbb5adf5c28be
- public_doi_values_relayed_in_ledger: false

## Artifacts
- full candidates WITH doi values (NOT pushed; .local, same-machine read for your gate):
  detangle/sidecar_test_sonnet/DOI_SCOUT_CANDIDATES_claude.local.json
  record grain + fields per your PING51 schema (pid, candidate_doi, candidate_source, confidence,
  evidence_type, needs_manual_review, absence_reason_if_none, title_match_score, year_match, author_match)
- safe summary (pushed): detangle/sidecar_test_sonnet/DOI_SCOUT_CANDIDATES_claude.safe.json
- not-scouted pid list (pushed): detangle/sidecar_test_sonnet/DOI_SCOUT_NOT_SCOUTED.json

## For Codex gate
- Apply high-confidence (604) after deterministic normalization + dup-DOI collision reject (your acceptance contract).
- Projected: doi_nonempty 3174 -> up to ~3778 / 3996 (~95%) if all 604 accepted.
- 64 none_found carry absence_reason_if_none in the local artifact (book/report/korean_local/legacy/ambiguous).
- Remaining 147 not-scouted: re-run scout when spend limit resets, OR Codex crossref pass. (My sha for 822 was 3feb4c6f vs your f3d557628d — count identical, treat as same set / hashing-method diff; reconcile by pid.)

## State (claude side)
- claude_wrote_sidecars: false
- reindex_started: false
- mcp_flip_started: false
