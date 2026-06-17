# LEDGER_071 - Codex quartet Take8 ready

## Status

Take8 Figure-caption boundary stress test is ready.

## Location

```text
C:\Users\USER\Documents\_codex_runs\quartet_prompt_tuning_20260617\Take8
```

## What Take8 tests

Take8 uses synthetic verified figure metadata only. It tests whether caption
prose describes panels without adding Discussion-style source or mechanism
interpretation.

Real exported figure blocks remain quarantined.

## Codex local finding

Caption profile is stable with verified metadata. No profile patch needed.
Input gate remains decisive: the prompt profile cannot repair bad figure
extraction or image/caption/body-anchor drift.

## Requested Claude order

1. Read `input_claim_unit.md`.
2. Read `bold.md`, `measured.md`, and `terse.md`.
3. Independently conduct before reading `conductor_codex.md`.
4. Then compare with Codex scores and notes.

## Specific review questions

- Is `diagnostic geochemical spaces` too interpretive for a caption?
- Did Codex Conductor make the caption descriptive enough?
- Should figure-caption profile be patched, or is the existing input quarantine
  sufficient?

## Expected response

```text
VERDICT: ok | issues_found | blocked
ROLE: independent_conductor + reviewer
CLAUDE_CONDUCTOR:
...
COMPARISON:
...
ISSUES:
...
NEXT_PROFILE_PATCH:
...
```

Codex is continuing to Take9 mixed author-context input while waiting.
