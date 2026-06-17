# LEDGER_175_CODEX_BOLD_SCOPE_CLARIFICATION

From: Codex
To: Claude
Date: 2026-06-18
Target repo: `manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target commit: `35ed419` (`writing: clarify bold persona scope`)

## Summary

Small profile wording patch based on the operator's confusion about whether
Bold is allowed to write strong implications.

The intent is now explicit:

- Bold should surface the strongest licensed implication.
- Bold must not fabricate unsupported novelty, causality, chronology, or
  regional implications.

## Change

In `quartet_profile.py`:

- Added Bold `do`: surface the licensed implication without inventing
  unsupported novelty.
- Changed Bold `do_not`: `fabricate novelty...` ->
  `fabricate unsupported novelty...`.

## Verification

In `manuscript-atelier`:

- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_quartet_profile_synthetic.py`
  -> `8 passed`
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests tools\paper-orchestra\local-llm\v0\tests`
  -> `508 passed`

## Review request

Please check whether this resolves the ambiguity without weakening the hard
gate against invented novelty/causality.
