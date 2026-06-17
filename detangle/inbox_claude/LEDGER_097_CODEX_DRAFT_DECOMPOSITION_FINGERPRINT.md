# LEDGER_097 - Codex Draft Decomposition Fingerprint

Status: review_requested

Target repo: `C:\Users\USER\Documents\manuscript-atelier`

Branch: `codex/draft-context-workspace`

Target commit: `7bfb6b3` (`drafts: fingerprint decomposition notes`)

Supersedes review target for LEDGER_095 from `44997b4` to `7bfb6b3`.

## Patch Summary

After the initial checker build, Codex noticed that optional
`agent_notes/decomposition.json` was validated but not included in generated
fingerprints. That meant decomposition changes would not make generated files
stale.

Patch:

- added optional `decomposition.json` to loaded agent notes when present;
- generated fingerprints now include the decomposition file hash;
- added a regression test that changing decomposition content makes generated
  outputs stale.

## Tests

Ran:

```text
python -m pytest tools/paper-orchestra/drafts/v0/tests/test_draft_context_synthetic.py
```

Result:

```text
20 passed
```

## Review Request

Please review `7bfb6b3` as the current decomposition-checker target.

No live infra, corpus rebuild, or external model calls were performed.
