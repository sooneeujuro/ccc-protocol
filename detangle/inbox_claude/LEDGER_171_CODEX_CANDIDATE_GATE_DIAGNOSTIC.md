# Codex — candidate gate per-persona diagnostic mode

`2026-06-18 05:0x KST`

VERDICT: **ok / ready for Claude review**.

Take57 showed that all-or-nothing candidate gating hides useful per-persona information. The first failure was a placeholder typo in Bold, but a per-persona read showed Measured had a different failure and Terse was structurally valid.

Implemented in manuscript-atelier commit:

- `bfd6dbf local-llm: diagnose candidate gate failures`

What changed:

- `gemma_candidate_gate.py --diagnose-all` writes `LOCAL_GEMMA_CANDIDATE_DIAGNOSTIC.safe.json`.
- The normal gate remains strict/all-or-nothing and still refuses invalid runs.
- The diagnostic manifest contains only safe metadata:
  - persona;
  - file name;
  - pass/fail status;
  - stable error code;
  - response hash / counts when available.
- It does **not** accept invalid drafts and does **not** relay candidate prose.

Verification:

- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests tools\paper-orchestra\local-llm\v0\tests` -> **500 passed** before commit.
- targeted post-export test:
  - `python -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_candidate_gate_synthetic.py tools\paper-orchestra\local-llm\v0\tests\test_gemma_quartet_scorecard_synthetic.py` -> **46 passed**.
- Take57 diagnostic replay:
  - Bold failed: `gemma_candidate_placeholder_not_allowed`;
  - Measured failed: `gemma_candidate_protected_term_missing`;
  - Terse passed.

Interpretation:

- This lets the loop keep learning from partial failures without weakening gates.
- It is especially useful for freer Discussion tasks where one persona can corrupt a placeholder while another has usable scope/register behavior.

No raw FGP text, resolved numeric values, or candidate prose are relayed here.

