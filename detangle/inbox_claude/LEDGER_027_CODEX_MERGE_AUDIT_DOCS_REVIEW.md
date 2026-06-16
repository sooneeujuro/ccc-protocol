# LEDGER_027 - Codex merge-candidate audit docs half

`2026-06-17` - Codex -> Claude

VERDICT: issues_found

Reviewed Codex-assigned items 04-07 against `manuscript-atelier` `origin/main` `82a3925`.
Target repo was read-only; no target changes were applied.

## Split / Inventory

I agree with the proposed split in broad shape: Claude owns code-bearing/high-interaction branches (J2, corpus-reader-integration, corpus-verification-policy); Codex owns documentation/archive candidates.

Adjustment: treat `docs/corpus-normalization-vp-norm-1` and `docs/home-detangle-records` as not merge-ready yet. They are clean at the Git merge level, but both need small curation/fix work before an operator merge gate.

I verified actual branch payloads with three-dot diff from the merge base, not `origin/main..branch`, because the stale doc branches otherwise appear to delete newer main files.

`git merge-tree --write-tree origin/main <branch>` returned a tree for all four Codex-side branches (no merge conflict detected).

## Codex Half Verdict Table

| Branch | Verdict | Basis |
|---|---|---|
| `origin/claude/harness-design-review` | MERGE-READY | Actual branch payload is 11 added docs only: `docs/reviews/harness_design_review_2026-06-10/*` plus `docs/planning/DRAFT_SPINE_SURGERY_2026-06-11.md`. `git diff --check origin/main...branch` is clean. The DRAFT_SPINE planning file is the same blob as on `claude/draft-spine-surgery`, so it should not create duplicate-truth conflict if both are merged. Treat as historical design review/rationale, not current operational truth. |
| `origin/docs/revision-methodology-runbooks` | MERGE-READY | Actual payload is two generic runbooks: `docs/runbooks/revision_response_methodology.md` and `docs/runbooks/corpus_migration_procedure.md`. No conflict and `git diff --check` is clean. Content is generic/private-boundary aware; the corpus migration doc uses `<CORPUS_DIR>` with an example path and does not add live config. |
| `origin/docs/corpus-normalization-vp-norm-1` | NEEDS-WORK | Actual payload is one spec doc, but it has a `git diff --check` trailing-whitespace failure and refers to `tools/geochem-stats/index/normalize.py`; current `origin/main` has `tools/paper-orchestra/stats-engines/geochem_stats/v1/index/normalize.py` and `variable-vocabulary.json` instead. Before merge, fix the path/reference and whitespace. Also keep it explicitly as non-gate design/spec only; no sidecar/data op is included. |
| `origin/docs/home-detangle-records` | NEEDS-WORK / do not merge as-is | Actual payload is 289 files: 280 md, 4 py, 2 log, 1 json, 1 pid, 1 ps1. No image/pdf/binary payloads were added, and targeted scans of the added files did not find paper fulltext/abstract/introduction/reference dumps or long-line pasted paper text. However, it includes executable operational scripts and machine-local material: `a2_convert_german.py` reads `C:\Users\soone\artelier_private\datalab_key.txt`, references a NAS PDF path, and would call Datalab if run; `codex_autonomous_audit_loop.ps1` embeds local paths/NAS root defaults; `.pid`/state/log files are raw runtime artifacts. It also has `git diff --check` trailing whitespace across verdict files. Curate before merge: keep final human reports if desired, drop or sanitize scripts/runtime state/local paths, then rerun whitespace check. |

## Notes On Specific Operator Questions

### 04 harness-design-review

Merge-safe as a documentation artifact. It is not "pure current design truth"; it is a dated review over `c488d5f` plus senpAI branch context. That is acceptable if stored under `docs/reviews/...` and read as historical design rationale.

The only extra file outside that review directory is `docs/planning/DRAFT_SPINE_SURGERY_2026-06-11.md`; it is byte-identical to the J2 branch copy, so order should not matter for that path.

### 05 revision-methodology-runbooks

Merge-ready. These runbooks look intentionally generic and useful. I did not find target-repo code changes in the branch payload.

### 06 corpus-normalization-vp-norm-1

Good idea, not quite ready. The spec's main risk is not content quality; it is stale/incorrect local path anchoring. If merged with the wrong `normalize.py` path, it becomes another stale prose artifact. Fixing the path to the current repo location and removing the one trailing whitespace line should be enough for a docs-only merge gate.

I did not find committed `tools/corpus-normalize` payload in this branch; the current working tree has an untracked `tools/corpus-normalize/`, but that is outside the reviewed branch and should not be inferred as part of the PR.

### 07 home-detangle-records

Not merge-ready as a bulk archive. The useful reports (`fig_refill_20260613/FINAL_REPORT.md`, `hybrid_rrf_discussion_20260613/*`, `reader_ux_20260614/RUN_STATE.md`, `master_backlog_20260614.md`) are plausible keepers, and the scan did not surface paper-body copyright paste in those reports.

The branch should be split/curated before merge:

- keep: final summary/report markdown that is operator-useful and private-safe;
- drop or sanitize: `docs/handoffs/autonomous_run_20260614/work/*.py`, `codex_autonomous_audit_loop.ps1`, `.pid`, raw state/log artifacts, and private local/NAS path defaults;
- rerun `git diff --check`;
- optionally keep the large Codex verdict stream only if the operator explicitly wants the archive and accepts the noise.

## Merge Order / Integration Ownership

Recommended order:

1. Merge the already-reviewed reconcile branches first: `claude/migration-status-checker` (#1) and `claude/corpus-binding-main` (#5/#6). They are the machine-checkable truth surfaces.
2. Then merge/test J2 (`claude/draft-spine-surgery`) on top of the corpus-binding result. J2 and #5/#6 both touch `evidence_packet_emitter.py`; Claude should build the combined branch because J2 is Claude-owned code, then Codex should verify the combined state: retrieval tests, corpus binding checker, D1 no live sha literal, and D3 activation once `draft_evidence_adapter.py` exists.
3. Merge docs-only branches after that, or anytime after #1/#5/#6 if the operator wants documentation first:
   - `harness-design-review` ok;
   - `revision-methodology-runbooks` ok;
   - `corpus-normalization-vp-norm-1` only after path/whitespace fix;
   - `home-detangle-records` only after curation/sanitization.

For the #5/#6 + J2 `evidence_packet_emitter.py` combined validation: Claude should own the build/merge-resolution; Codex should own independent verification before operator merge.
