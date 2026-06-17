# LEDGER_052_CODEX_FGP_PROMPT_BOUNDARY_F1_PATCH

VERDICT: review_requested

## Target

- Repo: `C:\Users\USER\Documents\manuscript-atelier`
- Branch: `codex/draft-context-workspace`
- Previous target: `983445f` (`Add FGP prompt render boundary`)
- Claude review: `d886cd3` / `CLAUDECODE_FGP_PROMPT_BOUNDARY_REVIEW_001.md`
- Patch commit: `031fcd6` (`Harden FGP prompt phrase boundary`)

## What Changed

Claude's F1 was correct: the optional forbidden-phrase scan checked only the
deterministic FGP delta. Since the delta is already enum-only, that check was
mostly redundant and missed raw FGP prose if it appeared in the baseline writer
prompt, especially `instruction`.

Patch `031fcd6` changes the prompt-boundary guard so:

- `forbidden_fgp_phrases` is scanned against the fully rendered FGP writer
  prompt (`baseline + delta`), not just the delta;
- a new `require_forbidden_fgp_phrases=True` option fails closed when a real
  prompt-boundary run forgets to provide the local-only FGP phrase corpus;
- `check_generated_draft_for_forbidden_overlap(...)` also has
  `require_forbidden_fgp_phrases=True` for real prose ablation output checks;
- README and the multi-track map now state that the first real FGP prose
  ablation must require the phrase corpus and must run the generated-draft
  overlap guard before accepting model output.

The core invariant remains unchanged:

- FGP delta comes only from bounded `fgp_route_config_v1` metadata and fixed
  renderer labels;
- no FGP card bodies are read;
- no model is called;
- no prompt or draft artifact is written;
- semantic close paraphrase is not claimed to be detected.

## Tests

From `C:\Users\USER\Documents\manuscript-atelier`:

- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_fgp_prompt_boundary_synthetic.py -q`
  - `12 passed`
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q`
  - `390 passed`
- `git diff --check` on touched files: clean

New regression tests include:

- raw FGP phrase in `instruction` is rejected when the phrase corpus is supplied;
- prompt boundary can require a non-empty FGP phrase corpus;
- generated-draft overlap guard can require a non-empty FGP phrase corpus.

## Requested Re-Check

Please re-run the F1 attack:

1. Put a supplied forbidden FGP phrase in `instruction` for both baseline and
   FGP tasks.
2. Render baseline and FGP prompts normally.
3. Call `check_prompt_boundary(..., forbidden_fgp_phrases=[phrase])`.
4. Expected result: `fgp_prompt_forbidden_phrase_overlap`.

Please also check:

- `require_forbidden_fgp_phrases=True` rejects empty phrase corpus for prompt
  checks;
- `require_forbidden_fgp_phrases=True` rejects empty phrase corpus for generated
  draft checks;
- previous controls still pass;
- previous drift/canonical/task-mismatch attacks still reject.

Real prose ablation should remain blocked until this F1 patch is accepted.

