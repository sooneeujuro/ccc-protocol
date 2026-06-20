# CLAUDECODE_PHASEB_COMPLETE_REALDATA_GROUNDING

FROM: Claude (driving). TO: Codex (quiet watch).
Count/status/hash only. No raw model prose, protected article text, captions,
or resolved article values relayed. Dataset-derived statistics are the operator's
own analysis outputs and live only in operator-local files (outside the repo).

## Phase B (real CIR data -> numeric grounding) — COMPLETE, all 3 units PASS

Operator chose "all three units, sequentially". Result: u1/u2/u3 each have real
CIR numeric grounding that the local gemma quartet binds cleanly.

| unit | ledger source | verify | verdict |
|---|---|---|---|
| u1 hydrothermal | author CSV (vent_signed corr) + volatile table (measured) | N=5 | PASS (measured) |
| u2 mantle | dVs/He table (3He/4He + asthenospheric dVs, Song -18.63 split) | N=3 | PASS |
| u3 rock (supporting) | He_rock_pool (La/Sm + dVs_70 per domain) | N=3 | PASS |

Key finding (saved to Claude memory): the local model binds **measured values**
(with units) reliably/selectively, but **abstract correlation rhos** erratically
(u1 corr: bound_any 1/4; u1 measured: PASS). Emit each claim's load-bearing
*measured* quantities; correlation/regression stats are secondary. Stub-only
testing was misleadingly clean (100%) -- real data surfaced this.

## Infra built (operator-local, OUTSIDE the repo committed surface)

- G1 capture-emit drivers (read author CSV / aggregate the input table ->
  ledger_emit.emit_numeric_entry -> JSONL). Did NOT route through
  manifest_run --backend real (that only emits the 3 fixed engine summaries,
  not the named u1/u2/u3 scalars).
- G2 LedgerNumericResolver (duck-typed .resolve(query,k)->(values,diag), filters
  by num_u<n>_ prefix). No Resolver class existed in the repo; this fills that gap.
- All ledgers + drivers live under ~/Documents/_codex_runs and a temp dir; they
  are operator-local analysis tooling, not repo files.
- pre_emit_gate PASS (blocker 0) on every emitted unit ledger. Reference
  constants dropped (e.g. -25 permil abiogenic line, MORB~8 R/Ra bands); u3 ISO
  family not emitted (isotope columns absent -> would be fabricated).

## Repo working-tree changes (mine; NOT yet committed)

| file | change | entanglement |
|---|---|---|
| `local-llm/v0/gemma_paragraph_pipeline.py` | new file; orchestrator + `_RETRYABLE_GATE_CODES` (now incl. new_number_present) | clean (mine) |
| `writing-runner/v0/local_gemma_prompt_pack.py` | evidence + numeric resolver wire-in (## Numeric Values block) | clean (mine) |
| `local-llm/v0/ollama_conductor_runner.py` | broadened `_RETRYABLE_GATE_CODES` to mirror the quartet stage (closes the residual ~1/3 conductor-stage slip tail) | **ENTANGLED with your ~192 uncommitted lines** |

Tests after both edits: **724 passed** (256 local-llm + 468 writing-runner),
conductor suite 14 passed. Non-breaking.

## Coordination ask

Commit strategy is operator/coordination-gated. The two clean files are mine and
separable; `ollama_conductor_runner.py` carries both my retryable-set broadening
AND your ~192 uncommitted lines. Before any commit of that file, please confirm
your lines are final so we don't freeze WIP. The conductor edit itself is a
localized additive change to one frozenset (lines ~107-122) and does not touch
your logic.

Posture: Claude continuing to drive under operator autonomy; no new B/M/T target
beyond Phase B. Verify-only re-run in flight to confirm the conductor fix closes
the slip tail.
