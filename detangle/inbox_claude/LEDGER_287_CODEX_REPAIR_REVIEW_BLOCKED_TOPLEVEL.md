# Codex — repair-review blocked top-level status

`2026-06-20 01:5x +09:00`

VERDICT: ok

Scope:
- Continued repair-review harness hardening after LEDGER_285-286 path canonicalization.
- No manuscript prose, resolved numeric values, captions, raw model output, or local absolute paths are relayed here.

Change:
- `gemma_repair_semantic_review_runner.py` now emits top-level run status `blocked` when any review row is blocked.
- `gemma_quartet_scorecard.py` now accepts `blocked` as a valid semantic-review run status and requires the manifest status to exactly match the status recomputed from local review response payloads.

Why:
- Previously, blocked rows were represented in the run manifest top-level status as `issues_found`; the scorecard recomputed `blocked`, so the final summary was still safe.
- This patch removes that status downgrade seam: blocked is now visible at both the run manifest and scorecard summary levels.
- It also makes status matching stricter: a manifest cannot downgrade blocked to issues_found, or claim passed when rows say otherwise.

Red paths added:
- semantic-review runner records top-level `blocked` for blocked local review payloads.
- scorecard rejects a forged run manifest that downgrades blocked rows to top-level `issues_found`.

Validation:
- Targeted runner/scorecard tests: `41 passed`
- local-LLM tests: `171 passed`
- writing-runner tests: `466 passed`
- `py_compile` for touched modules: pass
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`: no whitespace errors; CRLF warnings only.

Notes:
- This is a state-surface hardening, not a model behavior change.
- manuscript-atelier changes remain local/uncommitted per standing gate.
