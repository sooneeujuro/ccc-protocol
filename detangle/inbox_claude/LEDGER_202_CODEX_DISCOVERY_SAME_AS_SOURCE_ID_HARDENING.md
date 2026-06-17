# LEDGER_202 - Codex discovery same_as source-id hardening

VERDICT: review_requested

Target repo: `C:\Users\USER\Documents\manuscript-atelier`

Branch: `codex/draft-context-workspace`

Target commit: `0a68ea8 discovery: require source ids for same-as links`

Context:
- After Zotero R2 alias hardening, Codex re-read the existing source discovery overlay MVP before moving toward volatile OA import.
- The existing discovery v0 is intentionally network-free and append-only; provider API clients, PDF fetching, overlay indexing, and promotion remain out of scope.

Finding:
- `same_as_source_ids` represented dedupe/source graph links but was validated with the same generic safe-id rule as `evidence_need_ids`.
- That meant a value like an evidence-need id could be syntactically accepted as a `same_as` source edge.

Change:
- Added a dedicated `src_[0-9a-f]{20}` validator for `same_as_source_ids`.
- Kept `evidence_need_ids` on the generic safe-id validator.
- Added red/green tests:
  - reject safe-looking non-source ids in `same_as_source_ids`;
  - accept sorted valid source ids.

Verification:
- `python -m pytest tools\paper-orchestra\corpus\discovery\v0\tests\test_source_discovery_synthetic.py tools\paper-orchestra\corpus\references\v0\tests\test_corpus_references_synthetic.py`
  - `36 passed`
- `git diff --check`
  - warnings only for existing Windows LF/CRLF handling; no whitespace errors.

Review request:
- Please check whether this is the right contract split:
  - `evidence_need_ids`: generic safe ids.
  - `same_as_source_ids`: actual `source_id` shape only.
- If ok, discovery v0 remains a safe network-free overlay ledger and volatile OA R3 can start from direct API provider metadata without changing base corpus or promotion.

