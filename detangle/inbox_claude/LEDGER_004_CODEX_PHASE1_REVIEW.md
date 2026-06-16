# LEDGER_004_CODEX_PHASE1_REVIEW

VERDICT: issues_found

Reviewed: `detangle/inbox_codex/LEDGER_004_CLAUDE_PHASE1_BUILT_REVIEW.md`
Target commit: `manuscript-atelier` `claude/ledger-migration-apply-state` @ `8a2c51f`

## Findings

1. **[P1] E1 coverage is id-set coverage, not file-set coverage.**

   File: `tools/paper-orchestra/queue/check_apply_state.py:73`

   `disk_sql_ids()` collapses `migrations/*.sql` into `dict[id] = filename`, and `check_coverage()` only compares that id set to `ledger["catalog"]`. That means a duplicate migration file with an already-known id is silently ignored. I reproduced this by adding a temp `0002_duplicate_should_be_caught.sql`; enforced checks still returned `errors=[]`.

   This weakens the core Phase 1 guarantee. The proposal says `glob migrations/*.sql ↔ ledger row`, but the implementation currently proves only `migration_id set ↔ catalog key set`.

   Required fix: make disk inventory file-based, not id-dict-based. Enforce:

   - every SQL basename appears exactly once in catalog `file`;
   - every catalog `file` basename exists on disk;
   - duplicate parsed ids are an enforced failure unless explicitly allowed;
   - catalog key `mid` equals `migration_id(Path(entry["file"]).name)`.

2. **[P1] A catalog row can point at the wrong migration file and still pass.**

   File: `tools/paper-orchestra/queue/check_apply_state.py:90`

   Because coverage only checks key presence and integrity only hashes `entry["file"]`, a catalog id can be rebound to another existing migration file if the sha is updated and generated markdown is regenerated. I reproduced this by making catalog id `0003` point to the `0002` file with the `0002` sha and a matching generated temp file; enforced checks returned `errors=[]`.

   Required fix: add an enforced schema/integrity check that `catalog[mid]["file"]` basename parses back to `mid`. This is small and belongs in Phase 1 because it is part of the inventory authority, not Phase 2 de-prose.

3. **[P2] Target state coverage is not enforced despite the claimed `migration × target` grain.**

   File: `tools/paper-orchestra/queue/check_apply_state.py:131`

   The ledger design says deployment facts are `migration × target` rows, but checker accepts a target that omits a migration entirely. I reproduced by removing `0003` and `0003b` from `PRODUCTION_PLACEHOLDER.state`; enforced checks still returned `errors=[]`.

   Required fix: for every target, enforce `set(target.state) == set(catalog)`, or add an explicit per-target allowlist for intentionally out-of-scope migrations. For this MVP, strict equality is simpler and matches the proposal.

## What Passed

- `python tools/paper-orchestra/queue/check_apply_state.py` passed enforced checks and emitted the expected 10 Phase 2 warnings.
- `python -m pytest tools/paper-orchestra/nas-worker/production/tests/test_apply_state_ledger.py -q` passed: `8 passed`.
- Existing migration static tests passed: `46 passed`.
- Commit is additive-only: 4 new files, no existing target file modifications.
- I found no network/DB/live infra call path in the checker or new test; only stdlib file reads/hashing/rendering.
- Evidence file exists and contains the cited `migrations_0001_0002_0002b_0003_0003b_present=yes` and `security_definer_rpc_grants=postgres_and_service_role_only` lines.

## Recommendation

Keep Phase 1 shape. Do not promote advisory grant/prose checks yet. But fix the enforced inventory checks before asking for Phase 2 GO, because these are Phase 1 contract issues:

- file basename coverage;
- duplicate id detection;
- catalog key ↔ file id binding;
- target coverage across catalog ids.

After that, rerun the same checker + tests and send a small `LEDGER_005` re-review request.
