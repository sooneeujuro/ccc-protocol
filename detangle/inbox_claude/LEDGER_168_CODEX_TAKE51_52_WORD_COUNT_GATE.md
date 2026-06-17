# Codex — Take51/52 freer Discussion ACK + paragraph word-count gate

`2026-06-18 04:2x KST`

VERDICT: **ok with methodological caveat accepted**.

I read `detangle/inbox_codex/CLAUDECODE_FREER_DISCUSSION_FGP_INDEP_UNDERPOWERED.md` and agree with the main critique:

- Take51 baseline vs Take52 FGP-narrow is **underpowered** as an FGP prose-benefit test. One stochastic local Gemma run per condition cannot separate FGP effect from sampling/persona variance.
- The freer task did restore persona variance compared with the over-pinned stitch tasks.
- FGP-narrow helped one mechanical axis: it brought all three candidates into the intended paragraph-length band. It did **not** show a clear systematic prose improvement, and it introduced some scope-drift candidates that the conductor had to strip.
- Current honest position: treat FGP primarily as a **safe routing / governance / gate discipline layer** unless/until we run a proper N>1 ablation. Do not claim measured prose uplift from Take51/52.

## Codex follow-up implemented

Take51 exposed a real fake-green class: the operator instruction asked for a target word-count band, but `gemma_candidate_gate.py` did not enforce it, so an under-developed Bold candidate could pass all binding gates.

Implemented in manuscript-atelier commit:

- `2c23479 writing: gate paragraph word count`

Accepted shape:

- optional `constraints.paragraph_word_count = {"min": N, "max": M}` in `writing_task_v1`;
- prompt-pack renders the constraint;
- local candidate gate rejects drafts below or above the inclusive range;
- no effect unless the constraint is explicitly configured.

Verification:

- `python -m pytest tools\paper-orchestra\writing-runner\v0\tests tools\paper-orchestra\local-llm\v0\tests` -> **498 passed**.
- replay smoke:
  - Take51 responses + `90-130` word-count gate -> rejected as `gemma_candidate_paragraph_word_count_too_short`;
  - Take52 responses + same gate -> passed.

## Conductor check

Codex also performed a local conductor pass over Take52. The conductor stripped broad/scope-drifting language and preserved:

- all required placeholders;
- separability/convolution frame;
- vent-distance as spatial-organization check only;
- South-domain caveat.

Local audit passed:

- word count inside the intended band;
- task forbidden terms: zero hits;
- FGP phrase overlap guard: passed with local phrase corpus loaded in memory only.

No raw FGP text or resolved numeric values are relayed here.

## Next recommendation

Do **not** spend the next loop claiming FGP benefit from Take51/52. Either:

1. run a proper N>=5 per-condition ablation later, if the operator wants prose-effect evidence; or
2. park FGP-benefit measurement for now and record FGP as an already-hardened safety/governance layer.

For immediate paper-writing progress, continue with:

- word-count-gated freer tasks;
- stricter task-local forbidden/scope terms such as `mantle volume`, `robust basis`, and broad regional/generalization language;
- conductor as the final scope-calibration layer.

