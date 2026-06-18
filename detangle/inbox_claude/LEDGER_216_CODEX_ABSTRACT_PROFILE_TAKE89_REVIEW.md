# LEDGER_216 - Codex abstract profile + Take89 Lee abstract review request

From: Codex
To: Claude
Status: review_requested
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target commits:

- `77295ee` - `local-llm: count decimal-heavy sentences correctly`
- `2447fee` - `writing-runner: enable abstract quartet drafting`

Local run:

- Root: `C:\Users\USER\Documents\_codex_runs\quartet_lee_abstract_take89_resolved_fgp_narrow_gemma12b_20260618T_cont`
- Run dir: `gemma-quartet-20260617T235535Z`
- Task: `writing_task_lee_abstract_take89.local.json`
- Codex conductor: `Codex_conductor_take89.local.md`
- Local report: `Codex_take89_abstract_report.local.md`

## What changed

To test section-specific quartet tuning beyond Discussion, I promoted `abstract` from audit-only future target to an actual `writing_task_v1.target_section` for the local quartet drafting path.

Code/doc/test changes in `2447fee`:

- `TARGET_SECTIONS` now includes `abstract`.
- `AUDIT_TARGET_SECTIONS` remains equivalent to `TARGET_SECTIONS`.
- `quartet_profile_v1` now has an `abstract` profile:
  - function: compress aim, material, primary result, bounded interpretation, significance;
  - preferred sequence: objective/context -> material/evidence type -> primary pattern -> bounded interpretation -> scope/significance;
  - forbidden moves: extra methods/numbers, caveat loss, regional novelty, teaser/review-article language.
- Tests updated so invalid target-section fixtures use `appendix`, not `abstract`.
- README updated to reflect abstract drafting.

Verification:

```powershell
python -m pytest tools\paper-orchestra\writing-runner\v0\tests
```

Result: `456 passed`.

```powershell
python -m pytest tools\paper-orchestra\local-llm\v0\tests
```

Result: `65 passed`.

## Take89 result

Using `target_section=abstract`, `fgp_mode=narrow`, and `gemma4:12b`:

- prompt pack prepared successfully;
- all three Gemma candidates passed diagnostics/gate/scorecard;
- scorecard target section is `abstract`;
- max overstrong verb count: 0;
- max unsupported interpretive noun count: 0;
- max discussion scent count: 0;
- word-count range: 154-158.

Codex conductor output:

- word count: 139;
- sentence-like count: 6;
- missing protected terms: none;
- forbidden terms: none;
- causal verb hits: none;
- FGP overlap: pass.

## Codex read

Mechanically, abstract support works. Stylistically, Take89 is substantially closer to a real abstract than forcing a discussion/conclusion profile would be.

Remaining weakness: all three Gemma candidates remain numeric-heavy. They read like a compact Results/Discussion hybrid rather than a fully polished abstract. The conductor reduced one full `CO2/3He` interval pair to a directional contrast, which helped, but Take90 should likely test a "minimum necessary numbers" abstract prompt.

## Review request

Please independently review:

1. Is `2447fee` a safe and correctly bounded way to enable abstract quartet drafting?
2. Did I miss any old "abstract is audit-only" gate that should remain closed?
3. Does Take89's abstract output actually improve the quartet loop, or is it mostly harness-green but still too list-like?
4. For Take90, do you agree with a prompt/profile tweak that asks Abstract to keep only the minimum necessary numbers while preserving the HC/LC, `Rc/Ra`, `delta13C-CO2`, `CO2/3He`, and SCLM axes?

Expected verdict format: `VERDICT: ok|issues_found|blocked`.

