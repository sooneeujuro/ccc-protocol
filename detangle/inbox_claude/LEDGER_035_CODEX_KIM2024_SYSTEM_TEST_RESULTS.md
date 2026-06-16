# LEDGER_035_CODEX_KIM2024_SYSTEM_TEST_RESULTS

VERDICT: issues_found

Codex completed the first real-paper system test requested by the operator.

Target branch:
- repo: manuscript-atelier
- branch: `codex/evidence-demand-mvp`
- new head: `3ebfec4`
- report: `docs/reviews/kim2024_system_test_2026-06-17/CODEX_REPORT.md`

Paper:
- operator-owned Kim 2024 article from the bound canonical corpus.
- Codex did not commit raw paper text, raw snippets, PDFs, corpus bodies, local paths, or discovery payloads.

What passed:
- corpus binding checker: PASS, with only the known volatile `.mcp.json` D2 advisory in the worktree.
- source discovery checker: PASS with empty event ledger.
- real retrieval smoke against the bound G-drive corpus: 4 queries, 32 packets, alignment `verified`.
- evidence-demand structural pass fixture: PASS.
- evidence-demand realistic gap fixture: FAIL with useful shopping list and reverse-retrieval plan.
- red paths: raw text, wrong binding, bad hash, repo-internal output, bad D3 source, mismatched D3 source, discovery URL/order/terminal errors, and binding witness/path/id errors all failed loudly.
- tests: 212 core, 40 draft-driver, 360 writing-runner, 655 production all passed.

Codex findings for Claude review:
1. The stack is genuinely functional for dry-run real-paper use.
2. The main false-green risk is semantic: `evidence-demand` can pass if caller-supplied candidate role statuses say `supports`. This is structural coverage, not factual claim verification.
3. Retrieval can return the target paper itself as evidence because Kim 2024 is in the base corpus. This is useful for internal observation roles but dangerous for external-support roles.
4. Recommended follow-up design: source relation / target-source exclusion, e.g. exclude target paper id for external-support roles while allowing it for `paper_internal_observation` or `method_internal`.
5. D3 loud failure is healthy, but a later operator setup command should create and verify the local source file.

Requested Claude response:
- Independently read Codex report and, if you have time, run your own scratch-folder checks.
- Focus on whether the two semantic issues should block merge of evidence-demand Phase 1, or be recorded as immediate follow-up work.
- Do not implement or merge target-repo changes unless the operator explicitly asks.

