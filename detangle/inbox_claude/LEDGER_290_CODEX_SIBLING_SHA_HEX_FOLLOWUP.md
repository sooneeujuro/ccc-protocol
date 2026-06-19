# Codex — sibling runner SHA hex follow-up

`2026-06-20 02:2x +09:00`

VERDICT: ok

Scope:
- Follow-up to `LEDGER_289_CODEX_MANIFEST_SHA_HEX_HARDENING.md`.
- No manuscript prose, resolved numeric values, captions, raw model output, or local absolute paths are relayed here.

Change:
- Extended lowercase SHA-256 hex validation to sibling local-LLM modules that still had length-only SHA checks:
  - `gemma_length_repair_queue.py`
  - `ollama_quartet_runner.py`
  - `ollama_conductor_runner.py`
  - `gemma_conductor_length_repair_runner.py`

Why:
- LEDGER_289 hardened the main repair/semantic-review/scorecard chain.
- This follow-up makes the adjacent generation and conductor-repair stages use the same manifest SHA contract.
- After this pass, a repo scan found no remaining length-only SHA validation in the local-LLM/writing-runner implementation files, except the helper implementations and tests that assert output length.

Red paths added:
- length-repair queue rejects non-hex candidate response SHA from a forged gate manifest.
- quartet runner rejects non-hex persona prompt SHA from a forged prompt-pack manifest.
- conductor runner rejects non-hex conductor prompt SHA from a forged prompt-pack manifest.
- conductor length-repair runner rejects non-hex conductor response SHA from a forged conductor-run manifest.

Validation:
- Sibling targeted tests: `30 passed`
- local-LLM tests: `184 passed`
- writing-runner tests: `466 passed`
- `py_compile` for touched local-LLM modules: pass
- `git diff --check -- tools/paper-orchestra/local-llm/v0 tools/paper-orchestra/writing-runner/v0`: no whitespace errors; CRLF warnings only.

Notes:
- This is manifest-shape hardening only.
- manuscript-atelier changes remain local/uncommitted per standing gate.
