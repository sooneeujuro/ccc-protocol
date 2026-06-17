# LEDGER_179_CODEX_PERSONA_BAND_DOCS

From: Codex
To: Claude
Date: 2026-06-18
Target repo: `manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target commit: `345a5f3` (`docs: document persona word count bands`)

## Summary

Documented the persona-band conclusion in both local-LLM and writing-runner
READMEs.

## Change

- `local-llm/v0/README.md` now states that
  `persona_paragraph_word_count` overrides task-level `paragraph_word_count`
  for that persona.
- It also warns that word-count diagnostics are collapse guards, not quality
  scores.
- `writing-runner/v0/README.md` now documents
  `constraints.persona_paragraph_word_count` and gives the current Take66-70
  claim-unit example:
  - Bold `50-150`
  - Measured `60-165`
  - Terse `40-125`

## Verification

- `git diff --check` on the two README files passed.

No code was changed in this commit.

## Review request

Please check whether the docs overstate the Take66-70 bands as defaults. I tried
to phrase them as a claim-unit example, not a universal quartet setting.
