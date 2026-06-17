# Codex — Take55/56 word-count-gated freer Discussion loop

`2026-06-18 04:4x KST`

VERDICT: **issues_found / useful progress**.

After adding `constraints.paragraph_word_count` in manuscript-atelier `2c23479`, I ran one more freer Discussion pair with the new gate enabled and a narrower task-local forbidden list.

## Runs

- Take55 baseline: `gemma-quartet-synthetic-058`
- Take56 FGP-narrow: `gemma-quartet-synthetic-059`

No resolved numeric values or raw FGP text are relayed here.

## Results

Take55 baseline:

- failed local candidate gate;
- failure was not word count this time;
- cause: one persona corrupted the required caveat placeholder;
- the other two candidates were in range and structurally usable.

Take56 FGP-narrow:

- passed local candidate gate;
- passed scorecard;
- all three candidates stayed in the 90-130 word band;
- all required placeholders were preserved.

## Interpretation

This is the cleanest practical signal so far:

- FGP-narrow plus word-count gating improves **mechanical stability**: length discipline and placeholder preservation were better in the passing run.
- It still does not prove prose-quality uplift.
- The remaining failure mode is **semantic scope drift**: candidates can pass the current gates while using broad but plausible phrases about internal dynamics, mantle geometry, drivers, external processes, or generalized regional/domain behavior.

Codex conductor pass over Take56 stripped those scope-drifting phrases. Local audit:

- word count inside the configured band;
- required placeholders preserved;
- task forbidden terms: zero hits;
- FGP phrase overlap guard: passed with local phrase corpus in memory only.

## Next implementation target

Add a lightweight scorecard / diagnostic axis for scope drift rather than making FGP stronger.

Candidate terms/classes:

- internal dynamics;
- local mantle geometry / mantle volume;
- causal drivers / external processes;
- broad regional or system behavior;
- vague robustness / calibration language.

This should likely start as **scorecard diagnostics**, not a hard gate, because some phrases are section/context dependent. Hard gates remain task-local via `constraints.forbidden_terms`.

