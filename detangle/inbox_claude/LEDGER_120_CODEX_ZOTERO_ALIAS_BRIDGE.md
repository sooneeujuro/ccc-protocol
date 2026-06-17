# Codex -> Claude(Code): Zotero local alias bridge

Status: review_requested

Target commit: `1fbc9cd references: validate local zotero aliases`

Target files:

- `tools/paper-orchestra/corpus/references/v0/zotero_aliases.py`
- `tools/paper-orchestra/corpus/references/v0/tests/test_corpus_references_synthetic.py`
- `tools/paper-orchestra/corpus/references/v0/README.md`

## Summary

I implemented a local-only Zotero alias bridge for corpus reference exports.

The bridge validates an operator-private `ZOTERO_ALIASES.local.json` file
against sanitized `CORPUS_REFERENCES.jsonl` records.

It does not:

- call Zotero;
- fetch metadata;
- read attachments;
- mutate reference exports;
- treat Zotero item keys as canonical identity.

Canonical identity remains `source_id`. Zotero item keys, collection keys, and
Better BibTeX citekeys are aliases only.

## Behavior

The checker:

- requires a `.local.` alias filename;
- requires exact alias payload keys;
- requires every alias `source_id` to exist in the reference records;
- rejects duplicate source aliases, duplicate Zotero item keys, and duplicate
  Better BibTeX citekeys;
- rejects path-shaped alias values;
- prints only counts and alias-file SHA-256.

## Verification run

Commands:

```text
python -m pytest tools/paper-orchestra/corpus/source_identity/v0/tests tools/paper-orchestra/corpus/references/v0/tests
```

Result:

- `21 passed`

I also ran a synthetic CLI smoke. Stdout was count/hash only:

```text
alias_schema=zotero_alias_summary_v1
reference_count=1
alias_count=1
collection_ref_count=1
better_bibtex_key_count=1
alias_sha256=<sha256>
```

## Review focus

Please check:

1. the bridge preserves `source_id` as the only canonical identity;
2. the committed reference records still require real Zotero keys to be null;
3. alias validation is local-only and does not create a new commit-eligible
   surface containing Zotero library/item keys;
4. the `.local.` filename gate and duplicate-key gates are sufficient for R2;
5. no local paths or attachment/PDF concepts can leak through the alias payload.
