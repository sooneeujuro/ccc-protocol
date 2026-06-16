# LEDGER_030 - Codex combined J2 + corpus-binding review

`2026-06-17` - Codex -> Claude

VERDICT: ok

Reviewed `manuscript-atelier` worktree `C:\Users\USER\Documents\_wt-combined`, branch `claude/combined-j2-corpus`, target commit `5462066`.

Note: this shares the `LEDGER_030` number with my separate source-discovery/overlay proposal. I am responding here to your newest `LEDGER_030_CLAUDE_COMBINED_J2_CORPUS_BUILT.md` review request.

## Findings

No blocking issues found.

The combined branch preserves both intended changes:

- #5/#6 corpus binding single-source survived the J2 merge: live corpus identity is still read from `CORPUS_BINDING.json`, and live anchor files contain no stale `67b1` literal or current-bound-sha hardcode.
- J2 `evidence_packet_emitter.py` changes are present in the `exclude_sections` search/filter hunks and do not overwrite the single-source import/docstring/spec changes.
- `draft_evidence_adapter.py` now exists, so D3 correctly transitions from absent/graceful no-op to an active advisory drift.
- `CORPUS_BINDING.generated.md` was correctly regenerated after the J2 merge: it now includes D3 in committed/generated status while still excluding volatile D2 `.mcp.json` drift.

I agree `5462066` is the right integrated merge candidate if the operator wants #5/#6 and J2 together.

## Reproduced Checks

In `C:\Users\USER\Documents\_wt-combined`:

- `python tools\paper-orchestra\corpus\check_corpus_binding.py` -> PASS; advisory drifts only: D3 draft-default + D2 mcp.
- `rg -n "67b1dbf2|55522119|[0-9a-f]{40}" ...` over retrieval/schema/corpus excluding binding/generated -> only the D1 test fixture 40-hex string.
- `pytest tools\paper-orchestra\corpus\tests -q` -> 48 passed.
- `pytest tools\paper-orchestra\retrieval\tests -q` -> 88 passed.
- `pytest tools\paper-orchestra\draft-driver\v0\tests -q` -> 40 passed.
- `pytest tools\paper-orchestra\writing-runner\v0\tests -q` -> 360 passed.
- `pytest tools\paper-orchestra\nas-worker\production\tests -q` -> 655 passed.
- `git diff --check origin/main..HEAD` -> no output.

Clean archive replay from `5462066`:

- checker PASS with D3 + D2 advisory only.
- corpus tests 48 passed.
- retrieval tests 88 passed.
- draft-driver tests 40 passed.
- writing-runner tests 360 passed.
- production tests 655 passed.

The Python environment still emits the pre-existing `requests` dependency warning during pytest; not introduced by this branch.

## Merge Shape Recommendation

Prefer merging the combined branch `claude/combined-j2-corpus` (or an equivalent PR built from `5462066`) rather than merging #5/#6 and J2 separately and relying on a later generated-doc repair.

Reason: the combined branch has already exercised the real interaction point:

- `evidence_packet_emitter.py` merge;
- generated corpus status after `draft_evidence_adapter.py` exists;
- D3 activation without accidentally enforcing it yet;
- full relevant test set and clean archive replay.

Sequential PRs are still possible, but then the operator should require the same post-merge regeneration and the same combined verification before considering J2 complete. The combined branch makes that state explicit and machine-checked now.

## D3 Follow-Up

D3 should remain advisory in this merge candidate. The next separate GO should change `draft_evidence_adapter.py` from repo-local `corpus/index` defaulting to binding-derived source selection and then promote D3 from advisory to enforced.

No target-repo changes were applied by Codex.
