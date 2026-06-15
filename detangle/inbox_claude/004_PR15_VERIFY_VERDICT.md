VERDICT: issues_found

# TASK 004 - Codex PR#15 + PR#16 verification review

Read-only review completed for:

- PR#15 `sooneeujuro/manuscript-atelier#15` (`docs/corpus-verification-policy`)
- PR#16 `sooneeujuro/manuscript-atelier#16` (`docs/corpus-normalization-vp-norm-1`)

Inputs used: `gh pr view`, `gh pr diff --color=never`, and GitHub content API reads for line-numbered branch files. I did not merge PRs, check out PR branches, run PR code, or modify `manuscript-atelier`.

## Findings

### 1. PR#16 misses common isotope-label forms, so VP-NORM-1 may leave avoidable `raw_label_only` residue

Severity: P1, fix before data-op execution; preferably fix in the spec before merge.

`docs/design/corpus_normalization_VP-NORM-1.md:23-28` defines the variable-id rules, but the covered transformations are too narrow for the corpus examples and the stated 73% target.

Specific gaps:

- Line 23 names U+2070-2079 / U+2080-2089 only. That omits the very common legacy superscripts U+00B9/U+00B2/U+00B3 (`¹²³`). Existing geochem normalizer already folds `¹`, `²`, `³`; corpus/vocabulary examples include `³He/⁴He`, `δ¹⁸O`, `δ¹³C`, `²⁰Ne/²²Ne`.
- Lines 24-25 mention `Sr^87` and then define only a number-before-element isotope-ratio regex `(\d+)(El)/(\d+)(El)`. If `Sr^87` becomes `Sr87`, that regex will not match. The rule needs either canonical mass-before-element conversion or an explicit element-before-mass variant.
- Line 24 does not cover LaTeX forms with `\text{}` wrappers seen in the corpus, e.g. `$^{87}\text{Sr}/^{86}\text{Sr}$`.
- Line 25's placeholder `El` should be specified as an element-token class and should handle whitespace/braces/parentheses around isotope ratios.

Suggested patch: add a small golden sample table to §1 with expected IDs for at least:

- `³He/⁴He (R/Ra)` -> `He3_He4_RRa`
- `¹³C/¹²C`, `δ¹³C`, `δ^18O`, `$^{87}\text{Sr}/^{86}\text{Sr}$`
- `Sr^87/Sr^86` or decide it is invalid and document why
- `⁴⁰Ar/³⁶Ar`, `²⁰Ne/²²Ne`

### 2. PR#16 instrument mapping has an unresolved semantics conflict around `mc_icp_ms`

Severity: P2 for spec merge, P1 before execution.

`docs/design/corpus_normalization_VP-NORM-1.md:32` says schema enum should add `tims` and consider `mc_icp_ms`, but line 35 maps `mc_icp_ms`/`mc_icpms` to `icp_ms`, while line 57 leaves "add `mc_icp_ms` or absorb into `icp_ms`" open.

That is a real conflict. If an implementation follows line 35 before the line-57 decision is resolved, multi-collector ICP-MS will be collapsed into generic ICP-MS and the corpus loses method semantics relevant to isotope work.

Suggested patch: mark `mc_icp_ms` as "no rewrite until decision" or explicitly decide the canonical target in §2. Also clarify the `la-icp-ms -> laser_ablation (+combo la-icp-ms)` wording: is `laser_ablation` the category and `la-icp-ms` a raw/method combo field, or is `la-icp-ms` itself a canonical category?

### 3. PR#15 senpai prompt can drift from the VP-NORM prerequisite

Severity: P2.

The policy correctly gates build order:

- `docs/design/corpus_verification_policy_v0.md:32-43` says VP-NORM-1 must precede `record_verification`.
- `docs/design/corpus_verification_policy_v0.md:157-159` repeats "정규화 없이 빌드 금지" and says the tool should reject unregistered protocol codes.

But the live prompt patch says:

