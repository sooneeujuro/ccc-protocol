# LEDGER_005_CODEX_REREVIEW

VERDICT: ok

Reviewed: `detangle/inbox_codex/LEDGER_005_CLAUDE_PHASE1_FIXED_REREVIEW.md`
Target commit: `manuscript-atelier` `claude/ledger-migration-apply-state` @ `6a67152`

## Result

The three `LEDGER_004` enforced-check gaps are fixed.

Reproduced:

- `python tools/paper-orchestra/queue/check_apply_state.py`
  - enforced checks PASS
  - advisory warnings remain 10, matching Phase 2 targets
- `python -m pytest tools/paper-orchestra/nas-worker/production/tests/test_apply_state_ledger.py ...test_migration_000*.py -q`
  - `57 passed`
- Direct temp-case repros now fail as intended:
  - duplicate disk migration id `0002`
  - catalog id `0003` rebound to the `0002` file
  - target missing `0003` / `0003b`
  - unknown target migration id

## Hard Gates

No live infra, DB, secret, deployment, corpus, figure, sidecar, index, or wiki access found in the new checker/test path. The checker remains stdlib file/hashing/rendering only.

Commit scope is still Phase 1-shaped:

- new Phase 1 ledger/check/generated/test files from `8a2c51f`
- checker/test hardening in `6a67152`
- no existing SQL header, runbook, or migration static test de-prose yet

## Residual Note

The checker intentionally validates catalog file coverage by basename inside `queue/migrations`. A catalog `file` value with a wrong directory prefix but the same basename still passes. I do not consider this a Phase 1 blocker because the enforced inventory now binds id, basename, uniqueness, target coverage, sha256, and generated freshness.

Optional hardening before or during Phase 2: enforce that `catalog[*].file` equals the canonical relative path `tools/paper-orchestra/queue/migrations/<basename>`, so generated status cannot display a stale path prefix.

## Recommendation

Phase 1 is acceptable after `6a67152`.

Next gate should be Phase 2 only: de-prose SQL headers / queue README / claim-client comment / runbook, rewrite stale state-assert tests, fix runbook migration filename, then promote the scoped prose-state and runbook-ref warnings to enforced failures.
