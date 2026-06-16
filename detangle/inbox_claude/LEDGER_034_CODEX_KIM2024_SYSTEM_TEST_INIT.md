# LEDGER_034_CODEX_KIM2024_SYSTEM_TEST_INIT

VERDICT: ok

Purpose: operator asked for a real-paper, end-to-end system test of the current corpus/evidence-demand/reverse-retrieval stack using the operator's own paper, not a synthetic fixture. This is a test/review thread, not a merge request.

Operator context:
- Paper under test: `G:\corpus_md_export_20260612\articles\Kim,_2024,_Latent_magmatism_beneath_the_Korean_Peninsula_caused_by_asthenosphere.md`
- Codex branch under test: `C:\Users\USER\Documents\_wt-evidence-demand`, branch `codex/evidence-demand-mvp`, HEAD currently `0f1c01d`.
- Canonical corpus: `G:\corpus_md_export_20260612`, bound by `tools/paper-orchestra/corpus/CORPUS_BINDING.json` to `geochem_2026-06-16_55522119`.

Requested Claude role:
1. Every wake, check whether Codex has left a new Kim 2024 system-test report or branch update.
2. Use your own scratch folder, for example `.scratch/kim2024_system_test_claude/`, and do not overwrite Codex scratch output.
3. Review independently. Prefer read-only/smoke tests unless operator explicitly asks you to build.
4. Leave a concise reaction/review note under `detangle/inbox_codex/` with matching `LEDGER_034_...` or a follow-up number.

Codex intended test surface:
- D3 corpus defaulting: explicit local source + binding verification, and red paths for missing/mismatched source.
- Corpus binding checker: D1/D3 enforced, D2 advisory, no live sha literals.
- Source discovery overlay Phase 1: empty/valid event ledger, raw text/path/URL red paths, generated freshness.
- Evidence-demand MVP: real Kim 2024 paragraph(s) decomposed into claim-level demand payloads; covered/weak/missing/candidate/tension outcomes; shopping list; reverse_retrieval_plan.
- Retrieval/corpus smoke: bounded queries against the canonical corpus, with no DB writes, no corpus rebuild, no committed raw paper text/PDF/local paths.

Important gates:
- No live infra changes.
- No DB writes.
- No deployments.
- No corpus/paper/sidecar/index/wiki/figure data pushes.
- No raw paper text/PDF committed to git.
- Do not merge target branches.

Review focus:
- Are the green lights real, or merely synthetic/pass-by-construction?
- Do red-path tests fail loudly and for the right reason?
- Does the real-paper claim decomposition expose useful missing-evidence questions?
- Does the stack help answer "what source should we find next?" without bloating the canonical corpus?
- Is the current branch too coupled for merge, even if the experimental test passes?

Codex will proceed now in its own scratch folder and write a result report before asking for broader merge decisions.
