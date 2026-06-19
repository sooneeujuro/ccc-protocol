# LEDGER_296 CODEX TOURNAMENT ERROR TOKEN HARDENING

VERDICT: ok

Codex follow-up to LEDGER_294 and LEDGER_295.

## Scope

Codex audited safe manifest fields that copy exception codes into tournament run/scoring outputs. The local Gemma tournament runner now validates attempt `error_code` values as compact relay-safe metadata tokens before recording them.

If a lower-layer exception ever exposes a path-shaped or prose-shaped code, the tournament runner fails closed instead of copying that value into the run manifest.

## Red path added

- tournament runner rejects a path-shaped lower-layer attempt error code.

## Verification

- tournament runner synthetic suite: 5 passed
- local-LLM synthetic suite: 208 passed
- writing-runner synthetic suite: 468 passed
- diff check: no whitespace errors

No model calls were run. No manuscript content, resolved data values, raw protected prose, or figure/corpus payloads were committed or relayed. Manuscript repository changes remain uncommitted for operator review.

