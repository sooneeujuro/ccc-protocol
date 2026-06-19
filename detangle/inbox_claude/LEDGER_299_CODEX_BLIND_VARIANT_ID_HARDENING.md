# LEDGER_299 CODEX BLIND VARIANT ID HARDENING

VERDICT: ok

Codex follow-up to LEDGER_297 and LEDGER_298.

## Scope

Codex audited `blind_variant_id` as a generated manifest identifier that later becomes part of scoring response filenames. The generator already produced digest-shaped IDs, but the tournament runner accepted any value beginning with `blind_`.

The runner now requires `blind_variant_id` to match the generated shape before using it for execution/scoring cross-checks or response filenames. Duplicate blind IDs in the blind manifest are also rejected instead of being silently overwritten during cross-checking.

## Red path added

- tournament runner rejects a path-shaped `blind_variant_id` before writing scoring response files.

## Verification

- tournament runner synthetic suite: 9 passed
- prompt tournament synthetic suite: 11 passed
- local-LLM synthetic suite: 215 passed
- writing-runner synthetic suite: 468 passed
- diff check: no whitespace errors

No model calls were run. No manuscript content, resolved data values, raw protected prose, or figure/corpus payloads were committed or relayed. Manuscript repository changes remain uncommitted for operator review.

