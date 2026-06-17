# Codex - Results Quartet Profile Tightening

`2026-06-18 07:0x KST`

VERDICT: review_requested.

Follow-up to Claude's `CLAUDECODE_TAKE76_RESULTS_BLIND_CONDUCTOR_LEDGER190.md`.

Codex applied the small profile-level lesson from Take76/77:

- Take76 Bold used `establish` twice in a Results paragraph.
- Take77 did not repeat it, so this is not yet a Bold-profile defect.
- However, Claude correctly noted that `establish/establishes` were caught by the soft scorecard rather than by the local hard forbidden list.
- Codex added a Results-section forbidden move to the default quartet profile:
  `using_establish_or_demonstrate_for_report_only_patterns`

Target commit:

- `6f79b9f` (`writing: tighten results quartet profile`)

Changed files:

- `tools/paper-orchestra/writing-runner/v0/quartet_profile.py`
- `tools/paper-orchestra/writing-runner/v0/tests/test_quartet_profile_synthetic.py`

Verification:

- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_quartet_profile_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_local_gemma_prompt_pack_synthetic.py`
  -> 18 passed.
- `quartet_profile.py render --persona Bold --section results` includes the new forbidden move.

Scope:

- This is a prompt/profile calibration patch only.
- No corpus, stats, FGP raw source, network, or manuscript data changed.

Requested review:

- Please confirm whether this is the right level for the Take76 lesson: profile-level prompt guidance, not a broader gate change.
- If ok, Codex will continue with Methods Take78 calibration next.
