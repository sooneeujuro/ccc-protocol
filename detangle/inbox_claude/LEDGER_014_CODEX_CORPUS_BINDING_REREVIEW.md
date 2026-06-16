# LEDGER_014_CODEX_CORPUS_BINDING_REREVIEW

VERDICT: ok

Scope reviewed:
- manuscript-atelier branch `claude/corpus-binding-ledger`
- reviewed HEAD `c7a7bcd` (`fix(corpus-binding): Phase 1 - deterministic generated.md + implement D3 (Codex LEDGER_013)`)
- re-reviewed the two Codex `LEDGER_013` findings and direct regression surface
- no manuscript-atelier edits, corpus body/index/sidecar reads or writes, live infra, DB writes, deployments, or pushes performed by Codex

What passed:
- Current checkout: `python tools/paper-orchestra/corpus/check_corpus_binding.py` passes with 4 advisory known drifts: D1 x3 plus D3 x1.
- Current checkout: `python -m pytest tools/paper-orchestra/corpus/tests/ -q` passes: 47 passed. The only observed noise was the existing RequestsDependencyWarning.
- Current checkout: `python tools/paper-orchestra/corpus/check_corpus_binding.py --verify-source` passes and reports local corpus sha `55522119` OK.
- Clean archive of `c7a7bcd`: `python tools/paper-orchestra/corpus/check_corpus_binding.py` exits 0.
- Clean archive of `c7a7bcd`: `python -m pytest tools/paper-orchestra/corpus/tests/ -q` exits 0 with 47 passed.
- Clean archive of `c7a7bcd`: regenerating `CORPUS_BINDING.generated.md` produces no diff.
- `python tools/paper-orchestra/corpus/check_corpus_binding.py --quiet` exits 0.
- `git diff --check e58e81d..c7a7bcd` is clean.
- No network/DB imports were found in `check_corpus_binding.py` or `test_corpus_binding.py`.

Findings from LEDGER_013 status:
- Clean-checkout generated reproducibility is fixed. `render_generated()` no longer snapshots volatile `.mcp.json` / source-config drift; D2 remains runtime-only advisory output.
- D3 is now implemented and tested. `scan_draft_default_drift()` reports `draft_evidence_adapter.py`'s repo-local default index surface, and generated status includes D3.

Notes:
- A clean archive without the local `.mcp.json` hotfix still prints D2 as an advisory runtime drift (`could not read geochem-corpus args from .mcp.json`), but it no longer fails E6 or changes generated freshness. That is the intended Phase 1 behavior.
- D1/D3 remain Phase 2 targets and are correctly advisory in Phase 1.

Codex considers corpus-binding Phase 1 closed.

Recommended next operator gate:
- Phase 2 should be a separate GO because it changes behavior: replace/bind the 67b1 corpus identity anchors, wire draft/retrieval entrypoints to refuse mismatched evidence emission, and handle `.mcp.json` / NAS/web source verification under explicit operator approval.

