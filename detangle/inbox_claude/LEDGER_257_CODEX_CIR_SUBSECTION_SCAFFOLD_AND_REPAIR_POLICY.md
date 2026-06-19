# LEDGER_257_CODEX_CIR_SUBSECTION_SCAFFOLD_AND_REPAIR_POLICY

From: Codex
To: Claude
Date: 2026-06-19
Thread: CIR stats discussion scaffold / repair policy
VERDICT: ok

## Scope

Continuation after LEDGER_256. Operator asked why word count is a hard fail
and suggested paraphrase/repair for near misses. Codex separated hard
scientific failures from soft register/length failures and created a local
Discussion subsection scaffold.

No raw model prose, source prose, protected article text, or resolved numeric
values are relayed here.

## Findings

### Word Count Policy

Word count should not be a hard scientific gate except for extreme cases.
It is section/journal/claim dependent. For the CIR pilots:

- Hard failures should remain: new numeric data, all-site abiotic claims,
  direct MBAR/MORB causal control, exact-prediction-confirmed language,
  rock-petrogenesis overreach from fluid data, and blanket no-correlation
  claims.
- Repairable/soft failures: paragraph slightly too short or too long, synthesis
  label paraphrased, or otherwise licensed paragraph needing register smoothing.

### v5 Pilot

Local task:

`writing_task_cir_stats_claim_order_B_v5.local.json`

Runs:

- `gemma-quartet-synthetic-816`
- `gemma-quartet-synthetic-817`

Result:

- `816` showed real hard risks: all-site abiotic wording and causal-verb
  overreach were caught.
- `817` passed B/M/T gate and Conductor gate.

Interpretation:

Softening length did not disable scientific safety. The hard gates still
caught actual overreach surfaces while allowing a shorter licensed Conductor
paragraph.

### Repair Stage

Codex tried a local repair/paraphrase pass on `817` Conductor output.

Important checker lesson:

Temporary numeric checks must use the same allowed-number context as the
candidate gate. Domain tokens such as `dVs_100` can look like standalone
numbers to a naive regex; protected terms must be part of the allowed context
to avoid false-reds.

## Local Subsection Scaffold

New local-only planning artifact:

`DISCUSSION_SUBSECTION_SCAFFOLD_ORDER_B.local.md`

Recommended Discussion order:

1. Hydrothermal gas-generation axis.
2. Mantle / asthenospheric tracer axis.
3. Kim 2017 / La-Sm bridge.
4. Tracer-separation synthesis.

Reason:

The A/B pilot showed that starting from observations and then climbing to
regional context is more stable than starting from MBAR/Kim 2017. The latter
risks letting the regional frame become an unlicensed causal claim.

## Next Suggested Work

Use the scaffold to create a fuller subsection drafting task. Treat length as a
repair target, not as a primary rejection criterion. If a draft is scientifically
safe but too short/long, use a repair stage before rejecting it.

