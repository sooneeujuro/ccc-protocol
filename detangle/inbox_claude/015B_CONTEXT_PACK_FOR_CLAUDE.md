VERDICT: ok

# Context pack for Claude Code continuation

This is a high-context handoff from Codex to Claude Code. It is meant for either the current Claude loop or a newly opened Claude Code session that has lost conversation context.

## Current repo/session

- Repo: `C:\Users\USER\Documents\ccc-protocol`
- Branch: `coop/detangle-20260615`
- Coordination convention:
  - Claude -> Codex: `detangle/inbox_codex/NNN_*.md`
  - Codex -> Claude: `detangle/inbox_claude/NNN_*.md`
- Always `git pull --rebase origin coop/detangle-20260615` before push.
- Do not hardcode task numbers. Scan all `NNN_*.md`.

## Operator correction that must not be forgotten

The normalization `FINAL_SUMMARY` does NOT mean the full job is done.

The operator explicitly corrected both agents:

- Keep the 5-minute loop active.
- Stop only if `detangle/STOP.md` appears or the operator explicitly says to stop/pause.
- "Done" means all pending work is truly done, including B/sidecar decision, PR merge decisions, figure re-extraction follow-up, and next-phase improvement planning.

Relevant files:

- `detangle/inbox_codex/014_FINAL_DONE.md`: Claude initially said loop ended.
- `detangle/inbox_claude/014C_KEEP_5M_LOOP_ACTIVE.md`: Codex relayed operator correction.
- `detangle/inbox_codex/015_CLAUDE_LOOP_ACK.md`: Claude acknowledged correction and confirmed loop active.

## Hard constraints

- B/sidecar write gate is closed until the operator explicitly says to write sidecars.
- Do not write corpus sidecars.
- Do not push corpus, sidecar, paper, index, or figure data.
- Do not merge PRs without operator approval.
- Do not run irreversible execution.
- Allowed safe outputs: coordination notes, vocab/normalizer code snapshots, aggregate reports, audit samples, statistics.

## What was completed

### Normalization loop

The VP-NORM-1 variable/instrument normalization dry-run loop reached honest ceiling.

Final status from Claude:

- coverage: `75.4%` after Nd/Na and FeO_total pre-B patches
- precision: final sampled audit around `99.2%`
- regression probe set: `20/20 PASS`
- no sidecars written
- no corpus pushed
- spend: `$0`

Main artifact:

- `detangle/norm_artifacts/FINAL_SUMMARY.md`

Supporting latest artifacts:

- `detangle/norm_artifacts/normalize_corpus.py`
- `detangle/norm_artifacts/coverage_cycle6.json`
- `detangle/norm_artifacts/audit_sample_cycle6.json`
- `detangle/norm_artifacts/OVERNIGHT_STATUS.md`

### Ceiling decision

Both agents agreed:

- `90%` raw coverage is not precision-safe for this night run.
- The remaining tail is too singleton-heavy, ambiguous, OCR-ish, or intentionally blocked.
- Do not force-match to chase the original 90%.
- Report both raw coverage and adjusted normalizable-denominator coverage.

Relevant files:

- `detangle/inbox_codex/013_CEILING_REACHED.md`
- `detangle/inbox_claude/013_CEILING_FINAL_VERDICT.md`
- `detangle/norm_artifacts/FINAL_SUMMARY.md`

### Important late bug fixed

Codex noticed `Nd` and `Na` were being classified as junk because lower-case `nd`/`na` sentinels were case-folded before element matching.

Claude fixed:

- `Nd -> Nd_conc`
- `Na -> Na_conc`
- dotted/lower junk like `n.d.` and `n/a` remains junk

Relevant files:

- `detangle/inbox_claude/013B_ND_NA_SANITY_FINDING.md`
- `detangle/inbox_codex/014_FINAL_DONE.md`

### Final regression themes

Keep these in the regression probe set before any B/write:

- FeOT / FeO_total / total iron as FeO
- REE explicit lists containing Y / yttrium
- TREE as temperature acronym
- CO2 dissolved, mmol/mol, gas/fluid/phase variants
- F(ppm), F-, and F vs fraction collision
- Fe valence and Fe-valence ratios
- 3H/3He age
- Age-grid misfit
- P(CO2) / P(CO2) partial pressure vs phosphorus
- Pressure(GPa) / unit-agnostic physical ids
- LaN/YbN and normalized-ratio cues
- Nd/Na vs nd/na junk collision

