# LEDGER_090 - Codex Quartet Take25 Ready

Status: review_requested

Target repo: `C:\Users\USER\Documents\manuscript-atelier`

Branch: `codex/draft-context-workspace`

Latest profile commit: `be4ace2` (`docs: normalize mixed author dumps before drafting`)

Local run folder:

`C:\Users\USER\Documents\_codex_runs\quartet_prompt_tuning_20260617\Take25`

## Take25 Purpose

Stress-test a realistic messy author dump:

- mixed Korean/English notes;
- overclaim and underclaim mixed together;
- desired regional framing;
- citation/source roles;
- figure-provenance warning;
- missing evidence needs.

## Codex Result

VERDICT: ok

The quartet normalized the dump into author direction, licensed claims, unsupported components, source roles, and blocked provenance channels before drafting. Final output preserved the desired `not merely local` direction while blocking active-upwelling and unverified figure claims.

Profile patch:

- for mixed author dumps, normalize before drafting;
- hard-fail direct drafting when decomposition is needed.

## Review Request

Please review:

1. whether the final paragraph preserves enough of the operator's intended force;
2. whether `regional source-context implication` is too abstract;
3. whether Take26 should require a structured JSON-like decomposition before prose.

No target-repo implementation beyond docs/profile update was performed.
