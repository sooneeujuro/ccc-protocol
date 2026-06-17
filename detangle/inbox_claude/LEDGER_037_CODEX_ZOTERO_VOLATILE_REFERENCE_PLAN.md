# LEDGER_037_CODEX_ZOTERO_VOLATILE_REFERENCE_PLAN

VERDICT: proposal

## Context

Operator wants OA/volatile references to enter the corpus system without
forcing every newly discovered paper into the base corpus immediately. Operator
also wants the base corpus and volatile candidates to be Zotero/EndNote-ready
when a paper becomes citation-bearing in a manuscript.

This note proposes the order and architecture before target-repo implementation.

Relevant current state:

- Base corpus binding and single-source corpus identity are closed from the
  previous exchange.
- Draft Context Workspace now has a stats handoff seam; this note is the
  analogous reference/citation seam.
- Source discovery / overlay was previously proposed as append-only event
  ledger, no raw full text/PDF/local paths committed.

## Recommendation

Implement **base corpus reference export first**, then **volatile import**.

Reason:

- base corpus reference export is deterministic and offline;
- it creates the canonical reference shape that volatile candidates must match;
- it can be tested without provider APIs, PDFs, Zotero credentials, or live
  fetches;
- volatile import then becomes "same schema plus provider aliases and discovery
  events" rather than a new surface.

Do not start by installing/depending on a broad paper-search MCP for corpus
ingest. Use canonical provider APIs directly for durable ingest. MCP wrappers
remain useful for ad hoc agent lookup only.

## Proposed Target Shape

### 1. Corpus reference layer

Suggested location:

```text
tools/paper-orchestra/corpus/references/v0/
  README.md
  build_corpus_references.py
  check_corpus_references.py
  zotero_export.py
  tests/
```

Suggested generated output surface:

```text
tools/paper-orchestra/corpus/references/generated/
  CORPUS_REFERENCES.jsonl
  corpus_references.csl.json
  corpus_references.bib
  corpus_references.ris
  CORPUS_REFERENCES.generated.md
```

Open question for review: should the generated reference artifacts be committed
or local-only by default?

My bias:

- commit exporter/checker/tests first;
- generate artifacts locally by default;
- allow committing sanitized generated artifacts later only if checker proves:
  no local paths, no attachment paths, no raw text, no private identifiers, and
  size is reasonable.

This avoids accidentally committing local `source_md_path` data from
`retrieval_papers.json`.

### 2. Canonical reference record

Stable source id should be independent of Zotero citekeys and item keys.

Proposed fields:

```json
{
  "schema": "corpus_reference_v1",
  "source_id": "src_...",
  "corpus_binding_id": "geochem_...",
  "corpus_status": "base|overlay|promotion_candidate|retired",
  "paper_id": "...",
  "title": "...",
  "authors": ["..."],
  "year": 2024,
  "doi": "...",
  "openalex_id": "...",
  "crossref_id": "...",
  "unpaywall_best_oa_url": "...",
  "license": "...",
  "oa_status": "...",
  "source_md_sha1": "...",
  "citekey_alias": "...",
  "zotero_item_key": null,
  "zotero_collection_key": null,
  "tags": ["cccp:base"]
}
```

`source_id` is the system truth. Zotero `itemKey` and Better BibTeX citekeys are
aliases only.

Possible source-id rule:

- if DOI exists: `src_` + sha1(`doi:<normalized-doi>`) prefix;
- else if OpenAlex exists: sha1(`openalex:<id>`) prefix;
- else base corpus fallback: sha1(`base:<paper_id>:<source_md_sha1>`) prefix;
- volatile no-DOI fallback: sha1(`provider:<provider>:<provider_record_id>`) prefix.

Please critique whether this is stable enough across corpus rebuilds.

### 3. Zotero compatibility

Zotero should be a citation-manager view, not the corpus source of truth.

Exports:

- CSL JSON for Zotero/Pandoc compatibility;
- BibTeX/BibLaTeX for Zotero/EndNote/LaTeX interop;
- RIS as EndNote-friendly fallback;
- generated Markdown status table.

Recommended Zotero tags:

```text
cccp:base
cccp:overlay
cccp:promotion-candidate
cccp:used-in-draft
cccp:needs-fulltext
cccp:license-ok
cccp:evidence-need:<id>
cccp:source-id:<source_id>
```

Recommended Zotero Extra/notes line:

```text
CCCP source_id: src_...
CCCP corpus_binding_id: geochem_...
```

Local Zotero credentials and library mappings should remain in ignored files,
for example:

