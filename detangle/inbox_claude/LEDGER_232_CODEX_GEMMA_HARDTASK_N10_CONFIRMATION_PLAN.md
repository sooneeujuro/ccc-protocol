# LEDGER_232 - Codex Gemma hard-task N10 confirmation plan

Timestamp: 2026-06-18 17:12 KST

Scope: follow-up run after Claude scoring of `gemma-tournament-20260618T064019Z`.

## Decision

Operator approved a larger confirmation run with the same prompt/variant set, increasing repetitions to `10`.

This intentionally keeps the prompts fixed:

- Variant preset: `round1`
- Task family: same M1-M4 harder task shape used for `064019Z`
- Scoring rubric: `discriminating_v2`
- Primary interpretation focus: `claim_altitude_two_sided` + `caveat_survival`
- Other axes: diagnostic/floor support unless scoring shows a new separation pattern

Rationale: the N=5 pilot produced discrimination on the operator-critical claim/caveat axes, but winner stability is not yet proven. Changing prompts now would mix causes. The next run should test whether the B3/M3/T2 signal reproduces under a larger sample.

## Planned run

- Repetitions: `10`
- Expected model calls: `90`
- Model tag: `gemma4:12b`
- FGP mode: `narrow`
- Output location: local `_codex_runs` only
- Relay policy: counts, timing, paths, blind ids, and error codes only; no response prose or resolved task values

## Claude handoff

After the run completes, Codex will publish a value-free completion note with:

- Tournament id
- Manifest paths
- pass/fail counts by persona
- gate error codes
- elapsed timing
- confirmation that the blind scoring manifest is ready

Claude should then score blind using the same `discriminating_v2` 0-3 rubric, keeping reveal closed until scoring completes. The main question is whether the N=5 finding reproduces:

- B3 remains strongest among Bold variants
- M3 remains strongest among Measured variants
- T2 remains strongest among Terse variants
- B2 and T3 remain weak under the harder task
- claim/caveat axis separation remains larger than the easy-task rounds
