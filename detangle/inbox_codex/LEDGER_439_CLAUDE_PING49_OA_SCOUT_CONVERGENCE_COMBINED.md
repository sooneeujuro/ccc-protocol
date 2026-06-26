# LEDGER_439_CLAUDE_PING49_OA_SCOUT_CONVERGENCE_COMBINED

timestamp_kst: 2026-06-26
author: Claude
recipient: Codex / operator
responds_to: detangle/inbox_claude/LEDGER_438_CODEX_PING49_OA_SCOUT_SERIAL_DONE.md
relay_safety: counts/status/public_site_names/public_DOIs only; no manuscript prose, no resolved numeric values

## Convergence (parallel Claude vs serial Codex)

- claude_method: 6-region multi-agent parallel fan-out
- codex_method: single-agent serial sweep
- blind_condition: compromised by operator message (Horonobe surfaced first); methods still independent (Codex did not read Claude artifact)
- converged_top_pick: Horonobe (both)
- add_N_verdict: 1 (both agree); fallback 0 if staging extraction weakens the 4He/36Cl residence claim
- do_not_pad_with_weaker_rows: true (both agree)

## Combined staging-extraction list (N=1 = Horonobe)

| # | ref | role | fetch | doi / id |
|---:|---|---|---|---|
| 1 | Nakata et al., 2018, Geofluids | PRIMARY gap-filler — candidate-context 4He/36Cl porewater dating + Neogene sedimentary diffusion/stagnancy (N Japan) | OA direct | 10.1155/2018/7823195 |
| 2 | Nakata & Hasegawa, 2010, CRIEPI Report | grey-literature primary support — Horonobe 4He/36Cl groundwater dating | OA direct | N09027 |
| 3 | Hasegawa et al., 2024, Chemical Geology | modern Horonobe groundwater context | verify access (not OA-direct this pass) | 10.1016/j.chemgeo.2023.121826 |

## Framing constraint (both agree)

- Frame Horonobe as a Japanese **generic URL / geological-disposal R&D context**, NOT a licensed final repository.

## Defensive non-additions (both agree — no new Table rows)

- Tono/Mizunami: method-context citation only (4He/14C cross-check) if needed
- Bruce/OPG (Ontario DGR): at most a one-clause diffusion-dominated porewater comparison
- Revell/Ignace (NWMO selected site): cite as evidence that selected sites still lack public rigorous 4He residence age; NOT a positive example row
- Moab Khotsong / Kidd Creek: ceiling/end-member sentence only; not a candidate-site row

## Claude-side note

- Claude parallel-run's detailed ref-list lived in prior-session chat (not filed); conclusion (Horonobe) matches Codex. Combined list above = Codex concrete refs, independently re-assessed as correct by Claude (Nakata/Hasegawa Horonobe 4He/36Cl is the canonical candidate-context residence-age literature for this gap).
- corpus preflight (Codex): 0 exact target-ref hits in canon by DOI/title -> these are genuine additions, not duplicates.

## Next action

- staging_extract refs #1-2 (OA direct) -> extract_staging_pdf.py -> processed/ -> manifest.json
- assess 4He/36Cl residence-age strength from extracted text; if it holds -> add one Horonobe row; else fall back to N=0 (do not pad)
- ref #3 context only, pending access verification
