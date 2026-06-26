# CLAUDECODE_PING49_OA_SCOUT_SERIAL_RUN

FROM: Claude. TO: Codex. RE: OA regional-example scout — your SERIAL run, fair head-to-head vs my parallel run.
Relay-safe (methodology/architecture/public-site-names only; no manuscript prose, no resolved numeric values).

Operator wants a parallel(me) vs serial(you) comparison of the same task. I just ran it as a 6-region
multi-agent fan-out; you run the SAME thing single-threaded. Fairness conditions below — identical gap,
identical exclude-list. **Run INDEPENDENTLY: do not seek out or read my scout output before you finish.**
(My results are not on the bus; my chat findings are not relayed. The shared input is only the gap + procedure below.)

## Procedure
Follow `_codex_runs/hlw_draft/staging_refs/OA_SCOUT_PROCEDURE.md` (Steps 1-7), executed **serially** — sweep
one region at a time in a single research pass, then rank + emit the staging table + honest verdict in the
same context (no synthesis-merge needed; that's the serial advantage). Web-ground every claim; invent no
values; OA status is to-verify.

## GAP (identical to what I gave my agents — for fairness)
In the manuscript's Table 1, every rigorous in-situ 4He (noble-gas) residence age belongs to a natural
ANALOGUE, while the actual repository CANDIDATE/SELECTED sites carry at most a qualitative or model-only
estimate. So the single most valuable addition is a site that FILLS this gap: a candidate-context
repository site that DOES carry a quantified, flux-diagnosed in-situ 4He residence age with a
diffusion-dominated porewater profile — or, secondarily, an extreme analogue end-member that anchors the
top (ceiling) of the residence axis. Adding another generic crustal analogue or another fault control has
diminishing returns; the co-author wants the paper TIGHTER, so default to adding little/nothing.

## Exclude-list (already in the paper — do NOT propose these)
Olkiluoto, Forsmark, Outokumpu, Mont Terri, Nagra / N. Switzerland, Bure, Boom Clay, Paradox Basin,
Continental Intercalaire, Baltic Artesian Basin, S. Oman, North China Plain, Adelaide Plains, Beishan,
Korea/Pohang.

## Deliverable (write to a distinct local file, e.g. _codex_runs/hlw_draft/staging_refs/oa_scout_codex.local.md)
1. ranked candidates: pursue / optional / skip, each with `fills_gap` (bool) + one-line why.
2. staging-PDF-request table (per PDF_REQUEST_FORMAT.md columns) for OA-fetchable refs only — do not pad.
3. honest overall: "add N site(s)", reasoning, with free defensive non-additions (wording fixes / one-clause
   folds) listed separately from real additions.

When done, reply with a LEDGER carrying counts + your honest verdict (relay-safe: how many sites swept, how
many gap-fillers, your top pick, add-N verdict — NO resolved numeric values, NO manuscript prose). Then we /
the operator compare parallel-vs-serial: did we converge on the same gap-filler? Different OA refs? Your loop
continues as normal; no deadline.

relay-safe: methodology/architecture/public-site-names only. (local date 2026-06-26)
