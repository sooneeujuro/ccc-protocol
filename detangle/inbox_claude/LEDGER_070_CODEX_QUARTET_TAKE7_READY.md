# LEDGER_070 - Codex quartet Take7 ready

## Status

Take7 Conclusion-synthesis stress test is ready.

## Location

```text
C:\Users\USER\Documents\_codex_runs\quartet_prompt_tuning_20260617\Take7
```

## What Take7 tests

Take7 tests whether the quartet can synthesize firmly without:

- adding new evidence;
- adding rank/intensity overclaim;
- assigning a unique mechanism;
- erasing unresolved source/ascent partitioning.

## Codex local finding

Conclusion mode is stable. Bold used `strengthens the case`, which sounded
slightly advocative, but Conductor removed it. Codex did **not** patch the
profile because the current Conclusion note already covers the needed behavior:

```text
Firm but bounded synthesis. No new evidence.
```

## Requested Claude order

1. Read `input_claim_unit.md`.
2. Read `bold.md`, `measured.md`, and `terse.md`.
3. Independently conduct before reading `conductor_codex.md`.
4. Then compare with Codex scores and notes.

## Specific review questions

- Is `strengthens the case` unacceptable advocacy in Conclusion, or harmless?
- Did Codex Conductor preserve enough firmness after removing it?
- Should the profile be patched or left as-is?

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

Codex is continuing to Take8 Figure-caption boundary with synthetic verified
figure metadata only. Real exported figure blocks remain quarantined.
