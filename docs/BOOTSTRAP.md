# Supervisor v1 bootstrap

This runbook brings up the same-host supervisor without making a live Claude,
Codex, UI, or cloud call. Read `SUPERVISOR_V1.md` first.

The command names are stable for v1: `init`, `enqueue`, `run-once`, `serve`,
`recover`, `status`, `stop`, and `probe`. Use each command's `--help` output for
the exact flags of the installed build.

## 1. Preconditions

- Work from the intended target project, not the CCCP protocol repository.
- Read project-level `AGENTS.md`, `CLAUDE.md`, and STOP instructions first.
- Confirm that only one machine will own this run.
- Keep `coop/.ccc/` on a local filesystem, outside OneDrive and NAS sync.
- Do not bootstrap while `coop/STOP.md` exists. A stale STOP must be reviewed,
  not deleted automatically.
- Do not use a protected corpus, manuscript, or production repository for the
  first smoke test.

Record the intended project alias, operator, allowed write roots, forbidden
paths, cost policy, and adapter policy in `coop/RUN_STATE.md` and
`coop/SUPERVISOR_POLICY.md`.

## 2. Install or refresh the co-op template

Use the repository's `scripts/install-ccc.ps1` from the target project. Review
the resulting diff before accepting it; do not overwrite a project-specific
protocol blindly.

The installed `coop/.gitignore` must contain:

```gitignore
/.ccc/
```

Verify the rule before initializing state:

```powershell
git check-ignore -v coop/.ccc/state.sqlite3
```

If Git does not report an ignore rule, stop. Do not create or populate `.ccc/`.

## 3. Install the local supervisor build

Use an isolated Python 3.11-or-newer environment and install the reviewed local
checkout. Do not install from an unpinned network URL as part of a run.

Confirm that the executable resolves to the intended environment:

```powershell
python -m pip install -e C:\path\to\reviewed\ccc-protocol
Get-Command ccc-supervisor
ccc-supervisor --help
```

At this point no agent process should have started.

## 4. Probe capabilities first

Run `ccc-supervisor probe`. It does not take a project path and does not mutate
a project. The initial expected posture is:

- Claude adapter: disabled or unavailable;
- Codex adapter: disabled or unavailable;
- automatic timer wake: disabled;
- Windows UI nudge: disabled;
- cloud doorbell: unavailable.

`probe` is read-only. It may inspect executable identity and version, but must
not launch a model turn, attach to Codex Desktop, click UI, contact a cloud
endpoint, or modify the target project.

Resolve `version_unsupported`, `settings_hash_mismatch`, or permission-profile
errors before proceeding. Do not enable UI as a workaround.

## 5. Initialize one local run

Use `ccc-supervisor init` with the target `coop/` root and a non-sensitive
project alias. Keep the default policy for the first run:

```powershell
ccc-supervisor init --coop-root .\coop --project-alias synthetic-test
```

- `auto_wake_allowed=false`;
- `ui_nudge_enabled=false`;
- finite watch TTL and per-agent wake budget;
- finite lease and claim TTL;
- finite handoff, payload, output, and retry bounds.

Initialization should create `coop/.ccc/` and one active run generation. It
must fail if any run in that `coop/` root is nonterminal or if STOP exists.
Parallel projects require separate `coop/` roots.

Immediately check:

```powershell
ccc-supervisor status --coop-root .\coop
git status --short
```

The status output should contain counts, enums, booleans, and opaque ids only.
Git must not show `.ccc/`.

## 6. Exercise the state machine without a live adapter

Use a synthetic, non-sensitive read-only payload. Enqueue it with an explicit
idempotency key through `ccc-supervisor enqueue`.

```powershell
'Review only the synthetic fixture.' |
  ccc-supervisor enqueue --coop-root .\coop --target claude --idempotency-key smoke-1
```

Before enabling any adapter, verify:

1. enqueueing the identical key and identical canonical payload returns the
   existing task;
2. reusing the key with a changed payload fails with
   `idempotency_conflict`;
3. `status` shows one queued task without exposing the payload;
4. the stock CLI refuses an unbound live adapter before claiming the task,
   rather than invoking a shell or UI fallback;
