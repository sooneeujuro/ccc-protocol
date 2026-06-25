# BOOK_HOLDOUT_codex.md

author: Codex
date_kst: 2026-06-25
purpose: Facet-gold holdout plan for book sidecar v1, to instantiate after Claude segmentation dry-run emits segment ids.
status: draft_for_claude_round2_review

## Principle

The holdout should test the sidecar contract, not prose quality. Gold answers should be boolean/count/enum/list-of-id checks where possible.

Use 6-8 segments total. Each selected segment may cover multiple facets, but the set must cover:

- boundary
- topic_norm
- method_norm
- reference_kind
- locator
- false-value extraction

Keep dev and holdout separate. Do not tune prompt text against holdout failures until a new prompt version is declared.

## Selection Rules

Select segments only after the deterministic segmentation dry-run exists.

Required per candidate:

- stable `book_id`
- stable `segment_id`
- `segment_type`
- `segment_method`
- `segment_confidence`
- `page_range`
- `md_quality`
- visible locator candidates, if testing locator facets

Reject from holdout:

- `segment_confidence=low`, unless the explicit facet is boundary failure handling
- segments requiring domain judgment not visible from the segment text
- segments whose gold depends on exact numeric values
- segments where the expected answer requires copying protected table/equation content

## Proposed 8-Segment Holdout Mix

| slot | segment class | primary facet | secondary facets | expected gold shape |
|---|---|---|---|---|
| H1 | heading-derived textbook chapter/section | boundary | topic_norm, source_role | segment fields copied exactly; topic family id present or absent |
| H2 | radiogenic isotope/geochronology explanation | topic_norm | method_norm | isotope family id + geochronology topic id; no reference value extraction |
| H3 | stable isotope/fractionation explanation | topic_norm | false-value | fractionation topic id; no numeric value in summary/reference fields |
| H4 | method/instrumentation segment | method_norm | source_role | method id present; source_role=`method_background` |
| H5 | reference table dense segment | reference_kind | locator, false-value | reference_kind enum present; locator present; `value_extracted=false` |
| H6 | equation/derivation segment | reference_kind | locator, false-value | equation/thermodynamic relation locator present; equation text not extracted |
| H7 | solubility/property table segment | reference_kind | topic_norm, locator | solubility/property reference kind; locator present; no values |
| H8 | weak-heading or page-window segment | boundary | quarantine behavior | not production-eligible if low confidence; copied segment metadata exact |

If only 6 segments are available, drop H7 and H8. If 7 are available, keep H8 before H7 because boundary failure is the highest-blast-radius defect.

## Gold Sheet Schema

Create one JSON object per holdout segment:

```json
{
  "holdout_id": "H1",
  "book_id": "",
  "segment_id": "",
  "expected": {
    "copied_fields_exact": true,
    "allowed_segment_type": "",
    "allowed_segment_method": "",
    "allowed_segment_confidence": "",
    "content_type_any": [],
    "topics_norm_required": [],
    "topics_norm_forbidden": [],
    "methods_norm_required": [],
    "methods_norm_forbidden": [],
    "isotope_systems_norm_required": [],
    "reference_kind_required": [],
    "reference_kind_forbidden": [],
    "locator_required": true,
    "value_extracted_must_all_be_false": true,
    "numeric_value_string_count_must_be_zero": true,
    "summary_required": false,
    "production_allowed": true
  }
}
```

## Facet Metrics

Report these counts after running the holdout:

- `holdout_segment_count`
- `copied_field_mismatch_count`
- `invalid_json_count`
- `extra_key_count`
- `topic_norm_required_missing_count`
- `topic_norm_forbidden_present_count`
- `method_norm_required_missing_count`
- `method_norm_forbidden_present_count`
- `reference_kind_required_missing_count`
- `locator_required_missing_count`
- `value_extracted_true_count`
- `numeric_value_string_count`
- `low_confidence_production_count`

Pass rule for round2/round5:

- hard fail if copied-field mismatch > 0
- hard fail if value extraction count > 0
- hard fail if locator-required missing > 0 on H5/H6/H7
- hard fail if low-confidence production count > 0
- topic_norm and method_norm gold are semantic checks and should be soft-fail unless a later content-verified gold file explicitly promotes one to hard-fail
- soft fail if a normalized topic/method is missing but raw field captured the phrase
- pass only if all hard-fail counts are zero

## Candidate Source Families

Use source families, not fixed titles, until segmentation ids land:

- one broad textbook explanation segment
- one radiogenic isotope/geochronology segment
- one stable isotope/fractionation segment
- one methods/instrumentation segment
- one data-table/reference-heavy segment
- one equation/thermodynamic relation segment
- one solubility/property-reference segment
- one weak-boundary page-window or table-dense segment

This avoids overfitting the holdout to known book names while still covering the failure modes from `BOOK_SIDECAR_PLAN.md` v1.

## Review Hooks For Claude Segmentation Output

When Claude's segmentation dry-run arrives, Codex should verify:

- selected holdout ids exist exactly once
- selected segment confidence distribution includes at least one non-high boundary case
- selected segments cover at least four distinct `book_id`s if available
- selected segments do not require numeric gold values
- selected locator gold can be checked without copying table/equation content

Then freeze `BOOK_HOLDOUT_gold_v0.jsonl` under a new version before Gemma prompt tuning.
