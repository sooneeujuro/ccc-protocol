# LEDGER_043_CODEX_LEGACY_QUARANTINE_BUILT

VERDICT: ok

Codex created a review-only legacy quarantine in manuscript-atelier:

- Target branch: `codex/draft-context-workspace`
- Target commit: `0966356 docs: quarantine legacy repo review assets`
- Location: `docs/legacy_imports/from_old_repos/`

Scope:

- Imported selected text/code review assets from local legacy repos:
  - `geochemistry-analyzer`
  - `PaperOrchestra_CIR_2nd`
- Added local inventory:
  - `docs/legacy_imports/from_old_repos/README.md`
  - `docs/legacy_imports/from_old_repos/REVIEW_QUEUE.md`

Important quarantine rules:

- Do not execute code from this directory directly.
- Do not wire files into active `tools/paper-orchestra` by moving them wholesale.
- Treat hardcoded paths, NAS references, env var names, branch names, and old policy locks as stale review signals.
- Rewrite useful pieces into active locations with tests/checks.

Included:

- legacy Paper Orchestra command prompts
- legacy Dr.Kim / Prof.Park / Passerby agent drafts
- CIR2 Defender / two-round workflow notes
- Shirai-method notes
- old harness rules and migration docs
- `tools/geochem-stats` stats-engine prototype material
- legacy Librarian MCP design/code

Excluded intentionally:

- PDFs
- DOCX manuscripts
- XLS/XLSX data
- PNG/JPG/TIFF figure outputs
- `wiki/papers/**`
- `.claude/worktrees/**`
- old project data/manuscript folders

Codex checks:

- `git diff --check -- docs/legacy_imports/from_old_repos` passed.
- Binary/raw manuscript/data/figure extension scan found 0 files.
- Hardcoded local/NAS/env references do exist in legacy docs; this is expected and documented as a review hazard, not an active runtime import.

Suggested review order:

1. `CLAUDE_harness_rules.md` numeric discipline / intro leak / reviewer calibration.
2. `PaperOrchestra_CIR_2nd/.claude/agents/` Dr.Kim / Prof.Park / Passerby.
3. `PaperOrchestra_CIR_2nd/CLAUDE.md` Defender accept/rebut/defer and two-round cap.
4. `SHIRAI-METHOD.md` topic-sentence / abstract-backchain rules.
5. `tools/geochem-stats/` for stats-engine salvage.
6. legacy Librarian MCP only as historical design input.

No live infra changes, DB writes, deployments, corpus rebuilds, or active target-runtime wiring were performed.
