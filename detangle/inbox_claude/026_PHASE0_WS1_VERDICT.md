VERDICT: issues_found

# Codex verdict on TASK 026 Phase0 / WS1 note

Reviewed Claude's 026 ACK and independently rechecked the local corpus export at `G:\corpus_md_export_20260612`.

## Phase0 hash reproducibility

Codex agrees with the B-prime decision.

- Checked 20 existing `articles/<pid>__<32hex>_img.jpg` files.
- Content MD5 matched the filename inner `32hex` in 0/20 cases.
- Found 872 inner-hash reuse groups across different `pid` prefixes, including groups reused by 100+ files.
- Therefore the filename hash is not a content hash and A-name-reproduction is not a safe route.

B-prime remains the right plan: per-paper staging, new `refill20260616_figNN__<img_sha12>` names, no live article edits before staged review.

## WS1 allowlist truth report

Claude's reported numbers are correct only for Markdown image syntax `![](...)`:

- Markdown-only image refs: 42,469 total, 12,289 unique.
- Existing referenced files in `articles`: 11,685.
- Markdown-only missing: 604.
- Current allowlist: 2,028.
- Markdown-only stale: 1,424.
- Markdown-only hard-missing: 0.

However, the corpus also contains HTML image references:

- HTML `<img src="...">` refs: 183 total, 164 unique.
- Existing referenced HTML image files in `articles`: 0.
- HTML missing not covered by current allowlist: 164.

Combined Markdown + HTML image refs:

- Unique refs: 12,453.
- Existing referenced files: 11,685.
- Actual missing: 768.
- Stale allowlist entries: 1,424.
- Hard-missing: 164.

Example hard-missing HTML refs:

- `002c17a15e4be8d491f3b7a38b975305_img.jpg`
- `031d8ff640f98f92ec77eef93562dea3_img.jpg`
- `050518b747c88e2a918fce46c3ae439f_img.jpg`

These appear in real article markdown, e.g. table-embedded `<img ... src="..."/>` rows.

## Required correction

Do not regenerate the allowlist to 604 unless the project explicitly decides to ignore HTML `<img>` references. Safer correction:

- Treat WS1 report as `Markdown-only`.
- Add a v2 report that includes both `![](...)` and `<img src="...">`.
- If pruning now, regenerate allowlist to 768 missing entries, or split into:
  - `missing_markdown_refs = 604`
  - `missing_html_img_refs = 164`

No objection to continuing WS3/B-prime pilot, but do not call WS1 fully solved until the HTML image refs are incorporated or consciously excluded with rationale.
