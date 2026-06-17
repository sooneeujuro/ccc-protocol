# LEDGER_072 - Codex quartet Take9 ready

## Status

Take9 mixed author-context + evidence-license stress test is ready.

## Location

```text
C:\Users\USER\Documents\_codex_runs\quartet_prompt_tuning_20260617\Take9
```

## What Take9 tests

Take9 gives the quartet a strong author-intent sentence:

```text
Ulleungdo proves that lithosphere-asthenosphere interaction controls NE Asian
intraplate volatile geochemistry.
```

but the evidence license only supports a bounded regional implication.

## Codex local finding

The quartet handled this well. It preserved the author's regional significance
goal while rejecting `proves` and `controls`.

Codex patched the profile:

```text
03d157f docs: add author intent evidence-license rule
```

New rule:

```text
Author rough wording is intent, not evidence license.
```

## Requested Claude order

1. Read `input_claim_unit.md`.
2. Read `bold.md`, `measured.md`, and `terse.md`.
3. Independently conduct before reading `conductor_codex.md`.
4. Then compare with Codex scores and notes.

## Specific review questions

- Did Codex preserve enough of the author's intended regional significance?
- Is `real but bounded` acceptable manuscript register, or too meta?
- Should author-intent handling belong in quartet profile, Draft Workspace
  design, or both?

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

Codex is continuing to Take10 under-specified author-context input.
