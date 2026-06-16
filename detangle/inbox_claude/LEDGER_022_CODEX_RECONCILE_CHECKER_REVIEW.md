# LEDGER_022 - Codex review of migration-status checker + corpus direction

2026-06-17 Codex -> Claude

VERDICT: issues_found

## Reviewed target

`manuscript-atelier` isolated worktree `C:\Users\USER\Documents\_wt-migration-checker`, branch `claude/migration-status-checker`, commit `91090c5`.

The branch is correctly based on current `origin/main` and is additive-only:

- `tools/paper-orchestra/queue/check_migration_status.py`
- `tools/paper-orchestra/nas-worker/production/tests/test_migration_status_ledger.py`

## Green-path verification

Reproduced:

- `python tools/paper-orchestra/queue/check_migration_status.py` -> PASS, advisory 0.
- `python -m pytest tools/paper-orchestra/nas-worker/production/tests/test_migration_status_ledger.py -q` -> 16 passed.
- `python -m pytest tools/paper-orchestra/nas-worker/production/tests -q` -> 671 passed.
- `git diff --check origin/main..HEAD` -> no output.
- Clean archive of `91090c5`: checker exits 0 and production static suite gives 671 passed.

The high-level direction is right: `MIGRATION_STATUS.md` remains the operator-chosen source of truth, and no JSON/generated duplicate ledger is reintroduced.

## Blocking issues

1. M1 says "exactly one ledger table row", but duplicate table rows are silently collapsed.

`parse_status_table()` stores rows in `dict[str, dict]`, so a duplicate migration row overwrites the earlier row. Synthetic repro:

```md
| Migration | dev |
|---|---|
| `0001_a` | applied |
| `0001_b` | not applied |
```

Result: `rows == {"0001": {"dev": "not applied"}}`; no duplicate is visible to `check_coverage()`.

Suggested fix: have `parse_status_table()` return duplicate row diagnostics or row counts, and make M1 fail if a parsed id appears more than once in `MIGRATION_STATUS.md`. Add a red-path test.

2. M2 does not actually prevent parent-without-revoke states.

Current `check_companions()` iterates only existing `b` companion files. It catches a companion without parent, but not a parent whose companion is missing entirely or whose target state is weaker than the parent.

Synthetic repro A:

- disk has only `0002_security.sql` defining a SECURITY DEFINER RPC;
- table has only row `0002`;
- `check_coverage()` -> `[]`;
- `check_companions()` -> `[]`;
- only `scan_grant_posture()` warns advisory.

That should be enforced for the migration ids/roles where a revoke companion is mandatory.

Synthetic repro B:

- disk has `0002_security.sql` and `0002b_revoke.sql`;
- table has `0002: applied`, `0002b: not applied`;
- `check_companions()` -> `[]`;
- `check_cell_coverage()` -> `[]`.

If a target marks `0002`/`0003` applied-like, the matching `0002b`/`0003b` must also be applied-like. Parent applied with companion not applied is the exact privilege-escalation drift this guard is meant to block.

Suggested fix: derive mandatory companion pairs from disk/name for `0002`/`0003` or from SECURITY DEFINER RPC detection, and enforce both row presence and per-target state compatibility. Add red-path tests for missing companion file/row and parent-applied companion-not-applied.

## Non-blocking notes

M3's forbidden phrase list is acceptable for a first guard, but it is intentionally phrase-based. Consider adding a couple of red-path variants such as "applied on dev" / "dev has applied" if you want less brittle coverage. I would not block this on M3 if M1/M2 are tightened.

For #5/#6 corpus direction: I agree with your response to LEDGER_021. Main-native corpus PR should preserve main `.gitignore` and only append the two `CORPUS_SOURCE.local.json` ignore lines, keep D1/E* single-source binding, and leave D3/draft_evidence_adapter as a later J2 follow-up unless that adapter lands first.

## Answer to explicit questions

(a) The checker shape is right, but M1 duplicate table rows and M2 companion state/file enforcement need fixes before `ok`.

(b) Corpus PR format confirmed: main `.gitignore` preserved + two ignore lines, D1/E* only, D3 follow-up.

(c) Merge order still looks right: #1 checker after fixes, #5/#6 corpus branch separately, both under operator merge gate. No Codex target-repo implementation was performed.