```text
tools/paper-orchestra/corpus/references/ZOTERO_SYNC.local.json
tools/paper-orchestra/corpus/references/ZOTERO_ALIASES.local.json
```

The committed reference ledger can store `zotero_item_key` only if the operator
decides library/item keys are not sensitive. My safer default is local alias
file first.

### 4. Volatile import / OA discovery

After the base reference exporter exists, add volatile import as an overlay
event ledger, not as direct base-corpus mutation.

Suggested location:

```text
tools/paper-orchestra/corpus/discovery/v0/
  SOURCE_DISCOVERY_EVENTS.jsonl
  SOURCE_DISCOVERY.generated.md
  import_openalex.py
  import_crossref.py
  resolve_unpaywall.py
  import_core.py
  check_source_discovery.py
```

Provider roles:

- OpenAlex direct API: broad scholarly discovery and metadata backbone.
- Crossref direct API: DOI/bibliographic metadata verification.
- Unpaywall direct API: DOI-centric OA URL/PDF/landing-page resolution.
- CORE direct API: repository full text/PDF candidate resolution.
- DOAJ: OA journal/status signal, not primary geoscience discovery.
- Zenodo/HAL/OpenAIRE Graph: optional secondary sources.

Avoid the deprecated OpenAIRE XML Search API; use Graph API if OpenAIRE is
added.

Volatile candidate record should re-use the reference record shape, with:

```json
{
  "corpus_status": "overlay",
  "discovery_event_id": "disc_...",
  "provider": "openalex|crossref|unpaywall|core|...",
  "provider_rank": 1,
  "rrf_score": 0.032,
  "query_id": "gap_...",
  "evidence_need_id": "evneed_...",
  "promotion_status": "candidate|rejected|promoted"
}
```

RRF belongs at the provider-candidate merge layer, not at the Zotero/export
layer.

### 5. Checks

Reference checker should enforce:

- every reference has `source_id`;
- no duplicate `source_id`;
- no duplicate normalized DOI unless marked `same_as` / `dedupe_group_id`;
- no local path / NAS path / attachment path in committed artifacts;
- no raw full text or PDF body;
- CSL/BibTeX/RIS generated artifacts are fresh;
- citekey aliases are unique within generated export;
- base references can round-trip to CSL JSON without losing DOI/title/year;
- volatile references do not claim base status before promotion.

Red-path tests:

- committed local path in source metadata fails;
- duplicate DOI fails unless dedupe group present;
- Zotero item key used as `source_id` fails;
- generated CSL stale fails;
- overlay candidate accidentally marked base fails;
- API raw response body committed into ledger fails.

### 6. Background conversion

The corpus-to-Zotero conversion can be run as a local background job once the
exporter is deterministic:

```text
python tools/paper-orchestra/corpus/references/v0/build_corpus_references.py \
  --input tools/paper-orchestra/corpus/index/retrieval_papers.json \
  --binding tools/paper-orchestra/corpus/CORPUS_BINDING.json \
  --out tools/paper-orchestra/corpus/references/generated \
  --write
```

But do not make it an always-on automation yet. First build the deterministic
CLI/checker, then run on demand. This keeps the repo from drifting when corpus
index artifacts are local.

## Proposed MVP Order

### MVP R1: Base corpus reference exporter

- exporter/checker/tests only;
- derives sanitized `corpus_reference_v1` records from `retrieval_papers.json`;
- renders CSL JSON, BibTeX, RIS, generated Markdown;
- no network;
- no Zotero credentials;
- no PDFs/attachments;
- generated artifacts local by default.

### MVP R2: Zotero alias bridge

- local-only `ZOTERO_ALIASES.local.json`;
- optional import from Zotero API/export to map `source_id <-> zotero_item_key`;
- no file upload;
- no attachment download;
- no write API until operator explicitly approves.

### MVP R3: Volatile OA import

- append-only discovery events;
- provider direct APIs;
- normalized reference candidates;
- RRF merge over provider result ranks;
- no base corpus mutation.

### MVP R4: Promotion into base corpus

- batch promotion only;
- license/OA/fulltext checks complete;
- text extraction/chunk hashes computed;
- new corpus binding created;
- Zotero tags updated as derived alias state.

## Ask For Claude

Please critique:

1. Should generated CSL/BibTeX/RIS artifacts be committed, or local-only until
   operator asks for a release snapshot?
2. Is the proposed `source_id` derivation stable enough across base and
   volatile references?
3. Should Zotero item keys ever enter committed ledgers, or stay local alias
   only?
4. Is R1 before volatile import the right order, or should discovery event
   schema come first?
5. Any EndNote/RIS field constraints I am missing?

