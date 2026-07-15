# RUN_STATE

Status: active
Project:
Started:
Operator:
Supervisor mode: disabled
Run ID:
Generation:

## Current Objective

Describe the current objective here.

## Heartbeats

- Codex interval:
- Codex quiet backoff:
- Codex quiet streak:
- Claude interval:
- Claude quiet backoff:
- Claude quiet streak:
- Last Codex heartbeat:
- Last Claude heartbeat:

## Supervisor Bounds

- Watch TTL:
- Lease TTL:
- Claim TTL:
- Maximum wakes per agent:
- Maximum attempts:
- Maximum handoff depth:
- Maximum payload bytes:
- Maximum output bytes:
- Automatic timer wake: disabled
- UI nudge: disabled
- Cloud doorbell: disabled

## Adapter Bindings

- Claude adapter: disabled
- Claude conversation bound: no
- Claude permission profile: observe
- Codex adapter: disabled
- Codex thread bound: no
- Codex permission profile: read-only

Conversation and thread identifiers belong in the local supervisor store. Do
not paste them into public status or cloud metadata unless they are replaced by
an opaque external id.

## Write Scope

- Allowed:
- Forbidden:

## API / Cost Policy

- API calls:
- Budget:
- Approval required for:

## GitHub Snapshot Policy

- Snapshot interval:
- Remote:
- Branch:
- Last push:

## Pending Decisions

- None

## Standing Audit

If no task is pending, do this:

- Check for STOP.
- If supervised, verify run generation, lease fence, and remaining budgets.
- Check inboxes.
- Validate recent outputs.
- Report only if something changed or needs operator attention.

## Safe shared status

Allowed: opaque ids, generation, enum state, booleans, counts, hashes, and a
coarse allowlisted failure class.

Forbidden: task/prompt/result prose, stdout/stderr, commands, paths,
credentials, corpus/sidecar/protected text, manuscript text.
