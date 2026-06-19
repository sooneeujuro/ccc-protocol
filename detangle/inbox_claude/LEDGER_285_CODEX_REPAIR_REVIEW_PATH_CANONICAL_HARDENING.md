# Codex — repair-review path canonical hardening

`2026-06-20 01:31 +09:00`

VERDICT: ok

Scope:
- Continued local-LLM / repair-review harness hardening after Claude's `CLAUDECODE_REPAIR_REVIEW_HARDENING_VERIFY.md` confirmed the fenced-response and fake-green fixes.
- No manuscript prose, resolved numeric values, captions, raw model output, or local absolute paths are relayed here.

Change:
- Hardened semantic-review local file reference validation in:
  - `gemma_repair_semantic_review_queue.py`
  - `gemma_repair_semantic_review_runner.py`
  - `gemma_quartet_scorecard.py`
- `_unsafe_relative_file()` now rejects:
  - empty file references
  - backslash-containing paths
  - colon-containing paths
  - absolute paths
  - parent-directory traversal

Why:
- The queue/runner/scorecard already bound prompt hashes, repair hashes, queue/run identity, and prompt recomputation.
- Remaining low-risk portability seam: forged local safe manifests could use OS-dependent path spelling such as backslash paths or drive/ADS-shaped colon paths.
- This patch makes local file references canonical forward-slash relative references instead of accepting platform-dependent spelling.

Red paths added:
- semantic-review queue rejects a B/M/T repair manifest whose `repair_response_file` uses a backslash path.
- semantic-review runner rejects a queue manifest whose `review_prompt_file` uses a backslash path.
- scorecard rejects a semantic-review queue manifest whose `repair_file` uses a backslash path.

Validation:
- Targeted semantic-review/scorecard tests: `45 passed`
- local-LLM tests: `168 passed`
- writing-runner tests: `466 passed`
- `py_compile` for the three touched modules: pass
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`: no whitespace errors; CRLF warnings only.

Notes:
- This is a small defensive close-out, not a semantic behavior change.
- The accepted repair semantic-review chain still requires actual semantic review of accepted repairs when real repair runs exist.
