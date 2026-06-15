VERDICT: ok

# TASK 002 - Codex guard verify verdict

Read-only verification completed against `detangle/scripts/precommit_corpus_guard.sh` and `detangle/GUARD_DEPLOY.md`. No changes were made to `geochemistry-analyzer`, `manuscript-atelier`, or `sooneeujuro-web`.

## 1. Hook true positives

Using the exact hook regex from `precommit_corpus_guard.sh` with Git grep, the required corpus/risk samples all matched: 13/13.

Matched samples:
- `docs/handoffs/fig_refill_20260613/out/example.jpg`
- `docs/handoffs/fig_refill_20260613/out_raw/paper.md`
- `wiki/papers/Fischer_and_Chiodini.md`
- `wiki/data/table.json`
- `tools/geochem-stats/corpus/records.jsonl`
- `tools/geochem-stats/corpus/note.md`
- `tools/geochem-stats/sidecars/foo.json`
- `tools/paper-orchestra/corpus/index/embeddings.npy`
- `tools/paper-orchestra/corpus/index/cache.pkl`
- `tools/paper-orchestra/corpus/index/retrieval_units.jsonl`
- `index/root.npy`
- `foo.bak.20260518_120000`
- `judge.report.json`

Conclusion: the guard catches the requested `out*`, `wiki`, `sidecar`, `*.npy`/`*.pkl`, backup, and report-json families.

## 2. Hook false positives

Allowed-path checks were run through the same hook regex.

- `geochemistry-analyzer`: no hook hits for `tools/geochem-stats/index/variable-vocabulary.json`; the file is tracked in the live tree (`100644`, blob `6cc5965...`) and exists at 19,015 bytes. Generic public image samples such as `public/**/*.jpg|png` also do not match the hook pattern.
- `sooneeujuro-web`: no hook hits for tracked fixture/public image assets found in this checkout, including `tests/fixtures/classification/tas_lebas_1986_reference.png` and ternary reference PNGs.
- `manuscript-atelier`: no hook hits for normal docs and sample packet candidates such as `docs/README.md`, `docs/checklists/*.md`, `docs/design/*.md`, `docs/guardrails/*.md`, and top-level `docs/handoffs/*.md`.

Conclusion: no false-positive blocker found for the explicitly protected normal assets.

## 3. Gitignore deployment review

`GUARD_DEPLOY.md` is directionally correct:

- `manuscript-atelier` proposed ignore covers `docs/handoffs/**/out/`, `out_raw/`, handoff JPG/JPEG, and index backup/report leftovers. Current tracked handoff-risk count from the checked-out repo was 0.
- `geochemistry-analyzer` proposed ignore covers `wiki/papers/`, `wiki/data/`, `tools/geochem-stats/corpus/`, and `paper1-CIR-volatiles/`.
- `geochemistry-analyzer` explicitly preserves `!tools/geochem-stats/index/variable-vocabulary.json`, matching `FUNCTIONALITY_GUARDRAILS.md` requirement that the live tree file must remain available for static import.
- The warning that ignore-only is insufficient for already tracked geochem corpus is correct: current tracked dangerous path count is 663 under the guarded geochem families.

Conclusion: the deploy document blocks dangerous growth while preserving the known build dependency.

## Advisory, not blocking

- `P0_LANDMINE_GUARD.md` includes `docs/handoffs/**/*.png`, but `GUARD_DEPLOY.md` currently lists JPG/JPEG only. The hook still blocks PNGs inside `out/` and `out_raw/` through the directory rule. If all handoff scratch PNGs outside `out*` should also be forbidden, mirror the P0 PNG line into `GUARD_DEPLOY.md`.
- The hook catches nested `*/corpus/*.jsonl` through `/corpus/`, which matches the known target paths. If a repo may have a root-level `corpus/` directory, consider changing that branch to `(^|/)corpus/`.
