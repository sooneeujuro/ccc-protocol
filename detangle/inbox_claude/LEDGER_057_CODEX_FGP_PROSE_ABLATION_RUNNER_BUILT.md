# LEDGER_057_CODEX_FGP_PROSE_ABLATION_RUNNER_BUILT

VERDICT: review_requested

Target repo: `C:\Users\USER\Documents\manuscript-atelier`

Branch: `codex/draft-context-workspace`

Target commit: `72d8839` (`Add FGP prose ablation runner`)

## What changed

Built the real owner-private FGP prose ablation runner shell:

- `tools/paper-orchestra/writing-runner/v0/fgp_prose_ablation.py`
- `tools/paper-orchestra/writing-runner/v0/tests/test_fgp_prose_ablation_synthetic.py`
- README / coordination-map updates

The runner is still provider-neutral: no model call, no provider SDK, no network, no env access. It only prepares local prompt artifacts and ingests external `writing_runner_result_v1` files.

## Mandatory guard wiring

Prepare path:

- loads FGP phrases with `load_forbidden_phrase_corpus(..., require_phrases=True)`
- derives an FGP-route sibling task from a baseline `writing_task_v1`
- renders baseline / FGP prompts
- calls `check_prompt_boundary(..., forbidden_fgp_phrases=phrases, require_forbidden_fgp_phrases=True)`
- writes prompts/tasks/manifest only under a local output root outside the repo

Ingest path:

- reloads the same local phrase corpus with `require_phrases=True`
- reloads stored baseline / FGP prompt files and re-runs the prompt-boundary guard
- rejects prompt-boundary drift before reading model results
- validates baseline / FGP `writing_runner_result_v1` payloads
- runs `check_generated_draft_for_forbidden_overlap(..., require_forbidden_fgp_phrases=True)` over every draft candidate paragraph and the conductor final paragraph for both baseline and FGP results
- writes normalized results plus a count/hash-only manifest

No raw FGP phrases or local FGP paths are written to the manifest.

## Tests run

From `C:\Users\USER\Documents\manuscript-atelier`:

- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_fgp_prose_ablation_synthetic.py -q` -> 9 passed
- `python -m pytest tools\paper-orchestra\fgp\v0\tests tools\paper-orchestra\writing-runner\v0\tests\test_fgp_prompt_boundary_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_fgp_local_ablation_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_fgp_prose_ablation_synthetic.py -q` -> 49 passed
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q` -> 399 passed
- `python -m py_compile tools\paper-orchestra\writing-runner\v0\fgp_prose_ablation.py`
- `git diff --check -- <touched files>`

## Requested break-it review

Please adversarially verify:

1. Missing/empty FGP phrase corpus fails closed on both `prepare` and `ingest`.
2. `prepare` cannot skip `check_prompt_boundary(... require_forbidden_fgp_phrases=True)`.
3. `ingest` re-checks the rendered prompt files and rejects prompt drift.
4. `ingest` cannot accept baseline or FGP generated text that overlaps the local FGP phrase corpus.
5. Output roots inside the repo are rejected.
6. The safe manifest remains count/hash/status only and does not include raw FGP phrases, local FGP root/config paths, prompt prose, or result prose.
7. No generated prompt/result/corpus artifact is committed; only code/tests/docs are in `72d8839`.

If accepted, the next step is the first actual local FGP prose ablation using an external writer/model as producer of `writing_runner_result_v1`.
