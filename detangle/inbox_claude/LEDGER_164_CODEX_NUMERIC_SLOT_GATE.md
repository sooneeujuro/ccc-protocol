# LEDGER_164_CODEX_NUMERIC_SLOT_GATE

## VERDICT: implemented

Codex promoted the recurring numeric-slot drift from prompt prose into an optional structured gate.

Target commit:

- manuscript-atelier branch: `codex/draft-context-workspace`
- commit: `c8b5128` (`writing: gate numeric placeholder slots`)

## What changed

Added optional task constraint:

```json
"constraints": {
  "numeric_placeholder_slots": {
    "{{NUMERIC:...}}": {
      "prefixes": ["allowed prefix"],
      "suffixes": ["optional allowed suffix"]
    }
  }
}
```

The writing contract validates the structure. The local Gemma prompt pack renders the rules into the prompt. `gemma_candidate_gate.py` now rejects:

- numeric placeholder used after a non-allowed prefix;
- numeric placeholder followed by a non-allowed suffix;
- numeric slot rule that references a placeholder absent from the task instruction.

## Verification

Tests:

- focused contract/local-LLM tests: passed
- writing-runner + local-LLM suites: `489 passed`

Smoke:

- Take46 used structured numeric slots and correctly failed before slot evaluation because one model invented an unallowed evidence placeholder (`CIR_DOMAIN_LM_MODEL`) and inserted self-correction prose.
- Take47 added a domain-placeholder pin and passed candidate gate, scorecard, stitch shape, and full local preview.

Exact unpublished numeric values remain local-only and are not relayed here.

## Interpretation

The new gate catches the class of issue exposed by Take44/45: placeholder presence alone is not enough; long numeric displays need local grammar constraints. This also confirms that the previous candidate gate was a presence/shape guard, not a slot-context guard.

## Current best local candidate

Take47 Terse is the best current structured-slot baseline candidate. It passes the new gate and reads cleanly after numeric + evidence/caveat preview, though the Introduction remains dense.

## Next

Rerun a freer FGP comparison using `numeric_placeholder_slots`, then pass the best full-preview candidate to a conductor/frontier polish stage.
