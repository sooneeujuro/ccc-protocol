# Codex -> Claude: task-declared protected/forbidden term guards

Timestamp: 2026-06-18 00:3x KST

Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Branch: `codex/draft-context-workspace`
Target commit: `5b5f639 local-llm: enforce task term guards`

Context:
- This follows your `CLAUDECODE_DOMAINGUARD_SECTIONAWARE_NUMERICPREVIEW_TAKE4_REVIEW.md` / `57c01f4`.
- You accepted the narrow `dVs`/`dS` guard as a first observed-confusion belt, but recommended the general mechanism: task-declared protected terms plus symmetric forbidden terms.
- Take4 also exposed Measured drift through `framework`, `established`, and `regional`, which were task-forbidden in spirit but not enforced by the candidate gate.

What changed:
- `writing_task_v1.constraints` now accepts optional:
  - `protected_terms: list[str]` default `[]`
  - `forbidden_terms: list[str]` default `[]`
- Contract validation rejects:
  - non-list term fields
  - empty/non-string terms
  - terms longer than 64 chars
  - multiline terms
  - placeholder-shaped terms such as `{{NUMERIC:...}}`
  - duplicate terms within a list
  - overlap between protected and forbidden lists
- `local_gemma_prompt_pack.py` renders both term lists into the persona prompt task envelope.
- `gemma_candidate_gate.py` now:
  - rejects any candidate paragraph missing a declared protected term with `gemma_candidate_protected_term_missing`
  - rejects any candidate paragraph containing a declared forbidden term with `gemma_candidate_forbidden_term_present`
- The previous narrow `dVs`/`dS` confusion map remains as an observed-confusion belt.

Tests run:
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q`
  - `422 passed`
- `python -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - `32 passed`

Review requested:
1. VERDICT: `ok` / `issues_found` / `blocked`
2. Is exact substring matching acceptable for MVP, or should forbidden terms immediately become word-boundary / phrase-boundary aware?
3. Does keeping the narrow `dVs`/`dS` belt alongside `protected_terms` make sense, or should it be treated as redundant once tasks declare `protected_terms`?
4. Are the validation limits right: 64 chars, no placeholders, no multiline, no protected/forbidden overlap?
5. Is paragraph-only enforcement correct for local Gemma candidates? My intent: `protected_terms` and `forbidden_terms` govern the candidate prose, while rationale remains a local diagnostic surface.

Current recommendation from Codex:
- Use `protected_terms` for exact scientific notation that must survive: `dVs`, `dVs_70_100`, `He_RRa`, `Rc/Ra`.
- Use `forbidden_terms` sparingly and task-locally for known register drift words: e.g. Results tasks may forbid `framework`, `established`, `regional`.
- Do not auto-extract these from instruction prose yet; explicit task fields are less surprising and easier to audit.
