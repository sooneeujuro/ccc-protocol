# Codex — length-repair path canonical follow-up

`2026-06-20 01:4x +09:00`

VERDICT: ok

Scope:
- Follow-up to `LEDGER_285_CODEX_REPAIR_REVIEW_PATH_CANONICAL_HARDENING.md`.
- No manuscript prose, resolved numeric values, captions, raw model output, or local absolute paths are relayed here.

Change:
- Extended the same canonical local-file-reference rule to the upstream B/M/T length-repair runner.
- `gemma_length_repair_runner.py` now rejects queue manifest file references that are:
  - empty
  - backslash-containing
  - colon-containing
  - absolute
  - parent-directory traversal

Why:
- The length-repair queue already emits prompt paths with `.as_posix()`.
- The runner now rejects forged or platform-dependent queue path spelling before opening local prompt files.
- This keeps the length-repair stage consistent with the semantic-review queue/runner/scorecard path guard added in LEDGER_285.

Red path added:
- A forged length-repair queue manifest whose `repair_prompt_file` uses a backslash path is rejected with `gemma_length_repair_prompt_file_invalid`.

Validation:
- Length-repair + semantic-review + scorecard targeted tests: `53 passed`
- local-LLM tests: `169 passed`
- writing-runner tests: `466 passed`
- `py_compile` for the touched runner/queue/scorecard modules: pass
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`: no whitespace errors; CRLF warnings only.

Notes:
- This is defensive manifest hardening only.
- manuscript-atelier changes remain local/uncommitted per standing gate.
