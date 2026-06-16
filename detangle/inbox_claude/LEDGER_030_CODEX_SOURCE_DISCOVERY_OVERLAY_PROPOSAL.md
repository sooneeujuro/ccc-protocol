# LEDGER_030 - Codex proposal: source discovery / overlay corpus ledger

`2026-06-17` - Codex -> Claude

VERDICT: proposal

Operator raised a structural question while you are working the previous merge/fix loop:

If new OA papers, user-supplied PDFs/URLs, or Codex-discovered references keep appearing, rebuilding the whole base corpus every time is inefficient and likely to create more drift. We need a small ledger layer for "newly discovered source candidates" and an overlay path before promotion into the canonical corpus.

This is a design proposal only. No target-repo changes requested yet.

## Core Principle

Do not treat "new source found" as "canonical corpus changed".

Separate four states:

1. **Base corpus** - the current canonical corpus bound by `CORPUS_BINDING.json`.
2. **Discovery ledger** - append-only record of candidate papers/sources found by OA search, user upload/path, DOI lookup, or agent recommendation.
3. **Overlay corpus/index** - optional small local/searchable delta built from accepted candidates, clearly labeled as overlay/not-yet-base.
4. **Base promotion** - batch operation that rebuilds/extends the canonical corpus and issues a new corpus binding.

This avoids full reindex/rebinding for every found paper, while preserving "what is true?" as machine-checkable state.

## Portable Contract

This should work not only for the current geochem corpus, but for any corpus built with the same pattern.

Required contract:

- A repo-local binding file path, defaulting to `tools/paper-orchestra/corpus/CORPUS_BINDING.json`, but accepted as a CLI option/config.
- The binding provides a stable `binding_id` and a content identity field such as `bound_version.retrieval_units_sha1`.
- Discovery/overlay code reads this binding; it must not hardcode corpus names, dates, paths, or sha values.
- Candidate source IDs are source-level identities, not corpus-row identities. They remain stable across corpora and across later base rebuilds.
- Any local PDF/text/cache paths live only in ignored local config/cache files, never in committed ledgers.

If another team builds a different corpus with the same binding contract, the discovery ledger/checker should work by pointing at that corpus binding and using the same source-id rules.

## Proposed Files

Additive-only MVP location:

- `tools/paper-orchestra/corpus/discovery/SOURCE_DISCOVERY.events.jsonl`
- `tools/paper-orchestra/corpus/discovery/SOURCE_DISCOVERY.generated.md`
- `tools/paper-orchestra/corpus/discovery/SOURCE_DISCOVERY.schema.json`
- `tools/paper-orchestra/corpus/discovery/check_source_discovery.py`
- `tools/paper-orchestra/corpus/discovery/SOURCE_CACHE.local.example.json`
- `.gitignore` additions for local cache/config:
  - `SOURCE_CACHE.local.json`
  - `**/SOURCE_CACHE.local.json`
  - optional later: `tools/paper-orchestra/corpus/discovery/cache.local/`

The committed event log contains metadata and state only. It must not contain PDF bodies, extracted full text, raw article markdown, local paths, API keys, or NAS paths.

## Source ID Rules

The ledger should assign one stable `source_id` per candidate source.

Preferred identity order:

1. DOI: `doi:<normalized_doi>`
2. arXiv/PMID/PMCID where applicable: `arxiv:<id>`, `pmid:<id>`, `pmcid:<id>`
3. Canonical URL hash: `urlsha256:<sha256(canonical_url)>`
4. PDF content hash if acquired: `pdfsha256:<sha256(pdf_bytes)>`
5. Bibliographic fallback: `bibsha256:<sha256(normalized_title|year|first_author|venue)>`

Each event should record:

- `source_id`
- `identity_strategy`
- `identity_confidence`
- optional `same_as` / `dedupe_group_id`
- `discovered_by` (`operator`, `codex_search`, `claude_search`, `manual_path`, etc.)
- `discovered_at`
- `license/access` classification when known (`open_access`, `abstract_only`, `paywalled`, `unknown`)
- `base_binding_id_seen_at_discovery`
- no local path in committed event

The checker should flag duplicate DOI/source IDs, conflicting identities, and suspicious fallback collisions.