- `tools/research-discussion/v0/prompts/senpai.md:128-131`: when `record_verification` is live, emit provenance judgments while reading full MD; until the tool exists, do not fabricate capability.

That prompt-level guard does not mention "only after VP-NORM-1 is complete / registry-backed tool is live". If the tool appears before normalization is complete, the prompt would still encourage writes.

Suggested patch: change the prompt note to "When the registry-backed `record_verification` tool is live **after VP-NORM-1 normalization**, emit..." or say the tool itself must reject recording until the corpus normalization/version precondition is satisfied.

### 4. PR#15 adjacent verification-sidecar write safety needs one more explicit CAS target

Severity: P2.

`docs/design/corpus_verification_policy_v0.md:107-109` recommends adjacent `<paper>.verifications.json`, CAS on `sidecar_sha1_at_judgment`, and history-preserving dedup. This is directionally good, but CAS only on the original sidecar SHA is not enough to prevent lost updates between two writers if the source sidecar is unchanged and both append to the adjacent verification file.

Suggested patch: explicitly require lock/CAS on the verification-sidecar file itself too, e.g. expected current verification-file hash/generation, append-only event records with atomic rename, or a single-writer lock. Keep `sidecar_sha1_at_judgment` as provenance, not the only concurrency guard.

## Checks That Passed

### PR#15 A/B boundary and senpai/RIL scope

The A/B distinction is solid:

- `docs/design/corpus_verification_policy_v0.md:19-28` clearly separates corpus provenance (A) from student-claim certification (B).
- `tools/research-discussion/v0/prompts/senpai.md:119-131` narrows "Never" to the student's claims and explicitly says not to fabricate the capability before the tool exists.

The wording avoids the previous overbroad "no verification decision" conflict while preserving the RIL boundary.

### PR#15 protocol registry

`docs/design/verification_protocols.json` is internally coherent:

- VP-NORM-1, VP-CVM-1, and VP-CERT-1 have distinct `code`, `kind`, `purpose`, `method`, `scope`, `version`, `introduced`, checks, and known limits.
- `docs/design/corpus_verification_policy_v0.md:81` uses `protocol: VP-CVM-1`, and `verifications_meta.protocols` includes `VP-CVM-1` and `VP-NORM-1`.
- The version-bump/tag-preservation rule in `corpus_verification_policy_v0.md:93-97` and registry comment line 2 is the right traceability shape for later re-certification.

### PR#15 data-model direction

The model is additive and mostly safe for a v0.1 policy:

- It does not overwrite `variables_measured`.
- It includes `raw_label_snapshot`, `confidence`, `evidence_loc`, `protocol`, server-side-ish metadata fields, and source sidecar SHA.
- The adjacent-file recommendation keeps provenance annotations out of the extraction layer and avoids BM25 reindex churn.

`raw_label_snapshot` should be treated as audit/display fallback, not as a reliable substitute for normalization. The policy already says VP-NORM-1 must run first, so this is acceptable.

### PR#16 scope boundary and execution safety

The PR#16 scope boundary is clean:

- `docs/design/corpus_normalization_VP-NORM-1.md:3-8` and `42-43` explicitly keep cited/measured judgment in PR#15/VP-CVM.
- §5 (`45-49`) defines backup -> deterministic normalization -> validation -> report -> rollback.
- §6 (`51-54`) keeps the PR as non-gate spec and warns that enum/schema work must observe geochem drift-contract.

The in-place vs `id_normalized` question is correctly left open at line 60. My preference for execution is still `id_normalized` or an audit-preserving migration report until spot checks prove in-place update is harmless.

## Recommendation

Do not treat either PR as live execution approval.

PR#15 can proceed as policy text after tightening the prompt precondition and adjacent-file CAS wording.

PR#16 should add the missing isotope-label variants/golden samples and resolve `mc_icp_ms` mapping before any data operation. As a spec PR, it is close; as an execution contract, it is not ready yet.
