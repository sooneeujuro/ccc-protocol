# LEDGER_258_CODEX_CIR_SUBSECTION_ORDERB_PILOT

VERDICT: ok

Codex continued the CIR statistics real-use exercise after LEDGER_257 and ran the Order-B subsection scaffold as four paragraph-level B/M/T+Conductor pilots. This note is count-only/prose-free: no raw model prose, protected article text, or resolved result values are relayed.

## Scope

- Target: draft-internal Discussion subsection scaffold using the data-first Order-B structure.
- Paragraph functions:
  - p1 hydrothermal gas-generation axis.
  - p2 mantle/asthenospheric tracer axis.
  - p3 Kim 2017 / La-Sm bridge.
  - p4 tracer-separation synthesis.
- Model: local Gemma via the existing B/M/T quartet and Conductor runners.
- Output: local-only generated prose under the existing `_codex_runs` experiment root; not committed.

## Results

Accepted local stitch:

| paragraph | accepted run | B/M/T gate | Conductor | conductor words |
|---|---:|---|---|---:|
| p1 hydrothermal axis | 822 | 3/3 pass | pass after retry | 166 |
| p2 mantle axis | 824 | 3/3 pass | pass | 159 |
| p3 Kim 2017 / La-Sm bridge | 820 | 3/3 pass | pass after retry | 229 |
| p4 tracer synthesis | 821 | 3/3 pass | pass | 196 |

Local stitch artifacts:

- `DISCUSSION_SUBSECTION_ORDER_B_GEMMA_STITCH_v1.local.md`
- `DISCUSSION_SUBSECTION_ORDER_B_GEMMA_STITCH_v1.safe.json`

The safe manifest records paragraph count, selected run ids, word counts, and response hashes only.

## What Changed During The Pilot

- p1 first attempt failed one Terse candidate on causal-verb overreach. Adding an explicit compatibility/diagnostic verb ladder fixed the surface: the v2 B/M/T run passed 3/3.
- p2 first attempts showed length-gate brittleness: one Measured candidate missed the word-count floor by a few words while preserving the intended bounded role. Lowering the floor for this calibration run produced a clean 3/3 pass and Conductor pass.
- p3 and p4 passed B/M/T directly; p3 needed a Conductor retry for a required-term miss, while p4 passed Conductor directly.

## Policy Finding

The operator's concern about word count is supported by this pilot. Length should be treated as:

- a hard gate only for extreme outputs that are too short to carry the required claim/evidence/caveat structure or too long for the section role;
- otherwise a soft warning / repair trigger, because near-bound length misses can be fixed by paraphrase without changing the scientific claim.

In contrast, causal overreach remains a hard semantic gate. The p1 fix supports adding section-specific safe verb ladders where causal verbs are tempting but not licensed.

## Next Suggested Step

Ask Claude to review the local stitch by scorecard only first:

- Does the four-paragraph order preserve the intended implication arc?
- Are any accepted paragraphs still too timid or too strong?
- Is the current length policy suitable for Discussion drafting, or should the gate distinguish `hard_length_fail` from `repairable_length_warning`?

If that review is acceptable, the next implementation target is a formal repair loop for near-bound word-count failures rather than repeated full Gemma reruns.
