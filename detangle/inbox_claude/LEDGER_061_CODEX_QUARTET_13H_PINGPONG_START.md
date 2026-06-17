# LEDGER_061 - Codex quartet 13h pingpong start

## Request

Operator asked us to start a long-running quartet prompt tuning loop for up to
13 hours, with short review cycles. Please participate as the independent
review/conductor partner when available. If Claude Code has server trouble,
Codex will continue solo and leave artifacts for later review.

## Current target

Primary manuscript-atelier profile:

```text
C:\Users\USER\Documents\manuscript-atelier\docs\handoffs\quartet_prompt_profile_v1_2026-06-17.md
```

Codex already patched the Bold wording to clarify:

- Bold should surface novelty / causality / regional implication when licensed
  by supplied evidence, author context, or task brief.
- Bold must not fabricate those beyond the evidence license.

## Calibration baseline

Use Lee 2025 / Wonhee Lee Ulleungdo paper as calibration for:

- section function,
- data/claim density,
- geoscience register,
- evidence-to-interpretation rhythm.

Do not copy sentences. Do not use its figure-derived Markdown blocks as
calibration or evidence. The figure export is currently quarantined because
image/caption/body anchoring was shown to be unreliable.

Local calibration source noted by the operator:

```text
G:\corpus_md_export_20260612\articles\Lee_W._et_al._(2025)_Water_and_gas_geochemistry_of_springs_in_Ulleungdo_volcano,.md
```

## Loop design

For each Take:

1. Codex prepares a small target writing unit, preferably a Discussion
   claim-unit first.
2. Bold / Measured / Terse drafts are generated or simulated according to the
   profile.
3. Codex acts as one Conductor.
4. Claude, when available, independently acts as a second Conductor before
   reading Codex's conductor result.
5. Both agents review:
   - hard-fail gates,
   - verb-ladder calibration,
   - register,
   - claim/evidence/caveat alignment,
   - whether Conductor added new claims,
   - whether the prose is too timid or overclaimed.
6. Codex produces a revised persona/profile proposal and the next Take starts.

The operator prefers a fast cadence, initially around 5-minute review loops.
Do not block on perfect design. The objective is trial-and-error data over time.

## Review rubric

Hard fails:

- FGP raw leakage;
- Conductor new claim / number / citation / mechanism / implication;
- meta-writing in final prose;
- numeric invention or placeholder loss;
- unsupported weakening;
- unsupported strengthening;
- caveat/counterpoint silently dropped;
- figure-derived material used before verification.

Scored criteria:

- manuscript register;
- claim/evidence/caveat alignment;
- verb-ladder calibration;
- section function;
- data/claim density;
- logical connective integrity;
- compression.

## Claude response requested

If available, please reply with:

```text
VERDICT: ok | issues_found | blocked
ROLE: reviewer | conductor | both
NOTES:
- ...
NEXT:
- ...
```

For the first response, focus on whether the patched profile is ready for
Take1 and whether Discussion claim-unit is the right first target.
