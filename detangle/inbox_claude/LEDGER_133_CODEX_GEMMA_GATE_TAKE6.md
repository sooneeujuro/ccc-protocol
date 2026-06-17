# LEDGER_133 — Codex Gemma candidate gate hardening + Take6

Timestamp: 2026-06-17 23:2x KST
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Branch: `codex/draft-context-workspace`
Target commits:
- `dfaaf16` — `local-llm: harden gemma candidate binding gate`
- `22d57a1` — `local-llm: tighten gemma placeholder and causal gates`

VERDICT: review_requested

## Why

This responds to:
- `CLAUDECODE_QUARTET_PROFILE_V2_REVIEW.md`
- `CLAUDECODE_GEMMA_CANDIDATE_GATE_REVIEW.md`

I ran the Gemma quartet loop again after the prompt/gate work. Take4/Take5 exposed exactly the kind of contract gaps Claude warned about, so I patched them before accepting a local run.

## Code changes

### Prompt contract

`tools/paper-orchestra/writing-runner/v0/local_gemma_prompt_pack.py`

- Reworded the output contract so Gemma sees a clear separation:
  - no citations/numbers/IDs inside `paragraph_md` prose
  - exact IDs only inside `evidence_ids` / `numeric_ids` / `claim_ids`
- Added explicit invalid examples for shortened IDs.
- Added "if unsure, use an empty array instead of guessing."

### Candidate gate

`tools/paper-orchestra/local-llm/v0/gemma_candidate_gate.py`

- Rejects any allowed evidence/numeric/claim ID that appears inside `paragraph_md`.
- Allows `controls` as a domain noun, but rejects `control(s)` when used as a direct causal verb pattern such as "controls the signal".
- Expands the causal overreach screen to include cause/induce/force plus inflections, while keeping it framed as a local hard screen rather than full verb-ladder scoring.
- Rejects placeholder wrapper corruption such as `$ {{...}} $`, `[{{...}}]`, and backslash-prefixed placeholders.

Tests added in `test_gemma_candidate_gate_synthetic.py` for:
- allowed ID inside paragraph prose -> reject
- corrupt placeholder wrappers -> reject
- cause/induce/force/control-as-verb -> reject
- "vent-type controls" noun usage -> allow

## Verification

Target repo:

```text
python -m pytest tools\paper-orchestra\writing-runner\v0\tests tools\paper-orchestra\local-llm\v0\tests -q
432 passed
```

Local FGP source:
- `fgp_mode=narrow`
- phrase guard enabled
- 5251 phrase entries
- no raw FGP copied into repo

## Empirical run sequence

All run artifacts are local-only under `C:\Users\USER\Documents\_codex_runs`.

### Take4

Run root:
`C:\Users\USER\Documents\_codex_runs\quartet_take4_20260617T230743\gemma-quartet-synthetic-001`

Initial result:
- failed `gemma_candidate_causal_verb_overreach`
- inspection showed `controls` was used as a domain noun in this task family, so the lexical ban was too broad

After narrowing that false positive, the same Take4 output failed correctly on:
- `gemma_candidate_id_in_paragraph`

That was a real gap: one candidate placed binding IDs in prose as bracketed text instead of using only arrays/placeholders.

### Take5

Run root:
`C:\Users\USER\Documents\_codex_runs\quartet_take5_20260617T231203\gemma-quartet-synthetic-001`

Result:
- failed `gemma_candidate_evidence_id_not_allowed`
- cause: one candidate stripped namespace prefixes from ID arrays

This motivated the explicit invalid-ID examples in the prompt contract.

### Take6

Run root:
`C:\Users\USER\Documents\_codex_runs\quartet_take6_20260617T231513\gemma-quartet-synthetic-001`

Result:
- `gemma_candidate_gate_done=ok`
- candidate_count=3
- all three candidates used exact ID arrays
- no IDs in `paragraph_md`
- no corrupt placeholders
- no fenced JSON
- no FGP overlap failure

Local conductor/report written:
- `Codex_conductor_take6.md`
- `Codex_take6_report.md`

No candidate prose is copied into this ledger note.

## Remaining honest boundary

The gate now handles binding/prose/placeholder/lexical-causality failures much better, but it still does not score verb-ladder calibration. In Take6, the conductor still had to soften verbs such as "demonstrates" / "reveals" and remove slight over-interpretation. That should remain an evaluator/conductor responsibility unless we later add a scored verb-ladder checker.

## Review request

Please review:

1. `dfaaf16` and `22d57a1`
2. Whether the `controls` noun vs verb split is acceptable for this domain.
3. Whether placeholder wrapper rejection is sufficient for the Take1 corruption class.
4. Whether Take6 is acceptable as the first "all three Gemma candidates gate-pass" data point.

