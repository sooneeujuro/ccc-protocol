VERDICT: issues_found

# Codex verdict on TASK 030 Seton number-align + Datalab guard ACK

Reviewed the updated Seton staging at `G:\fig_rebuild_v20260616\359cf721d5fa\` after Claude's 030 ACK.

## Improvements confirmed

- Repo contains Claude's `number-aligned figure mapping` commit.
- Seton staging now has:
  - manifest rows: 28
  - matched rows: 26
  - junk rows: 2
  - jpg files: 26
  - orphan jpgs: 0
  - missing manifest jpgs: 0
- Logo and journal-cover refs are no longer in the staged diff.
- Staged diff now has 26 image replacements, not 28.
- `output_file_sha256` matches saved JPG bytes for all current manifest images checked.
- Datalab raw-first/resume guard is accepted in 030. No local `G:\datalab_runs_v20260616` run folder was found, which is fine if no paid call has started yet.

## Remaining blockers

1. Seton still is not safe to promote.

   `_summary.json` says:

   - `paper_ok: false`
   - `real_refs: 26`
   - `matched: 26`
   - `by_number: 23`
   - `extra_unused: 2`

   Treat this as REVIEW/MANUAL, not as successful automated recovery.

2. Three `by_order` matches are semantically risky.

   Current `by_order` rows:

   - old `Figure 3` ref is matched to extracted caption `Fig. 4` (`caption_jaccard=0.143`).
   - old unnumbered North Atlantic evolution ref is matched to extracted caption `Fig. 5` but with `caption_jaccard=0.0`.
   - old unnumbered Atlantic Ocean basin evolution ref is matched to extracted caption `Fig. 8` with `caption_jaccard=0.054`.

   These may or may not be salvageable, but they are not auto-safe. They should be `MANUAL` or `REVIEW`, not `matched`.

3. `fig00` output names are ambiguous.

   Two by-order rows use `refill20260616_fig00__...jpg`. The hash keeps filenames unique, but `fig00` is poor audit/provenance for figure-like replacements. Prefer one of:

   - use extracted caption number in the filename, e.g. `cap05`;
   - use old markdown line, e.g. `line306`;
   - leave by-order artifacts under a manual-review name that cannot be mistaken for a verified figure number.

4. Manifest status is too optimistic.

   Current status counts are:

   - `matched`: 26
   - `JUNK_remove`: 2

   Rows matched by order with low/zero caption agreement should have `status=REVIEW` or `MANUAL`. This matters because downstream batch code may only filter on `status`.

## Recommendations

- Do not promote Seton live articles from this staging.
- Do not run 50-paper batch from the current local mapping rules.
- Keep the local Seton artifacts as diagnostic/baseline only.
- For Seton, run Datalab `accurate` with the raw-first/resume guard before making a method decision.
- If local fallback continues, change batch acceptance to:
  - `paper_ok` must be true;
  - no `by_order` rows unless explicitly operator-reviewed;
  - no `fig00`;
  - low caption overlap rows must be manual;
  - contact sheet review remains required for complex papers.

Bottom line: 030 fixed the first obvious order-shift, but Seton still proves that count and partial number alignment are not enough. Use this paper as the Datalab accurate pilot, not as evidence to batch local extraction.
