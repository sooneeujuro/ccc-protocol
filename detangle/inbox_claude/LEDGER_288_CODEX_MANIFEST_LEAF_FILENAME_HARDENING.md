# Codex — manifest leaf filename hardening

`2026-06-20 02:0x +09:00`

VERDICT: ok

Scope:
- Continued local-LLM harness hardening after LEDGER_285-287.
- No manuscript prose, resolved numeric values, captions, raw model output, or local absolute paths are relayed here.

Change:
- Added canonical leaf filename checks for manifest fields that must name a single local response file.
- Hardened:
  - `gemma_candidate_gate.py`
  - `gemma_length_repair_runner.py`
  - `gemma_repair_semantic_review_queue.py`
  - `gemma_quartet_scorecard.py`
- Hardened relative-file helpers to reject non-canonical `.` segments in semantic-review local file references.

Rejected shapes:
- empty leaf filenames
- `.` / `..`
- slash or backslash separators
- colon-containing names
- newline/carriage-return-containing names

Why:
- LEDGER_285-286 closed multi-component local path references.
- This follow-up closes the sibling leaf-file seam so forged run/gate/repair manifests cannot defer bad filename shapes into later file-open errors or platform-specific path interpretation.

Red paths added:
- candidate gate rejects a forged run manifest response file containing a colon.
- length-repair runner rejects a forged gate manifest file containing a colon.
- semantic-review queue rejects an accepted repair with an empty source file.
- scorecard rejects an accepted repair source file containing a colon.

Validation:
- Targeted candidate/length-repair/semantic-review/scorecard tests: `123 passed`
- local-LLM tests: `175 passed`
- writing-runner tests: `466 passed`
- `py_compile` for touched modules: pass
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`: no whitespace errors; CRLF warnings only.

Notes:
- This is defensive manifest-shape hardening only.
- manuscript-atelier changes remain local/uncommitted per standing gate.
