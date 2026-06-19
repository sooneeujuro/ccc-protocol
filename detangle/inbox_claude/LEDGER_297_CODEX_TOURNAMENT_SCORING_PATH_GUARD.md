# LEDGER_297 CODEX TOURNAMENT SCORING PATH GUARD

VERDICT: ok

Codex follow-up to LEDGER_296.

## Scope

Codex audited the blind tournament scoring manifest surface for future prose/path leakage through free-text scoring metadata. The tournament scoring manifest already withheld prompt-pack paths and variant labels; this pass adds a final local-path pattern backstop to the scoring manifest blindness assertion.

If future scoring metadata accidentally carries a local absolute path, UNC path, or common POSIX private path shape, the scoring manifest is rejected before write.

## Red paths added

- blind scoring guard rejects Windows drive-shaped local paths.
- blind scoring guard rejects UNC-shaped local paths.
- blind scoring guard rejects POSIX home-shaped local paths.

## Verification

- tournament runner synthetic suite: 8 passed
- local-LLM synthetic suite: 211 passed
- writing-runner synthetic suite: 468 passed
- diff check: no whitespace errors

No model calls were run. No manuscript content, resolved data values, raw protected prose, or figure/corpus payloads were committed or relayed. Manuscript repository changes remain uncommitted for operator review.

