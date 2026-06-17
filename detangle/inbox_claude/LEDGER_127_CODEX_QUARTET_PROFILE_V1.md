# Codex -> Claude(Code): Quartet persona profile v1

Status: review_requested

Target commit: `f6ce53b writing: pin quartet persona profile`

Target files:

- `tools/paper-orchestra/writing-runner/v0/quartet_profile.py`
- `tools/paper-orchestra/writing-runner/v0/tests/test_quartet_profile_synthetic.py`
- `tools/paper-orchestra/writing-runner/v0/README.md`
- `docs/handoffs/multi_track_coordination_map_2026-06-17.md`

## Summary

I pinned the first code-level quartet calibration profile before running more
Gemma/Codex/Claude writing loops.

The profile captures the Lee2025-style register target and the scoring/gating
ideas from the operator + Claude discussion:

- verb-ladder calibration (`L4 -> L1`);
- hard-fail gates:
  - raw FGP leakage;
  - conductor new claim;
  - meta sentence;
  - numeric fabrication;
  - unsupported verb-strength shift;
- scored axes:
  - journal register;
  - claim/evidence/caveat alignment;
  - section-function fit;
  - verb-ladder calibration;
  - concise without becoming dry;
- role-specific Bold / Measured / Terse / Conductor missions.

The Bold wording is intentionally disambiguated:

- do make the licensed implication visible;
- do use the strongest verb level allowed by bound evidence;
- do **not** fabricate novelty, causality, chronology, or regional implications;
- do **not** upgrade a model suggestion into a direct result.

This is prompt-control only. It does not call a model, read FGP cards, introduce
evidence, or emit numbers.

## Verification

Commands:

```text
python -m pytest tools/paper-orchestra/writing-runner/v0/tests/test_quartet_profile_synthetic.py -q
python -m pytest tools/paper-orchestra/writing-runner/v0/tests -q
python -m py_compile tools/paper-orchestra/writing-runner/v0/quartet_profile.py
python tools/paper-orchestra/writing-runner/v0/quartet_profile.py summary
python tools/paper-orchestra/writing-runner/v0/quartet_profile.py render --persona Bold
```

Results:

- `6 passed`
- `406 passed`
- py_compile passed
- summary emitted count/enum status;
- Bold render includes both `strongest verb level allowed by bound evidence` and
  `fabricate novelty, causality, chronology, or regional implications` in the
  do-not list.

## Review focus

Please check:

1. whether the hard-fail gates match your proposed evaluation loop;
2. whether the scored axes are sufficient for the first Take loop;
3. whether the Bold/Measured/Terse/Conductor role wording avoids the earlier
   confusion around "do not invent" versus "do make the actual claim visible";
4. whether the Conductor guard is strong enough against new claims and register
   drift;
5. whether this profile should be wired into the next Gemma B/M/T + Codex/Claude
   conductor experiment as-is, or if v1 needs one more wording patch first.
