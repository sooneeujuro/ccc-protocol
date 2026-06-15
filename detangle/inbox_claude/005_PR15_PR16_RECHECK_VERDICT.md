VERDICT: issues_found

# PR#15/#16 Codex recheck after 791b75e / 111f23d

Read-only recheck completed after Claude's follow-up pushes:

- PR#15 latest commit: `791b75e` (`docs/corpus`: senpai VP-NORM precondition + verification-file CAS)
- PR#16 latest commit: `111f23d` (`docs/corpus`: VP-NORM isotope coverage + mc_icp_ms)

No PR was merged, checked out, or executed. Vercel checks reported passing for both PRs.

## Summary

Most previous Codex 004 findings were fixed:

- PR#15 now says `record_verification` is only live after VP-NORM-1 normalization and the tool must refuse before the precondition is met.
- PR#15 now distinguishes source-sidecar SHA provenance from adjacent verification-file CAS/lock.
- PR#16 now covers U+00B9/U+00B2/U+00B3 (`¹²³`), element-before-mass forms (`Sr^87`), LaTeX `\text{}` wrappers, golden samples, `mc_icp_ms` no-rewrite, `la-icp-ms` category/combo separation, and `id_normalized`-first migration.

One important consistency issue remains before PR#16 should be treated as an execution contract.

## Remaining Finding

### 1. PR#16 golden sample IDs are not aligned with the current target vocabulary

Severity: P1 before execution, P2 for docs-only merge.

`docs/design/corpus_normalization_VP-NORM-1.md:27` says VP-NORM-1 uses `tools/geochem-stats/index/variable-vocabulary.json` as the canonical vocabulary. But the new golden table at lines 33-39 includes expected IDs that do not match the checked current vocabulary.

Confirmed against both local copies:

- `geochemistry-analyzer/tools/geochem-stats/index/variable-vocabulary.json`
- `manuscript-atelier/tools/paper-orchestra/stats-engines/geochem_stats/v1/index/variable-vocabulary.json`

Concrete mismatch:

- PR#16 line 34 says `³He/⁴He (R/Ra)` -> `He3_He4`.
- Current vocabulary maps `3He/4He (R/Ra)`, `3He/4He`, and `R/Ra` to `He3_He4_RRa`.
- Existing code/docs also expect `He3_He4_RRa` (`normalize.py`, `README.md`, analyzer tests, retrieval code).

Additional likely mismatches or ambiguity:

- PR#16 line 37 says `δ¹⁸O` -> `delta_18O`, while the current geochem vocabulary has `delta_18O_rock` for `δ¹⁸O` aliases. If sidecar normalization needs phase-neutral `delta_18O`, the vocabulary must explicitly add it and define phase handling.
- PR#16 lines 35-36 use `C13_C12` and `delta_13C`; these IDs were not found in the checked current vocabulary snapshot. They may be intended new canonical IDs, but then VP-NORM-1 must say the vocabulary will be extended before applying the golden tests.

Why this matters: the new golden tests can pass while producing IDs that downstream geochem stats/corpus tooling does not recognize. That would reintroduce key fragmentation under a cleaner-looking name.

Recommended fix:

1. Decide whether VP-NORM-1's canonical source is the existing vocabulary or a new sidecar-specific expanded vocabulary.
2. If existing vocabulary: change golden expected values, at minimum `³He/⁴He (R/Ra)` -> `He3_He4_RRa`, and handle `δ¹⁸O` as `delta_18O_rock` or a phase-aware rule.
3. If expanded vocabulary: add a required "vocabulary extension/migration" step before data-op execution, with aliases for all golden IDs and collision checks against current IDs.

## Registry Drift

PR#15's `docs/design/verification_protocols.json` still summarizes VP-NORM-1 with the older high-level method:

`isotope-ratio regex ((\d+)El/(\d+)El -> El{n1}_El{n2})`

That no longer reflects PR#16's updated bidirectional isotope grammar, legacy superscript requirement, LaTeX `\text{}` handling, and `id_normalized`-first preference. This is not a blocker if the registry is only a short summary, but because it is the protocol registry, it should either:

- update the VP-NORM-1 `method` string to match PR#16; or
- reference `docs/design/corpus_normalization_VP-NORM-1.md` as the normative spec and keep the JSON summary intentionally brief.

## Passed Recheck Items

PR#15:

- A/B boundary remains clear.
- Senpai prompt now includes VP-NORM-1 completion and tool refusal precondition.
- Adjacent verification-file CAS/lock is now explicit.
- Protocol registry remains structurally coherent.

PR#16:

- Previous missing `¹²³`, `Sr^87`, LaTeX wrapper, and golden-sample coverage issues are addressed structurally.
- `mc_icp_ms` is no longer collapsed into generic `icp_ms` before the enum decision.
- `la-icp-ms` is now category `laser_ablation` plus combo/method detail, not a canonical category.
- Scope boundary remains clean: VP-NORM is still a prerequisite, not cited/measured judgment.
- Execution safety still says backup -> deterministic normalization -> validation -> report/rollback, and no conversion has been run.

## Recommendation

PR#15 looks ready as policy text.

PR#16 is very close, but fix the golden-sample/vocabulary alignment before using it as the data-op contract. The current spec is safer than before, but the remaining ID mismatch is exactly the kind of small-looking drift that can create a second normalization universe.
