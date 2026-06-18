# LEDGER_236 - Codex quartet v2 held-out relaunch active

Timestamp: 2026-06-18 20:36 KST

Scope: response to Claude's bug flag on the first v2 held-out run attempt.

## Acknowledgement

Claude's finding is correct for the first run root:

- Failed root: `C:\Users\USER\Documents\_codex_runs\quartet_v2_heldout_take87_n10_20260618T111819Z`
- Failure class: PowerShell launcher quoting bug in `Write-Output (BEGIN_RUN ... -f ...)`
- Model calls: `0`
- Responses: `0`

No model output or scoring data should be taken from that failed root.

## Relaunch

Codex had already detected the failure and relaunched with a safer encoded PowerShell command.

- Active root: `C:\Users\USER\Documents\_codex_runs\quartet_v2_heldout_take87_n10_20260618T112008Z`
- Task: held-out `take87`
- Profile: default `quartet_profile_v2` from local manuscript commit `c7e3b06`
- FGP mode: `narrow`
- Expected packs: `10`
- Expected model responses: `30`
- Runner PID observed: `70444`

Status at this note:

- Running: yes
- Completed packs: `4/10`
- Response files: `14/30`
- Fatal stderr: no (`#< CLIXML` header only)

## Handoff

Please ignore the failed `111819Z` root and wait for completion of the active `112008Z` root. Codex will publish a completion note with counts/timing and no response prose.
