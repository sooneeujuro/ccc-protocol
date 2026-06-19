# LEDGER_270_CODEX_CONDUCTOR_LENGTH_REPAIR_RUNNER

VERDICT: ok

Context:
- Operator asked whether paragraph word-count bounds should be treated as hard scientific failures or as journal/section/task-level format constraints.
- Codex interpretation: word-count bounds belong to the writing task contract. Near-bound misses should become paraphrase/tighten/expand repair work when the task explicitly sets `constraints.paragraph_word_count_repair_margin`; larger misses remain hard failures.

Implemented in manuscript-atelier local patch:
- Added `tools/paper-orchestra/local-llm/v0/gemma_conductor_length_repair_runner.py`.
- The new runner handles Conductor outputs that passed with a repairable word-count warning in `LOCAL_OLLAMA_CONDUCTOR_RUN.safe.json`.
- If no Conductor warning exists, it writes a `not_needed` safe manifest and does not call the model.
- If a repair is needed, it writes one local-only repair prompt, calls the configured local Ollama model, re-runs the full Conductor candidate validator, and rejects outputs that still carry repairable length warnings.
- Repaired output must exactly preserve `evidence_ids`, `numeric_ids`, and `claim_ids`.
- FGP phrase guard is still mandatory for repair prompt and repair response when FGP routing is active.
- Safe manifest is `LOCAL_GEMMA_CONDUCTOR_LENGTH_REPAIR_RUN.safe.json`; it contains hashes/counts/relative filenames/status only, not repaired prose or absolute local paths.
- README now states the policy explicitly: word-count ranges are journal/section/task contracts, not scientific truth; repair margin converts small length drift into a local paraphrase repair pass rather than a failed draft.

Tests:
- Added synthetic tests for Conductor repair success, no-op when not needed, still-out-of-range rejection, changed-ID rejection, source response hash drift, and prompt-manifest schema drift.
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 136 passed
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`
  - no whitespace errors; CRLF warnings only

Scope:
- No manuscript-atelier commit/push.
- No model run.
- No raw model prose, protected article text, resolved numeric result values, or local absolute paths relayed in this note.

Next suggested review:
- Please break-it the new Conductor repair runner with the same posture used for B/M/T repair:
  1. forged or stale Conductor manifest,
  2. source response drift,
  3. repaired output still near-bound,
  4. repaired output changing ID arrays,
  5. FGP phrase overlap in repair prompt/response,
  6. safe manifest prose/path leakage.
