# LEDGER_001_CODEX_ARCHITECTURE_REVIEW

VERDICT: issues_found

Date: 2026-06-16
Reviewer: Codex
Target repo inspected read-only: `C:\Users\USER\Documents\manuscript-atelier`
Coordination branch: `coop/detangle-20260615`

## Scope and Constraint Check

- Pulled `ccc-protocol` with `git pull --ff-only`; branch was already up to date.
- Looked for Claude's proposal at `detangle/inbox_codex/LEDGER_001_CLAUDE_STRUCTURAL_PROPOSAL.md`.
- Result: the Claude proposal file is not present, and no `LEDGER_*` coordination note exists in either inbox at review time.
- No live infra changes, no DB writes, no deployments, no target repo edits, and no CCCP corpus/paper/sidecar/index/wiki/figure data touched.

Because Claude's exact proposal is missing, I cannot review its exact wording or accept/reject its first MVP directly. I can still give the independent architectural recommendation the operator asked for.

## Independent Finding

The highest-leverage first ledger MVP is the migration/apply-state ledger for `paper-orchestra/queue`.

Rationale:

1. The current state is already structurally contradictory, not merely untidy.
   - `0002_orchestra_jobs_security_definer_rpcs.sql` and `0003_orchestra_jobs_orphan_reclaim_rpc.sql` say file-only / not applied.
   - `0002b_revoke_authenticated_orchestra_job_rpcs.sql` and `0003b_revoke_authenticated_orphan_reclaim_rpc.sql` say they were applied to `manuscript-atelier-dev`.
   - `docs/runbooks/nas_worker_deployment.md` still speaks of "the two SECURITY DEFINER migrations" and omits the b-revoke companions in the activation gate.
   - Static tests assert stale prose such as "not applied", so a false status can become test-protected.

2. The security blast radius is real.
   - The affected objects are SECURITY DEFINER RPCs on the queue boundary.
   - If a future project applies only the parent migrations without the b-revokes, authenticated users may retain EXECUTE on functions that mutate queue state.
   - This is exactly the class of state where "what is true?" must not live in headers, runbooks, or memory.

3. It is checkable without live writes.
   - An offline guard can verify migration file inventory, ordering, dependencies, file hashes, required companion migrations, and absence of applied-state claims in SQL headers.
   - A later optional read-only live guard can verify actual RPC grants and applied migration rows, but that does not need to exist in phase 1.

4. It helps CCCP-style cooperation.
   - Both agents can reference one small ledger row instead of re-arguing prose state.
   - Coordination notes can say `ledger_check=pass|fail`, `target=dev`, `migration=0002b`, `grant_posture=service_role_only`.
   - It turns cross-agent review from "Claude remembers X, Codex saw Y" into a deterministic diff.

## Comparison With Live Surface Registry

I would not choose live surface registry as the first MVP, though it is likely the right second MVP.

Live surface registry has obvious value because the review found drift such as `app/page.tsx` claiming "No production endpoints active" while `app/README.md` documents production-capable Supabase mode and HMAC webhook behavior.

But as a first MVP it has two weaknesses:

- Without live probing, it risks becoming another hand-maintained inventory of routes and deployment claims.
- With live probing, it immediately wants access to deployment state, Supabase state, NAS state, or Vercel state, which is outside the current hard gates and more operationally sensitive.

For phase 2, I would build it as a derived registry from route files, app README, env gates, and deployment config first, then add explicit operator-run live checks later. But the migration ledger has a cleaner first slice and a tighter enforcement path.

## Recommended First MVP

### Name

`LEDGER_migration_apply_state`

### Ledger Location

Recommended target repo file:

`tools/paper-orchestra/queue/LEDGER_migration_apply_state.json`

This should be the source of truth for migration application and grant posture. SQL headers and runbooks should not encode live application state except by linking to the generated status.

### Generated Status Location

Recommended generated file:

`tools/paper-orchestra/queue/LEDGER_migration_apply_state.generated.md`

Properties:

- Generated only from the JSON ledger and local SQL files.
- Clearly marked `DO NOT EDIT`.
- Contains a compact table: migration id, path, sha256, role, target posture, dependency, required companion, known target state, last verification method/time.
- Safe for agents to quote into CCCP notes because it contains no secrets and no live credentials.

### Minimal Schema

Suggested JSON shape:

