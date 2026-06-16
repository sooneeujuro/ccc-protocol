# INIT_012_CIR_REPO_FUNCTION_STRESS_RESULTS

From: Codex
To: Claude Code
Date: 2026-06-17 KST
Thread: CIR repo-function stress test, not thesis evaluation

## VERDICT

issues_found

The CIR substrate successfully exercised many manuscript-atelier paths, but the important result is not "draft green." It is that two fake-green risks and several integration/test-runner gaps are now visible.

## What Codex Ran

Local-only, no merge/deploy/live infra. Raw unpublished data and private paths were not committed or copied into coordination notes.

Covered paths:

- corpus binding checker
- source discovery checker
- evidence-demand checker
- draft-driver prepare/ingest/assemble with no-search
- writing-runner synthetic mode
- md-reader on empty bundle
- claim-extractor
- md-reader-builder claim append path
- md-reader after claim append
- numeric audit
- review-runner synthetic mode and review append
- backchain
- retrieval adapter direct BM25 calls
- draft-driver search mode
- source-support checker with synthetic anchor/support maps
- figure-bridge preview-emission contract
- Python aggregate figures from safe summary tables
- Data Analytics MCP chart/table over tiny reviewed aggregate rows
- local Ollama/Gemma smoke
- per-suite pytest subprocess matrix

## Key Findings For Your Review

1. Fake green: `md-reader` can report READY when a bundle has zero claims. This should probably become `needs_claim_extraction`, `skeleton_only`, or another non-final state unless explicitly marked as a fixture.

2. Fake green: search-mode draft-driver can retrieve evidence packets, but the synthetic writer used zero evidence IDs and generated zero references. The final reader can still look READY if no claims are appended.

3. Useful red: after claim extraction was wrapped and appended, the same draft became BLOCKED with 18 unverified/uncited claim blockers. This is the behavior we want once claims exist.

4. Integration issue: claim-extractor output is not directly consumable by md-reader-builder `--claim-drafts`; wrapping it under `schema: claim_ledger_append_drafts_v1` works. Please verify whether README/CLI contract should change or claim-extractor should optionally emit appender-ready output.

5. Useful red: backchain reported missing evidence categories for the safe CIR claim. That is appropriate; it means reverse-demand is doing work.

6. Source-support checker behaved correctly: metadata-only and ambiguous anchors remained human-review instead of becoming support.

7. Figure-bridge preview works locally for advisory-only emissions. Codex intentionally did not call live MCP submit.

8. Test-runner issue: running many `v0/tests` folders in one pytest process fails due duplicate `v0.tests.conftest` plugin/import names. Running suites in separate Python processes gives 10/11 green.

9. Retrieval pytest issue: `test_constructor_fails_closed_without_md_dir` fails on the D3-era branch because repo-local corpus source resolution now satisfies md-dir lookup even after env vars are removed. Please decide whether the test should hide/disable the local source file or the constructor should expose a stricter fail-closed mode for tests.

10. Windows UX issue: some CLI help output can still be unsafe under CP949 unless `PYTHONIOENCODING=utf-8` is set.

11. Local LLM note: Gemma/Ollama smoke returns a Korean response, but CLI capture includes spinner control sequences. Use API or sanitize stdout before treating local LLM logs as stable test artifacts.

## Suggested Next Actions

1. Review the fake-green semantics first. They matter more than scientific polish.
2. Add a first-class claim-extractor -> claim-appender bridge or update docs.
3. Add a meta-test command that runs `v0` suites as subprocesses, or fix package names so one-process pytest works.
4. Keep source-support and backchain in the paper-writing loop because they are the best guards against "looks cited but is not really supported."
5. Treat the CIR scientific draft as a test fixture until source provenance and boundary-independence are resolved.

## Operator Context

The operator clarified that this task is not "analyze my thesis"; it is "use my thesis/data as material to test whether all repo code paths work." Please keep your review pointed at system behavior, false pass/fail behavior, and missing automation seams.
