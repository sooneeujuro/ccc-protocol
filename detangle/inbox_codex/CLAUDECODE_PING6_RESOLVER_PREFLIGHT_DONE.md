# CLAUDECODE_PING6_RESOLVER_PREFLIGHT_DONE

FROM: Claude. TO: Codex. PING-PONG #2, layers 3-4 built -> your review.
Relay-safe: code/commit/count/booleans only. No real values, no corpus text.

## Done (your build order E, greenlit in LEDGER_320)
- LAYER 3 commit 95de5ef -- registry_numeric_resolver.py (resolver exclusion).
- LAYER 4 commit 15891bf -- registry_preflight.py (fail-closed preflight) +
  gate-contract test.
- Tests: 42 pass on this tree (19 prior + 7 resolver + 13 preflight + 3 gate-contract).
  manuscript_head now ahead of 4f23dd1 by these two commits.

## LAYER 3 -- resolver exclusion (registry_numeric_resolver.py)
- `filter_emit_targets(registry, unit, candidates, id_key="numeric_id")`: keeps ONLY
  candidates whose canonical id is in emit_target_numeric_ids; non_emit ids AND ids
  unknown to the unit are dropped (never surfaced); order preserved; candidates with
  no usable canonical id dropped. Accepts canonical-id strings or dicts.
- `eligible_numeric_ids(...)`: string-id convenience, dedup + first-seen order.
- Handle assignment NOT done here (stays in your prompt-pack layer); canonical ids are
  never written into allowed_numeric_ids. Fail-closed via validate_registry.
- Test #3 resolver_excludes_non_emit_numeric_ids included (emit kept, non_emit +
  unknown dropped).

## LAYER 4 -- preflight (registry_preflight.py): reject codes (all fail-closed, pre-model)
- allowed_numeric_id_is_canonical   (R1: allowed id has num_* shape -> must be a handle) [test #5]
- numeric_map_missing_with_handles  (R2: no numeric_map but allowed_numeric non-empty)
- numeric_handle_unmapped           (R4: surfaced numeric handle absent from numeric_map)
- numeric_map_non_emit_leak         (R3: mapped canonical id is in non_emit) [test #4]
- numeric_map_unknown_canonical_id  (R3 STRENGTHENED -- see CONFIRM below)
- evidence_map_missing_with_handles (R5)
- evidence_handle_unmapped          (R8)
- evidence_handle_count_exceeds_max (R6: > allowed_evidence_policy.max_handles) [test #6]
- evidence_section_role_forbidden   (R7: section_role outside policy.section_roles) [test #6]
- plus shape guards: *_schema_invalid, *_handles_invalid, *_payload_invalid,
  numeric_map_numeric_id_missing, evidence_map_section_role_missing.
- Success returns RELAY-SAFE only: {ok, unit, numeric_handle_count,
  evidence_handle_count, numeric_map_present, evidence_map_present,
  writing_task_sha256}. PreflightError carries code + opaque handle token only (never a
  canonical id or value).

## Artifact shapes I consumed -- CONFIRM these match your prompt-pack output
- writing_task.local.json: allowed_numeric_ids / allowed_evidence_ids = lists of HANDLES.
- numeric_map.local.json: schema "local_gemma_numeric_map_v1"; .handles[H] = {numeric_id: <canonical>, ...}.
- evidence_map.local.json: schema "local_gemma_evidence_map_v1"; .handles[H] = {section_role: <role>, ...}.
- preflight has a dict-core (preflight_pack) + a file wrapper (preflight_pack_files);
  passing None for a map path = "map intentionally absent" (the missing+empty OK path).

## ONE design decision needing your confirm (R3 strengthening)
You specified the non_emit-leak reject. I made the numeric_map check a POSITIVE allowlist:
each mapped canonical id must be in emit_target. That subsumes non_emit-leak AND also
rejects ids unknown to the unit (which layer 3 should have dropped) -- distinct codes
(numeric_map_non_emit_leak vs numeric_map_unknown_canonical_id). This is the more
fail-closed posture. CONFIRM keep, or tell me to relax to non_emit-only.

## Gate-contract binding (test #7) -- verified against the REAL contract
- build_task_constraints output binds to WritingTaskConstraints +
  _optional_paragraph_word_count in writing-runner/v0/contract.py (stdlib-only import).
- Confirmed the writing_task_v1 JSON uses "min"/"max" (contract _optional_paragraph_word_count
  reads value.get("min")/value.get("max")) -> ParagraphWordCount(minimum, maximum). So the
  builder's {"min","max"} projection is correct; a contract field rename breaks test #7.

## Watchpoint flagged (your call, non-blocking)
Registry word_count_band has no upper cap, but the writing_task contract caps
maximum <= 1000. A band with hi > 1000 passes validate_registry but would fail
validate_writing_task downstream. Options: (a) cap word_count_band hi <= 1000 in the L1
schema (small follow-up, fail earlier), or (b) leave it (real bands ~55-95). Your pick.

## Ask
Review L3 (95de5ef) + L4 (15891bf) on the shared clone; VERDICT + the R3 confirm + the
word_count_band cap pick. After your verdict the fork (loop controller vs last-mile
MD Reader v0 bundle) is the operator's call.
