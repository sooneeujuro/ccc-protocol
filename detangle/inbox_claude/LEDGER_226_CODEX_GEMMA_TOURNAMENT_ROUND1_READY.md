# LEDGER_226 - Codex Gemma Tournament Round 1 Ready For Blind Scoring

VERDICT: ready_for_blind_scoring

Codex ran the first 45-entry Gemma prompt tournament after operator GO for model execution.

Local-only tournament directory:

`C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T111500Z`

Blind scoring manifest:

`C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T111500Z\LOCAL_GEMMA_TOURNAMENT_SCORING_BLIND.local.json`

Run manifest:

`C:\Users\USER\Documents\_codex_runs\gemma-tournament-20260618T111500Z\LOCAL_GEMMA_TOURNAMENT_RUN.local.json`

Scope:

- Model: `gemma4:12b`
- FGP mode: `narrow`
- Entries: 45
- Passed response files: 44
- Failed entries: 1
- Max retries: 1
- Timeout: 420 seconds per attempt
- Total wall time: 3,885,484 ms, about 64 minutes 45 seconds
- Median entry elapsed: 83,717 ms
- P90 entry elapsed: 122,625 ms

Failure:

- `blind_2355fcb677598466`
- Persona: `Terse`
- Repetition: 2
- Attempts: 2
- Gate: `gemma_candidate_new_number_present`
- Response file: null

Scoring instruction:

- Score only entries with `status: "passed"` and non-null `response_file`.
- Treat the failed entry as a pass-rate failure for the associated blinded variant/persona once reveal is allowed.
- Do not inspect prompt pack directories or reveal maps during blind scoring.
- The scoring manifest was checked for obvious de-blind fields (`prompt_pack_dir`, variant prose, instruction) and none were found.

Please perform independent blind scoring using the agreed rubric:

- hard-fail gates first: raw FGP leakage, new unsupported numbers, meta prose, conductor/new-claim behavior if applicable
- scored axes: claim altitude calibration, caveat survival, register, protected-token integrity, concision, section fit
- no best-of selection; use distribution/variance and worst-case behavior

After blind scoring, request reveal only after score records are written.
