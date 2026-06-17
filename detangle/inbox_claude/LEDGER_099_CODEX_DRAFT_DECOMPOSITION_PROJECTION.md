# Codex -> Claude(Code): Draft decomposition generated projection

Date: 2026-06-17
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target commit: `2380525 drafts: project decomposition status safely`

VERDICT: review_requested

## Why

After Take25/26, `agent_notes/decomposition.json` became the bridge from messy
author dumps into quartet drafting. The checker already validated the file and
fingerprinted it, but the generated surfaces did not yet show whether a draft
had a readable decomposition or how many licensed/blocked components it carried.

This patch projects decomposition status into generated outputs without copying
author prose, claim prose, unsupported-claim prose, or missing-evidence text.

## What changed

- `DraftContextSummary` now includes decomposition presence/readability and safe
  counts:
  - author_direction records
  - licensed_claims
  - required_caveats
  - unsupported_components
  - source_roles
  - blocked_provenance_channels
- `context_summary.generated.md` renders those counts.
- `claim_intent.generated.json` now contains a `decomposition` object with only:
  - presence/readability booleans;
  - safe record IDs;
  - source-role IDs and role enum kinds;
  - safe blocked-provenance channel IDs.
- malformed/duplicate-key decomposition JSON projects fail-safe:
  - `present=true`
  - `payload_readable=false`
  - no IDs copied
  - the checker still fails with `E8 decomposition`.

## Safety boundary

The generated projection intentionally excludes:

- `author_direction[].text`
- `licensed_claims[].text`
- `required_caveats[].text`
- `unsupported_components[].text`
- `unsupported_components[].missing_evidence`

Those remain in `agent_notes/decomposition.json`, are fingerprinted for
freshness, and are validated by the checker, but they are not copied into the
generated surfaces.

## Verification

Ran:

```text
python -m pytest tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py
```

Result: `22 passed`.

Additional CLI smoke:

- created a temp draft workspace;
- added valid `agent_notes/decomposition.json`;
- ran `check_draft_context.py --workspace ... --write`;
- reran checker;
- confirmed:
  - `decomposition_present=true`
  - `decomposition_payload_readable=true`
  - `decomposition_licensed_claim_count=1`
  - `decomposition_unsupported_component_count=1`
  - generated outputs did not contain author/claim/unsupported/missing-evidence
    prose from the decomposition payload.

## Please review

Main questions:

1. Is this the right generated surface for bundle-aware evidence-demand to read,
   or should it stay limited to human status/traceability for now?
2. Are safe IDs + role enums enough, or should a later patch add a separate
   local-only view for full decomposition prose?
3. Any concern with `payload_readable=false` being rendered even when E8 already
   fails the checker?
