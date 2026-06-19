# LEDGER_269_CODEX_LENGTH_REPAIR_SCORECARD_HARDENING

VERDICT: ok

Codex hardened scorecard handling of accepted length-repair manifests.
Manuscript-atelier remains a local patch only; no manuscript-atelier push.

Issue found:
- The scorecard observed repair-run manifests but could be stricter about
  manifest shape and repair necessity.

Patch:
- Scorecard now rejects repair manifests whose accepted count does not match
  the row count.
- Scorecard now rejects repair manifests that are not local-only or that claim
  commit/relay safety.
- Scorecard now rejects an accepted repair row for a candidate that did not
  carry any gate warning.

Verification:
- `py -3.11 -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 130 passed.
- `py -3.11 -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_contract_synthetic.py -q`
  - 157 passed.
- `git diff --check` on the touched scorecard / repair-runner files produced no
  whitespace errors (CRLF normalization warnings only).

Safety:
- This note includes only count/status information.
- No raw model prose, protected text, resolved values, captions, or absolute
  local paths are relayed.
