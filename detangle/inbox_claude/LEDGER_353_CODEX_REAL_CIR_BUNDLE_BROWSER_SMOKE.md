# LEDGER_353_CODEX_REAL_CIR_BUNDLE_BROWSER_SMOKE

STATUS: real_bundle_browser_smoke

STOP: absent

NEW_CLAUDE_PING_AFTER_LEDGER_352: false

MAIN_REPO_HEAD_MD_READER: 8b631b59a80fdf14699ea54dc20a986cc6747ca2

READER_INTERACTIONS_BLOB: 7016e41348ac964edd89f3f98440201611da7b2f

REAL_BUNDLE_MANIFEST_SHA256: 5233F333F27C196BB82B722BBCCC8B1718051ED06D2948AFE244E2E60A0C9415

REAL_BUNDLE_LOAD:
- load_status: pass
- paragraphs: 9
- claims: 41
- evidence_packets: 31
- numeric_entries: 0

ROUTE_FUNCTION_SMOKE:
- get_root_status: 200
- get_safe_summary_json_status: 200
- get_safe_summary_txt_status: 200
- get_reader_interactions_js_status: 200
- get_healthz_status: 200
- root_fsection_count: 1
- root_data_section_count: 50
- root_fold_token_count: 8
- root_snippet_packet_count: 31
- root_forbidden_snippet_present_count: 0
- safe_summary_schema_present: true

HEADLESS_CHROME_REAL_BUNDLE_SMOKE:
- runtime_exception_count: 0
- log_error_count: 1
- log_error_favicon_only: true
- section_option_count: 5
- initial_visible_issues: 41
- initial_visible_paragraphs: 9
- selected_section_visible_issues: 9
- selected_section_hidden_issues: 32
- selected_section_visible_paragraphs: 2
- selected_section_hidden_paragraphs: 7
- clear_restored_visible_issues: 41
- clear_restored_visible_paragraphs: 9
- fold_checkbox_count: 3
- fold_checked_body_display_none: true

VERIFY:
- cited_source_snippet_guard_tests_status: pass
- cited_source_snippet_guard_tests_passed: 19
- cited_source_snippet_guard_tests_skipped: 5

VERDICT: ok

NEXT_EXPECTED_ACTION:
- wait_for_operator_phase2_decisions_or_new_claude_ping
