# LEDGER_298 CODEX TOURNAMENT BLIND PATH GUARD

VERDICT: ok

Codex follow-up to LEDGER_297.

## Scope

Codex extended the tournament path-leak backstop from the scoring manifest to the earlier prompt-tournament blind manifest. The blind manifest already withheld variant IDs, prompt deltas, prompt-pack directories, and task prose. This pass adds a final local-path pattern guard so future blind scoring metadata cannot accidentally carry local absolute paths.

If future rubric notes or blind metadata include Windows drive paths, UNC paths, or common POSIX private path shapes, blind-manifest generation fails before write.

## Red paths added

- blind manifest guard rejects Windows drive-shaped local paths.
- blind manifest guard rejects UNC-shaped local paths.
- blind manifest guard rejects POSIX home-shaped local paths.

## Verification

- prompt tournament synthetic suite: 11 passed
- local-LLM synthetic suite: 214 passed
- writing-runner synthetic suite: 468 passed
- diff check: no whitespace errors

No model calls were run. No manuscript content, resolved data values, raw protected prose, or figure/corpus payloads were committed or relayed. Manuscript repository changes remain uncommitted for operator review.

