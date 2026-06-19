# LEDGER_293_CODEX_MANIFEST_TIMESTAMP_SHAPE_HARDENING

VERDICT: ok

Scope: continued local Gemma / quartet harness hardening after LEDGER_291 id-shape and LEDGER_292 provenance-bit checks. No model calls, no manuscript commit/push, no corpus/figure data changes.

What changed in manuscript-atelier working tree:

- Added shared UTC timestamp shape guard:
  - `gemma_manifest_id_guard.is_utc_created_at`
- Consumers now reject forged `created_at` fields that are not compact UTC manifest timestamps.
- Applied to manifest intake across:
  - Ollama quartet runner prompt-pack manifest
  - Ollama conductor runner prompt-pack and quartet-run manifests
  - B/M/T candidate gate prompt-pack and quartet-run manifests
  - length repair queue prompt and gate manifests
  - length repair runner prompt, queue, and gate manifests
  - conductor length repair runner prompt and conductor-run manifests
  - repair semantic-review queue prompt, scorecard, and repair-run manifests
  - repair semantic-review runner queue manifest
  - quartet scorecard prompt, gate, repair, conductor, conductor-repair, semantic-review run, and semantic-review queue manifests
  - stitch shape checker quartet-run manifest
- Added red-path tests for invalid `created_at` values in prompt-pack, run, gate, queue, scorecard, and stitch-shape surfaces.

Why:

- The previous passes pinned id fields, provenance bits, counts, filenames, and SHA fields.
- `created_at` remained a low-risk string field in many consumed manifests. A forged manifest could place prose/path-like text there while keeping other fields valid.
- This pass makes timestamp fields shape-validated at the consumer boundary, completing the small safe-string surfaces left by the prior id/provenance hardening.

Validation:

- `python -m py_compile` on touched local-LLM modules passed.
- Targeted tests:
  - Ollama quartet + candidate gate + scorecard: 129 passed
  - semantic-review runner + stitch shape: 20 passed
- Full suites:
  - `python -m pytest tools\paper-orchestra\local-llm\v0\tests -q` -> 204 passed
  - `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q` -> 466 passed
- `git diff --check -- tools\paper-orchestra\local-llm\v0 tools\paper-orchestra\writing-runner\v0` -> no whitespace errors; Windows CRLF warnings only.

Notes:

- `ccc-protocol` still has unrelated untracked detangle JSONs and `Anthropic_Invoices_2026-06.zip`; none touched.
- `manuscript-atelier` remains intentionally uncommitted per operator instruction.
- This note contains no raw model prose, protected article text, resolved numeric values, captions, local path payloads, or corpus payloads.

