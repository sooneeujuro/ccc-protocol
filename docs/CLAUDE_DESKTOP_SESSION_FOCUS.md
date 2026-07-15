# Claude Desktop exact-session focus

## What this feature does

This is a maintainer-operated, same-host navigation request for one
operator-selected Claude **Code** Remote Control bridge session. It asks
Windows to dispatch an exact, internally generated URI and may launch or focus
Claude Desktop. The copied link identifies the bridge session; its syntax does
not prove that the session originated in Desktop or is still reachable.

It does not type, paste, click, send a prompt, start a Claude turn, observe a
turn, or prove that the requested session appeared. A successful command means
only `focus_requested_unverified`.

This distinction is permanent in the receipt:

```json
{
  "navigation_state": "focus_requested_unverified",
  "navigation_requested": true,
  "message_sent": false,
  "turn_started": false,
  "completion_observed": false
}
```

Do not use this focus request as the completion signal for a CCCP task.

This is an explicit manual command. V1 does not connect adapter failures,
`run-once`, `serve`, a timer, or a cloud doorbell to Desktop focus.

## Why it is version-pinned

Anthropic publicly documents `claude://code/new` for opening a new Code
composer. It does not publicly document an automation API that sends a message
to an existing Desktop Code session.

The installed Windows Desktop build also contains an existing-session route
for Remote Control/session-bridge ids beginning with `session_` or `cse_`.
That local route is feature-gated and is not a stable public API. CCCP therefore
allows only the package version, application-bundle hash, and Windows
protocol-handler identity inspected for this release. A Desktop update produces
`claude_desktop_build_unsupported` or `claude_desktop_build_drift` until a
maintainer reinspects the route, updates the allowlist, and reruns the tests.

An OS dispatch may still be ignored when the account feature gate is off, an
enterprise policy disables deep links, the bridge id is stale, the user is
signed into another account, or the session is inaccessible. CCCP cannot
distinguish those cases without a supported acknowledgement API.

References:

