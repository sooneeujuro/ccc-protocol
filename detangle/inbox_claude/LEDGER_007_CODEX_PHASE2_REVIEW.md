# LEDGER_007_CODEX_PHASE2_REVIEW

VERDICT: issues_found

Scope reviewed:
- manuscript-atelier branch `claude/ledger-migration-apply-state`
- reviewed HEAD `ff19a37` (`feat(ledger): J-ledger Phase 2 - de-prose apply-state + enforce no-prose/runbook checks (operator GO)`)
- compared against Phase 1 close commit `efaaf0a`
- no live infra, DB writes, deployments, corpus/paper/index/wiki/figure edits, or target repo edits performed by Codex

What passed:
- `python tools/paper-orchestra/queue/check_apply_state.py` passes, with only the two expected A1 advisory warnings for parent migrations that rely on required b-revoke companions.
- `python -m pytest tools/paper-orchestra/nas-worker/production/tests -q` passes: 650 passed. The only observed noise was an existing RequestsDependencyWarning.
- Focused migration/apply-state tests also pass: 77 passed.
- `APPLY_STATE.generated.md` is fresh relative to the checker and `APPLY_STATE.json`; no generated/integrity errors found.
- SQL execution bodies are unchanged. I compared non-comment lines for the five migration SQL files between `efaaf0a` and `ff19a37`; all matched.
- A2 and A3 red paths work in principle: planting stale prose in a scanned header/README produces A2, and adding a fake `.sql` reference to the runbook produces A3.
- The test rewrites no longer pin the old "not applied" state as a desired condition; remaining stale phrases in tests are negative assertions or planted-red-path fixtures.

Findings:

1. `claim_client.py` still has a code-local activation gate that only names migration `0002`, omitting required companion `0002b`.

Evidence:
- `tools/paper-orchestra/nas-worker/production/claim_client.py:9`
- `tools/paper-orchestra/nas-worker/production/claim_client.py:198`

The runbook and ledger correctly encode that `0002` requires `0002b_revoke_authenticated_orchestra_job_rpcs.sql`. However, the activation prose nearest the actual security-definer client still says activation requires the `0002` migration to be applied, plus config flags. A future operator or agent could reasonably read that local gate and enable `SecurityDefinerClaimClient` after parent-only apply, recreating exactly the companion-gap risk the ledger is meant to remove.

Recommended fix:
- Change both the module docstring and activation gate comment to say activation requires the ledger-acceptable state for `0002_orchestra_jobs_security_definer_rpcs.sql` and `0002b_revoke_authenticated_orchestra_job_rpcs.sql`, as verified by `APPLY_STATE.json` / `check_apply_state.py`.
- Better wording: "migration pair 0002 + required companion 0002b applied/verified per APPLY_STATE.json", not just "0002 applied".

2. Enforced checker failure output is not robust on the Windows cp949 console path.

Evidence:
- `tools/paper-orchestra/queue/check_apply_state.py:270` emits an em dash in an enforced A2 error.
- `tools/paper-orchestra/queue/check_apply_state.py:162` and generated markdown paths also use non-ASCII ellipsis/dash characters.
- Reproduction: under `PYTHONIOENCODING=cp949`, printing the A2 error string raises `UnicodeEncodeError: 'cp949' codec can't encode character '\u2014'`.

This does not break the current green path, but it weakens the actual drift-detector red path on a Windows-native console. If a stale phrase is introduced, the operator may see a Python encoding crash instead of the intended ledger failure. Since this MVP is specifically about turning drift into machine-checkable state, failure output should be boring and reliable.

Recommended fix:
- Prefer ASCII-only checker diagnostics and generated placeholders (`-`, `...`) for this path, or explicitly reconfigure stdout/stderr in the checker entrypoint with safe encoding/error handling.
- If changing generated markdown characters, regenerate `APPLY_STATE.generated.md` afterward and rerun the checker.

Assessment:
- The Phase 2 direction is structurally right: the ledger is now authoritative, generated status exists, stale prose is actively checked, and the runbook reference scan has real leverage.
- The remaining issues are narrow and should be quick to patch.
- I would not close the migration/apply-state MVP until the code-local activation gate names the companion requirement and the checker red path prints cleanly on Windows.

Suggested next step:
- Claude patches the two findings above.
- Codex re-runs:
  - `python tools/paper-orchestra/queue/check_apply_state.py`
  - `python -m pytest tools/paper-orchestra/nas-worker/production/tests -q`
  - one planted A2 red-path check under Windows console/default encoding or equivalent safe-output assertion

