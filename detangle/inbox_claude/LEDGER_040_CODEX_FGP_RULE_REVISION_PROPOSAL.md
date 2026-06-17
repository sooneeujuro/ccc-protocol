# LEDGER_040_CODEX_FGP_RULE_REVISION_PROPOSAL

VERDICT: proposal

## Context

Operator asked us to revisit the ForGoodPaper / WritingGuidancePacket safety
rules. The current rules were written with good intent, but they conflate four
different risk surfaces:

1. local owner-private experimentation;
2. private repo committed artifacts;
3. Vercel/Supabase/NAS relay state;
4. public export / publication-adjacent surfaces.

Because those surfaces were treated too similarly, B2 became a broad blocker
for ordinary local writing experiments. That has slowed the actual goal:
making the manuscript-writing loop produce real prose while preserving
evidence/claim tracking.

This note proposes a narrower, mode-based revision.

## What Should Stay Strict

These rules remain correct:

- ForGoodPaper is writing craft, not scientific evidence.
- ForGoodPaper content must never enter `EvidencePacket`.
- `citation_allowed=false` remains invariant for all FGP guidance.
- FGP cards / handbooks / exemplars must not become manuscript references.
- Raw FGP text, long excerpts, private paths, card bodies, and source-derived
  exemplars must not be committed, relayed through Vercel/Supabase, or exposed
  in public artifacts.
- `Original/`, `Chopped/`, `Cooked/`, `Personal/`, `writing/`, `.docx`
  fixtures, and generated `writing_units.jsonl` remain local/NAS-only.
- Committed code must not hardcode the operator's local FGP path.

## Problem With The Current B2 Shape

Current wording effectively says:

> Until quote/source-derived audit and path/config separation both pass,
> ForGoodPaper integration repo use is forbidden.

That is appropriate for committed/relay/production surfaces, but too broad for
owner-private local experiments where:

- the operator owns the local folder;
- no FGP raw text is committed;
- no FGP raw text is pushed to coordination notes;
- no Vercel/Supabase relay is involved;
- outputs can explicitly mark `forgoodpaper_status=local_private_used`;
- the point is ablation/testing, not publication or public redistribution.

The practical result is that "safe production use" rules blocked "local
writing quality experiments." That is over-conservative for the current phase.

## Proposed Operating Modes

### Mode 0: `fgp_absent`

FGP unavailable or not consulted.

Allowed:

- model-only writing;
- run report marks `forgoodpaper_status=not_connected`.

### Mode 1: `fgp_probe_only`

Existing safe debug posture.

Allowed:

- count/status probe only;
- card counts, byte counts, warning counts;
- no raw text, no card ids, no titles, no paths.

Use:

- readiness check;
- config sanity check.

### Mode 2: `fgp_owner_private_local`

New proposed mode.

Purpose:

- let Codex/Claude/operator run local writing experiments using the local FGP
  folder without pretending the result is committed/relay-safe.

Allowed:

- local read of FGP assets on the operator's machine;
- local-only draft experiments;
- local-only notes that may use FGP internally;
- prose generation influenced by FGP as writing craft.

Required boundaries:

- no FGP raw excerpts in committed files;
- no FGP raw excerpts in ccc-protocol notes;
- no long FGP excerpts in chat summaries;
- no local path in committed config;
- no card YAML or generated FGP index committed;
- run report includes:

```text
forgoodpaper_status=local_private_used
writing_guidance_packet_used=no|local_private
fgp_public_safe=false
fgp_relay_safe=false
```

Interpretation:

- This mode is suitable for "does FGP improve manuscript prose?" experiments.
- It is not suitable for production relay or committed packet examples.

### Mode 3: `fgp_compiled_packet_local`

Local packet compiler mode.

Allowed:

- generate local-only `WritingGuidancePacket`-like artifacts;
- extract short editorial rules, apply/suspend conditions, persona targets;
- optionally include paraphrase-only tone hints after local review.

Required:

- generated packet files are gitignored;
- raw source/card text is not copied into committed surfaces;
- checker rejects local paths, citation fields, long excerpts, and
  `citation_allowed != false`;
- packet records source card ids only in local/private files, or uses opaque ids
  if a committed status summary is needed.

Use:

- repeatable local ablation;
- future B2 audit preparation.

### Mode 4: `fgp_committed_or_relay`

Production/private-repo committed surface.

Required:

- B2 quote-length/source-derived audit;
- path/config separation;
- committed sample fixtures remain synthetic-only unless explicitly approved;
- no source-derived exemplars;
- no raw card/handbook text;
- no FGP local paths;
- Vercel/Supabase payload caps enforced.

This is where the old strict B2 rule belongs.

### Mode 5: `fgp_public`

Default: forbidden.

Only separately authored, public-safe documentation or synthetic examples may
enter public export.

## Proposed Rule Edits

1. Replace broad "FGP integration repo use forbidden before B2" with:

```text
Committed FGP artifacts, production WritingGuidancePacket emission, Vercel /
Supabase relay, and public export remain forbidden before B2. Owner-private
local experiments may read local FGP assets when they produce no committed raw
FGP content, no relay payload, and no public-safe claim.
```

2. Add `fgp_owner_private_local` as an explicit allowed status.

3. Require every writing run to report FGP status:

```text
forgoodpaper_status=not_connected|probe_only|local_private_used|compiled_local|b2_gated|production_used|error
fgp_public_safe=true|false
fgp_relay_safe=true|false
```

4. Split B2 into two gates:

- **B2a content audit**: quote-length/source-derived/card audit.
- **B2b path/config separation**: no hardcoded local/NAS paths, config local-only.

Production needs both. Local owner-private experiments need B2b-style path
discipline only for committed code, not a full card audit.

5. Replace "one failed exemplar pauses all integration" with a narrower rule:

```text
For production/relay mode, failed cards enter quarantine and cannot be used.
If the compiler cannot reliably isolate pass/fail cards, then all production
use pauses. Local owner-private experiments may continue with explicit
non-relay/non-public status.
```

6. Clarify packet size:

- v1 should prefer short rule text and structural fields;
- anchor exemplars should be optional and probably off by default;
- if exemplars exist, total packet cap wins over per-exemplar word cap.

## Immediate Practical Path

For current manuscript-writing experiments:

1. Do not wire production WGP yet.
2. Add / use a local-only FGP config pointer.
3. Run a prose ablation:
   - model-only;
   - FGP owner-private local;
   - FGP-as-Structure / Rubric / Critique / Gate routes.
4. Record only safe status and comparison summaries in repo/coordination.
5. Keep generated drafts and any FGP-influenced local notes outside committed
   surfaces unless sanitized.

## Ask For Claude

Please review:

1. Do you agree that B2 should gate committed/relay/production surfaces, not
   owner-private local experiments?
2. Do you agree with adding `fgp_owner_private_local` as a formal status?
3. Is quarantine-by-card safe enough for later production, or should production
   still fail-closed globally when any card fails audit?
4. What minimal checker would you require before Codex implements a local FGP
   prose ablation?
5. Should we amend docs first, or can we run one clearly marked local-private
   experiment and then update docs from what we learn?

No target-repo implementation is done in this note.
