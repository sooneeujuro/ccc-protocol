# LEDGER_184_CODEX_REFERENCES_ALIAS_HARDENING

Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Branch: `codex/draft-context-workspace`
Target commit: `6f074cc` (`references: harden path and hash checks`)

## Summary

Codex rechecked the Zotero/reference track after R1 closure and found the two
release-snapshot nits were not both fully closed in code:

1. `LOCAL_PATH_RE` in `build_corpus_references.py` did not include `/home/`
   or `/Users/`.
2. `check_corpus_references.py` skipped path scanning for
   `content_version.source_md_sha1` without first proving the value was a
   40-hex SHA-1.

Patch:

- Added `/home/` and `/Users/` to the shared local-path regex.
- Added `SHA1_RE`.
- `content_version.source_md_sha1` and `content_version.source_md_sha1s[]`
  are exempt from path scanning only when they are valid 40-hex SHA-1 strings;
  otherwise the checker reports `E8 content-hash`.
- Added red-path tests for a POSIX user path and path text hidden in
  `source_md_sha1`.

## Verification run

Codex ran:

```text
python -m pytest tools\paper-orchestra\corpus\references\v0\tests
```

Result: `17 passed`.

## Review request

Please independently review/break this as a small R1/R2 hardening patch:

1. Are the old `/home/` / `/Users/` and SHA-field exemption gaps now closed?
2. Does this preserve valid `source_md_sha1` / `source_md_sha1s[]` witnesses?
3. Does Zotero alias validation remain local-only/count-only?
4. Any remaining release-snapshot blockers for corpus references / Zotero alias bridge?

Suggested verdict shape:

`VERDICT: ok | issues_found | blocked`

