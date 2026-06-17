# LEDGER_135 — Codex Quartet Take10 / placeholder-ID split

Timestamp: 2026-06-17 23:4x KST
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Branch: `codex/draft-context-workspace`
Target commit: `ae870f9` — `writing: separate quartet placeholders from binding ids`

VERDICT: review_requested

## Why

Claude's Take3 review and my Take7/Take9 runs converged on the same problem:

- paragraph placeholder tokens like `{{EVIDENCE:CIR_DOMAIN_MODEL}}`
- JSON binding IDs like `evidence:cir_domain_model`

were visually and structurally too close in the Gemma prompt. The 12B model kept converting one family into the other.

## Changes

### Prompt structure

`local_gemma_prompt_pack.py`

- Stopped embedding the full baseline prompt under `Task Envelope`, because it repeated the operator instruction and binding counts.
- `Task Envelope` now contains only task metadata and constraints.
- Added an explicit `Paragraph Placeholder Tokens` section listing only legal `{{...}}` tokens.
- Renamed the ID section to `JSON Array Binding IDs`.
- Updated the output contract:
  - `paragraph_md` may use only listed `{{...}}` placeholders;
  - ID arrays may use only listed JSON binding IDs;
  - binding IDs must not appear in `paragraph_md`;
  - no LaTeX/math delimiters/backslashes.

### Profile tuning

`quartet_profile.py`

- Bold: frame capability as `can_test` / `provides_a_test`.
- Measured: prefer `suggests`, `is consistent with`, or `provides a test`; avoid `demonstrates/reveals/establishes` for framework-level claims unless the direct measurement is the grammatical subject.
- Terse: leave ID arrays empty rather than shortening/compressing binding IDs.

### Gate hardening

`gemma_candidate_gate.py`

- Rejects backslash/LaTeX in parsed `paragraph_md`.

## Verification

```text
python -m pytest tools\paper-orchestra\writing-runner\v0\tests tools\paper-orchestra\local-llm\v0\tests -q
435 passed
```

## Empirical run sequence after Take6

All artifacts are local-only under `C:\Users\USER\Documents\_codex_runs`.

### Take7

Run:
`C:\Users\USER\Documents\_codex_runs\quartet_take7_20260617T232619\gemma-quartet-synthetic-001`

Result:
- gate failed `gemma_candidate_evidence_id_not_allowed`
- Terse compressed binding IDs by dropping namespace prefixes
- prose quality improved, but binding arrays were not reliable

### Take8

Run:
`C:\Users\USER\Documents\_codex_runs\quartet_take8_20260617T232913\gemma-quartet-synthetic-001`

Result:
- gate failed `gemma_candidate_response_json_invalid`
- cause: raw LaTeX/backslashes in JSON string

### Take9

Run:
`C:\Users\USER\Documents\_codex_runs\quartet_take9_20260617T233405\gemma-quartet-synthetic-001`

Result:
- gate failed `gemma_candidate_evidence_id_not_allowed`
- Bold converted a binding ID into a placeholder-like token and stripped array prefixes
- confirmed that the prompt needed structural separation, not just more warning text

### Take10

Run:
`C:\Users\USER\Documents\_codex_runs\quartet_take10_20260617T233727\gemma-quartet-synthetic-001`

Result:
- candidate gate passed
- scorecard passed
- conductor/report written:
  - `Codex_conductor_take10.md`
  - `Codex_take10_report.md`

Scorecard:
- candidate_count = 3
- max_meta_phrase_count = 0
- max_overstrong_verb_count = 0
- paragraph word-count range = 62 to 69
- min_placeholder_count = 2

Interpretation:
- Take10 is the best convergence point so far.
- The placeholder-vs-binding split appears to have fixed the main Gemma confusion class.
- Candidate prose is still not automatically publication-ready, but it is finally structurally clean enough for a conductor/reviewer loop.

## Review request

Please review:

1. `ae870f9`
2. Take10 local artifacts
3. Whether the prompt structure split is the right long-term direction
4. Whether Take10 is strong enough to move from single discussion paragraph to a second section/function test

No candidate prose is copied into this ledger note.

