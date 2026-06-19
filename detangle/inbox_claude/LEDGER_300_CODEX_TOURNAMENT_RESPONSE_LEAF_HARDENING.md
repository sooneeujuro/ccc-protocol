# LEDGER_300 CODEX TOURNAMENT RESPONSE LEAF HARDENING

VERDICT: ok

Codex follow-up to LEDGER_299.

## Scope

Codex audited the tournament runner path that copies a passed local model response into the blind scoring package. The response filename comes from the local Ollama run manifest. It was already blocked for slash and backslash separators, but did not reject other unsafe leaf-file shapes.

The runner now requires the response filename to be a safe leaf file before reading/copying it. Empty names, dot segments, slash/backslash, colon, and newline-bearing values are rejected. This prevents path-shaped or Windows stream-shaped response filenames from becoming scoring-package file reads.

## Red path added

- tournament runner rejects an unsafe response leaf filename from the local run manifest.

## Verification

- tournament runner synthetic suite: 10 passed
- local-LLM synthetic suite: 216 passed
- writing-runner synthetic suite: 468 passed
- diff check: no whitespace errors

No model calls were run. No manuscript content, resolved data values, raw protected prose, or figure/corpus payloads were committed or relayed. Manuscript repository changes remain uncommitted for operator review.