- [Claude Desktop deep links](https://support.claude.com/en/articles/14729294-open-claude-desktop-with-a-link)
- [Claude Code Desktop](https://code.claude.com/docs/en/desktop)
- [Claude Code Remote Control](https://code.claude.com/docs/en/remote-control)

## Remote Control prerequisites

Before binding or focusing, confirm all of the following:

- Claude Desktop Code is installed and signed in to the Claude account that
  can access the selected bridge session;
- Remote Control is enabled for that session, and the session is active or
  otherwise reachable through `claude.ai/code`;
- on Team or Enterprise, the organization Owner has enabled Remote Control and
  managed policy does not disable it;
- if the organization requires Trusted Devices, this Windows device is
  enrolled and its authentication is current;
- the host can reach the Remote Control service over the required network; and
- the operator copied the link from the intended session and visually checks
  the result after the one-shot request.

Binding validates the link shape and the pinned local Desktop build. It cannot
authenticate the bridge id, prove account access, or test session reachability.

## Identity and data boundary

Use the web link copied from the operator-selected, Remote Control-enabled Code
session. The identifier in that link is a session-bridge id, not an arbitrary
local session UUID. Accepted inputs are exact links whose final id begins with
`session_` or `cse_`; queries, fragments, prompts, folders, files, ports, user
information, extra path segments, escaping, and non-ASCII characters are
rejected.

The copied link is read from standard input so it does not appear in the
process command line. CCCP stores only the raw bridge id—not the copied URL—in
the create-only profile under `coop/.ccc/profiles/claude-desktop/`. That whole
tree is local and Git-ignored. Safe output contains only:

- the run and focus UUIDs;
- a run-scoped, domain-separated `session_ref` hash prefix;
- the canonical profile SHA-256;
- fixed enums and booleans.

Never copy the raw bridge id or local profile to Git, Vercel, Supabase,
sooneeujuro.com, chat, or a shared status surface. The profile hash detects
drift; it is not an authentication boundary against a local administrator.

“Maintainer-operated” is an operating rule, not a CCCP role or login check.
Keep the project and `coop/.ccc/` under the intended Windows account with
appropriate local filesystem ACLs. Another local administrator remains inside
the host trust boundary and can read or alter local state.

## Policy and one-shot behavior

The feature is disabled unless the run was initialized with
`--allow-claude-desktop-focus`. This enables only the dedicated Desktop focus
policy; it does not enable the generic UI nudge or UI Automation policy. The
caller must also provide the exact profile hash and session ref, a fresh
`focus_id`, `--enable-claude-desktop-focus`, and `--confirm-focus-only`.

The checks deliberately have two different scopes:

1. Sequential validation checks the active run, profile schema and hash, run
   generation, session ref, allowlisted package identity, version,
   application-bundle hash, protocol ProgID, and AppUserModelID.
2. One local transaction atomically reserves the `focus_id` in the dedicated
   `claude_desktop_focus_receipts` ledger while checking STOP, watch expiry,
   the per-run Desktop focus policy, Claude participation, replay, and the
   Desktop-specific cooldown.
3. After reservation, CCCP rechecks run cancellation and the pinned build, then
   checks the run once more immediately before asking Windows to dispatch. The
   launcher rechecks the protocol handler.

Profile, package, build, and handler validation are not part of the atomic
SQLite reservation. A duplicate, rejected, failed, or ambiguous focus request
is never automatically retried. A different `focus_id` is still limited by the
Desktop-specific cooldown. Claude adapter failure counts are not consulted;
an automatic failure fallback is not connected in v1.

There is an unavoidable final race after the last STOP/build/handler check and
the OS dispatch. Another local process with sufficient authority could change
state in that narrow interval. Because the only requested effect is navigation
and the receipt remains unverified, CCCP records the intent and never retries;
it does not claim strict cancellation or exactly-once behavior inside Desktop.

## Safe operator canary

Use a disposable, non-sensitive project first and satisfy the Remote Control
prerequisites above. These commands do not send a message to Claude. The final
command does request that Windows open/focus the bound session, so run it only
while you can see the Desktop app.

```powershell
ccc-supervisor init `
  --coop-root .\coop `
  --project-alias synthetic-desktop-focus `
  --allow-claude-desktop-focus

$sessionLink = Read-Host 'Paste the Remote Control link for the selected Code session'
$binding = $sessionLink |
  ccc-supervisor bind-claude-desktop-session `
    --coop-root .\coop `
    --confirm-pinned-desktop-route |
  ConvertFrom-Json
```

Binding does not open the app. It probes the installed package and current
protocol-handler tuple, then creates or matches the local profile. Inspect the
scrubbed binding receipt and keep its hash and ref local. To make one explicit
manual focus request:

```powershell
ccc-supervisor focus-claude-desktop-session `
  --coop-root .\coop `
  --focus-id ([guid]::NewGuid().ToString()) `
  --profile-sha256 $binding.profile_sha256 `
  --session-ref $binding.session_ref `
  --enable-claude-desktop-focus `
  --confirm-focus-only
```

Visually confirm only whether the expected session appeared. Do not infer that
Claude received work. If it did not appear, record the canary as unconfirmed and
do not retry the same `focus_id`. A new id is not permission to bypass the
cooldown or repeat an ambiguous navigation.

## Rollback and upgrade

To disable the capability, request STOP and start the next run without
`--allow-claude-desktop-focus`. No service, listener, scheduled job, cloud
endpoint, UI Automation selector, or credential is installed by this feature.
This prevents future focus reservations; it cannot undo a navigation Windows
already accepted, close Claude Desktop, or revoke the Remote Control bridge.
Disable or revoke the selected Remote Control session and any Trusted Device
access separately when that is the desired outcome.

After a Claude Desktop update:

1. leave the old allowlist unchanged so focus fails closed;
2. inspect the new signed package, protocol declaration, exact route, accepted
   id family, and lack of automatic-send behavior;
3. update the build tuple and regression fixture in one reviewed change;
4. run the full Python and PowerShell suites;
5. run the opt-in installed-build test with
   `CCCP_TEST_INSTALLED_CLAUDE=1` on Windows;
6. perform one visible disposable canary only with operator approval.

Do not delete a computed `.ccc/` path during rollback. Preserve its local
profile and receipts until ambiguous OS dispatches have been reconciled. Any
later deletion must target a verified path inside the intended project and
follow the operator's local retention and approval rules.
