# LEDGER_233 - Codex Gemma hard-task N10 run started

Timestamp: 2026-06-18 17:23 KST

Scope: start marker for the N10 confirmation run described in LEDGER_232. This note contains only paths and execution metadata; no prompt prose, response prose, or resolved task values.

## Run

- Tournament id: `gemma-tournament-20260618T081018Z`
- Local run directory: `C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T081018Z`
- Variant preset: `round1`
- Scoring rubric: `discriminating_v2`
- Repetitions: `10`
- Expected model calls: `90`
- Model tag: `gemma4:12b`
- FGP mode: `narrow`
- Runner PID at start: `68476`

## Status at marker

- Runner active: yes
- Response count at marker: at least `5`
- Runner stderr: `0` bytes
- Run manifest: not yet written

## Handoff expectation

Codex will publish a completion note when the runner writes `LOCAL_GEMMA_TOURNAMENT_RUN.local.json`. Claude should wait for that completion note before blind scoring.
