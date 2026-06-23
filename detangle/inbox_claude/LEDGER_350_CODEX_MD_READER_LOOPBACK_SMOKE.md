# LEDGER_350_CODEX_MD_READER_LOOPBACK_SMOKE

STATUS: quiet_smoke_probe

STOP: absent

NEW_CLAUDE_PING_AFTER_LEDGER_349: false

MAIN_REPO_HEAD_MD_READER: 6f21e2f993126da5cc1db396269ff97beda836e5

CODEX_MAIN_REPO_PATCH_APPLIED: false

SYNTHETIC_BUNDLE_COUNTS:
- paragraphs: 4
- claims: 6
- evidence_packets: 7

ROUTE_FUNCTION_SMOKE:
- get_root_status: 200
- head_root_status: 200
- get_safe_summary_json_status: 200
- get_safe_summary_txt_status: 200
- get_healthz_status: 200
- root_fsection_count: 1
- root_data_section_count: 10
- root_fold_token_count: 8
- root_forbidden_snippet_present_count: 0
- safe_summary_schema_present: true

LOOPBACK_HTTP_SMOKE:
- temporary_server_started: true
- temporary_server_stopped: true
- get_healthz_status: 200
- get_root_status: 200
- get_root_cache_control_no_store: true
- get_root_fsection_count: 1
- get_root_fold_token_count: 8
- get_safe_summary_json_status: 200
- get_safe_summary_json_cache_control_no_store: true
- get_safe_summary_json_schema_present: true
- head_root_status: 200
- head_root_cache_control_no_store: true

VERDICT: ok

NEXT_EXPECTED_ACTION:
- wait_for_operator_phase2_decisions_or_new_claude_ping
