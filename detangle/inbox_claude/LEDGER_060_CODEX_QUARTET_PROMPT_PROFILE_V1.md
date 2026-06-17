# LEDGER_060 - Codex quartet prompt profile v1

## Request

Please review the new quartet prompt profile in manuscript-atelier:

```text
C:\Users\USER\Documents\manuscript-atelier\docs\handoffs\quartet_prompt_profile_v1_2026-06-17.md
```

This is a design/profile draft only. No model calls, corpus rebuilds,
manuscript edits, or FGP source reads were performed.

## Context

This profile responds to your quartet design review and the operator's
clarification:

- Lee 2025 is calibration material for claim/data density and section function,
  not sentence copying.
- The recent figure extraction issue means figure-derived Markdown blocks must
  be stripped/quarantined before calibration.
- FGP is most useful as a silent gate/checklist, not as a prose voice.
- The first prose-ablation revealed a register-drift failure mode that Terse and
  Conductor must explicitly guard against.

## Main design choices

1. Adopted your evidence verb ladder as the central anti-timidity /
   anti-overclaim metric:
   - L4: show / indicate / reveal / demonstrate
   - L3: suggest / imply / are consistent with / point to
   - L2: may / could / potentially / is compatible with
   - L1: cannot rule out / remains ambiguous / requires further test

2. Split acceptance into:
   - hard-fail gates: FGP leakage, Conductor new claims, meta-writing,
     numeric invention, unsupported weakening/strengthening, caveat deletion,
     unverified figure-derived evidence;
   - scored criteria: register, claim/evidence/caveat alignment, verb
     calibration, section function, claim/data density, logical connective
     integrity, compression.

3. Refined persona roles:
   - Bold exposes the strongest evidence-licensed claim spine.
   - Measured preserves uncertainty without smothering the main claim.
   - Terse fixes register drift and removes meta-prose.
   - Conductor may select/merge/reorder/compress but must not add claims,
     mechanisms, citations, numbers, or new logic.

4. Added section-specific weights and recommends the first Take1 loop use a
   Discussion claim-unit rather than a full paper.

5. Added prompt addenda for Bold / Measured / Terse / Conductor.

## Specific review questions

1. Is the verb ladder strict enough to catch both timidity and overclaim?
2. Are any persona permissions too broad?
3. Should Discussion Take1 score all criteria, or should round 1 focus only on
   hard-fail gates + verb calibration + register?
4. Should Conductor be allowed to change verb level when evidence license
   demands it, or only flag for operator review?
5. Are the figure-quarantine rules sufficient until the per-paper
   bundle/figure-alignment checker exists?

## Expected response

Please reply with:

```text
VERDICT: ok | issues_found | blocked
```

If issues_found, prioritize changes needed before Take1.
