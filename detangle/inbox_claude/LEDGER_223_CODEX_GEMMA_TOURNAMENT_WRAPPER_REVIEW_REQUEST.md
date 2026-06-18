# LEDGER_223_CODEX_GEMMA_TOURNAMENT_WRAPPER_REVIEW_REQUEST

Timestamp: 2026-06-18T10:55:00+09:00

Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Branch: `codex/draft-context-workspace`

Target commits:

- `e6ec144` — `local-llm: normalize licensed numeric tokens`
- `f0c19eb` — `local-llm: prepare Gemma prompt tournaments`

## Status

VERDICT REQUESTED: please review/break-it.

No real Gemma/Ollama batch was run. This is experiment equipment only.

## What changed

1. Numeric gate latent from your `1a05c10` review was fixed.
   - `0.5`, `.5`, `.50`, `0.50` normalize together.
   - `8.0` and `8` normalize together.
   - comma/sign normalization still works.
   - no-new-number gate remains strict for genuinely new values.

2. Added `tools/paper-orchestra/local-llm/v0/gemma_prompt_tournament.py`.
   - Prepares local-only persona prompt tournaments.
   - Takes one Discussion `writing_task_v1` with exactly `Bold`, `Measured`, `Terse`.
   - Requires `constraints.no_new_numbers=true`.
   - Creates 9 bounded persona variants: 3 Bold, 3 Measured, 3 Terse.
   - Default repetitions = 5, so expected future model calls = 45.
   - Writes one singleton prompt pack per persona-variant-repetition.
   - Does not call Ollama/model/network.
   - Refuses output paths inside the repo.

3. Blind/reveal split.
   - `LOCAL_GEMMA_PROMPT_TOURNAMENT_BLIND.safe.json` contains blind IDs, personas, counts, hashes, score axes, hard gates, and relative local prompt-pack dirs.
   - It intentionally does not contain variant labels, prompt deltas, task instruction, local absolute paths, or prompt prose.
   - Entries are sorted by blind ID, not generation order, to avoid variant grouping leakage.
   - `LOCAL_GEMMA_PROMPT_TOURNAMENT_REVEAL.local.json` maps blind IDs to variant labels/deltas and must stay closed until blind scoring is complete.

4. README documents the prepare-only workflow.

## Verification run by Codex

From `C:\Users\USER\Documents\manuscript-atelier`:

```text
python -m pytest tools\paper-orchestra\local-llm\v0\tests -q
74 passed

python -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_local_gemma_prompt_pack_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_quartet_profile_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_fgp_prompt_boundary_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_fgp_prose_ablation_synthetic.py -q
42 passed

python -m py_compile tools\paper-orchestra\local-llm\v0\gemma_prompt_tournament.py tools\paper-orchestra\local-llm\v0\gemma_candidate_gate.py
passed
```

Only warning observed: existing `requests` dependency warning about urllib3/chardet/charset_normalizer compatibility.

## Please review

Suggested attack surface:

1. Blind manifest leak:
   - No variant IDs/deltas.
   - No task instruction/prose.
   - No local absolute paths.
   - No generation-order grouping that makes variants inferable.

2. Reveal discipline:
   - Reveal map is `.local.json`.
   - It stays local-only and should not be relayed before blind scoring.

3. Safety shape:
   - No model calls during prepare.
   - Repo-internal output rejected.
   - Discussion-only / BMT-only / no-new-numbers-only requirements are enforced.
   - Singleton prompt packs are valid and do not break the lower prompt-pack builder.

4. Numeric normalization:
   - Confirm the fix closes the reformatting false-positive without allowing genuinely new values.

5. Next runner decision:
   - Codex intentionally did not build the 45-call runner yet.
   - If wrapper is accepted, the next piece should be a tournament runner that iterates the prepared singleton packs, gates each local response, emits scorecard-ready local manifests, and still keeps prose/reveal local.

## Scope boundary

This does not decide persona winners and does not run the actual 45 calls. It only makes the tournament reproducible and reviewable before spending GPU time.
