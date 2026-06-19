# LEDGER_302 CODEX PROMPT TOURNAMENT HASH HARDENING

VERDICT: ok

Codex follow-up to LEDGER_301.

## Scope

Codex audited the prompt-tournament generator path that copies hash fields from the generated prompt-pack manifest into the blind and execution manifests.

The generator now validates copied `prompt_sha256` and `task_sha256` values as lowercase SHA-256 hex before recording them. This prevents malformed or path-shaped hash fields from becoming blind/execution manifest metadata if an intermediate prompt-pack manifest is corrupted.

## Red paths added

- prompt tournament generation rejects a non-hex prompt hash copied from a prompt-pack manifest.
- prompt tournament generation rejects a non-hex task hash copied from a prompt-pack manifest.

## Verification

- prompt tournament synthetic suite: 13 passed
- local-LLM synthetic suite: 220 passed
- writing-runner synthetic suite: 468 passed
- diff check: no whitespace errors

No model calls were run. No manuscript content, resolved data values, raw protected prose, or figure/corpus payloads were committed or relayed. Manuscript repository changes remain uncommitted for operator review.

