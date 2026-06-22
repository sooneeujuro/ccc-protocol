# CLAUDECODE_CONTEXT_BRIDGE_OVERNIGHT_LOOP

FROM: Claude (driving). TO: Codex (quiet watch, context gap).
Relay-safe: counts / status / hashes / booleans only. No raw model prose, no
resolved article/dataset values, no captions. Dataset-derived stats referenced by
handle-count / bind-rate, never the numbers.

Your last context ends at CLAUDECODE_PHASEB_COMPLETE_REALDATA_GROUNDING +
LEDGER_313. This bridges that -> now. Operator asked me to brief you so you can
REVIEW while a generation cycle runs.

## What happened since Phase B complete (operator-driven)

1. n=1 challenge -> NUMBER-TYPE finding. Operator questioned "one pass = verified?".
   N=5 robustness on stub = 100% bind, BUT real-data u1 verify exposed: the local
   model binds MEASURED values (with units) reliably/selectively, and abstract
   CORRELATION statistics (Spearman rho/p) erratically (bound_any 1/4). Conclusion:
   emit each claim's load-bearing MEASURED quantities, not correlation rhos. Saved to
   Claude memory (numeric-grounding-number-type). Re-verified: u1/u2/u3 all PASS with
   measured-value ledgers.

2. Commit A landed (main repo, 7a46da2): gemma_paragraph_pipeline.py (new) +
   local_gemma_prompt_pack.py (evidence+numeric wire-in). file-specific add only.
   ollama_conductor_runner.py left MODIFIED/uncommitted -- your note still current:
   Claude's change = broadening its _RETRYABLE_GATE_CODES to mirror the quartet stage
   (added latex/json/causal/id_in_paragraph/new_number_present) to close the residual
   conductor-stage slip tail; that sits ON TOP of your ~192 uncommitted lines, so the
   commit decision stays operator-gated. (Tests after: 724 green, conductor suite 14.)

3. Canonical corpus wired for evidence grounding. Operator promoted the new bundle
   G:\corpus_md_export_20260612 (3903 papers, index<->md 3903/3903, alignment=VERIFIED)
   over the stale 5/19 index. DraftEvidenceSearcher now constructs in ~25s and returns
   relevant citations (validated on hydrothermal + mantle queries). Rule (Claude memory
   corpus-canonical-20260612): index bm25 path AND md_dir must be the SAME bundle.

4. Overnight improvement loop (operator-directed): per cycle ->
   gen (evidence+numeric, best-of-N) -> stitch -> adversarial audit (multi-agent
   Workflow) -> quality_report -> pick 3-5 critical improvements -> implement (edit
   task_specs) -> next cycle, until operator STOP.

## Cycle results (relay-safe metrics)

- cycle 1: u1 SUCCESS (best roll bound numeric 6/7 + evidence 4/5, clean, 63 words);
  u2 FAILED 3/3 on gemma_candidate_new_number_present (model wrote measured values as
  digits in prose); u3 weak (24 words, evidence 1/5). Subsection verdict = FAIL
  (load-bearing u2 absent -> non-sequitur).
- ENVIRONMENT FINDING: machine slept ~04:22 -> loop stalled (audit-completion
  notification AND scheduled fallback both could not fire until operator returned).
  Unattended overnight running needs PC sleep disabled.
- cycle 2: RUNNING now with improvements applied -> (a) global qualitative-reference
  rule (values in words only, bind id, no digits) targeting new_number; (b) retry
  budget 3->5; (c) u3 instruction -> substantive 2-3 sentences.
- Operator directive: finish cycle 2 (gen->audit->report) then STOP the loop; breather
  + plan next with Codex. No cycle 3, no sleep change.

## Artifacts I produced (all operator-local, OUTSIDE the repo unless noted)

Repo (committed 7a46da2): tools/paper-orchestra/local-llm/v0/gemma_paragraph_pipeline.py,
tools/paper-orchestra/writing-runner/v0/local_gemma_prompt_pack.py.
Repo (modified, uncommitted, gated): tools/paper-orchestra/local-llm/v0/ollama_conductor_runner.py.

Operator-local tooling (C:\Users\USER\AppData\Local\Temp\quartet_breakit):
- ledger_numeric_resolver.py (G2 duck-typed resolver, num_u<n>_ prefix filter)
- cir_u1_emit.py / cir_u1_measured_emit.py / cir_u2u3_measured_emit.py (G1: author
  CSV/table -> ledger_emit.emit_numeric_entry -> JSONL; pre_emit_gate PASS, blocker 0)
- overnight_cycle_gen.py (preflight + best-of-N + load-once DraftEvidenceSearcher +
  numeric resolver; writes draft.local.md + metrics.json)
- evidence_searcher_test.py, *_verify*.py (validation harnesses)

Operator-local outputs (C:\Users\USER\Documents\_codex_runs):
- phaseb/u{1,2,3}_*_entries.local.jsonl (numeric ledgers, gate PASS)
- overnight_loop/{LOOP_STATE.md, task_specs.local.json, cycle1/, cycle2/}
  (each cycle: draft.local.md [local prose, NOT relayed], metrics.json, quality_report.md)

Claude memories added: numeric-grounding-number-type, corpus-canonical-20260612,
preflight-before-long-model-runs.

## What you can REVIEW now (while cycle 2 runs)

1. The two committed files: is the evidence+numeric wire-in in local_gemma_prompt_pack
   and the produce_paragraph orchestrator in gemma_paragraph_pipeline sound / consistent
   with the contract + your other modules?
2. ollama_conductor_runner.py _RETRYABLE broadening: do you agree re-rolling on
   new_number_present / id_in_paragraph / causal_verb_overreach is safe (the gate still
   guarantees accepted output is clean), or does it mask a defect? This is the gated file.
3. Grounding strategy: is "emit measured values, not correlation rhos" the right call
   for these claim units, given your subsection history (822+826C+825+821)?
4. Loop architecture: preflight-before-long-run, best-of-N selection, audit->improve.

## Open decision points for the joint plan

- ollama_conductor_runner.py: operator accepts the mixed file as final, OR Claude splits
  the conductor-retryable change into a small standalone patch for clean review.
- Next target: continue overnight loop (with sleep disabled) to converge the CIR
  Discussion, OR hand-tune the 3 units, OR move to a different section/claim unit.
- Whether cycle 2's improvements actually fixed u2 (new_number) -- result pending; will
  post counts when cycle 2 audit completes.

Posture: Claude finishing cycle 2 then pausing the loop per operator. No new B/M/T
target beyond that. Awaiting your review + the joint plan.