5. a second worker cannot claim work held by an unexpired lease.

Use the project's mock adapter/test harness for `run-once`; do not point the
smoke test at Claude or Codex. `serve` is not required for bootstrap.

## 7. Test STOP and recovery

With only synthetic work present:

1. request STOP through `ccc-supervisor stop`;
2. confirm that `coop/STOP.md` contains only the scrubbed stop envelope;
3. confirm that queued/claimed tasks are cancelled and no new task starts;
4. confirm that the run reaches `stopped` after active work drains;
5. run `ccc-supervisor recover` and verify that it does not resurrect the
   stopped generation.

Also test the compatibility direction in a disposable run: create the legacy
STOP signal first, then verify that the next supervisor transition enters
`draining`. Do not perform this test in an active human collaboration folder.

## 8. Live adapter enablement gate

Enabling a live adapter is a separate operator decision. Before that decision,
all of the following must pass:

- duplicate-wake, lease-fence, retry-budget, STOP, timeout, and output-cap tests;
- a supervisor-owned Windows Job Object test leaving no child process;
- strict prompt-via-stdin and JSONL parsing tests;
- permission profile and tool/MCP allowlist review;
- synthetic proof that raw prompts, stdout, paths, and result prose cannot enter
  safe status, events, Git, or cloud schemas;
- adapter-specific cancellation and session reconciliation tests.

For Claude, use explicit session ids and one process per wake initially. For
Codex, use only an independently invocable, supervisor-owned app server. The
app server already owned by Codex Desktop is outside the supervisor boundary.

The current stock CLI still refuses live dispatch with
`live_adapter_profile_not_bound`; two consent flags alone are intentionally
insufficient. A later maintainer-owned binding must pin the working directory,
executable/version, plan/read-only profile, settings/MCP sources, process-tree
ownership, and structured result parser. After that binding is reviewed,
enable one adapter and one read-only task at a time with `run-once`.

## 9. Moving from `run-once` to `serve`

`serve` is not live-capable in the stock v1 CLI because no live adapter profile
is bound. Once a later binding has repeated `run-once` success, preserve these
defaults:

- no timer wake unless explicitly configured;
- no UI nudge;
- one active task per agent;
- bounded idle interval and watch TTL;
- fail closed on adapter drift or approval request;
- STOP checked before every lifecycle boundary;
- no cloud doorbell.

Start with a short supervised window. Observe safe status and local process
ownership. Stop the run at the end; do not leave a development daemon running
indefinitely.

## 10. UI nudge remains a separate experiment

Do not enable UI nudge merely because a structured adapter is unavailable. A
future experiment needs a pinned app version, exact AutomationId selector,
foreground/focus guards, one-shot receipt, cooldown, and synthetic UIA tests.
Until then, `probe` should report it disabled.

## 11. Cloud doorbell is not part of bootstrap

Do not add Supabase credentials, Vercel environment variables, DNS changes,
polling jobs, or sooneeujuro.com routes during v1 bootstrap. The future doorbell
requires a separate go decision and must implement only the strict
metadata-only schemas in `SUPERVISOR_V1.md`.

In particular, there is no “temporary” free-text field. A local queue contains
the work; the doorbell may only ask the local supervisor to look.

## 12. Rollback

1. Request STOP and wait for a terminal run state.
2. Verify that all supervisor-owned child processes are gone.
3. Disable the local service or remove the isolated package environment.
4. Preserve `.ccc/` locally until any ambiguous effects are reconciled.
5. Do not commit the database or payload/result directories as an archive.
6. Restore only the scoped protocol-template diff if the project no longer
   wants supervisor metadata.

Never recursively delete a computed path. Resolve the intended project and
`coop/.ccc/` path, verify that it is inside that project, and obtain operator
approval before removal.

## Operator decisions after bootstrap

The bootstrap should leave only these meaningful choices:

1. enable no live adapter, Claude read-only, or Codex read-only;
2. keep manual `run-once` or permit bounded `serve`;
3. later test a named workspace-write profile;
4. later review UI nudge separately;
5. later review the metadata-only outbound doorbell separately.

None of these choices is implied by successful local state-store tests.
