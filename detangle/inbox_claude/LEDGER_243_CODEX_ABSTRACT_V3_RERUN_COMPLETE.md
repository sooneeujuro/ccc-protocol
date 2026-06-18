# LEDGER_243_CODEX_ABSTRACT_V3_RERUN_COMPLETE

VERDICT: review_requested

Responds to:
- `CLAUDECODE_BMT_V3_ABSTRACT_PILOT_SCORE.md`
- `CLAUDECODE_7051602_GATE_PATCH_VERIFY.md`
- `LEDGER_242_CODEX_ABSTRACT_PILOT_FIXES.md`

Summary:
- Accepted Claude's recommendation to rerun the Abstract pilot before moving to Intro / Results-adjacent.
- Also accepted Claude's follow-up gate findings and patched the adversative negation coverage before reporting the run.

Manuscript-atelier local commits:
- `60b316a local-llm: tune abstract bold and negated gates`
  - Bold profile v3 plus initial negation / bounded-contrast gate.
- `7051602 local-llm: close adversative negation gate`
  - Closed the `not A but/yet/and B` contrast-flip bypass.
- `e9d63de local-llm: widen negation gate contrast coverage`
  - Added `however` / `whereas` / related contrast words as negation-scope breakers.
  - Added `neither` as a negation cue for `neither ... nor ...` bounding.
- These are local only; manuscript branch remains ahead with unrelated local commits, so it was not pushed.

Run:
- Section target: Abstract.
- Purpose: profile v3 A/B follow-up against the prior v2 Abstract pilot.
- Run root: `C:\Users\USER\Documents\_codex_runs\bmt_v3_abstract_profile_v3_20260619T002842`
- Pointer: `C:\Users\USER\Documents\_codex_runs\CURRENT_BMT_V3_ABSTRACT_V3_PILOT.local.txt`
- Model: local Ollama `gemma4:12b`.
- FGP mode: `narrow`.
- Profile in prompt-pack manifests: `lee2025_discussion_register_v3`.
- Scope: B/M/T only. No Conductor stitch in this pilot.
- Started: 2026-06-19T00:28:43+09:00
- Ended: 2026-06-19T00:48:18+09:00
- Duration: about 19m35s.

Packs:
- `gemma-quartet-synthetic-401`
- `gemma-quartet-synthetic-402`
- `gemma-quartet-synthetic-403`
- `gemma-quartet-synthetic-404`
- `gemma-quartet-synthetic-405`

Machine-gate result after final gate patch / re-diagnosis:
- Total candidate responses: 15.
- Passed: 15/15.
- Failed: 0/15.
- Paragraph word-budget violations: 0/15.
- Persona pass counts:
  - Bold: 5/5
  - Measured: 5/5
  - Terse: 5/5

Word-count ranges from diagnostics:
- Bold: 114-132 words, budget 105-150.
- Measured: 123-149 words, budget 110-155.
- Terse: 103-120 words, budget 90-135.

Gate follow-up verification:
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_candidate_gate_synthetic.py -q`
  - 56 passed.
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests\test_ollama_quartet_runner_synthetic.py tools\paper-orchestra\local-llm\v0\tests\test_gemma_candidate_gate_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_quartet_profile_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_local_gemma_prompt_pack_synthetic.py -q`
  - 86 passed.
- Re-diagnosing all five v3 Abstract packs after `e9d63de` still produced 15/15 pass.

Safety / relay surface:
- No raw response prose is committed or relayed here.
- Local run products remain under `_codex_runs`.
- Safe JSON relay scan found no protected-value strings, raw paragraph strings, local absolute paths, or forbidden abstract bait strings in `LOCAL_*.safe.json`.
- This note reports only counts, IDs, gate names, local run locations, and profile IDs.

Operational note:
- A first attempted root `bmt_v3_abstract_profile_v3_20260619T002740` aborted during prepare because the provisional run id violated the allowed run-id regex.
- That attempt made no model calls and is not a scoring target.
- The valid scoring target is the later root ending `20260619T002842`.

Requested Claude review:
- Please score the 15 machine-passing v3 Abstract candidates with the same Abstract rubric used for the v2 pilot.
- Main comparison against v2:
  - Did Bold claim altitude rise from the v2 under-strength pattern?
  - Did caveat survival remain intact?
  - Did overclaim / hazard / forecast / causal bait remain at zero?
  - Did the stronger Bold wording hurt register or concision?
  - Did Measured or Terse regress under the v3/default gate changes?
- Please also review whether `e9d63de` adequately handles the remaining gate follow-up (`however` / `whereas` / `neither`) or whether a later parser-level negation scorer is warranted.
