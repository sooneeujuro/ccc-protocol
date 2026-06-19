# LEDGER_301 CODEX TOURNAMENT PROMPT PACK PATH HARDENING

VERDICT: ok

Codex follow-up to LEDGER_300.

## Scope

Codex audited the tournament runner path that consumes `prompt_pack_dir` entries from the local execution manifest. That value decides which local prompt pack is read for a tournament entry. It was already constrained to remain under the tournament directory, but the runner now rejects unsafe relative path syntax before resolving the path.

`prompt_pack_dir` must be a non-empty relative path with no backslashes, no colon, no absolute path, and no dot or parent-directory segments.

## Red paths added

- tournament runner rejects parent-directory traversal in `prompt_pack_dir`.
- tournament runner rejects colon-bearing `prompt_pack_dir` values.

## Verification

- tournament runner synthetic suite: 12 passed
- local-LLM synthetic suite: 218 passed
- writing-runner synthetic suite: 468 passed
- diff check: no whitespace errors

No model calls were run. No manuscript content, resolved data values, raw protected prose, or figure/corpus payloads were committed or relayed. Manuscript repository changes remain uncommitted for operator review.

