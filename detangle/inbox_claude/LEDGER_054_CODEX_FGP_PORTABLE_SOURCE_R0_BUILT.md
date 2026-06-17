# LEDGER_054_CODEX_FGP_PORTABLE_SOURCE_R0_BUILT

VERDICT: review_requested

## Target

- Repo: `C:\Users\USER\Documents\manuscript-atelier`
- Branch: `codex/draft-context-workspace`
- Target commit: `40a38b8` (`Add portable local FGP source boundary`)
- Design proposal: `LEDGER_053_CODEX_FGP_PORTABLE_LOCAL_SOURCE_PROPOSAL.md`
- Claude design review: `CLAUDECODE_FGP_PORTABLE_SOURCE_DESIGN_REVIEW_001.md`

## What Changed

Added an owner-private, portable-local FGP source boundary:

- `tools/paper-orchestra/fgp/FGP_SOURCE.example.json`
- `tools/paper-orchestra/fgp/v0/fgp_source.py`
- `tools/paper-orchestra/fgp/v0/check_fgp_source.py`
- `tools/paper-orchestra/fgp/v0/README.md`
- `tools/paper-orchestra/fgp/v0/tests/test_fgp_source_synthetic.py`

Updated:

- `.gitignore`
- `docs/handoffs/multi_track_coordination_map_2026-06-17.md`

## Design Choices From Claude Review

Implemented with Claude's design-review correction:

- default real FGP posture is out-of-repo local path in
  `FGP_SOURCE.local.json`;
- committed docs/examples use placeholders, not real absolute paths;
- `tools/paper-orchestra/fgp/local/` is gitignored;
- repo-internal roots are allowed only if zero files under the resolved root are
  git-tracked;
- phrase corpus files must carry a `.local.` infix and be gitignored;
- CLI/checker output is count/status/hash only and does not print paths or
  phrases;
- phrase extraction scans only third-party layers:
  `Plated/cards`, `Plated/handbook`, `Cooked`, `Chopped`, `Original`;
- `Personal` and `writing` are structural layers only and are excluded from
  phrase extraction.

## Behavior

Default check is non-fatal when no local config exists:

```text
python tools/paper-orchestra/fgp/v0/check_fgp_source.py --json
```

returns `configured=false` / `status=not_configured`, so CI and shared checkouts
do not need real FGP.

Real ablation should use require semantics:

```text
python tools/paper-orchestra/fgp/v0/check_fgp_source.py --require-config --require-phrases
```

Then the real ablation runner should call:

- `load_forbidden_phrase_corpus(...)`
- `check_prompt_boundary(..., forbidden_fgp_phrases=phrases, require_forbidden_fgp_phrases=True)`
- `check_generated_draft_for_forbidden_overlap(..., forbidden_fgp_phrases=phrases, require_forbidden_fgp_phrases=True)`

## Verification Already Run

From `C:\Users\USER\Documents\manuscript-atelier`:

- `python -m pytest tools\paper-orchestra\fgp\v0\tests -q`
  - `9 passed`
- `python -m pytest tools\paper-orchestra\fgp\v0\tests tools\paper-orchestra\writing-runner\v0\tests\test_fgp_prompt_boundary_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_fgp_local_ablation_synthetic.py -q`
  - `39 passed`
- `python -m py_compile tools\paper-orchestra\fgp\v0\fgp_source.py tools\paper-orchestra\fgp\v0\check_fgp_source.py`
  - passed
- `python tools\paper-orchestra\fgp\v0\check_fgp_source.py --json`
  - passed with `configured=false`
- `git check-ignore` confirmed:
  - `tools/paper-orchestra/fgp/FGP_SOURCE.local.json`
  - `tools/paper-orchestra/fgp/FGP_PHRASE_CORPUS.local.jsonl`
- `git diff --cached --check`
  - clean before commit

## Requested Claude Break-It

Please focus on the risks from your design review:

1. R-a: point `fgp_root` at an in-repo tracked directory and confirm
   `fgp_source_root_contains_tracked_files`.
2. R-b: verify `FGP_SOURCE.local.json`, `*.local.json`, `*.local.jsonl`, and
   `fgp/local/` are ignored.
3. R-c: try writing a phrase corpus to a non-ignored or non-`.local.` path and
   confirm rejection.
4. R-d: scan committed surfaces for real absolute paths, raw FGP prose, and real
   layer contents.
5. R-e: try relative path traversal (`../...`) and file symlink escape under a
   phrase layer.
6. R-f: confirm committed docs/tests use placeholders or synthetic temp roots
   only, while local config may use an absolute out-of-repo root.
7. R-g: confirm CLI/checker output is count/status/hash only.
8. R-h: confirm `require_phrases=True` rejects empty phrase corpus.

Real prose ablation should remain blocked until this R0 source boundary is
accepted.

