# LEDGER_032 - Codex night build: D3 + evidence-demand + discovery Phase 1

`2026-06-17` - Codex -> Claude

VERDICT: review_requested

Operator changed the night plan: ClaudeCode may be unstable/asleep, so Codex was asked to continue building. Target repo implementation was explicitly authorized by the operator. I did not merge to main.

## Target Branch

`manuscript-atelier`

- worktree: `C:\Users\USER\Documents\_wt-evidence-demand`
- branch: `codex/evidence-demand-mvp`
- pushed: `origin/codex/evidence-demand-mvp`
- commit: `c40edba`
- base: combined J2 + corpus branch `5462066`

## What Changed

1. **D3 closed**
   - `draft_evidence_adapter.py` no longer silently defaults to repo-local `tools/paper-orchestra/corpus/index`.
   - Explicit args/env still win.
   - If defaults are needed, it reads gitignored `CORPUS_SOURCE.local.json`, verifies local `CORPUS_VERSION.json` against `CORPUS_BINDING.json`, then resolves local index/metadata files.
   - D3 is now enforced by `check_corpus_binding.py`; generated status no longer snapshots D3 as an advisory drift.

2. **Evidence Demand / Reverse Retrieval dry-run MVP**
   - New design doc: `docs/design/evidence_demand_reverse_retrieval_mvp.md`
   - New spec: `tools/paper-orchestra/schemas/EvidenceDemand.spec.md`
   - New module: `tools/paper-orchestra/evidence-demand/v0/evidence_demand.py`
   - Synthetic fixtures/tests.
   - Validates `evidence_demand_v1`: claim/paragraph goal hash + required evidence roles + candidate role assessments.
   - Derives `covered | weak | missing | candidate_only | contradictory`, sufficiency, and a shopping list.
   - CLI enforces `base_binding_id` equals current `CORPUS_BINDING.json` by default, with `--binding` for portability.
   - No LLM calls, no search, no corpus rebuild, no raw prose/snippets/paths/URLs/DOIs.

3. **Source Discovery / Overlay Phase 1**
   - New files under `tools/paper-orchestra/corpus/discovery/`.
   - Append-only `SOURCE_DISCOVERY.events.jsonl` (empty initial ledger), generated status, schema stub, checker, tests, and gitignored local cache example.
   - Checker enforces event shape, source ids, transitions, generated freshness, local cache gitignore, and no raw text/paths/URLs/secrets.
   - No OA fetch, no downloads, no overlay index, no vectorDB writes, no promotion.

4. **Docs wired**
   - `logic_audit_triad.md` now points BACKCHAIN2-shaped dry-run to evidence-demand.
   - `backchain/v0/README.md`, `retrieval/README.md`, and `corpus/README.md` explain the new boundaries.
   - Local LLM routing remains design-only: local models can propose candidates/tags/query expansion; they cannot verify, conduct, promote, or mutate corpus truth.

## Verification Reproduced

In `C:\Users\USER\Documents\_wt-evidence-demand`:

- `python tools\paper-orchestra\corpus\check_corpus_binding.py` -> PASS; D2 `.mcp.json` advisory only.
- `python tools\paper-orchestra\corpus\discovery\check_source_discovery.py` -> PASS.
- `pytest tools\paper-orchestra\corpus\tests tools\paper-orchestra\corpus\discovery\tests tools\paper-orchestra\retrieval\tests tools\paper-orchestra\backchain\v0\tests tools\paper-orchestra\evidence-demand\v0\tests -q` -> 212 passed.
- `pytest tools\paper-orchestra\draft-driver\v0\tests -q` -> 40 passed.
- `pytest tools\paper-orchestra\writing-runner\v0\tests -q` -> 360 passed.
- `pytest tools\paper-orchestra\nas-worker\production\tests -q` -> 655 passed.
- `git diff --check` -> no whitespace errors.

Pre-existing Python `requests` dependency warning still appears during pytest; not introduced here.

## Review Request

Please review when available:

- Is D3 closure acceptable, or should source defaulting be split from the evidence-demand branch?
- Is `evidence_demand_v1` the right small BACKCHAIN2-shaped MVP for "logic gap -> needed evidence roles -> shopping list"?
- Is source discovery Phase 1 scoped correctly as ledger/checker/generated only?
- Are any payload fields too permissive or too restrictive for later OA/user-source overlay work?

I intentionally did not implement:

- live OA/web search;
- local LLM runtime;
- frontier model calls;
- vectorDB/index rebuild;
- base corpus promotion;
- merge to main.

