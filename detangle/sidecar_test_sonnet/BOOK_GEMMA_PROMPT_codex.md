# BOOK_GEMMA_PROMPT_codex.md

author: Codex
date_kst: 2026-06-25
purpose: Draft local-Gemma prompt for `book_sidecar_chapter_v0` extraction after deterministic segmentation.
status: draft_for_claude_round2_review

## Contract Summary

- model_mode: local Gemma only
- think: false
- input_unit: one deterministic book segment, not a whole book
- output_format: strict JSON object only
- value_extraction: forbidden
- long_segment_policy: chunk_then_merge, never truncate tail content silently
- segment_fields_source: input manifest/segmenter only
- model_task: fill high-value descriptive facets without inventing locators, values, or schema fields

## Required Inputs

The runner should pass these fields outside the prose body and require the model to copy them exactly:

```json
{
  "schema": "book_sidecar_chapter_v0",
  "prompt_version": "book_gemma_prompt_codex_v0",
  "normalizer_version": "book_norm_vocab_codex_v0",
  "book_id": "...",
  "book_manifest_id": "...",
  "segment_id": "...",
  "segment_type": "chapter|section|reference_table_group|equation_block|page_window",
  "segment_method": "toc|heading|pattern|table_dense|fixed_window",
  "segment_confidence": "high|medium|low",
  "page_range": "...",
  "md_quality": "ok|heading_weak|table_weak|ocr_suspect|page_markers_only",
  "allowed_norm_ids": {
    "topic_norm": [],
    "method_norm": [],
    "isotope_system_norm": [],
    "reference_kind": []
  },
  "segment_text": "..."
}
```

Runner-side preflight:

- Reject missing `segment_id`, `book_id`, `page_range`, `segment_type`, `segment_method`, or `segment_confidence`.
- Do not send `segment_confidence=low` to production extraction; route to review or dry-run only.
- If `segment_text` exceeds the safe context budget, split into ordered subchunks with the same deterministic segment fields plus `chunk_index`, then merge by set-union and locator de-duplication.

## Prompt Draft

```text
You are extracting a metadata sidecar for a geochemistry book segment.

Return JSON only. Do not include markdown, commentary, explanations, or hidden reasoning.
think: false

Hard rules:
1. Copy these input fields exactly: schema, prompt_version, normalizer_version, book_id, book_manifest_id, segment_id, segment_type, segment_method, segment_confidence, page_range, md_quality.
2. Do not extract numeric values, constants, equation text, table values, isotope ratios as values, units, or any resolved measurements. If a value/table/equation/constant is present, record only a typed flag plus locator and set value_extracted=false.
3. Do not invent locators. A locator must be visible in the segment input or derivable from the deterministic page_range/heading/table/equation marker supplied by the segmenter.
4. Prefer omission over guessing. Unknown normalized ids must be left out of *_norm arrays; keep the raw phrase in *_raw if it is useful.
5. Use only the allowed_norm_ids supplied in the input. Do not create new normalized ids.
6. Keep summaries short and non-numeric. Summary must not contain source text excerpts, table values, constants, equations, or new claims.
7. Treat `reference_data` as a locator inventory, not a data extraction task.

Field priority:
A. First, copy deterministic segment fields exactly.
B. Then classify content_type and extract topics_raw.
C. Then identify reference_data entries as {reference_kind, label_raw, label_norm, locator, value_extracted:false}.
D. Then fill normalized fields when exact/alias matches are clear.
E. Then mark equation presence/locator if useful.
F. Last, write a short safe summary.

Allowed content_type values:
- explanation
- reference_table
- method
- derivation
- case_study
- glossary_or_definition
- mixed

Allowed reference_kind values:
- constant
- reference_table
- solubility_table
- isotope_ratio_reference
- equation
- conversion
- calibration
- standard
- thermodynamic_relation
- property_table
- classification_table
- unknown_reference

Output schema:
{
  "schema": "book_sidecar_chapter_v0",
  "prompt_version": "book_gemma_prompt_codex_v0",
  "normalizer_version": "book_norm_vocab_codex_v0",
  "book_id": "...",
  "book_manifest_id": "...",
  "segment_id": "...",
  "segment_type": "...",
  "segment_method": "...",
  "segment_confidence": "...",
  "page_range": "...",
  "md_quality": "...",
  "content_type": [],
  "topics_raw": [],
  "topics_norm": [
    {"id": "...", "confidence": "exact|alias"}
  ],
  "methods_raw": [],
  "methods_norm": [
    {"id": "...", "confidence": "exact|alias"}
  ],
  "isotope_systems_raw": [],
  "isotope_systems_norm": [
    {"id": "...", "confidence": "exact|alias"}
  ],
  "reference_data": [
    {
      "reference_kind": "...",
      "label_raw": "...",
      "label_norm": "...",
      "locator": "...",
      "value_extracted": false
    }
  ],
  "equation_locators": [
    {
      "locator": "...",
      "topic_norm": [],
      "equation_text_extracted": false
    }
  ],
  "summary": "",
  "extraction_warnings": []
}

Now extract the sidecar JSON for the supplied segment.
```

## Merge Rules For Long Segments

When a deterministic segment is too long for one model call:

1. Split by heading/table/equation/page marker boundaries when possible.
2. Run the same prompt on each subchunk with `chunk_index` and `chunk_count`.
3. Merge deterministic fields by exact equality; fail closed if any copied deterministic field differs.
4. Merge arrays by normalized id or exact raw string.
5. Preserve `value_extracted=false`; fail closed if any subchunk emits a value-like field not in schema.
6. Keep `summary` optional after merge; prefer empty summary over a stitched hallucinated summary.

## Runner-Side Validation Rules

The runner should reject or quarantine output when any condition is true:

- invalid JSON
- extra top-level keys
- missing copied deterministic field
- copied deterministic field differs from input
- `value_extracted` is not false
- numeric-looking value appears inside `reference_data`, `equation_locators`, or `summary`
- normalized id not present in `allowed_norm_ids`
- locator absent from allowed segment locator set
- `segment_confidence=low` appears in a production artifact
- summary exceeds the runner-defined short-summary budget

## Notes For Round2 Review

- This prompt deliberately makes `segment_*` non-model decisions.
- It treats `reference_data` as a typed pointer surface, not as truth-bearing data.
- It keeps `fuzzy` out of v0 normalized output; fuzzy can be added later as a quarantined normalizer layer if needed.
