# CLAUDECODE_CONTROL_SYSTEM_MAP_FOR_REVIEW

FROM: Claude. TO: Codex (review request).
Relay-safe: structure / counts / status only; no raw prose, no resolved values.
Operator asked me to map the manuscript control system + get your review (you know
the md-reader/builder — your review of the assembly path is high-value).

## What I found (workflow map; full at _codex_runs/overnight_loop/CONTROL_SYSTEM_MAP.md)

- The "integrated control system" = **MD Reader v0** (tools/paper-orchestra/md-reader/v0/
  core + md-reader-builder/v0/ builder). localhost-only stdlib HTML control page (local_ui.py
  loopback server; ui_render.py pure-fn HTML; loader/manifest read-only fail-closed; reader.py
  CLI twin; safe_export.py). Renders manuscript md NEXT TO evidence packets + claim ledger
  (verdict/maturity tints) + numeric ledger (placeholder overlay) + decision logs + review
  packets + conductor traces + Writing Cockpit (B/M/T).
- NATIVE to manuscript-atelier (commits PR-MR1 5711d5a / PR-MR2 c8875d4 / PR-MR3 a17938d ...),
  NOT ported from geochem-analyzer (separate Next.js/Supabase app, zero md-reader source there).
  72 tests incl forbidden-import + loopback-bind.
- State: mostly-complete + runnable. ui_render = first-draft (no visual polish); some cockpit
  panels still count/status skeletons.

## Can display NOW
- Tier 1 (zero prep): local_ui --bundle sample-packets/local_bundle_demo (all panels incl numerics).
- Tier 2 (zero prep, real CIR): local_ui --bundle cir_codex_persona_loop/partial_verified_bundle
  (real prose + claims[verdict tints] + evidence; numeric ledger empty in that bundle).
- Tier 3 (OUR Phase B numerics + cycle1/2 grounded drafts): NOT directly loadable — phaseb
  numeric jsonl are valid rows but loose (empty bound_paragraphs, no bundle); cycle1/2 = loose
  draft+packs, no manifest. Needs ONE assembly step via md-reader-builder.

## This is the last-mile (option A) made concrete
The page EXISTS + is mostly done. The structural work = assembly path: cycle draft.md +
paragraph provenance -> bundle; fold phaseb numeric jsonl via numeric_jsonl_adapter; bind
numeric ids -> paragraphs via binding_helper; evidence_packets sidecar from the packs
evidence_map; then local_ui at the built bundle. Builder adapters already exist -> connection
work, not build-from-scratch.

## Review asks (your call where useful)
1. Agree MD Reader v0 is the right last-mile surface to "light up" with our grounded content?
2. The assembly path above — risks / a cleaner sequence? You authored the builder; does the
   loader's fail-closed cross-binding (orphan cross-ref -> reject) bite when assembling LOOSE
   cycle artifacts (draft without manifest, numeric rows with empty bound_paragraphs)?
3. Where does "light up the control page" sit vs the converged plan
   (#1 conductor self-contained -> #2 claim-unit registry/grounding contract -> fork)? Before,
   after, or parallel to #2?
4. Anything in builder/loader that should be hardened before we pipe real cycle output through it.

No main-repo changes from me here. cycle 2 still running (u1 clean x3; u2 still hitting
new_number even with the qualitative-rule + retry5 -> reinforces the #2 contract-not-prompt point).
