# Codex — manifest sha hex hardening

`2026-06-20 02:1x +09:00`

VERDICT: ok

Scope:
- Continued local-LLM harness hardening after LEDGER_288 leaf filename canonicalization.
- No manuscript prose, resolved numeric values, captions, raw model output, or local absolute paths are relayed here.

Change:
- Manifest SHA fields now require lowercase SHA-256 hex strings, not merely 64 characters.
- Hardened:
  - `gemma_candidate_gate.py`
  - `gemma_length_repair_runner.py`
  - `gemma_repair_semantic_review_queue.py`
  - `gemma_repair_semantic_review_runner.py`
  - `gemma_quartet_scorecard.py`

Why:
- Several manifest readers already recomputed hashes before trusting payloads.
- However, accepting arbitrary 64-character strings delayed malformed SHA detection until a later mismatch path.
- Hex-shape validation gives a clearer earlier failure mode and prevents garbage/prose-shaped 64-character identifiers from entering downstream manifest comparisons.

Red paths added:
- candidate gate rejects a prompt-pack task SHA containing non-hex characters.
- length-repair runner rejects a queue prompt SHA containing non-hex characters.
- semantic-review queue rejects an accepted repair SHA containing non-hex characters.
- semantic-review runner rejects a queue prompt SHA containing non-hex characters.
- scorecard rejects a semantic-review response SHA containing non-hex characters.

Validation:
- Targeted candidate/length-repair/semantic-review/scorecard tests: `139 passed`
- local-LLM tests: `180 passed`
- writing-runner tests: `466 passed`
- `py_compile` for touched modules: pass
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`: no whitespace errors; CRLF warnings only.

Notes:
- This is manifest-shape hardening only.
- manuscript-atelier changes remain local/uncommitted per standing gate.
