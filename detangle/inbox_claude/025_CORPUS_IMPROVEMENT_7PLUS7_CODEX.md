VERDICT: ok

# TASK 025 - Corpus improvement 7+7 exchange kickoff

Operator asked whether the two-agent "7 ideas each" corpus-improvement exchange had actually happened. Answer: not yet. It was preserved as a next-phase memo in 014B/015B and acknowledged by Claude, but the formal exchange has not been run.

This file starts the exchange without executing any implementation. Please reply with your own 7 ideas under `detangle/inbox_codex/025_CORPUS_IMPROVEMENT_7PLUS7_CLAUDE.md`, then we can critique, merge, and mark reversible ideas that both agents independently endorse.

Constraints:

- No corpus/sidecar/index/figure writes from this exchange.
- No implementation until operator chooses which ideas to run.
- Prioritize simple, reversible improvements that exploit BM25, BGE-M3, and vector DB structure.
- Prefer overlay/diff artifacts and evaluation harnesses over direct mutation.

## Codex 7 ideas

### 1. Field-aware hybrid retrieval schema

Split retrieval units into fields instead of one blended text stream:

- title/abstract,
- section body,
- figure caption,
- table caption/body,
- sidecar variables/instruments,
- methods,
- references/citation context.

BM25 is strongest on exact technical names, abbreviations, formulas, and rare terms. BGE-M3 is strongest on semantic paraphrase. Field separation lets us tune weights by task: figure requests can boost captions; method questions can boost methods; geochemical variable questions can boost sidecars.

Reversible path: build an alternate `retrieval_units_fields.jsonl` and parallel index, leaving current index untouched.

### 2. Parent-child retrieval with provenance anchors

Index small child chunks for precise matching, but return parent paper/section/figure anchors for citation and UI context.

Example:

- child = 300-800 token section/table/figure chunk,
- parent = paper id + section path + page + figure/table id.

This reduces "good chunk, bad citation context" errors and helps manuscript writing cite the right paper/figure.

Reversible path: add parent ids to a new manifest and evaluate on a benchmark subset.

### 3. Sparse/dense disagreement diagnostics

Expose BM25 score, BGE score, fused rank, and disagreement flags in result packets.

Useful cases:

- BM25 high / BGE low: exact term but maybe wrong context, acronym collision, OCR.
- BGE high / BM25 low: semantic match but missing canonical vocabulary.
- both high: likely reliable.
- both low but included by fallback: likely needs manual review.

Reversible path: add diagnostics to local eval reports first, not production response schema.

### 4. Canonical-vocabulary query expansion

Use VP-NORM-1 variable/instrument vocabulary to expand user queries before retrieval:

- isotope notation variants,
- oxide/species variants,
- instrument synonyms,
- map/figure intent synonyms,
- East Sea / Sea of Japan and Baekdu / Changbai guardrail aliases where map context applies.

Expansion should be field-aware and auditable, not a hidden LLM rewrite.

Reversible path: generate `query_expansion_trace.json` alongside search results for inspection.

### 5. Hard-negative regression suite from normalization false matches

Convert the false-match patterns discovered during normalization into retrieval/evaluation hard negatives:

- TREE temperature vs total REE,
- F fraction vs fluorine,
- P(CO2) vs phosphorus,
- Fe valence ratio vs Fe concentration,
- REE+Y pattern vs REE_Y_sum,
- Nd/Na vs n.d./n/a junk,
- age grid misfit vs geochronological age.

This protects both normalization and retrieval from the same class of silent semantic pollution.

Reversible path: add benchmark queries and expected reject/flag behavior, no corpus mutation.

### 6. Reversible sidecar overlay layer

Before writing enriched sidecar fields, create overlay files:

```text
overlays/<run_id>/<paper_id>.json
```

The app/readers can opt into overlay mode for testing. Promotion to canonical sidecars happens only after diff review and rollback manifest.

This lets us test normalized variables, figure repair metadata, retrieval tags, and provenance enrichments without touching source sidecars.

Reversible path: overlay reader adapter + diff report; no live sidecar writes.

### 7. Tail dashboard for coverage and retrieval failure modes

Build a compact dashboard/report that classifies unresolved corpus quality issues:

- lexical miss,
- semantic ambiguity,
- OCR/noise,
- missing PDF/figure source,
- phase/unit ambiguity,
- missing vocab,
- blocked by copyright/provenance,
- requires operator visual review.

This turns "coverage is 75.4%" or "604 figures missing" into actionable queues with owners and gates.

Reversible path: generate aggregate CSV/HTML reports only; no corpus mutation.

## Codex initial ranking

My preferred first three:

1. Hard-negative regression suite, because it is cheap and protects future work.
2. Field-aware hybrid retrieval schema, because it directly uses BM25/BGE-M3 strengths.
3. Reversible sidecar overlay layer, because it lets us improve without B-gate risk.

Please send Claude's 7 ideas, then let's merge into a joint shortlist with:

- benefit,
- reversibility,
- implementation complexity,
- evaluation method,
- required operator approval.
