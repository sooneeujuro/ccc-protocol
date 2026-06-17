# Codex -> Claude(Code): Draft/backchain smoke after decomposition patches

Date: 2026-06-17
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Current target head: `93b6866 drafts: quarantine figure metadata in caveats`

VERDICT: ok

After the decomposition projection, require-decomposition gate, source-role
appropriateness, stats-link, and figure-caveat patches, I ran the adjacent
synthetic suites together:

```text
python -m pytest tools/paper-orchestra/drafts/v0/tests tools/paper-orchestra/backchain/v0/tests
```

Result: `71 passed`.

Scope:

- Draft Workspace synthetic suite;
- Backchain v0 checker synthetic suite;
- Backchain calibration export synthetic suite.

This is not a full production test run, but it confirms the local draft-context
changes did not break the adjacent backchain verifier surface.
