# LEDGER_039_CODEX_ZOTERO_REFERENCE_MVP_BUILT

VERDICT: review_requested

## Target

Repo: `C:\Users\USER\Documents\manuscript-atelier`

Branch: `codex/draft-context-workspace`

Target commit: `bfb64c6 Add corpus reference source identity MVP`

Note: this branch also contains the earlier draft-context workspace commit
`1771e5b`. The new reference/source-id work is isolated in `bfb64c6`.

## What Changed

Implemented the corrected LEDGER_038 contract as a small offline MVP:

```text
tools/paper-orchestra/corpus/source_identity/v0/
  README.md
  source_identity.py
  tests/test_source_identity_synthetic.py

tools/paper-orchestra/corpus/references/v0/
  README.md
  build_corpus_references.py
  check_corpus_references.py
  tests/test_corpus_references_synthetic.py
```

Also updated `.gitignore` so local generated reference exports and Zotero alias
files are protected:

```text
tools/paper-orchestra/corpus/references/generated/CORPUS_REFERENCES.jsonl
tools/paper-orchestra/corpus/references/generated/corpus_references.csl.json
tools/paper-orchestra/corpus/references/generated/corpus_references.bib
tools/paper-orchestra/corpus/references/generated/corpus_references.ris
tools/paper-orchestra/corpus/references/*.local.json
```

## Contract Implemented

- DOI-derived `source_id` first.
- OpenAlex-derived `source_id` second.
- Base fallback uses `base:<source_namespace>:<paper_id>`.
- Provider fallback uses `provider:<provider>:<provider_record_id>`.
- `source_md_sha1` is carried only as `content_version`, never as identity.
- Zotero item/collection keys are local-only; committed records must keep them
  null.
- CSL JSON is the canonical export shape; BibTeX/RIS render from the same
  reference record shape.
- RIS emits repeated `AU  - ` lines.
- BibTeX escapes common special characters and keeps citekeys unique.

## Live Dry Run

The current local `retrieval_papers.json` is ignored/local and contains local
paths, so no generated exports were committed.

Dry-run:

```text
python tools\paper-orchestra\corpus\references\v0\build_corpus_references.py
```

Result:

```text
rendered 3220 references (dry-run; pass --write to write)
```

The input index has 3339 paper rows. The exporter coalesces duplicate
`source_id` rows into one reference item because the citation/Zotero layer wants
one item per scholarly source, with `paper_ids` and content-version witnesses
retained.

Checker:

```text
python tools\paper-orchestra\corpus\references\v0\check_corpus_references.py --json
```

Result:

```json
{
  "ok": true,
  "errors": []
}
```

## Tests

Passed:

```text
python -m pytest tools\paper-orchestra\corpus\source_identity\v0\tests tools\paper-orchestra\corpus\references\v0\tests -q
16 passed

python -m pytest tools\paper-orchestra\corpus\tests\test_corpus_binding.py tools\paper-orchestra\corpus\source_identity\v0\tests tools\paper-orchestra\corpus\references\v0\tests -q
29 passed

python -m py_compile tools\paper-orchestra\corpus\source_identity\v0\source_identity.py tools\paper-orchestra\corpus\references\v0\build_corpus_references.py tools\paper-orchestra\corpus\references\v0\check_corpus_references.py
```

The usual local `requests` dependency warning appeared during pytest but tests
passed.

## Review Focus

Please review especially:

1. **source namespace**: Codex used `cccp_geochem` as the stable base fallback
   namespace. If you prefer `paper_orchestra_geochem` or another corpus-profile
   id, say so before this becomes a wider contract.
2. **duplicate coalescing**: live index duplicates are collapsed by `source_id`
   into one reference. This made the live checker green while preserving
   duplicate red-path tests at the checker layer.
3. **generated policy**: bulk CSL/BibTeX/RIS remain local-only. The manifest is
   code-supported but not written/committed here because current
   `retrieval_papers.json` is ignored/local and path-bearing.
4. **Zotero key guard**: committed non-null Zotero keys fail synthetic red-path
   tests. Real alias files remain `*.local.json`.

No network, no Zotero API, no PDF/fulltext read, no corpus rebuild, no DB/write
infra, no generated reference export committed.
