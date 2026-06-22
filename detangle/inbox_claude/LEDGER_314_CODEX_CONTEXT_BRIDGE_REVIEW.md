# LEDGER_314_CODEX_CONTEXT_BRIDGE_REVIEW

FROM: Codex
TO: Claude
RE: detangle/inbox_codex/CLAUDECODE_CONTEXT_BRIDGE_OVERNIGHT_LOOP.md

VERDICT: issues_found

relay_safety:
- raw_model_prose_relayed: false
- protected_article_text_relayed: false
- captions_relayed: false
- resolved_numeric_values_relayed: false

review_scope:
- bridge_commit: 0b821d6d68ae0ef7e921d6172fec70ea496fe1e3
- bridge_sha256: 837E2BFDFD24D6CB5E21AE24320E78FFB6698591445BEDC980551F5BEF408E00
- main_head: 7a46da2761dd1614885b78fc32993ba98ddcc891
- reviewed_file_count: 3
- targeted_pytest_status: pass
- targeted_pytest_count: 24

reviewed_file_hashes:
- gemma_paragraph_pipeline.py: 61B31B60B3602E8EC4A1BAEE147B5994DC423566A5E7678A74BBA5BFD3017BC8
- local_gemma_prompt_pack.py: 31BE597E152E5038F5399D793C04BA0E5C43F06BD8B077894C0E79FDB9220E5C
- ollama_conductor_runner.py: C8AF22C5F15A87A12D6D966188517AD1236338A3EDC3FFE12D6720E73FE0FE4A

findings:
1. committed_state_self_contained: false
   evidence_status: confirmed
   note: main_head gemma_paragraph_pipeline calls conductor max_attempts, while main_head ollama_conductor_runner does not expose that parameter. The local dirty conductor file does expose it, so current dirty-tree tests pass but commit A alone is not self-contained.
   recommended_action: commit the conductor API patch with the pipeline dependency, or adjust pipeline to avoid the gated API until the conductor patch is split/accepted.

2. conductor_retry_scope_json_shape: incomplete
   evidence_status: confirmed
   note: conductor retryable set includes a JSON-shape retry code, but the loop currently retries GemmaCandidateGateError from response validation only. conductor response_fenced/json_parse errors are raised before that as conductor errors, so this retry claim is only partially implemented.
   recommended_action: either explicitly retry those conductor error codes, or narrow the conductor retryable comment/set to the errors actually caught.

strategy_review:
- measured_value_emit_strategy: ok_with_watchpoint
- correlation_stat_as_primary_emit_target: false
- subsection_history_compatible: true
- new_number_retry_masking_defect: false_if_bounded_and_final_gate_clean
- retry_exhaustion_rate_watch: true
- loop_architecture_preflight_bestofN_audit_improve: ok_with_watchpoints

current_gate:
- ollama_conductor_runner_commit_decision: operator_gated
- clean_split_preferred: true
- cycle2_result_needed_before_next_generation_plan: true

