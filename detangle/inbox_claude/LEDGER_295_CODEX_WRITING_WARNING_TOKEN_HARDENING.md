# LEDGER_295 CODEX WRITING WARNING TOKEN HARDENING

VERDICT: ok

Codex follow-up to LEDGER_294.

## Scope

After narrowing local-LLM `warning_codes`, Codex audited the writing-runner result contract for the same class of small-string manifest surface.

The writing-runner `citation_warnings` and `naming_warnings` arrays now accept duplicate warning entries when callers need that behavior, but each value must still be a lowercase safe warning token. Path-shaped or prose-shaped warning entries are rejected at contract validation time.

## Red paths added

- draft candidate `naming_warnings` rejects path-shaped values.
- conductor decision-log `citation_warnings` rejects path-shaped values.

## Verification

- writing-runner contract synthetic suite: 159 passed
- writing-runner synthetic suite: 468 passed
- local-LLM synthetic suite: 207 passed
- diff check: no whitespace errors

No model calls were run. No manuscript content, resolved data values, raw protected prose, or figure/corpus payloads were committed or relayed. Manuscript repository changes remain uncommitted for operator review.

