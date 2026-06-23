# LEDGER_351_CODEX_FRONTEND_BOUNDARY_SMOKE

STATUS: quiet_frontend_boundary_probe

STOP: absent

NEW_CLAUDE_PING_AFTER_LEDGER_350: false

MAIN_REPO_HEAD_MD_READER: 6f21e2f993126da5cc1db396269ff97beda836e5

CODEX_MAIN_REPO_PATCH_APPLIED: false

BLOB_HASHES:
- tools/paper-orchestra/md-reader/v0/reader_interactions.js: fd3b849fa48cdfd66a8aa6f2865798362a02b563
- tools/paper-orchestra/md-reader/v0/local_ui.py: fc64c31c9f3b4fd4c3114abf29e0927e2cad9667
- tools/paper-orchestra/md-reader/v0/ui_render.py: f0e82fb4c149674b7ed01abc9a4827474d0f4ad5

STATIC_BOUNDARY_SCAN:
- fetch_hits_runtime_files: 0
- xmlhttprequest_hits_runtime_files: 0
- websocket_hits_runtime_files: 0
- eventsource_hits_runtime_files: 0
- sendbeacon_hits_runtime_files: 0
- indexeddb_hits_runtime_files: 0
- eval_hits_runtime_files: 0
- new_function_hits_runtime_files: 0
- storage_cookie_hits_are_docstring_only: true
- loopback_url_print_expected: true
- local_script_asset_expected: true

JS_ASSET_ROUTE_CHECK:
- get_reader_interactions_status: 200
- content_type_javascript: true
- body_len: 26073
- js_fetch_count: 0
- js_xmlhttprequest_count: 0
- js_websocket_count: 0
- js_localstorage_count: 0
- js_sessionstorage_count: 0
- js_eval_count: 0

ROOT_SCRIPT_CHECK:
- script_src_total: 1
- remote_script_src_count: 0
- local_reader_interactions_src_count: 1

VERIFY:
- reader_interactions_js_syntax: pass
- local_ui_py_compile: pass
- ui_render_py_compile: pass
- focused_interaction_local_ui_section_tests_status: pass
- focused_interaction_local_ui_section_tests_passed: 85
- focused_interaction_local_ui_section_tests_skipped: 16
- focused_route_boundary_tests_status: pass
- focused_route_boundary_tests_passed: 29
- focused_route_boundary_tests_skipped: 1

VERDICT: ok

NEXT_EXPECTED_ACTION:
- wait_for_operator_phase2_decisions_or_new_claude_ping
