# LEDGER_203 - Codex volatile provider import adapter

VERDICT: review_requested

Target repo: `C:\Users\USER\Documents\manuscript-atelier`

Branch: `codex/draft-context-workspace`

Target commit: `925f36a discovery: add provider result import adapter`

Scope:
- Added the first volatile OA import building block.
- This is not a live API client.
- It does not call OpenAlex, Crossref, Unpaywall, CORE, or any network.
- It does not fetch PDFs, read full text, write vector indexes, touch Zotero, or promote into base corpus.

What it does:
- Adds `tools/paper-orchestra/corpus/discovery/v0/provider_import.py`.
- Consumes already scrubbed provider metadata rows with schema `provider_discovery_result_v1`.
- Normalizes DOI/OpenAlex/provider identifiers using shared `source_identity_v1`.
- Emits `source_discovery_event_v1` events that pass `source_discovery.validate_event`.
- Computes an in-memory RRF merge summary by `source_id` so provider overlap can be measured before any overlay upsert.
- Keeps raw provider responses, abstracts, URLs, PDFs, full text, attachments, local paths, and secrets outside this layer.

Notable behavior:
- OpenAlex URL-shaped IDs are normalized to short OpenAlex IDs before event emission.
- Crossref DOI provider IDs are converted to safe provider record IDs while `source_id` still derives from normalized DOI.
- Duplicate DOI results from different providers collapse to the same `source_id` in RRF.
- CLI prints counts only; it does not print titles or provider candidate contents.

Tests added:
- OpenAlex URL id normalization without URL leakage.
- Crossref DOI record-id safe fallback while preserving DOI identity.
- Discovery-event round-trip validation.
- RRF merge across OpenAlex/Crossref duplicate DOI.
- Rejection of forbidden `abstract` key.
- Rejection of URL/path-shaped titles.
- Status markdown count/hash only; no title leakage.
- CLI writes event JSONL and prints counts only.
- AST check: no network/provider/subprocess imports.

Verification:
- `python -m pytest tools\paper-orchestra\corpus\discovery\v0\tests\test_provider_import_synthetic.py tools\paper-orchestra\corpus\discovery\v0\tests\test_source_discovery_synthetic.py tools\paper-orchestra\corpus\references\v0\tests\test_corpus_references_synthetic.py`
  - `45 passed`
- `python -m py_compile tools\paper-orchestra\corpus\discovery\v0\provider_import.py`
  - passed

Review request:
- Please check whether this is the right R3 boundary:
  - direct API clients can later produce scrubbed `provider_discovery_result_v1` rows;
  - this adapter handles identity/RRF/event emission;
  - the base corpus and overlay index remain untouched;
  - provider raw responses never become committed artifacts.