```json
{
  "schema": "ledger_migration_apply_state_v1",
  "scope": "paper-orchestra.queue",
  "generated_status": "tools/paper-orchestra/queue/LEDGER_migration_apply_state.generated.md",
  "targets": [
    {
      "id": "manuscript-atelier-dev",
      "kind": "supabase_project",
      "live_verification": "operator_readonly_only"
    }
  ],
  "migrations": [
    {
      "id": "0002_orchestra_jobs_security_definer_rpcs",
      "path": "tools/paper-orchestra/queue/migrations/0002_orchestra_jobs_security_definer_rpcs.sql",
      "sha256": "<computed>",
      "role": "security_definer_rpc_parent",
      "depends_on": ["0001_init_orchestra_jobs"],
      "required_companions": ["0002b_revoke_authenticated_orchestra_job_rpcs"],
      "expected_posture": {
        "functions": [
          "public.claim_next_orchestra_job(text, text)",
          "public.update_orchestra_job_status(uuid, text, text)"
        ],
        "execute_grants": ["service_role"],
        "forbidden_execute_grants": ["public", "anon", "authenticated"]
      },
      "target_state": {
        "manuscript-atelier-dev": {
          "state": "applied_verified|file_only|unknown|blocked",
          "verified_at": null,
          "verification_method": "not_verified|manual_live_readonly|supabase_migrations_table|static_only",
          "evidence_note": "no secrets; short operator-readable summary only"
        }
      }
    }
  ]
}
```

The exact initial states should be operator-confirmed. If the current review's live claim is accepted, the ledger can record `manuscript-atelier-dev` as `applied_verified` for the b-revokes with the review timestamp and method. If not, mark all live states `unknown` until a read-only inspection is run.

### Drift Check Command

Recommended offline command:

```powershell
python tools/paper-orchestra/queue/LEDGER_check_migration_apply_state.py --offline
```

Offline checks should:

- Verify every `tools/paper-orchestra/queue/migrations/*.sql` file is listed in the ledger.
- Verify every ledger path exists and its sha256 matches.
- Verify parent/companion rules, especially `0002 -> 0002b` and `0003 -> 0003b`.
- Verify SECURITY DEFINER migrations name their expected functions.
- Verify grant-tightening migrations revoke `authenticated`, `anon`, and `public`, then grant only `service_role`.
- Flag SQL headers or runbooks that assert applied/not-applied state outside the ledger, except for target-posture wording.
- Regenerate `LEDGER_migration_apply_state.generated.md` and fail if the committed generated file is stale.

Optional later command, operator-run only:

```powershell
python tools/paper-orchestra/queue/LEDGER_check_migration_apply_state.py --live-readonly --target manuscript-atelier-dev
```

That command should perform read-only privilege inspection only. No migrations, no writes, no grants, no revokes.

### CI or Local Guard

Phase 1 guard:

- Add the offline check to local verification and CI with no secrets.
- It should be allowed to fail until the operator approves converting the current prose state into the ledger.
- Once approved, make it blocking for PRs that touch:
  - `tools/paper-orchestra/queue/migrations/**`
  - `tools/paper-orchestra/nas-worker/production/tests/test_migration_*`
  - `docs/runbooks/nas_worker_deployment.md`
  - `tools/paper-orchestra/queue/README.md`

Do not put live Supabase inspection in CI for the MVP. Keep live verification as an explicit operator command.

## Implementation Phases

Phase 0 - Architecture lock:

- Claude and Codex agree the first MVP is migration/apply-state ledger.
- Operator approves that live application state moves out of SQL headers and prose into `LEDGER_migration_apply_state.json`.

Phase 1 - Offline ledger and generated status:

- Add JSON ledger with current local migration inventory.
- Add generator/checker.
- Add generated markdown status.
- Do not edit live DB or deployment.

Phase 2 - Prose detangling:

- Update migration headers to describe target posture, not live application state.
- Update static migration tests so they assert safety posture, not "NOT applied".
- Update `nas_worker_deployment.md` to enumerate all four migrations and companion order.

Phase 3 - Optional read-only live verification:

- Add operator-run live check for RPC grant posture and applied migration table state.
- Record only short evidence metadata in the ledger.
- No DB writes.

Phase 4 - Second MVP candidate:

- Build `LEDGER_live_surface_registry` as a derived local registry for app routes, deployment-sensitive env gates, NAS services, and Supabase projects.
- Keep it derived-first, live-readonly-later, so it does not become another stale prose artifact.

## Response to Claude If Claude's Missing Proposal Was Migration Ledger

If Claude's first MVP is migration/apply-state ledger, I agree with that direction, with one condition: the MVP must be enforced by an offline drift check from day one. A hand-written `STATUS.md` without a checker would repeat the existing failure mode.

If Claude's first MVP is live surface registry, I think it should be sequenced second. It is important, but its first enforceable slice is less crisp unless it is strictly derived from route/config files.

## Bottom Line

Choose `LEDGER_migration_apply_state` first.

This is not cleanup. It is a small state authority that prevents security-sensitive deployment truth from being split across SQL comments, static tests, runbooks, and agent memory. It is low-blast-radius, locally checkable, and directly improves CCCP cooperation by making the next exchange about a machine-verifiable ledger diff rather than prose recollection.
