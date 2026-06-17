# LEDGER_053_CODEX_FGP_PORTABLE_LOCAL_SOURCE_PROPOSAL

VERDICT: design_review_requested

## Context

Operator suggested moving FGP into the same operational shape as the local
corpus: carry the private asset tree alongside the repo, but keep raw assets and
machine paths out of git.

This should happen before the first real FGP prose ablation, because that
ablation needs a local-only FGP phrase corpus for:

- prompt boundary guard:
  `check_prompt_boundary(..., forbidden_fgp_phrases=..., require_forbidden_fgp_phrases=True)`
- generated draft guard:
  `check_generated_draft_for_forbidden_overlap(..., require_forbidden_fgp_phrases=True)`

## Proposed Shape

Add a small owner-private FGP source layer, separate from
`writing-runner/v0`:

```text
tools/paper-orchestra/fgp/
  v0/
    fgp_source.py
    check_fgp_source.py
    README.md
    tests/test_fgp_source_synthetic.py
  FGP_SOURCE.local.json        # gitignored
  local/ForGoodPaper/          # gitignored raw asset copy, symlink, or junction
```

Example local config:

```json
{
  "schema": "fgp_source_local_v1",
  "mode": "owner_private_local",
  "fgp_root": "tools/paper-orchestra/fgp/local/ForGoodPaper",
  "phrase_corpus_enabled": true
}
```

`fgp_root` should support repo-relative paths. Absolute paths may be allowed in
the local-only file, but committed docs/tests should use repo-relative synthetic
paths.

## R0 Scope

R0 should be additive and local-only:

- resolver reads `FGP_SOURCE.local.json`;
- resolves repo-relative `fgp_root` safely;
- confirms root exists when checking a real local setup;
- confirms expected FGP layer directories if present (`Original`, `Chopped`,
  `Cooked`, `Plated`, etc.) without committing their contents;
- can build a local-only forbidden phrase corpus from text-like files under the
  private root for prompt/draft overlap guards;
- checker emits only counts/status/enums;
- tests use synthetic temp FGP trees only;
- no LLM calls;
- no network;
- no Zotero/corpus mutation;
- no raw FGP text committed or printed;
- no real local path committed.

## Gitignore Proposal

Add:

```gitignore
# === ForGoodPaper portable local source ===
tools/paper-orchestra/fgp/FGP_SOURCE.local.json
tools/paper-orchestra/fgp/*.local.json
tools/paper-orchestra/fgp/local/
```

Potentially leave existing root-level legacy ignores in place:

```gitignore
ForGoodPaper/Original/
ForGoodPaper/Chopped/
ForGoodPaper/Cooked/
ForGoodPaper/Plated/handbook/
ForGoodPaper/Personal/
ForGoodPaper/writing/
```

## Preferred Integration Path

1. Build FGP source R0: resolver/checker/tests/README/gitignore.
2. Update FGP prompt-boundary docs to say real ablation obtains
   `forbidden_fgp_phrases` from this local source.
3. Then build the real prose ablation runner using:
   - `fgp_source.load_forbidden_phrase_corpus(...)`;
   - `check_prompt_boundary(... require_forbidden_fgp_phrases=True)`;
   - `check_generated_draft_for_forbidden_overlap(... require_forbidden_fgp_phrases=True)`.

## Questions For Claude

1. Do you agree with `tools/paper-orchestra/fgp/` as the shared FGP source
   layer, rather than placing source resolution under `writing-runner/v0/`?
2. Should absolute paths be allowed inside `FGP_SOURCE.local.json` because it is
   gitignored, or should R0 force repo-relative roots to improve portability?
3. What directory names should R0 recognize as expected FGP layers? Suggested:
   `Original`, `Chopped`, `Cooked`, `Plated`, `Personal`, `writing`.
4. For phrase corpus extraction, should R0 initially use only text-like files
   (`.md`, `.txt`, `.yaml`, `.yml`) with count/hash-only reporting?
5. Any additional red-path tests before Codex builds R0?

No target-repo implementation has been done for this proposal yet.

