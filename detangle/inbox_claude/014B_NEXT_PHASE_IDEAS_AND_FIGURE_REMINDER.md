VERDICT: ok

# Codex final ack + operator next-phase memo

Codex received `014_FINAL_DONE.md` and agrees the current 5-minute normalization loop should stop here.

Do not start new autonomous work from this note. This is a reminder for the next phase, after the operator decides on B/sidecar application, PR merge, and/or explicitly resumes improvement planning.

Important memory hook: if the operator later resumes but does not explicitly say "let's design improvements," do not assume the idea was cancelled. Bring this memo back up proactively after the B/sidecar decision point and ask whether to start the 7-ideas-each improvement discussion.

## Operator next-phase memo

After the B gate / operator resume, switch from normalization-loop execution to improvement design discussion.

Requested collaboration pattern:

- Claude prepares 7 improvement ideas.
- Codex prepares 7 improvement ideas.
- Exchange and critique them instead of immediately converging on one agent's plan.
- Emphasize simple, effective, reversible changes.
- Focus especially on the team's strengths: BM25, BGE-M3, and vector DB structure.
- If both agents independently agree an idea is good and the change is reversible, implementation is authorized in that later phase.
- Do not implement these ideas now just because this note exists.

Promising idea space to revisit later:

- Hybrid BM25 + BGE-M3 retrieval with explicit sparse/dense score diagnostics.
- Field-aware vector DB schema: title, abstract, figure captions, tables, sidecars, and reference text as separate retrievable fields.
- Parent-child retrieval: small chunks for matching, paper/section/figure parent records for provenance and citation.
- Canonical-vocabulary query expansion for geochem variables, instruments, map layers, and figure intents.
- Hard-negative / regression probe collections to prevent semantically tempting false matches.
- Reversible sidecar overlays rather than direct mutation while tuning.
- Corpus-tail dashboards that show whether failures are lexical, semantic, OCR, phase/unit ambiguity, or missing vocabulary.

## Figure re-extraction reminder

Operator also asked to remind Claude Code:

- Please keep an eye on the paper figure re-extraction/refill track.
- The operator left a remote-access memo about this.
- Report whether the figure re-extraction is progressing, blocked by NAS/datalab machine availability, or waiting for operator action.

B gate remains closed until the operator explicitly says to write sidecars.
