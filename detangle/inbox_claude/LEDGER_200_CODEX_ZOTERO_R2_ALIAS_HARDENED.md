# LEDGER_200 - Codex Zotero R2 alias bridge hardened

VERDICT: review_requested

Target repo: `C:\Users\USER\Documents\manuscript-atelier`

Branch: `codex/draft-context-workspace`

Target commit: `9a03e90 references: harden zotero alias local checks`

Scope:
- Hardened the local-only Zotero alias bridge.
- No Zotero API calls, no attachment import, no citation-manager mutation.
- Canonical identity remains `source_id`; Zotero item keys, collection keys, and Better BibTeX citekeys remain local aliases only.
- No raw alias values, Zotero item keys, local library IDs, paths, attachments, PDFs, or corpus text are committed in this note.

Changes:
- `zotero_aliases.py`
  - Fixed CLI error path by importing `sys`.
  - Rejects in-repo `*.local.json` alias files unless `git check-ignore` confirms the path is ignored.
  - Leaves out-of-repo alias files allowed, matching the preferred operator-private local-asset workflow.
- `.gitignore`
  - Expanded corpus reference local-ignore coverage to nested reference folders:
    `tools/paper-orchestra/corpus/references/**/*.local.json`
- Tests
  - Added red paths for duplicate Better BibTeX citekeys.
  - Added red path for duplicate collection keys within one alias record.
  - Added red/green paths for in-repo alias files: unignored rejected, ignored accepted.
  - Added CLI error-path coverage so validation failures report stable error codes instead of crashing.

Verification:
- `python -m pytest tools\paper-orchestra\corpus\references\v0\tests\test_corpus_references_synthetic.py`
  - `25 passed`
- `python -m pytest tools\paper-orchestra\corpus\references\v0\tests\test_corpus_references_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_task_builder_synthetic.py`
  - `82 passed`

Review request:
- Please independently check whether R2 now satisfies the agreed shape:
  - alias file is operator-private/local-only,
  - committed reference records never carry Zotero keys,
  - alias values cannot hide local paths,
  - duplicate item keys/citekeys are rejected,
  - in-repo alias files are accepted only when gitignored,
  - summaries expose counts/hash only, not alias contents.
- If ok, R2 can be treated as closed from Codex side and Zotero R3 or volatile OA import can be considered next.

