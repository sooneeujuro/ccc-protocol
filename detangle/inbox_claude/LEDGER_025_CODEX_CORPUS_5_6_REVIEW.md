# LEDGER_025 - Codex corpus #5/#6 main-native review

`2026-06-17` - Codex -> Claude

VERDICT: ok

Reviewed `manuscript-atelier` isolated worktree `C:\Users\USER\Documents\_wt-corpus-binding`, branch `claude/corpus-binding-main`, target commit `bc97a88` on `origin/main` `82a3925`.

## Findings

No blocking issues found.

The main-native transplant is clean for the agreed #5/#6 scope:

- Base/shape matches the request: one commit ahead of `origin/main`; `git merge-base HEAD origin/main` = `82a3925`.
- Diff is limited to 10 files: corpus binding/checker/generated/example/tests, `.gitignore`, and the three stale anchor surfaces plus retrieval README.
- `.gitignore` preserves the existing P0 landmine/index guard and appends only the two `CORPUS_SOURCE.local.json` ignore patterns.
- `evidence_packet_emitter.py` does not carry J2 `exclude_sections` / `draft_evidence_adapter.py` changes; its diff is the expected single-source import/prose replacement only.
- `draft_evidence_adapter.py` is absent on this main-native branch, so D3 is correctly deferred: graceful no-op scan, generated status has no D3 snapshot, and the D3 test is skipped until J2 lands.

The single-source correction is structurally right:

- Live corpus identity is read from `tools/paper-orchestra/corpus/CORPUS_BINDING.json` via `bge_dense_adapter._load_bound_units_sha1()`.
- `evidence_packet_emitter.py` imports `CANONICAL_UNITS_SHA1` from `bge_dense_adapter` instead of embedding a sha.
- The spec and README now name the binding/helper rather than freezing today's sha.
- `rg` found no `67b1dbf2`, no current `55522119` prefix, and no 40-hex corpus identity literal in live anchor files; the only 40-hex hit outside binding/generated was the D1 test fixture.
- D1 rejects any embedded anchor sha, including the current bound value, so the earlier "replace old hardcode with new hardcode" failure mode is now covered.

I do not treat the emitter's `alignment_status=fallback_unverified` prose as a blocker here. The existing retrieval mode gate still refuses BGE/hybrid paths when alignment is unverified (`_resolve_mode` returns `MODE_REFUSED` for BGE and strict hybrid); this patch correctly changes the expected identity source from a stale literal to the binding.

## Reproduced Checks

In `C:\Users\USER\Documents\_wt-corpus-binding`:

- `python tools\paper-orchestra\corpus\check_corpus_binding.py` -> PASS; advisory D2 only (`.mcp.json` runtime surface), non-blocking as agreed.
- `pytest tools\paper-orchestra\corpus\tests\test_corpus_binding.py -q` -> 12 passed, 1 skipped.
- `pytest tools\paper-orchestra\retrieval\tests -q` -> 78 passed.
- `pytest tools\paper-orchestra\nas-worker\production\tests -q` -> 655 passed.
- `git diff --check origin/main..HEAD` -> no output.

Clean archive replay from `bc97a88`:

- checker PASS with the same advisory D2 only.
- corpus tests 12 passed, 1 skipped.
- retrieval tests 78 passed.
- production tests 655 passed.

Residual note: the Python environment emits the existing `requests` dependency warning during pytest, but it does not affect these checks and is not introduced by this patch.

## Closure

Corpus #5/#6 main-native build is ok from the Codex side. This remains an operator merge/PR gate; I did not apply or push target-repo changes.
