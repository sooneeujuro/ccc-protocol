# LEDGER_096 - Codex Draft Decomposition Smoke

Status: info

Target repo: `C:\Users\USER\Documents\manuscript-atelier`

Branch: `codex/draft-context-workspace`

Target commit: `44997b4` (`drafts: validate structured decomposition notes`)

## Smoke Results

After publishing LEDGER_095, Codex ran two CLI-level smoke checks in temporary repo roots outside the target repo.

Green path:

- created a draft workspace with `create_draft_workspace.py`;
- added valid `agent_notes/decomposition.json`;
- ran `check_draft_context.py --write`;
- ran `check_draft_context.py`;
- result: `draft_context_check=PASS`, `enforced_error_count=0`.

Red path:

- created a draft workspace with malformed `agent_notes/decomposition.json`;
- missing `verb_level`;
- source id used but absent from `source_roles`;
- unsupported component missing `missing_evidence`;
- result: `draft_context_check=FAIL`, `enforced_error_count=4`;
- leak check: missing source id value was not echoed in checker output.

## Interpretation

The optional decomposition checker behaves as intended at CLI level:

- valid decomposition does not break MVP A workspace checks;
- malformed decomposition fails closed;
- checker output remains enum-like and non-leaky.

No additional target-repo changes were made for this smoke.
