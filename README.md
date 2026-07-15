# CCC Protocol

CCCP is a small, local-first coordination layer for Codex and Claude Code. It
keeps the familiar `coop/` inbox and status files, and adds a deterministic
supervisor for leases, task claims, bounded retry, handoffs, and STOP.

The supervisor is deliberately fail-closed:

- lifecycle state and raw task/result envelopes stay in `coop/.ccc/`;
- `.ccc/` is ignored by Git and excluded from snapshots and safe status;
- one `coop/` root permits only one nonterminal run because STOP is root-global;
- duplicate wakes and stale workers cannot publish twice;
- only read-only or proven-reversible work may retry automatically;
- Desktop focus, UI nudging, cloud doorbells, and live agent bindings are off
  by default.

The v1 CLI manages and tests the lifecycle state machine. It ships a bounded
Claude subprocess transport and a validated Codex app-server protocol adapter,
but it does **not** infer a live workspace/permission profile. Consequently,
the stock CLI refuses live model dispatch until a maintainer supplies and
tests that explicit binding. No existing Codex Desktop process is attached to
or controlled.

The optional maintainer-operated Claude Desktop binding is narrower: for one
operator-selected, version-pinned Remote Control/session-bridge id, it can
manually request that Windows open or focus that Code session. It uses a
Desktop-specific policy and one-shot focus ledger; it does not enable UI
Automation or an automatic failure fallback. It never types or sends a message
and never reports a model turn as started or completed. Local Windows account
and filesystem ACLs, not a CCCP maintainer role, are the access boundary. See
[docs/CLAUDE_DESKTOP_SESSION_FOCUS.md](docs/CLAUDE_DESKTOP_SESSION_FOCUS.md).

## Start safely

From a target Git repository, install the human collaboration template. The
installer creates missing files only and never overwrites existing project
instructions:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\USER\Documents\ccc-protocol\scripts\install-ccc.ps1 -ProjectRoot .
```

Install the reviewed local Python package in an isolated environment:

```powershell
python -m pip install -e C:\Users\USER\Documents\ccc-protocol
ccc-supervisor probe
```

`probe` reports the Desktop focus contract as available but does not inspect
the installed Desktop package or protocol handler. Binding and focusing perform
those version-pinned checks and fail closed on drift.

Initialize and inspect a synthetic run without starting either model:

```powershell
ccc-supervisor init --coop-root .\coop --project-alias synthetic-test
'Review the synthetic fixture only.' | ccc-supervisor enqueue --coop-root .\coop --target claude --idempotency-key smoke-1
ccc-supervisor status --coop-root .\coop
```

Read [docs/SUPERVISOR_V1.md](docs/SUPERVISOR_V1.md) and
[docs/BOOTSTRAP.md](docs/BOOTSTRAP.md) before binding a live adapter or using
the separate Desktop focus command.

## Repository layout

```text
src/cccp_supervisor/       local state machine, adapters, CLI
tests/                     Python and PowerShell regressions
templates/coop/            create-missing project template
scripts/install-ccc.ps1    non-overwriting installer
scripts/ccc_status.ps1     scrubbed read-only file status
scripts/ccc_push_snapshot.ps1
                           allowlisted, branch-locked snapshot helper
docs/SUPERVISOR_V1.md      canonical v1 contract
docs/BOOTSTRAP.md          safe bring-up and rollback
docs/CLAUDE_DESKTOP_SESSION_FOCUS.md
                           version-pinned exact-session focus boundary
docs/ANTIPATTERNS.md       known unsafe patterns
```

## Verification

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -p 'test_*.py' -v
pwsh -NoProfile -ExecutionPolicy Bypass -File .\tests\powershell\test_ccc_scripts.ps1
git diff --check
```

The older heartbeat, GitHub-remote, and snapshot notes remain as legacy human
coordination guidance. They are not schedulers and must not override the
supervisor contract or project-local STOP instructions.
