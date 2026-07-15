# Supervisor Policy

The local supervisor is disabled until the operator completes this policy.
`RUN_STATE.md` remains the human run summary; `coop/.ccc/` is the local-only
lifecycle state store when supervisor v1 is enabled.

## Scope

- Project alias (non-sensitive token):
- Operator:
- Same-host owner:
- Allowed workspace roots:
- Forbidden roots:
- Protected data classes:

## Lifecycle bounds

- Watch TTL:
- Lease TTL:
- Claim TTL:
- Maximum wakes per agent:
- Maximum task attempts:
- Maximum handoff depth:
- Maximum handoffs per result:
- Maximum payload bytes:
- Maximum output bytes:

## Adapter posture

- Claude adapter: disabled
- Claude permission profile: observe
- Codex app-server adapter: disabled
- Codex permission profile: read-only
- Automatic timer wakes: disabled
- Windows UI nudge: disabled
- Cloud doorbell: disabled

Enabling an adapter requires an explicit operator decision and a successful
`probe`. Do not fall back to UI automatically.

## Effect policy

- Read-only tasks may retry only when the adapter marks a stable failure
  retryable and the attempt budget remains.
- Reversible tasks require verified rollback or idempotency.
- Mutating and external tasks do not retry automatically.
- A handoff cannot expand write scope, tool access, cost authority, or external
  side-effect authority.

## STOP policy

- STOP actor(s):
- Adapter cancellation grace period:
- Hard timeout:
- Operator reconciliation contact:

`STOP.md` moves the run to draining. Removing the file does not resume the old
generation.

## Audit and data boundary

Shareable status is limited to opaque ids, generation, enums, booleans, counts,
and hashes. Do not publish prompts, result prose, stdout/stderr, command lines,
local paths, credentials, corpus content, sidecars, protected text, or
manuscript text.

`coop/.ccc/` must remain local and ignored by Git.

## Future doorbell

The future sooneeujuro.com/Vercel/Supabase doorbell is not enabled by this
policy. If separately approved, it is outbound-poll and metadata-only. It may
request `wake`, `stop`, or `status_probe`; it may not carry work or free text.

## Operator approvals

- [ ] Local state-store smoke tests passed.
- [ ] `.ccc/` ignore rule verified.
- [ ] Live Claude adapter approved.
- [ ] Live Codex adapter approved.
- [ ] Bounded `serve` approved.
- [ ] Workspace-write profile approved.
- [ ] UI nudge experiment approved.
- [ ] Metadata-only cloud doorbell approved.
