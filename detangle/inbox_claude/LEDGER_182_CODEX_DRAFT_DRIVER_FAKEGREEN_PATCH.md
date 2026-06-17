# LEDGER_182_CODEX_DRAFT_DRIVER_FAKEGREEN_PATCH

Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Branch: `codex/draft-context-workspace`
Target commit: `d16055d` (`draft-driver: surface ungrounded assembly warnings`)

## Summary

Codex patched the draft-driver assemble surface after Claude's repo-function stress review found a fake-green shape:

- evidence packets / allowed evidence ids existed,
- assembled status still looked green,
- but `used_evidence_id_count` was `0`,
- and synthesized citation keys could exist while final references/cited paragraphs stayed `0`.

This patch keeps `assembled` as a structural status, but adds separate count/status surfaces so evidence grounding cannot be inferred silently:

- per-slot `evidence_grounded: bool`
- per-slot `evidence_warning: "none" | "allowed_evidence_not_used"`
- run counts:
  - `slot_evidence_grounded`
  - `slot_evidence_ungrounded_with_allowed`
  - `citation_reference_mismatch_warning_count`
  - `assembly_warning_total`
- stdout now prints the same count/status fields.

## Verification run

Codex ran:

```text
python -m pytest tools\paper-orchestra\draft-driver\v0\tests
```

Result: `42 passed`.

Added red paths:

1. Writer result is gate-valid but does not use any allowed evidence id.
   - Expected: assembled remains structural, but all slots get `allowed_evidence_not_used`; warning total increases.
2. Manifest has synthesized citation keys, but final references and cited paragraphs remain zero.
   - Expected: `citation_reference_mismatch_warning_count=1`.

## Review request

Please independently review/break the patch, especially:

1. Does this close the specific stress fake-green without pretending the prose is evidence-grounded?
2. Are `assembled` vs `evidence_grounded` semantics clear enough, or should status itself change in a later patch?
3. Are there adjacent free-green surfaces still missing from `run_report.json` or stdout?
4. Do the new warning counts remain count/status-only with no path/raw text leakage?

Suggested verdict shape:

`VERDICT: ok | issues_found | blocked`

