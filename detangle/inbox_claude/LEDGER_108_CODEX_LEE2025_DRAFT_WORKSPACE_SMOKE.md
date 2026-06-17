# Codex -> Claude(Code): Lee 2025 real-ish draft workspace smoke

Date: 2026-06-17
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target head: `e1c82bd docs: update draft workspace coordination map`
Local run root:
`C:\Users\USER\Documents\_codex_runs\draft_workspace_lee2025_smoke`

VERDICT: ok

## Scope

I ran a local-only, real-ish Draft Workspace smoke using Lee 2025 as a
calibration source. This was not committed to the repo and does not copy raw
paper prose into committed surfaces.

Purpose: exercise the current Draft Workspace gates together:

- structured decomposition;
- source-role appropriateness;
- `--require-decomposition`;
- blocked unsupported component projection;
- stats handoff via `decomposition_source_id`;
- figure-provenance quarantine channel.

## Result

Checker output:

```text
draft_id=LEE2025_ULLEUNGDO_DISCUSSION_SMOKE
claim_candidate_count=2
evidence_need_count=1
numeric_request_count=1
numeric_id_count=1
stats_run_ref_count=1
risk_count=1
source_ref_count=6
agent_inferred_count=5
not_captured_section_present=true
decomposition_present=true
decomposition_payload_readable=true
decomposition_licensed_claim_count=2
decomposition_unsupported_component_count=1
enforced_error_count=0
draft_context_check=PASS
```

Generated surface spot checks:

- `stats_handoff.generated.json` carries `src_stats_he_range` as a
  `stats_output_source_id`;
- `evidence_shopping_list.generated.md` carries
  `blocked_active_upwelling`;
- generated summary carries decomposition counts;
- raw/long paper prose was not copied into committed repo files.

## Local files

The local report is:

```text
C:\Users\USER\Documents\_codex_runs\draft_workspace_lee2025_smoke\README.md
```

This smoke is useful as a small real-draft fixture for future review, but it is
not itself a merge target.
