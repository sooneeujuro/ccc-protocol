# CODEX_PING51_DOI_SCOUT_HANDOFF_TO_CLAUDE

timestamp_kst: 2026-06-26
author: Codex
recipient: Claude
relay_safety: counts/status/hash/boolean_only
purpose: request Claude multi-agent candidate scouting for remaining DOI gaps; Codex remains single-writer gate

## Coordination State

- stop_local_present_at_start: false
- ccc_branch_expected: coop/detangle-20260615
- corpus_root: G:/corpus_20260626
- corpus_payload_text_relayed: false
- protected_text_relayed: false
- raw_model_prose_relayed: false
- resolved_numeric_values_relayed: false
- sidecar_write_by_claude_requested: false
- final_sidecar_writer: Codex/local deterministic gate only
- reindex_started: false
- mcp_flip_started: false

## Current DOI State

- sidecar_count: 3996
- doi_nonempty_count_current: 3174
- doi_missing_count_current: 822
- missing_pid_list_sha256_prefix: f3d557628d6cf167
- variables_reported_count: 3996
- archive_space_gate_status: cleared_by_operator
- reindex_space_available: true
- reindex_should_wait_for_doi_gate: true

## Backfill Already Applied

- preexisting_or_model_doi_count_before_backfill: 1914
- claude_body_regex_added_count: 833
- codex_local_article_pdf_added_count: 1
- codex_crossref_high_confidence_added_count_current: 426
- doi_nonempty_after_all_applied_count: 3174
- remaining_missing_after_all_applied_count: 822

## Codex Local Artifacts

- local_reconcile_script_path: C:/Users/USER/Documents/_codex_runs/corpus_0626_doi_backfill/local_doi_reconcile_pass.py
- local_reconcile_script_sha256_prefix: af02fde53de20d81
- local_reconcile_safe_path: C:/Users/USER/Documents/_codex_runs/corpus_0626_doi_backfill/local_doi_reconcile.safe.json
- local_reconcile_safe_sha256_prefix: fc3fe669ab2063a4

- crossref_parallel_script_path: C:/Users/USER/Documents/_codex_runs/corpus_0626_doi_backfill/crossref_doi_backfill_parallel.py
- crossref_parallel_script_sha256_prefix: 3f468ec2b31dce0a
- crossref_parallel_safe_path: C:/Users/USER/Documents/_codex_runs/corpus_0626_doi_backfill/crossref_parallel.safe.json
- crossref_parallel_safe_sha256_prefix: 5aaad0a65bbece19

## Observations

- doi_was_prompted_but_not_gated: true
- doi_absence_is_contract_failure_not_model_quality_only: true
- haiku_sidecar_prompt_had_doi_field: true
- build_0626_had_no_required_doi_reconcile_gate: true
- flat_article_markdown_exact_doi_remaining_count_low: true
- local_pdf_first_pages_unique_doi_remaining_count_low: true
- crossref_high_confidence_path_productive: true
- crossref_rate_or_timeout_errors_observed: true

## Request To Claude

Please use multi-agent scouting to find candidate DOI/status for the remaining 822 missing sidecars.

Do not write sidecars directly.
Do not emit protected text, article snippets, captions, or resolved numeric values.
Public DOI candidate values are acceptable in a local candidate artifact if needed, but avoid relaying them in coordination notes; ledger should remain counts/status/hash.

Suggested output artifact:

- path: detangle/sidecar_test_sonnet/DOI_SCOUT_CANDIDATES_claude.local.json
- record grain: one record per remaining pid
- fields:
  - pid
  - candidate_doi
  - candidate_source: crossref|openalex|publisher|pdf_metadata|article_text|none_found|manual_review
  - confidence: high|medium|low|none
  - evidence_type: metadata_match|title_year_author_match|doi_in_source_metadata|doi_in_article_text|no_doi_found|ambiguous
  - needs_manual_review: boolean
  - absence_reason_if_none: no_crossref_hit|book_or_chapter|report_or_thesis|korean_local_publication|legacy_no_doi|metadata_ambiguous|unknown
  - title_match_score_if_available
  - year_match: true|false|null
  - author_match: true|false|null

Suggested safe summary artifact:

- path: detangle/sidecar_test_sonnet/DOI_SCOUT_CANDIDATES_claude.safe.json
- include only counts/status/hash/boolean:
  - input_missing_count
  - high_confidence_candidate_count
  - medium_confidence_candidate_count
  - needs_manual_review_count
  - none_found_count
  - ambiguous_count
  - candidate_local_sha256_prefix
  - public_doi_values_relayed_in_ledger: false

## Acceptance Contract For Codex Gate

- Codex will apply only high-confidence candidates after deterministic normalization.
- Codex will reject duplicate DOI collisions unless explicitly same-work duplicate.
- Codex will preserve before/after sidecar sha256 prefixes.
- Codex will add doi_backfill source metadata.
- Codex will generate safe ledger before reindex.

## Next After Candidate Handoff

- Codex gate applies accepted DOI candidates.
- Codex assigns doi_status for all remaining unresolved sidecars.
- Then retrieval_units -> BM25 -> BGE can run.
- .mcp flip stays after successful reindex and operator go.
