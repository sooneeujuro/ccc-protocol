# LEDGER_291_CODEX_MANIFEST_ID_SHAPE_HARDENING

VERDICT: ok

Scope: continued local Gemma / quartet harness hardening after the manifest SHA and leaf-filename passes. No model calls, no corpus/figure data, no manuscript commit/push.

What changed in manuscript-atelier working tree:

- Added a shared local helper for relay-safe manifest identifiers:
  - `gemma_manifest_id_guard.is_prompt_pack_run_id`
  - `gemma_manifest_id_guard.is_model_tag`
- Reused the generator's strict prompt-pack run id contract downstream instead of allowing arbitrary copied strings.
- Added shape + mismatch checks for prompt-pack ids across:
  - B/M/T candidate gate
  - length repair queue
  - length repair runner
  - conductor length repair runner
  - repair semantic-review queue
  - repair semantic-review runner
  - quartet scorecard
  - Ollama quartet runner
  - Ollama conductor runner
  - stitch shape checker
- Tightened scorecard validation of semantic-review run `model_tag` to the same local model tag shape used by the producer.
- Added red-path tests for malformed prompt-pack ids and model tags in producer, gate, repair, scorecard, semantic-review, conductor, and stitch-shape surfaces.

Why:

- A downstream manifest could previously compare or relay `prompt_pack_run_id` without proving the value itself was a generator-valid run id.
- Most normal paths were already producer-safe, but this closes the forged-manifest case where matching arbitrary strings could drift into safe manifests.
- This follows the same invariant used in the previous hardening passes: relay-safe manifest fields must be recomputed, value-pinned, or shape-validated.

Validation:

- `python -m py_compile` on touched local-LLM modules passed.
- Targeted tests:
  - `test_ollama_quartet_runner_synthetic.py`
  - `test_ollama_conductor_runner_synthetic.py`
  - `test_gemma_candidate_gate_synthetic.py`
  - `test_gemma_length_repair_queue_synthetic.py`
  - `test_gemma_quartet_scorecard_synthetic.py`
  - `test_gemma_repair_semantic_review_runner_synthetic.py`
- Full suites:
  - `python -m pytest tools\paper-orchestra\local-llm\v0\tests -q` -> 193 passed
  - `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q` -> 466 passed
- `git diff --check -- tools\paper-orchestra\local-llm\v0 tools\paper-orchestra\writing-runner\v0` -> no whitespace errors; Windows CRLF warnings only.

Notes:

- `ccc-protocol` still has unrelated untracked detangle JSONs and the invoice zip; none touched.
- `manuscript-atelier` remains intentionally uncommitted per operator instruction.
- No raw model prose, protected article text, resolved numeric values, captions, local paths, or corpus payloads are included here.

