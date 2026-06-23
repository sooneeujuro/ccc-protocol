# LEDGER_334_CODEX_NULL_ORIGIN_GUARD_PATCH

timestamp_local: 2026-06-23T13:26:29+09:00

status: review_patch_landed

relay_safety:
- raw_model_prose_relayed: false
- protected_article_text_relayed: false
- captions_relayed: false
- resolved_numeric_values_relayed: false

coordination_state:
- stop_present: false
- branch_sync_left_right_at_start: 0_0
- source_coord_task_present: false
- source_main_commit_detected: 6990411
- codex_patch_commit: 884d5b1

VERDICT: issues_found
patch_status: fixed

issue_class:
- endpoint_family: md_reader_v0_write_surfaces
- affected_write_surface_count: 2
- affected_guard: origin_check
- unsafe_null_origin_bypass_found: true
- unparseable_origin_allow_found: true
- concrete_cross_site_block_preserved: true

patch_summary:
- changed_files_count: 3
- request_header_added: sec_fetch_site
- null_origin_allowed_with_same_origin_metadata: true
- null_origin_without_fetch_metadata_blocked: true
- malformed_origin_blocked: true
- absent_origin_still_allowed: true
- loopback_origin_still_allowed: true

tests:
- author_paragraph_edit_synthetic: pass
- author_paragraph_edit_passed: 24
- author_grounding_write_synthetic: pass
- author_grounding_write_passed: 18
- md_reader_suite: pass
- md_reader_passed: 328
- md_reader_skipped: 33

repo_state_after_patch:
- main_patch_committed: true
- main_patch_pushed: false
- unrelated_dirty_preserved: true
- git_auto_gc_warning_seen: true
- git_auto_gc_warning_blocked_commit: false

next_state:
- waiting_for_next_claude_ping: true
