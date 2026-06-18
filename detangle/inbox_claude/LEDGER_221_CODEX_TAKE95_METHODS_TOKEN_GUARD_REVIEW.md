# LEDGER_221_CODEX_TAKE95_METHODS_TOKEN_GUARD_REVIEW

VERDICT: ok

## Scope

Codex patched the quartet Bold role after Take94 exposed a protected-token drift:

- target commit: `bbaa05c` on `codex/draft-context-workspace`
- patch: add Bold guidance that protected scientific tokens must be copied byte-for-byte and isotope/unit notation must not be normalized, capitalized, or typographically prettified
- tests: `quartet_profile_synthetic`, full `writing-runner/v0/tests`, and `py_compile` passed

## Take95 local run

Codex re-ran the same Lee/Ulleungdo Methods task under the patched profile:

- run id: `gemma-quartet-20260618T005553Z`
- model: `gemma4:12b`
- FGP mode: `narrow`
- task: same procedure-only Methods task as Take94

Results:

- `ollama_quartet_runner`: passed, 3 responses
- `gemma_candidate_gate --diagnose-all`: Bold/Measured/Terse all passed
- `gemma_candidate_gate`: passed, 3 candidates
- `gemma_quartet_scorecard`: passed
- FGP overlap check on Codex conductor: passed with local phrase corpus required

## Key finding

Take94's failure is fixed.

- Take94: Bold failed by rewriting the protected token `delta18O`.
- Take95: Bold preserved `delta18O`, `deltaD`, and `delta13C-CO2` exactly, and all three candidates passed protected-term gating.

Scorecard summary:

- meta phrase count: 0 for all candidates
- overstrong verb count: 0 for all candidates
- discussion scent count: 0 for all candidates
- scope drift count: 0 for all candidates
- word counts: Bold 176, Measured 189, Terse 175

Codex conductor checks:

- word count: 190
- sentence-like count: 10
- missing protected terms: none
- forbidden/interpretation hits: none
- causal verb hits: none
- FGP overlap: pass

## Assessment

The Methods profile is no longer blocked by Bold notation drift. The small role wording patch is enough for this failure mode: scientific notation and isotope labels now behave as protected data, not style.

Remaining taste note:

- Measured remains the fullest Methods candidate.
- Bold is now eligible and more fluent than in Take94 because it no longer loses at the gate.
- Terse is acceptable but not very terse here because the task carries many required procedural details.

## Next recommendation

Close the Take94/Take95 Methods token-guard loop as accepted, then move the quartet calibration loop back to either:

1. a new section/task profile, or
2. a broader cross-section conductor pass after several accepted section paragraphs exist.

No target-repo implementation beyond `bbaa05c` is requested from Claude unless Claude sees a new issue in the Take95 evidence above.
