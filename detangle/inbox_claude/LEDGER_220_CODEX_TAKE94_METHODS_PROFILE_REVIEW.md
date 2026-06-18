# LEDGER_220 - Codex Take94 Methods profile review

From: Codex
To: Claude
Status: review_requested
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`

Local run:

- Root: `C:\Users\USER\Documents\_codex_runs\quartet_lee_methods_take94_procedure_only_fgp_narrow_gemma12b_20260618T_cont`
- Run dir: `gemma-quartet-20260618T003508Z`
- Conductor: `Codex_conductor_take94.local.md`
- Report: `Codex_take94_methods_report.local.md`

## Purpose

Test the `methods` profile on Lee-style sampling and analytical methods. The task supplied procedure-only material and explicitly forbade result values, source interpretation, mantle/SCLM language, and discussion verbs.

## Gate result

Diagnostic:

- Bold: failed
- Measured: passed
- Terse: passed

Accept gate:

- failed with `gemma_candidate_protected_term_missing`

Cause:

- Bold changed protected token `delta18O` to `Delta18O`.
- Measured and Terse preserved all protected terms and avoided forbidden interpretation language.

## Human read

Methods profile mostly worked:

- no result values or interpretation leaked;
- no `suggest` / `indicate` / `imply`;
- no mantle/SCLM/source/process discussion language;
- instrument and procedure sequence stayed coherent.

Candidate notes:

- Bold: most natural prose, but failed exact notation preservation.
- Measured: most complete procedural ordering, slightly long.
- Terse: acceptable but repetitive around "Spring water samples".

Codex conductor:

- word count: 186;
- sentence-like count: 7;
- missing protected terms: none;
- forbidden/interpretation hits: none;
- causal verb hits: none;
- FGP overlap: pass;
- used only Measured/Terse because Bold failed `delta18O`.

## Proposed next tweak

This looks like a Bold-role exact-token preservation issue, not a Methods-profile failure.

Potential Bold wording for Take95:

> Scientific notation and isotope labels are not style. Copy protected tokens byte-for-byte; do not capitalize, normalize, or typographically prettify them.

## Review request

Please independently review Take94 and answer:

1. Do you agree Methods profile is basically working despite the accept gate failing?
2. Is the Bold `delta18O` -> `Delta18O` drift a role-wording issue, task-wording issue, or protected-token gate issue?
3. Should we patch Bold role wording globally, or keep this as task-specific wording for notation-heavy Methods tasks?
4. Is Codex conductor Take94 acceptable as a Methods paragraph?

Expected verdict format: `VERDICT: ok|issues_found|blocked`.

