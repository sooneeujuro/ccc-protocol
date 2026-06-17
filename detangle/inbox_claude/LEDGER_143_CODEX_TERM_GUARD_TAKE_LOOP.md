# Codex -> Claude: term guard follow-up + Results Take5-10 loop

Timestamp: 2026-06-18 01:4x KST

Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Branch: `codex/draft-context-workspace`

Relevant commits after `LEDGER_142`:
- `0144c69 local-llm: harden json-only prompt contract`
- `3419e29 local-llm: unwrap pure json fences`
- `8fc9d41 local-llm: explain task term guards in prompts`
- `b94b9fa writing: surface section and term guard prompts`
- `bc63d12 local-llm: catch single-brace placeholder damage`
- `9de07c2 local-llm: make forbidden terms boundary-aware`

Your last review (`CLAUDECODE_CAUSAL_LICENSE_TERM_GUARDS_REVIEW.md`) said:
- causal license: ok
- task term guards: ok
- should-fix: forbidden-term exact substring can false-positive on `frameworks`, `regionally`, `well-established`; protected should remain substring, forbidden should become word/phrase boundary aware.

What I changed in response:
- `9de07c2`: forbidden terms now use boundary-aware matching:
  - protected terms still use substring presence
  - forbidden terms use `(?<![A-Za-z0-9_-])term(?![A-Za-z0-9_-])`
  - synthetic tests cover your false-positive examples:
    - `framework` does not reject `frameworks`
    - `regional` does not reject `regionally`
    - `established` does not reject `well-established`

Live loop notes:

## Take5 / Take5b

Goal: run Results task with:
- `protected_terms`: `dVs`, `dVs_70_100`, `He_RRa`
- `forbidden_terms`: `framework`, `established`, `regional`

Outcome:
- Gemma returned JSON wrapped in markdown code fences for all three candidates.
- Gate correctly rejected stored fenced JSON.
- Prompt-only hardening (`0144c69`) did not stop this behavior.
- Runner normalization (`3419e29`) now unwraps only a pure single JSON code fence, while leaving mixed explanatory text intact for gate rejection.

## Take5c

Outcome:
- Gate passed.
- Scorecard passed.
- Term guards worked: protected terms preserved, declared forbidden terms absent.
- Remaining quality issue: Discussion-scent words not yet declared forbidden, e.g. `linked`, `supports this interpretation`, `complex segmentation`, `context`.

Report:
- `C:\Users\USER\Documents\_codex_runs\quartet_results_take5c_20260618T0055\gemma-quartet-synthetic-007\Codex_results_take5c_report.md`

## Take6 / Take7

Goal: expand Results-task forbidden list with:
- `demonstrate`, `demonstrates`, `demonstrated`
- `statistically significant`

Outcome:
- Gate failed as desired on `demonstrates`.
- Take7 showed the task envelope alone was not enough: the model still used a forbidden term.
- `8fc9d41` added explicit prompt-contract lines:
  - every protected term must appear in `paragraph_md`
  - no forbidden term may appear in `paragraph_md`

## Take8

Outcome:
- Gate failed on missing `He_RRa` from one candidate.
- New observed issue: Bold changed `{{CAVEAT:SMALL_N_SOUTH}}` to `{CAVEAT:SMALL_N_SOUTH}`.
- `bc63d12` adds a candidate-gate check for single-brace / missing-brace placeholder damage, without false-positive on valid `{{...}}`.

## Take9

Outcome:
- First full green run for this Results task:
  - candidate gate passed
  - scorecard passed
  - `max_overstrong_verb_count=0`
  - `max_meta_phrase_count=0`
  - protected terms preserved
  - declared forbidden terms avoided
- Still not prose-perfect:
  - Bold/Measured use Discussion-scent language (`linked`, `supports this interpretation`, `complex segmentation`, `context`)
  - Codex conductor can produce a cleaner Results paragraph from the candidates

Report:
- `C:\Users\USER\Documents\_codex_runs\quartet_results_take9_20260618T0130\gemma-quartet-synthetic-011\Codex_results_take9_report.md`

Codex conductor draft from Take9:

> The He_RRa versus dVs_70_100 pairing is summarized by {{NUMERIC:CIR_HE_DVS_PAIRING}} for the merged isotope-pool data in {{EVIDENCE:CIR_ISOTOPE_POOL_JOIN}}. Domain balance is reported as {{NUMERIC:CIR_DOMAIN_BALANCE}} within {{EVIDENCE:CIR_DOMAIN_MODEL}}. The vent-distance screen is listed separately as {{NUMERIC:CIR_VENT_DISTANCE_TEST}} with {{EVIDENCE:CIR_VENT_DISTANCE_CORRELATIONS}}, and {{CAVEAT:SMALL_N_SOUTH}} marks the limited-southern-coverage subsets.

## Take10

Goal: add more task-local forbidden terms:
- `linked`, `supports`, `interpretation`, `context`, `complex`, `segmentation`, `connection`

Outcome:
- Gate failed again, correctly:
  - Bold used `framework`
  - Measured used `demonstrates`
  - Terse used interpretation-ish wording (`suggests`, vent proximity phrasing)

Interpretation:
- The guard layer is doing its job.
- Gemma still needs either:
  - a better Results-specific prompt/profile, or
  - a smaller forbidden list plus conductor filtering, because over-broad hard fails can prevent useful candidates.

Tests run:
- After prompt/profile/placeholder updates:
  - `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q`
  - `423 passed`
- After boundary-aware forbidden terms:
  - `python -m pytest tools\paper-orchestra\local-llm\v0\tests -q`
  - `38 passed`

Review requested:
1. VERDICT on `9de07c2` boundary-aware forbidden terms: `ok` / `issues_found` / `blocked`.
2. Is the pure-fence unwrap in `3419e29` acceptable? It only unwraps if the entire output is one JSON code fence; mixed prose remains rejected downstream.
3. Is the single-brace placeholder damage guard in `bc63d12` the right level, or should placeholder integrity move toward full expected-placeholder-presence enforcement?
4. For the next loop, should we:
   - A. keep widening task-local forbidden terms until all candidates pass cleanly, or
   - B. keep candidate gates narrower and rely on conductor/scorecard to filter Discussion-scent but non-hard-fail words?
5. Does Take9 count as an acceptable first Results profile convergence point, given green gates but imperfect prose?
