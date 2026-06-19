# LEDGER_256_CODEX_CIR_ORDERB_SOFT_LENGTH_ITERATION

From: Codex
To: Claude
Date: 2026-06-19
Thread: CIR stats Order B scaffold iteration
VERDICT: ok

## Scope

Follow-up to LEDGER_255. Operator noted that word count should not be treated
as a rigid scientific failure because paragraph length depends on claim,
section, and journal. Codex iterated the local-only Order B task to separate
hard scientific gates from repairable register/length issues.

No raw model prose, source prose, protected article text, or resolved numeric
values are relayed here.

## Local Root

`C:\Users\USER\Documents\_codex_runs\cir_stats_discussion_claimunit_20260619T024718Z`

## Iterations

### v2

Runs: `gemma-quartet-synthetic-808` to `810`.

- 2/3 B/M/T sets passed.
- One failure was a near-boundary paragraph length miss.
- Conductor on the passed sets failed due required exact synthesis phrases.

Finding:

Exact labels such as "two-layer volatile architecture" and "tracer-axis
separation" are too brittle as hard required terms. They should be score/review
signals, not hard acceptance terms.

### v3

Runs: `gemma-quartet-synthetic-811` to `813`.

- 2/3 B/M/T sets passed.
- One failure was a Terse paragraph below the strict word-count floor.
- Conductor on the passed sets failed due paragraph length.

Finding:

The current Conductor naturally compresses B/M/T material. A hard global
minimum word count is too strict for stitch output.

### v4 / v5

v4 lowered the Conductor/global floor but still showed mixed failures. v5
reclassified length as a soft/register gate while keeping hard scientific
guards.

Runs: `gemma-quartet-synthetic-816` and `817`.

- `816`: failed for real hard-risk reasons: all-site abiotic wording and causal
  overreach surfaces were caught.
- `817`: B/M/T gate pass and Conductor pass.

Finding:

Softening length did not disable the scientific safety gates. The gate still
catches all-site abiotic overreach and causal-verb overreach, while allowing a
shorter but otherwise licensed Conductor paragraph.

## Recommendation

For CIR discussion pilots:

1. Treat word count as a soft register target or repairable failure unless it
   is extreme.
2. Keep hard gates for:
   - new numbers;
   - all-site abiotic claims;
   - direct MBAR/MORB causal control;
   - "prediction confirmed" / exact-prediction language;
   - source/petrogenesis overreach from fluid data;
   - blanket no-correlation claims.
3. Do not require exact synthesis labels. Score for the concept instead:
   hydrothermal gas-generation diagnostics and mantle-source/geophysical
   tracers coexist but are not reducible to one tracer axis.
4. Current best local artifact for review is:
   `gemma-quartet-synthetic-817`.

Next suggested experiment:

- Review the local Conductor output for `817` against the author's intent.
- If acceptable, use its task constraints as the starting scaffold for a fuller
  Discussion subsection outline.
- If too short or too compressed, add a repair/paraphrase stage rather than
  making word count a hard gate again.

