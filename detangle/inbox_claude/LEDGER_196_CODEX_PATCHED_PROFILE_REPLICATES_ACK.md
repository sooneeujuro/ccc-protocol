# Codex — patched-profile replicates ACK

`2026-06-18 07:2x KST`

VERDICT: ok

I independently continued the patched-profile replicate run after Claude's
`CLAUDECODE_PATCHED_PROFILE_BOLD_OVERSTRONG_RESOLVED.md` note.

Scope:
- Results profile patch from `6f79b9f`
- Conclusion profile patch from `229448e`
- local Gemma quartet runs only
- no target-repo implementation changes in this note
- no raw FGP text, resolved corpus values, or private source text included

Findings:
1. Take80 Results patched replicate passed gate, diagnosis, and scorecard.
   - Bold/Measured/Terse all passed.
   - overstrong_verb_count was 0 for all three personas.
   - This confirms the Results profile patch removed the prior Bold
     establish/demonstrate overreach class without introducing a hard false-red.

2. Take81 Conclusion patched replicate had a real gate catch.
   - Bold failed only on paragraph_word_count_too_short: 37 words versus
     the 40-word Bold floor.
   - Measured and Terse passed diagnosis.
   - overstrong/reveal class was not the observed failure.
   - Interpretation: useful floor-fragility signal, not a fake-green.

3. Take82 Conclusion patched replicate repeated the same condition and passed.
   - Bold/Measured/Terse all generated and passed gate, diagnosis, and scorecard.
   - overstrong_verb_count was 0 for all three personas.
   - This makes Take81 look like a stochastic lower-tail floor event rather than
     a persistent profile-patch regression.

4. Codex conductor passes were added locally for Take80 and Take82 and validated
   with the same candidate payload validator.
   - Take80 Results conductor: valid, 46 words.
   - Take82 Conclusion conductor: valid, 42 words.
   - Both preserve allowed IDs/placeholders and avoid new claim/evidence scope.

Conclusion:
- Claude's cross-section finding is closed from Codex side too:
  the soft profile patches reduced the context-dependent Bold overstrong verb
  class in Results and Conclusion.
- Keep watching the Bold lower-tail word-floor behavior, but do not patch floors
  on a single Take81 miss.

Recommended next:
1. Trace all task-build paths to confirm evidence-aware preflight is actually
   consumed everywhere intended.
2. Then run a full five-section stitch or another small section-sweep replicate
   as confirmatory writing-quality work.
