# LEDGER_311_CODEX_CIR_P3_POLISH_RUN_825

VERDICT: review_requested

Codex completed the P1 CIR subsection p3 polish run requested by the application
pivot. This note is count/status/hash only and does not relay raw model prose,
protected article text, captions, or resolved numeric values.

## Scope

- Target: CIR subsection p3 Kim 2017 / La-Sm bridge polish.
- Prior selected run: `gemma-quartet-synthetic-820`.
- New run: `gemma-quartet-synthetic-825`.
- FGP mode: none.
- Model tag: gemma4:12b.
- Local-only: true.
- Commit/relay safe: false.

## Task change

Codex created a local polish task from the 820 task and added the missing bridge
requirements for the MORB-like / Plume-like mantle-source vocabulary and the
mantle-heterogeneity bridge. The instruction also bounded the bridge so helium
remains the direct fluid evidence, La/Sm remains supporting enrichment/melting
context, and rock petrogenesis is not inferred from fluid data.

## Execution status

- Prompt pack prepared: ok.
- B/M/T model run: ok.
- Candidate gate: passed.
- Candidate count: 3.
- Quartet scorecard: ok.
- Conductor model run: ok.
- Conductor response count: 1.
- Conductor response sha256: `54977b67a908f6a9b5facf70f0aaf3b7609a89ba68d93520a9118592571190e0`.
- Conductor paragraph word count: 105.
- Conductor warning count: 0.

## Count-only scorecard summary

| persona | paragraph_words | sentences | warnings | overstrong | meta | scope_drift | discussion_scent |
|---|---:|---:|---:|---:|---:|---:|---:|
| Bold | 131 | 4 | 0 | 0 | 0 | 0 | 2 |
| Measured | 144 | 6 | 0 | 0 | 0 | 0 | 2 |
| Terse | 87 | 4 | 0 | 0 | 0 | 0 | 1 |

## Required bridge presence

The 825 conductor output contains all seven required bridge tokens checked by
Codex, including the two source-vocabulary tokens that were absent from the 820
conductor output. Presence result: 7/7.

## Review request

Please independently inspect the local 825 artifacts and compare against 820,
with attention to:

1. whether the MORB-like / Plume-like vocabulary is restored without becoming a
   circular similarity claim;
2. whether helium remains the direct fluid bridge;
3. whether La/Sm stays as supporting enrichment/melting context rather than a
   proxy for fluid helium;
4. whether no rock petrogenesis or causality overreach was introduced.

Codex recommends treating 825 as the current P1 candidate unless semantic review
finds issues.
