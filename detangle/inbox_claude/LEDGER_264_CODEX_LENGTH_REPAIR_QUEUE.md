# LEDGER_264_CODEX_LENGTH_REPAIR_QUEUE

VERDICT: ok

Follow-up to LEDGER_259-263. Codex added a local-only preparation layer for actual paraphrase/tighten repair of near-bound word-count warnings.

## New Tool

Added locally in manuscript-atelier:

- `tools/paper-orchestra/local-llm/v0/gemma_length_repair_queue.py`
- `tools/paper-orchestra/local-llm/v0/tests/test_gemma_length_repair_queue_synthetic.py`

Purpose:

- Read a gate-passed prompt pack.
- Select only candidates with repairable word-count warning codes.
- Write local repair prompts under `length_repair_prompts.local/`.
- Write `LOCAL_GEMMA_LENGTH_REPAIR_QUEUE.safe.json` with counts, hashes, warning codes, and relative prompt file names only.

Safety:

- The repair prompts may include local draft prose, so they are `.local` artifacts under the operator-local prompt-pack directory.
- The safe manifest does not include candidate prose, prompt text, resolved values, or absolute paths.
- The tool rechecks response hashes before rendering repair prompts.
- The tool rejects repository-internal prompt-pack paths.
- It does not call a model.

## Docs

Updated:

- `tools/paper-orchestra/local-llm/v0/README.md`

The README now documents `gemma_length_repair_queue.py` and the relationship between repairable word-count warnings and later paraphrase/tighten passes.

## Verification

Commands run with system Python 3.11:

- `py -3.11 -m pytest tools/paper-orchestra/local-llm/v0/tests -q`
  - Result: 120 passed.
- `py -3.11 -m pytest tools/paper-orchestra/writing-runner/v0/tests/test_contract_synthetic.py -q`
  - Result: 157 passed.
- `git diff --check` on the edited local-LLM and writing-runner files
  - Result: no whitespace errors.

Only the pre-existing `requests` dependency warning appeared during pytest startup.

## Current Recommendation

The patch now covers the full first half of a repair loop:

1. candidate/conductor gates accept near-bound length misses with warnings;
2. scorecard preserves the warnings;
3. repair queue converts warning-bearing candidates into local-only repair prompts.

Next possible increment, after review, is a model runner for the queued repair prompts plus a post-repair gate that verifies no new claims/numbers/citations were introduced.
