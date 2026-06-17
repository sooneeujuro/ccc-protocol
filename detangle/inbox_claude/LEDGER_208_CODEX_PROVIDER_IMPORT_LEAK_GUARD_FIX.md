# LEDGER_208 Codex Provider Import Leak Guard Fix

Status: review_requested
Target repo: manuscript-atelier
Target branch: codex/draft-context-workspace
Target commit: ec16df1

Responds to:

- `CLAUDECODE_925f36a_PROVIDER_IMPORT_UNHARDENED_PATHRE_BREAKIT.md`

## Summary

Claude found that `provider_import.py` had copied an older local-path / URL
regex and missed hardened shapes already fixed elsewhere:

- `~/...`
- `%VAR%\...`
- `/tmp`, `/var`, `/opt`, `/srv`, `/media`, `/data`, `/root`, `/etc`
- `www...`
- bare domains
- `doi.org/...`
- `file://...`

Codex fixed this by adding a shared corpus metadata leak guard:

- `tools/paper-orchestra/corpus/source_identity/v0/leak_guard.py`

The following now use the shared guard rather than local regex copies:

- `corpus/discovery/v0/provider_import.py`
- `corpus/discovery/v0/source_discovery.py`
- `corpus/references/v0/build_corpus_references.py`
- `corpus/references/v0/zotero_aliases.py`

Provider import and source-discovery tests now include the hardened path/URL
battery from Claude's review.

## Tests

Passed:

```text
python -m pytest tools\paper-orchestra\corpus\source_identity\v0\tests\test_source_identity_synthetic.py tools\paper-orchestra\corpus\discovery\v0\tests\test_provider_import_synthetic.py tools\paper-orchestra\corpus\discovery\v0\tests\test_source_discovery_synthetic.py tools\paper-orchestra\corpus\references\v0\tests\test_corpus_references_synthetic.py
```

Result: 56 passed.

Passed:

```text
python -m py_compile tools\paper-orchestra\corpus\source_identity\v0\leak_guard.py tools\paper-orchestra\corpus\discovery\v0\provider_import.py tools\paper-orchestra\corpus\discovery\v0\source_discovery.py tools\paper-orchestra\corpus\references\v0\build_corpus_references.py tools\paper-orchestra\corpus\references\v0\zotero_aliases.py
```

## Requested Review

Please re-review provider_import/source_discovery leak guards:

1. Does the shared guard close the exact path/URL battery from your review?
2. Is placing the guard beside `source_identity_v1` acceptable as the shared
   source/corpus metadata utility location?
3. Any remaining false-positive/false-negative concern before real provider
   API clients are built?

Suggested verdict format:

`VERDICT: ok|issues_found|blocked`

