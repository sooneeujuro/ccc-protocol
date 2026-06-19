# LEDGER_268_CODEX_LENGTH_REPAIR_RUNNER_HARDENING

VERDICT: ok

Codex hardened the local length-repair runner after self break-it review.
Manuscript-atelier remains a local patch only; no manuscript-atelier push.

Issue found:
- The runner originally consumed `LOCAL_GEMMA_LENGTH_REPAIR_QUEUE.safe.json`
  without independently rechecking that each queued repair candidate still
  matched the original candidate gate manifest.
- A stale or forged queue manifest could therefore try to repair a candidate
  that was not actually marked repairable by the gate.

Patch:
- `gemma_length_repair_runner.py` now reloads
  `LOCAL_GEMMA_CANDIDATE_GATE.safe.json`.
- It verifies the gate schema, gate status, run id, queue-declared gate schema,
  candidate count, source file, source response hash, and warning-code subset.
- It rejects queue/gate mismatches before any model call.
- Synthetic tests cover forged warning codes and queue count drift.

Verification:
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 128 passed.
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed.

Safety:
- This note includes only count/status information.
- No raw model prose, protected text, resolved values, captions, or absolute
  local paths are relayed.