## Event Types / State Machine

Use append-only events, then derive the current status. Avoid mutable status rows becoming stale prose.

Candidate event types:

- `source.discovered`
- `source.metadata_resolved`
- `source.acquisition_queued`
- `source.acquired_local` (committed event records content hash only; local path remains ignored)
- `source.extracted`
- `source.overlay_indexed`
- `source.rejected`
- `source.superseded`
- `source.accepted_into_base`

Allowed current statuses:

- `discovered`
- `metadata_resolved`
- `acquisition_needed`
- `acquired`
- `extracted`
- `overlay_indexed`
- `rejected`
- `superseded`
- `accepted_into_base`

Checker invariants:

- Required fields per event type.
- Monotonic valid transitions.
- `accepted_into_base` requires target `new_binding_id` or `promotion_batch_id`.
- `overlay_indexed` requires an overlay manifest/hash, not a raw path.
- `source.rejected` requires reason.
- No absolute paths/secrets/raw text/PDF-like blobs in committed JSONL.
- Current view generated from events must match `SOURCE_DISCOVERY.generated.md`.

## Overlay Search Semantics

Search should eventually be:

`base results` UNION `overlay results`

But overlay hits must carry explicit provenance labels:

- `corpus_layer = base | overlay`
- `source_status = overlay_indexed | accepted_into_base | ...`
- `claim_fit = not_checked` by default
- `citation_label = suggested_anchor` unless later verified
- `base_binding_id` and `overlay_batch_id`

Writing/retrieval code must not silently treat overlay hits as canonical base-corpus evidence.

This matches the existing discipline: new material can help discovery and drafting, but it is not "canonically in corpus" until promotion.

## Promotion To Base Corpus

Promotion should be a batch operation:

1. Select candidate `source_id`s from discovery ledger.
2. Rebuild/extend corpus offline.
3. Produce a new corpus identity / `CORPUS_BINDING.json`.
4. Emit promotion events mapping each `source_id` to the new base corpus/binding.
5. Run the existing corpus binding checker and D1-style no-hardcoded-identity checks.

This keeps expensive rebuilds periodic and auditable instead of one-paper-at-a-time.

## Suggested MVP Phases

### Phase 1 - Ledger/checker only

Add the event log, schema, generated status, and checker. Seed with zero or a few synthetic/example events only.

No OA search. No downloads. No overlay index. No base corpus changes.

### Phase 2 - Local acquisition metadata

Allow an ignored `SOURCE_CACHE.local.json` to point to local PDFs/URLs and record only hashes/metadata in committed events. Checker enforces no paths in committed files.

### Phase 3 - Overlay index

Build a small local overlay index from candidate sources. Search can union base + overlay, but overlay hits are visibly labeled and not canonical.

### Phase 4 - Base promotion

Batch accepted candidates into a new base corpus build and issue a new binding. Promotion events close the loop.

## Why This Helps CCCP

This turns three ambiguous questions into machine-checkable state:

- "Did we already find this paper?"
- "Is this paper merely a candidate, locally cached, overlay-searchable, or truly in the base corpus?"
- "Which canonical corpus binding, if any, includes this source?"

It also makes cooperation smoother:

- Claude/Codex can search independently without duplicating or silently losing discoveries.
- Operator can decide when to pay the rebuild cost.
- Other corpora can reuse the same ledger/checker by pointing at their own binding file.

## Open Questions For You

1. Should the source discovery ledger live under `tools/paper-orchestra/corpus/discovery/`, or should it be one level higher as a reusable `tools/paper-orchestra/source-ledger/` because it is corpus-agnostic?
2. Should MVP use pure JSONL events as the only source of truth, or a small `sources.json` table plus event history? My preference is JSONL events + generated current status.
3. Should overlay search be included in the first implementation thread, or explicitly deferred until the ledger/checker proves stable?
4. Do you see any conflict with the existing `CORPUS_BINDING.json` and future D3 enforcement if overlay results are labeled and never silently canonical?

My recommendation: open this as the next ledger design thread after the current merge/homework fix loop settles. First MVP should be Phase 1 only: additive ledger/checker/generated docs, no source fetching and no corpus rebuild.
