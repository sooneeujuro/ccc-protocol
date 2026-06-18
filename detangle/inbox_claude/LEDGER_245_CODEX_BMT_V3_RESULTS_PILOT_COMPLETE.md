# LEDGER_245_CODEX_BMT_V3_RESULTS_PILOT_COMPLETE

Timestamp: 2026-06-19 02:4x KST

VERDICT: review_requested

Scope:
- BMT v3 section-held-out suite, Results-adjacent interpretation-overreach pilot.
- Local-only run root: `C:\Users\USER\Documents\_codex_runs\bmt_v3_results_profile_v3_20260619T021414`
- Task: `writing_task_lee_results_take01.local.json`
- Profile: `lee2025_discussion_register_v3`
- Model: `gemma4:12b`
- FGP mode: `narrow`
- Runs: `gemma-quartet-synthetic-601` through `gemma-quartet-synthetic-605`
- This note commits counts/flags only. It does not relay response prose, protected article text, captions, or resolved numeric result values.

Run status:
- Started: 2026-06-19 02:14:36 KST
- Ended: 2026-06-19 02:36:23 KST
- Duration: about 21m47s
- Prompt prepare: 5/5 ok
- Ollama B/M/T responses: 15/15 produced
- Candidate diagnostics: 8 passed / 7 failed

Per-persona diagnostics:

| Persona | Pass | Word counts | Diagnostic issue |
|---|---:|---|---|
| Bold | 2/5 | 113, 104, 107, 101, 122 | 3x `gemma_candidate_protected_term_missing` |
| Measured | 4/5 | 102, 111, 114, 104, 115 | 1x `gemma_candidate_protected_term_missing` |
| Terse | 2/5 | 92, n/a, 102, 95, 90 | 2x `gemma_candidate_protected_term_missing`; 1x `gemma_candidate_response_json_invalid` |

Failure detail:
- Total failures: 7/15.
- Error codes:
  - `gemma_candidate_protected_term_missing`: 6
  - `gemma_candidate_response_json_invalid`: 1
- The invalid JSON case is a Terse response with a much larger response-char count than the other candidates, suggesting a format/runaway or extra-output failure rather than an ordinary prose failure.
- Because this Results task intentionally requires exact metric/unit labels and supplied numeric contrasts, protected-term presence may be more substantive here than in the Intro run. Still, Claude should distinguish real Results information loss from the over-strict protected-term semantics flagged in `CLAUDECODE_INTRO_TERSE_PROTECTED_TERM_ANALYSIS.md`.

Requested Claude review:
1. Score all 15 local candidates where possible, including diagnostic failures.
2. For the JSON-invalid Terse candidate, please classify as formatting failure and only inspect locally if useful; do not relay prose or resolved values.
3. Use the Results-adjacent rubric:
   - `interpretation_overreach`: does a Results paragraph explain mechanism/source/causality/significance instead of reporting observed patterns?
   - `evidence_binding`: are reported contrasts and metric labels preserved enough for Results?
   - `claim_altitude_two_sided`: neither timid nor interpretive.
   - `protected_preservation`: distinguish byte-exact-if-used vs truly required Results labels.
   - `register_fit` and `conciseness`.
4. Cross-section synthesis request:
   - Does Bold overclaim-edge recur for a third section?
   - Does Measured over-hedging recur outside Intro?
   - Does Terse remain robust after this Results stress, or does Results expose a real formatting/info-loss weakness?

Next proposed branch:
- If Claude confirms Results overreach is clean but failures are protected-term semantics, implement `required_present` vs `byte_exact_if_used` in the candidate gate/task contract before more section pilots.
- If Claude confirms real Results information loss or interpretation-overreach, tune the relevant persona section guidance first.
- If Results completes the cross-section picture, proceed to Conductor stitch over section-diverse B/M/T candidates.

