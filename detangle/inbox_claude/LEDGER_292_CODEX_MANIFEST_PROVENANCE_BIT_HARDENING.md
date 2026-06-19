# LEDGER_292_CODEX_MANIFEST_PROVENANCE_BIT_HARDENING

VERDICT: ok

Scope: continued local Gemma / quartet harness hardening after LEDGER_291 manifest id-shape checks. No model calls, no manuscript commit/push, no corpus/figure data changes.

What changed in manuscript-atelier working tree:

- Tightened manifest trust boundaries beyond schema/id checks.
- Consumers now reject forged or drifted provenance bits before accepting downstream manifests:
  - `provider`
  - `model_called`
  - `network_used`
  - `local_only`
  - `commit_or_relay_safe`
  - manifest count fields such as `response_count` / `candidate_count`
- Applied to:
  - Ollama quartet runner prompt-pack intake
  - Ollama conductor runner prompt-pack and quartet-run intake
  - B/M/T candidate gate prompt-pack and quartet-run intake
  - length repair queue gate intake
  - length repair runner prompt/gate intake
  - conductor length repair runner prompt/conductor intake
  - repair semantic-review queue prompt/scorecard/repair intake
  - quartet scorecard prompt/gate intake
  - stitch shape checker quartet-run intake
- Added red-path tests for networked run manifests, relay-safe-forged manifests, count drift, and malformed provenance-bearing manifests.

Why:

- Previous hardening closed shape issues for file names, SHA fields, and prompt-pack ids.
- A separate trust boundary remained: a forged manifest could retain a valid id while changing provenance flags or count fields.
- This pass makes those flags value-pinned at the consumer boundary, so local-only / no-network / no-relay assumptions are mechanically checked rather than merely producer-intended.

Validation:

- `python -m py_compile` on touched local-LLM modules passed.
- Targeted tests:
  - candidate gate + length repair queue + scorecard: 121 passed
  - Ollama quartet/conductor + stitch shape: 27 passed
  - conductor repair + length repair runner + semantic-review queue: 26 passed
- Full suites:
  - `python -m pytest tools\paper-orchestra\local-llm\v0\tests -q` -> 199 passed
  - `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q` -> 466 passed
- `git diff --check -- tools\paper-orchestra\local-llm\v0 tools\paper-orchestra\writing-runner\v0` -> no whitespace errors; Windows CRLF warnings only.

Notes:

- `ccc-protocol` still has unrelated untracked detangle JSONs and `Anthropic_Invoices_2026-06.zip`; none touched.
- `manuscript-atelier` remains intentionally uncommitted per operator instruction.
- This note contains no raw model prose, protected article text, resolved numeric values, captions, local path payloads, or corpus payloads.

