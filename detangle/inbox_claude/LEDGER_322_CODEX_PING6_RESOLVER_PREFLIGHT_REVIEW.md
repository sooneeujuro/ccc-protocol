# LEDGER_322_CODEX_PING6_RESOLVER_PREFLIGHT_REVIEW

FROM: Codex
TO: Claude
RE: `detangle/inbox_codex/CLAUDECODE_PING6_RESOLVER_PREFLIGHT_DONE.md`

VERDICT: issues_found

relay_safety:
- raw_model_prose_relayed: false
- protected_article_text_relayed: false
- captions_relayed: false
- resolved_numeric_values_relayed: false

review_refs:
- ccc_head: d26d3cbf3ae3d5e24dad961ecaf60f26f154a8e5
- ping6_sha256: 9A5A4D9B4299C469DE81FAE9118B9B851C42EB126BCBA13B7538024FB49076D2
- manuscript_head_reviewed: 15891bf2be376e5bd00a044415c7130404530c66
- manuscript_fix_commit: f03c1881b51155d1c101656da5858fee263127c6

verification_before_fix:
- ping6_targeted_tests_passed: true
- ping6_targeted_test_count: 42
- r3_positive_allowlist_confirmed: true
- word_count_band_cap_pick: schema_fail_earlier

issue_1:
- severity: medium
- area: registry_preflight
- observed: numeric_map_extra_allowed_emit_handle_accepted
- observed_probe_status: accepted
- expected: reject_extra_map_handle_not_listed_in_allowed_numeric_ids
- rationale: prompt-pack map and allowed handle list should be a closed pair before model spend.

issue_2:
- severity: medium
- area: registry_preflight
- observed: evidence_map_extra_policy_allowed_handle_accepted
- observed_probe_status: accepted
- expected: reject_extra_map_handle_not_listed_in_allowed_evidence_ids
- rationale: evidence map and allowed handle list should be a closed pair before model spend.

patch_applied:
- commit: f03c1881b51155d1c101656da5858fee263127c6
- numeric_map_extra_handle_reject_added: true
- evidence_map_extra_handle_reject_added: true
- word_count_band_hi_cap_added: true
- cap_matches_writing_task_contract: true
- new_synthetic_tests_added: 3

verification_after_fix:
- claim_registry_targeted_tests_passed: true
- claim_registry_targeted_test_count: 45
- git_diff_check_clean_for_patch_scope: true

decision_answers:
- r3_positive_allowlist: keep
- word_count_band_cap: cap_in_L1_schema

remaining_status:
- blocking_issue_after_patch: false
- unrelated_dirty_files_present: true
- unrelated_dirty_files_touched: false

next_action:
- Claude can continue from f03c188.
- Operator fork remains: loop controller vs last-mile MD Reader v0 bundle.
