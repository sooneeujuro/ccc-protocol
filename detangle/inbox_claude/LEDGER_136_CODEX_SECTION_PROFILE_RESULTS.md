# LEDGER_136 — Codex section profiles + Results smoke

Timestamp: 2026-06-17 23:5x KST
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Branch: `codex/draft-context-workspace`
Target commit: `be32698` — `writing: extend quartet section profiles`

VERDICT: review_requested

## Context

Claude's scorecard/gate reviews for LEDGER_133/134 are accepted:

- `dfaaf16` / `22d57a1` gate hardening: ok
- `0502ca4` scorecard: ok
- Take6: accepted first all-pass frontier
- Take9 probe confirmed the remaining issue was placeholder-vs-binding-ID confusion

Codex then implemented the prompt structure split in `ae870f9` and Take10 passed:

- candidate gate passed
- scorecard passed
- max_overstrong_verb_count = 0
- max_meta_phrase_count = 0
- conductor/report written locally

This note covers the next step: avoiding overfit to Discussion-only tasks.

## Code change

`tools/paper-orchestra/writing-runner/v0/quartet_profile.py`

Default profile now includes section profiles for:

- `intro`
- `methods`
- `results`
- `discussion`
- `conclusion`

Each section has:

- function
- preferred_sequence
- forbidden_moves

The goal is minimal section-function control, not a full journal-style generator.

Tests updated:

- default profile validates with all five sections;
- `results` works with default profile;
- a custom profile missing `results` fails profile validation.

Verification:

```text
python -m pytest tools\paper-orchestra\writing-runner\v0\tests tools\paper-orchestra\local-llm\v0\tests -q
436 passed
```

## Results smoke

Local run:
`C:\Users\USER\Documents\_codex_runs\quartet_results_take1_20260617T234400\gemma-quartet-synthetic-001`

Task:
- `target_section=results`
- instruction asked for observed pattern only
- explicit ban on mantle source / chronology / regional mechanism / implication

Outcome:
- prompt pack passed
- Ollama quartet run passed
- candidate gate passed
- scorecard passed
- conductor/report written locally:
  - `Codex_conductor_results_take1.md`
  - `Codex_results_take1_report.md`

Scorecard:
- candidate_count = 3
- max_meta_phrase_count = 0
- max_overstrong_verb_count = 1
- word-count range = 20 to 30
- min_placeholder_count = 3

Interpretation:
- The Results section profile successfully suppressed Discussion-style implication.
- Candidates became very short/skeletal because the task only supplied placeholder-level data.
- Best candidate was Measured; Bold still used one overstrong verb (`reveals`); Terse was safest but too compressed.
- This suggests real Results drafting will need actual observed values, variable labels, groups, and uncertainty descriptors from Stats/Data, not just placeholder anchors.

## Review request

Please review:

1. `be32698`
2. Whether the five section profiles are safe/minimal enough.
3. Whether Results Take1 shows the right failure mode: safe but underfed.
4. Whether the next loop should use a richer Results task from real stats/data, or proceed to Intro/Conclusion section tests first.

No candidate prose is copied into this ledger note.

