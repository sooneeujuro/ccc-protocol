# LEDGER_265_CODEX_LENGTH_REPAIR_RUNNER

VERDICT: ok

Codex extended the length-repair harness in manuscript-atelier, local patch only
(not pushed to manuscript-atelier).

Scope:
- Added `gemma_length_repair_runner.py`.
- It consumes `LOCAL_GEMMA_LENGTH_REPAIR_QUEUE.safe.json`.
- It runs queued local repair prompts through the local Ollama executor.
- It writes repaired responses under `length_repair_responses.local/`.
- It writes `LOCAL_GEMMA_LENGTH_REPAIR_RUN.safe.json` with counts, hashes, relative
  filenames, and warning status only.

Safety / invariants:
- Rejects repository-internal prompt-pack paths.
- Rechecks source response hashes and repair prompt hashes.
- Re-applies the candidate validator to repaired output.
- Rejects repaired output if any repairable word-count warning remains.
- Requires repaired `evidence_ids`, `numeric_ids`, and `claim_ids` arrays to
  exactly match the source response.
- If FGP routing is active, keeps the existing forbidden-phrase guard mandatory.
- Does not relay repaired prose, raw protected text, resolved values, or absolute
  local paths in the safe manifest or this note.

Verification:
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 125 passed.
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed.
- `git diff --check` on the touched harness files produced no whitespace errors
  (CRLF normalization warnings only).

Review request:
- Please review the length repair margin + queue + runner series as one harness
  arc.
- Main review question: does the repair runner's exact ID-array preservation
  plus no-warning post-gate adequately prevent a length/paraphrase pass from
  weakening claim tracking?
