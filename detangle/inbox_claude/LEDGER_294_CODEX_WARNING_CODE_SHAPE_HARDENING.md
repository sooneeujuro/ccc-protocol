# LEDGER_294 CODEX WARNING CODE SHAPE HARDENING

VERDICT: ok

Codex follow-up to the length-repair / semantic-review harness hardening sequence.

## Scope

This pass closes a small manifest side channel: `warning_codes` are metadata tokens, not a free string surface.

The checker/helper layer now requires warning codes to match a narrow lowercase safe-token shape. Path-shaped, prose-shaped, empty, mixed-case, or punctuation-bearing values are rejected before they can be copied into downstream repair queues, scorecards, or conductor repair summaries.

## Surfaces updated

- shared manifest guard helper: added warning-code token validation
- B/M/T length repair queue
- B/M/T length repair runner
- Conductor length repair runner
- quartet scorecard

## Red paths added

- B/M/T repair queue rejects path-shaped warning code values.
- scorecard rejects path-shaped candidate warning code values.
- scorecard rejects path-shaped Conductor warning code values.

## Verification

- scorecard synthetic suite: 38 passed
- local-LLM synthetic suite: 207 passed
- writing-runner synthetic suite: 466 passed
- diff check: no whitespace errors

No model calls were run. No manuscript content, resolved data values, raw protected prose, or figure/corpus payloads were committed or relayed. Manuscript repository changes remain uncommitted for operator review.

