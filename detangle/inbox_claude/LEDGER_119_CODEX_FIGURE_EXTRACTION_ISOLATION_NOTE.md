# Codex -> Claude(Code): PDF figure extraction isolation note

Status: info

Target commit: `18ac8e7 docs: isolate pdf figure extraction artifacts`

Target files:

- `docs/handoffs/pdf_figure_extraction_isolation_note_2026-06-17.md`
- `docs/handoffs/multi_track_coordination_map_2026-06-17.md`

## Summary

After the operator noticed an obviously wrong figure appearing inside a corpus
Markdown render, I added a durable note requiring PDF extraction artifacts to be
grouped by paper/source id.

Core rule:

- one PDF extraction capsule per paper/source id;
- no assembler may read images or captions outside the current capsule;
- generated Markdown image paths must remain capsule-local;
- figure sidecars must carry source id/page/bbox/hash before being trusted;
- mismatched or escaping figure metadata fails closed;
- until a checker exists, figure-derived Markdown remains a blocked provenance
  channel such as `unverified_figure_markdown`.

This is a docs-only note, not a figure extractor implementation. It is separate
from `CORPUS_POLICY.md` because that file currently has unrelated dirty edits in
the operator/peer workspace.

## Relation to Draft Workspace

This reinforces the current decomposition behavior:

- `figure_metadata` cannot support licensed claims or required caveats;
- unverified figure-derived material should stay in
  `blocked_provenance_channels`.

No tests were run for this docs-only commit.
