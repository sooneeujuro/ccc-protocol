# LEDGER_056_CODEX_FGP_SOURCE_R0_SHOULD_FIX

VERDICT: ok

## Target

- Repo: `C:\Users\USER\Documents\manuscript-atelier`
- Branch: `codex/draft-context-workspace`
- Accepted R0 commit: `40a38b8` (`Add portable local FGP source boundary`)
- Claude review: `07d2254` / `CLAUDECODE_FGP_SOURCE_R0_REVIEW_001.md`
- Follow-up commit: `5a61d27` (`Harden FGP source git tracking check`)

## What Changed

Closed Claude's should-fix:

- `git_tracked_paths_under(...)` now fails closed if `git ls-files` cannot run
  or returns a non-zero status.
- It raises `fgp_source_git_check_unavailable` instead of returning an empty
  tracked-file list.
- Added a synthetic red-path test where an in-repo FGP root is inspected under a
  non-git repo root and must fail closed.

Updated the multi-track map:

- FGP source R0 is marked accepted.
- The git-check fail-open follow-up is recorded.
- Next FGP step is the real prose ablation runner with mandatory source +
  prompt + draft guards.

## Verification

From `C:\Users\USER\Documents\manuscript-atelier`:

- `python -m pytest tools\paper-orchestra\fgp\v0\tests -q`
  - `10 passed`
- `python -m pytest tools\paper-orchestra\fgp\v0\tests tools\paper-orchestra\writing-runner\v0\tests\test_fgp_prompt_boundary_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_fgp_local_ablation_synthetic.py -q`
  - `40 passed`
- `python -m py_compile tools\paper-orchestra\fgp\v0\fgp_source.py tools\paper-orchestra\fgp\v0\check_fgp_source.py`
  - passed
- `git diff --check` on touched files
  - clean

## Next

Real FGP prose ablation runner can be built next. It must wire:

- `load_forbidden_phrase_corpus(...)`
- `check_prompt_boundary(..., require_forbidden_fgp_phrases=True)`
- `check_generated_draft_for_forbidden_overlap(..., require_forbidden_fgp_phrases=True)`

Real prose ablation should remain blocked until that runner wiring is reviewed.

