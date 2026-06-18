# LEDGER_230 - Codex Gemma Tournament Rubric Equipment

Timestamp: 2026-06-18 15:24 KST
From: Codex
To: Claude Code / operator
Thread: Gemma prompt tournament task/rubric hardening

## Status

VERDICT: update

Codex implemented the equipment-side part of the Round 3 capstone recommendation.

## Commit

- manuscript-atelier branch: `codex/draft-context-workspace`
- commit: `b3b73a2 local-llm: add discriminating tournament rubric`

## What Changed

- Added `--scoring-rubric` to `gemma_prompt_tournament.py`.
- Default remains `standard_v1`, preserving the existing 0-2 scoring contract.
- Added `discriminating_v2`, a 0-3 scoring contract for harder task sets:
  - two-sided claim altitude
  - bound tightness
  - caveat survival
  - register fit
  - protected preservation
  - conciseness vs completeness
- Kept the existing hard gates unchanged.
- Fixed the runner blind-surface DRY gap by deriving forbidden variant labels from the prepare-side single source, so evolved labels are covered too.
- Added synthetic tests for both the discriminating rubric and evolved-label scoring leak guard.

## Verification

- `python -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
- Result: `80 passed`

## Next

Do not create more prompt variants yet.

Next useful work is a local-only harder task instantiation that actually exercises the `discriminating_v2` rubric. It should introduce task pressure, not resolved value/prose relay:

1. overreach-looking but bounded evidence,
2. a weak/partial evidence clause,
3. protected near-miss pressure,
4. Discussion-register compression pressure.

Any next 45-run should use this harder task plus `--scoring-rubric discriminating_v2`, otherwise it will likely reproduce the saturated Round 1/2/3 result.
