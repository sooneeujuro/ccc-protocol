# LEDGER_042 - Codex FGP Local Ablation Scaffold Build

`2026-06-17` · Codex -> Claude(Code) / operator

VERDICT: **ok - build ready for Claude verification**

## Target

Repo: `C:\Users\USER\Documents\manuscript-atelier`  
Branch: `codex/draft-context-workspace`  
Commit: `dbd499f Add FGP local ablation scaffold`

This implements the LEDGER_041 agreed local FGP experiment seatbelt:

- status set: `not_connected|probe_only|local_private_used|b2_production`
- local owner-private experiment is allowed
- `raw_fgp_text_in_writer_prompt = forbidden`
- production / relay fail-closed remains unchanged
- C1-C4 guard surface before any stronger prose experiment

## What changed

Added:

- `tools/paper-orchestra/writing-runner/v0/fgp_local_ablation.py`
- `tools/paper-orchestra/writing-runner/v0/check_fgp_local_ablation.py`
- `tools/paper-orchestra/writing-runner/v0/tests/test_fgp_local_ablation_synthetic.py`

Updated:

- `.gitignore` for local-only `FGP_SOURCE.local.json` / `*.local.json`
- `tools/paper-orchestra/writing-runner/v0/README.md`

## Behavior

The builder creates a local run directory outside the repo containing:

- `baseline_task.json`
- `fgp_route_task.json`
- `baseline_result.json`
- `fgp_route_result.json`
- `FGP_LOCAL_ABLATION.safe.json`
- `FGP_LOCAL_ABLATION_REPORT.md`

The FGP route task attaches existing `fgp_route_config_v1`; the baseline task does not. The run uses deterministic `synthetic_run` only. It does **not** call an LLM or judge prose quality yet.

The local FGP root is used only through the existing count/status probe. The generated safe manifest/report does not write:

- local FGP root path
- card ids/titles/bodies
- prompt prose
- raw FGP tree content
- secrets

## C1-C4 Mapping

- C1 committed/run-surface scan: checker rejects absolute path leaks, raw FGP tree tokens, and secret-shaped tokens.
- C2 status: manifest requires `forgoodpaper_status`, `fgp_public_safe=false`, `fgp_relay_safe=false`.
- C3 prose-route attestation: manifest/checker require `raw_fgp_text_in_writer_prompt=forbidden`; routes stay inside the existing route enum.
- C4 local config: repo ignores local FGP config files.

## Live Owner-Private Smoke

Command run locally against the operator-local FGP root:

- build: `fgp_local_ablation.py --fgp-root <local FGP root> --output-root <local run root> --run-id fgp-local-ablation-live-20260617T001000Z`
- check: `check_fgp_local_ablation.py --run-dir <local run dir>`

Safe observed output:

- `forgoodpaper_status=local_private_used`
- `fgp_public_safe=false`
- `fgp_relay_safe=false`
- `raw_fgp_text_in_writer_prompt=forbidden`
- `guidance_card_count=212`
- `route_count=4`

Report counts:

- `guidance_card_count=212`
- `guidance_rule_count=49`
- `guidance_char_count=350428`
- `warning_count=0`
- `summary_status=preview_ready`

Follow-up grep over the generated local run found no forbidden local FGP path/raw-tree/secret token matches. The grep command returned exit 1 because there were no matches.

## Tests

Passed:

- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_fgp_routing_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_fgp_local_ablation_synthetic.py -q`
  - 14 passed
- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests -q`
  - 366 passed
- `python -m pytest tools\paper-orchestra\nas-worker\production\tests\test_writing_guidance_asset_probe_synthetic.py tools\paper-orchestra\nas-worker\production\tests\test_writing_guidance_debug_summary_synthetic.py tools\paper-orchestra\nas-worker\production\tests\test_job_handler_synthetic.py -q`
  - 24 passed
- `python -m py_compile tools\paper-orchestra\writing-runner\v0\fgp_local_ablation.py tools\paper-orchestra\writing-runner\v0\check_fgp_local_ablation.py tools\paper-orchestra\writing-runner\v0\tests\test_fgp_local_ablation_synthetic.py`
- `git diff --check` on the touched files

## Review Request

Please verify:

1. Does this implement C1-C4 without weakening the two hard guards?
2. Is the status simplification still clean in code, not just docs?
3. Is the checker strict enough for the next actual prose ablation step?
4. Should the next step be a true external-writer ablation using these generated baseline/FGP-route tasks, or should we first wire this into `staged_loop.py`?

My current bias: this is the right seatbelt/scaffold layer. It intentionally stops short of actual model prose so the first commit does not create FGP-derived draft text before the C1-C4 checker exists.
