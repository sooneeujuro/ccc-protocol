VERDICT: issues_found

# Codex verdict on TASK 025 WS2 manifest

Reviewed `G:\corpus_refs_v20260616\MANIFEST.csv` and `_consolidate_log.txt` against the agreed WS2/B-prime guardrails.

## Independent checks

- Repo branch was current with `origin/coop/detangle-20260615`; `detangle/STOP.md` absent.
- Manifest rows: 2,062 total.
- Kind counts: 2,014 `pdf`, 48 `supp`.
- Destination files: all 2,062 exist under `G:\corpus_refs_v20260616\`.
- Destination SHA-256: recomputed for all 2,062 files; 0 mismatches.
- Destination size: 0 mismatches.
- Duplicate manifest keys: 0 duplicate `sha256`, 0 duplicate `dest`.
- `dup_count` vs `sources` count: 0 mismatches after trimming source whitespace.
- Source paths: all 2,266 source path entries exist after trimming source whitespace.
- Source roots after trimming: `G:` 1,181, `D:` 1,003, `C:` 82, matching the stated scan sources.

## What passes

WS2 Stage 1 raw consolidation passes as a non-destructive SHA-256 deduplicated copy vault:

- SHA-256 dedup appears sound.
- Destination naming is collision-resistant via the 12-hex SHA prefix.
- Duplicate provenance is preserved in `sources`.
- The copied destination payloads match the manifest hashes.
- No corpus/PDF files were staged for git.

## Issues before accepting WS2 as final

1. The manifest is not yet the agreed corpus-linked WS2 artifact.
   Current columns are only `sha256, kind, size_bytes, dest, dup_count, sources`. There is no corpus `pid`, DOI/title-author-year match key, match tier, confidence, or unmatched reason. This is acceptable for a raw vault, but not enough to verify "corpus papers paired with reference PDFs" or figure rebuild coverage.

2. Supplementary provenance is not yet paper-linked.
   The 48 supplementary files are in one flat `supplementary/` area without `matched_pid`, match evidence, or `_unmatched` separation. Treat this as raw collection only until v2 matching exists.

3. `sources` values need string hygiene.
   The delimiter currently leaves outer spaces on duplicate-source entries (362 source strings had leading/trailing whitespace). A robust parser can trim them, but the manifest should either write `|` without outer whitespace or define that consumers must trim source tokens.

4. "Original unchanged" is plausible but not fully evidenced by the manifest alone.
   The destination hashes and existing source paths support copy-only behavior. For future audit-grade runs, include source `size`, `mtime`, and optionally source SHA in the manifest/log so no-mutation can be checked without relying on directory counts.

## Recommendation

Proceed to WS1/WS3 only if Claude labels this as `WS2 Stage 1 raw vault: PASS_WITH_ISSUES`, not final WS2. Before batch figure rebuild, add either `MANIFEST_MATCHED.csv` or v2 columns with:

- `matched_pid`
- DOI/title-author-year evidence
- `match_tier`
- `match_confidence`
- `match_status` / `unmatched_reason`
- supplementary `matched_pid` or `_unmatched` status

No objection to continuing the pipeline, as long as the missing matching layer remains an explicit open task.
