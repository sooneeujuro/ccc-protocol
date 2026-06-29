# CLAUDECODE_FGP_APPLY1_DESIGN — FGP post-hoc QC pass for a finished manuscript

`2026-06-26` · Claude (design house) → Codex (fab). TSMC model: Claude specs, Codex builds, Claude reviews.
Relay-safe (technical contract only; no manuscript prose, no ForGoodPaper prose, no resolved numeric values).

## Why
The FGP **source** layer (`tools/paper-orchestra/fgp/v0/`) is complete + live: `FGP_SOURCE.local.json` →
`fgp_root = C:\Users\USER\Documents\ForGoodPaper`, `phrase_corpus_enabled=true`; `fgp_source.py.load_forbidden_phrase_corpus()`
extracts forbidden craft phrases from Plated/cards, Plated/handbook, Cooked, Chopped, Original (Personal/writing excluded);
checker is count/hash-only; R-a..R-h enforced. **Packaging is DONE and it is already standalone-attachable — do NOT fold FGP
into the corpus** (corpus = inject-evidence; FGP = route-only / never-echo; opposite roles, conflating them breaks the
anti-echo design).

The one missing piece: a **consumer that APPLIES FGP to an existing, hand-written manuscript** (e.g. `hlw_draft_v11.2`).
Everything built so far targets the gemma *writing* pipeline (generate-then-judge ablation). We need a post-hoc QC pass that
takes a finished `.md` + the FGP source and emits **suggestions only** — no rewrite, no FGP prose injection.

## Module
`tools/paper-orchestra/fgp/v0/fgp_apply.py` (+ `tests/test_fgp_apply_synthetic.py`). Reuse, do not rebuild:
- `fgp_source.py` — `load_config()` / `load_forbidden_phrase_corpus()` (real phrases, local caller only).
- `fgp_routing.py` — `POSTHOC_GATE_ORDER = (prose_vocab_gate, anchor_structure_gate, llm_critique_suggestion_only)`.
- the existing generated-draft **overlap guard** (shingle/verbatim) from `fgp_prompt_boundary.py` / `fgp_prose_ablation.py` —
  apply it to the manuscript text instead of a generated draft.

## CLI / contract
`python fgp_apply.py --draft <manuscript.md> --out <report.local.md> [--require-config --require-phrases] [--no-llm]`
Pipeline (in `POSTHOC_GATE_ORDER`), each gate appends to a local report; none mutates the draft:

1. **prose_vocab_gate** (deterministic, no model): line-anchored flags from a committed *generic craft rubric*
   (weak/cliché verbs, hedge-cluster density, banned-vocab patterns, over-hedging). The rubric is a generic,
   committed wordlist/regex set — **NOT** ForGoodPaper prose. Output: `{line, span, rule_id, note}` flags.
2. **anchor_structure_gate** (deterministic): every load-bearing claim has a citation/evidence anchor; every figure/table
   reference resolves; section arc complete (intro promise ↔ body ↔ conclusion). Output: structural flags
   (e.g. `claim_unanchored`, `figref_unresolved`, `arc_gap`). (Reuse the figure-ref integrity idea.)
3. **llm_critique_suggestion_only** (optional; `--no-llm` skips): executor-injected, provider-neutral critique using the
   FGP rubric dimensions the ablation rewards (problem-naming precision, falsifiability framing, structural completeness).
   **Suggestions only — no rewrite, no rephrased lines.** Runs LOCALLY (manuscript stays operator-local; never relayed).
4. **phrase_overlap_guard** (always, fail-closed under `--require-phrases`): manuscript text vs `load_forbidden_phrase_corpus()`
   → verbatim/shingle overlap count. Expected ~0 for a science manuscript; it is the anti-echo safety check.

## Output: `<draft>_FGP_QC.local.md` (local-only, gitignored `.local.` infix)
- per-gate flags + suggestions (referencing the DRAFT's own text only)
- overlap-guard result (count + which shingles, LOCAL report only)
- a relay-safe tail block (counts/enums/hash only) suitable for a LEDGER.

## Safety / contracts (honor existing FGP discipline)
- **No mutation** of the manuscript; suggestions only.
- **No ForGoodPaper prose anywhere in committed code/tests or any relayed surface.** The report may hold overlap hits
  LOCALLY but the relay/LEDGER surface is counts/hash/enums only (extend the existing checker posture).
- Report is **local-only** (`.local.md`); fail-closed (`--require-config --require-phrases`) before loading phrases (R-h);
  empty phrase corpus → fail/warn.
- Manuscript prose is operator-local copyright → the LLM critique runs locally; **never relay the draft**.
- Honor R-a..R-h (no committed abs paths, no path printing, synthetic-only fixtures).

## Tests (synthetic-only)
- vocab gate flags a synthetic weak-vocab/over-hedge line; structure gate flags a synthetic unanchored claim + a dangling
  figref; overlap guard catches a synthetic planted forbidden phrase and reports 0 on clean text; `--require-phrases`
  fails closed on empty corpus; report is suggestion-only (asserts draft bytes unchanged); no source prose in committed
  fixtures or the relay tail.

## Acceptance / red-paths
- AP1 end-to-end on a synthetic draft → report with all four sections, draft unchanged.
- AP2 relay tail = counts/enums/hash only (grep: zero draft lines, zero forbidden phrases).
- RP1 missing/empty FGP config or phrases under `--require-*` → fail-closed.
- RP2 planted ForGoodPaper-style phrase in the synthetic draft → overlap guard count > 0, flagged.

## After build
Run `fgp_apply.py --draft hlw_draft_v11.2_2026-06-25.md` (and v11.3 once you cut it) → produce the FGP QC report; reply with a
relay-safe LEDGER (gate flag counts, overlap count, status). Operator/Claude then review the suggestions (this is the
"apply FGP to v11.x" the operator asked for — gates + anti-echo, NOT a rewrite, NOT content injection).

NB on the operator's questions: FGP content is at `C:\Users\USER\Documents\ForGoodPaper` (NOT G drive; G has Paper_Atelier);
the local config already points there. Packaging = already standalone; this PR is the consumer, not a repackage.

relay-safe: technical contract only. (local date 2026-06-26)
