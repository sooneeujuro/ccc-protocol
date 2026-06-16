# LEDGER_013_CODEX_CORPUS_BINDING_PHASE1_REVIEW

VERDICT: issues_found

Scope reviewed:
- manuscript-atelier branch `claude/corpus-binding-ledger`
- reviewed HEAD `e58e81d` (`feat(corpus-binding): J-corpus-binding Phase 1 - corpus-version binding ledger (additive)`)
- no manuscript-atelier edits, corpus body/index/sidecar reads or writes, live infra, DB writes, deployments, or pushes performed by Codex

What passed in the current dirty local checkout:
- `python tools/paper-orchestra/corpus/check_corpus_binding.py` passes with 3 D1 known drifts.
- `python -m pytest tools/paper-orchestra/corpus/tests/ -q` passes: 45 passed. The only observed noise was the existing RequestsDependencyWarning.
- `python tools/paper-orchestra/corpus/check_corpus_binding.py --verify-source` passes and reports local corpus sha `55522119` OK.
- A synthetic local-source mismatch test reports `DRAFT/CORPUS MISMATCH` as expected.
- I saw no network/DB imports in the checker/test path.

Findings:

1. The commit is not green from a clean checkout; it only passes with the local dirty `.mcp.json` hotfix present.

Evidence:
- Current worktree has uncommitted `.mcp.json` changes that add/repoint `geochem-corpus` to `G:\corpus_md_export_20260612`.
- `git show e58e81d --name-only` confirms `.mcp.json` is not part of the Phase 1 commit.
- In a clean archive of `e58e81d`, running `python tools/paper-orchestra/corpus/check_corpus_binding.py` fails:
  - `FAIL  E6 generated: CORPUS_BINDING.generated.md is stale (run --write)`
- In the same clean archive, `python -m pytest tools/paper-orchestra/corpus/tests/test_corpus_binding.py -q` fails 2 tests:
  - `test_enforced_checks_pass_on_repo_as_is`
  - `test_generated_status_is_fresh`
- The generated diff is exactly a missing D2 row:
  - `D2 mcp: could not read geochem-corpus args from .mcp.json`

Root cause:
- `render_generated()` includes `scan_mcp_drift()`.
- `scan_mcp_drift()` depends on machine/local `.mcp.json` state and may also read an external local `CORPUS_VERSION.json`.
- Therefore `CORPUS_BINDING.generated.md` is not deterministic from the committed tree. It was generated against the dirty company-PC `.mcp.json`, not the clean commit.

Recommended fix:
- Keep generated freshness deterministic over committed, repo-local static surfaces only.
- Either remove D2 from `render_generated()` / E6 generated freshness and print D2 only as runtime advisory output, or commit the `.mcp.json` hotfix and still avoid external-path-dependent D2 in generated status.
- After fixing, verify from a clean checkout/archive of `e58e81d` successor, not only the current dirty worktree.

2. D3 is documented and claimed, but not implemented.

Evidence:
- `check_corpus_binding.py` documents `D3 draft-default  draft_evidence_adapter default repo-local index surface`.
- `run_checks()` only adds `scan_anchor_drift()` and `scan_mcp_drift()`.
- There is no D3 scanner or D3 test.
- The drift surface exists:
  - `tools/paper-orchestra/retrieval/draft_evidence_adapter.py:50` sets `_INDEX_DIR = REPO_ROOT / "tools" / "paper-orchestra" / "corpus" / "index"`
  - lines 51-54 set default BM25/units/papers/manifest paths under that repo-local older index surface.

Recommended fix:
- Add a `scan_draft_default_drift()` report path and a synthetic test that proves this surface is reported.
- It can remain advisory/known_drift in Phase 1, but it should not be merely documented.

Notes:
- The Phase 1 shape is otherwise aligned with the converged design: correct location, committed binding metadata only, gitignore protection, local source example, cp949-safe diagnostics, and no runtime behavior change.
- I would not close Phase 1 until the checker is self-contained on a clean checkout and the promised D3 drift surface is actually reported.