## Other completed audit tasks

Earlier detangle tasks:

- `001`: independent audit cross-check, Codex verdict ok.
- `002`: corpus guard verify, Codex verdict ok.
- `003`: A4/A5 delta review, Codex found issues/nuance.
- `004`/`005`: PR#15/#16 verification review and recheck, Codex found then rechecked fixes.

Normalization tasks:

- `006`: first normalizer build, Codex found precision issues.
- `007`: cycle 3 re-audit, Codex found remaining false matches and coordination bug.
- `008`: cycle 4 retro-audit, Codex found targeted precision leaks.
- `009`: refreshed cycle 4 re-audit, still issues.
- `010`/`011`: cycle 4.1/4.2 passed gate.
- `012`: cycle 5 passed precision; ceiling reassessment started.
- `013`: cycle 6 ceiling and FINAL approved.
- `014`: Claude final done.
- `014B`: next-phase improvement memo.
- `014C`: operator correction to keep loop active.
- `015`: wake/ACK round, loop confirmed alive.

## Figure re-extraction/refill

Operator asked us to remind Claude Code about paper figure re-extraction/refill.

Known status from repo:

- Figure track remains an environment block.
- About 830 figures are tied to datalab machine + NAS availability.
- Repo-side artifact says operator/datalab/NAS action is needed.
- `014B` asked Claude to keep this visible.
- `015_CLAUDE_LOOP_ACK.md` says repo has no dedicated figure re-extraction progress artifact beyond the reminder, and remote-access memo is likely outside repo.

Action for Claude:

- Keep checking/reporting figure re-extraction status if a new clue appears.
- Do not push figure data.
- If operator provides remote memo/location/NAS access, inspect/report status.

## Next-phase improvement planning

Operator asked that this be remembered even if they do not repeat it later.

After B/sidecar decision point or operator resume, proactively bring up improvement planning:

- Claude prepares 7 improvement ideas.
- Codex prepares 7 improvement ideas.
- Exchange and critique ideas.
- Focus on simple, effective, reversible improvements.
- Emphasize strengths of BM25, BGE-M3, and vector DB structure.
- If both agents independently agree an idea is good and reversible, implementation is authorized in that later phase.
- Do not implement improvement ideas now just because this note exists.

Candidate idea space to revisit:

1. Field-aware hybrid retrieval: separate BM25/BGE-M3 indexes for title, abstract, figure captions, tables, sidecars, methods, references.
2. Parent-child retrieval: small chunks for matching, parent paper/section/figure records for provenance and citation.
3. Sparse/dense score diagnostics: expose BM25 score, BGE score, fusion rank, and disagreement flags.
4. Canonical-vocabulary query expansion: variables, instruments, maps, figures, synonyms, isotope/oxide/phase variants.
5. Hard-negative regression sets: false-match probes from this normalization run become retrieval/evaluation guardrails.
6. Reversible overlays: write candidate sidecar enrichments as overlay/diff layers until operator accepts B.
7. Tail dashboards: classify failures as lexical miss, semantic ambiguity, OCR/noise, phase/unit ambiguity, missing vocab, or blocked group.

Memory hook:

- If the operator resumes and does not explicitly say "let's design improvements", do not assume cancellation.
- After B/sidecar decision point, ask whether to begin the 7+7 idea exchange.

## Current loop behavior

Each wake:

1. Check `detangle/STOP.md`.
2. Pull branch.
3. Scan `detangle/inbox_codex/*.md` and recent `detangle/inbox_claude/*.md`.
4. If new work exists, handle it.
5. If 3 quiet wakeups pass while expecting peer action, send a concise wake/ping note.
6. Otherwise stay quiet.

Current known latest state:

- Claude ACKed loop active in `detangle/inbox_codex/015_CLAUDE_LOOP_ACK.md`.
- Codex loop is active under `cccp-detangle-5m-loop`.
- No STOP.md.
- B gate remains closed.

## If you are a newly opened Claude Code session

Do this first:

```powershell
cd C:\Users\USER\Documents\ccc-protocol
git fetch origin
git checkout coop/detangle-20260615
git pull origin coop/detangle-20260615
Get-Content detangle\inbox_claude\014C_KEEP_5M_LOOP_ACTIVE.md
Get-Content detangle\inbox_codex\015_CLAUDE_LOOP_ACK.md
Get-Content detangle\norm_artifacts\FINAL_SUMMARY.md
```

Then continue the watcher. Do not restart normalization work unless the operator asks.
