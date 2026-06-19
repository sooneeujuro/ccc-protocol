# LEDGER_305_CODEX_PROMPT_TOURNAMENT_MANIFEST_SELF_CHECK

VERDICT: ok

Scope:
- Continued Gemma tournament harness hardening after LEDGER_304.
- No model calls.
- No manuscript/corpus data push.
- No raw model prose, protected source text, or resolved numeric values relayed here.

Change:
- Added generator-side consistency checks before prompt tournament manifests are written.
- The prepare step now builds blind, execution, and reveal manifests in memory, checks them together, then writes them.
- The self-check verifies:
  - shared tournament id across blind/execution/reveal
  - expected schema values
  - expected local/provenance bits
  - blind scoring is not opened before reveal
  - blind/execution/reveal entry id sets are identical
  - blind expected call count and variant/repetition counts match generated entries
  - persona/repetition consistency across all three surfaces
  - prompt/task/pack hash consistency between blind and execution entries
- Added red tests that monkeypatch generated manifests to drift counts, entry metadata, or execution safety scope; prepare now fails before writing inconsistent manifests.

Why:
- LEDGER_303 and LEDGER_304 hardened the runner's consumer-side ingestion.
- This patch adds the matching producer-side invariant: the generator should not write a half-consistent tournament package if future edits drift one manifest surface.

Verification:
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_prompt_tournament_synthetic.py -q`
  - 16 passed
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - 241 passed
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q`
  - 468 passed
- `git diff --check -- tools\paper-orchestra\local-llm\v0 tools\paper-orchestra\writing-runner\v0`
  - no whitespace errors
  - only existing CRLF normalization warnings

Notes:
- `manuscript-atelier` remains uncommitted by design.
- ccc-protocol unrelated untracked files, including invoice and detangle JSON files, were not touched.
