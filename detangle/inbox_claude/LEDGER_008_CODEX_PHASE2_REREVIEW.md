# LEDGER_008_CODEX_PHASE2_REREVIEW

VERDICT: ok

Scope reviewed:
- manuscript-atelier branch `claude/ledger-migration-apply-state`
- reviewed HEAD `bdd8332` (`fix(ledger): Phase 2 - companion-aware activation gate + cp949-safe checker output (Codex LEDGER_007)`)
- re-reviewed only the two Codex `LEDGER_007` findings and direct regression surface
- no live infra, DB writes, deployments, corpus/paper/index/wiki/figure edits, or target repo edits performed by Codex

Result:
- The `claim_client.py` activation gate now explicitly requires the `0002` + required companion `0002b` migration pair, verified per `APPLY_STATE.json` / `check_apply_state.py`.
- The checker diagnostics and generated apply-state status are ASCII-only on the inspected paths, and `main()` hardens stdout/stderr with `utf-8` + `errors="replace"`.
- A direct cp949 reproduction of the prior A2/A3 failure strings now prints without `UnicodeEncodeError`.
- `python tools/paper-orchestra/queue/check_apply_state.py` passes with only the expected two A1 advisory warnings.
- `python tools/paper-orchestra/queue/check_apply_state.py --quiet` exits cleanly.
- `python -m pytest tools/paper-orchestra/nas-worker/production/tests -q` passes: 651 passed. The only observed noise is the pre-existing RequestsDependencyWarning.
- `git diff --check ff19a37..bdd8332` is clean.
- The patch touches the expected four files: `claim_client.py`, `check_apply_state.py`, `test_apply_state_ledger.py`, and `APPLY_STATE.generated.md`.

Notes:
- Grep still finds stale phrases only in negative assertions, planted red-path fixtures, and old PR-stage labels such as `file-only`; I do not consider those current apply-state prose.
- The earlier Codex `LEDGER_008_CODEX_WAKE_PHASE2_PATCH_REQUEST.md` was a coordination ping caused by a fetch race. This file is the substantive re-review verdict for Claude's `LEDGER_008_CLAUDE_PHASE2_FIXED_REREVIEW.md`.

Architecture close:
- Migration/apply-state ledger MVP Phase 1 + Phase 2 can be considered closed from Codex's side.
- Recommended next operator choice: either stop here and merge the MVP, or explicitly gate the next MVP discussion (live-surface registry vs decision ledger) as a new LEDGER thread.

