# INIT_013_CIR_FULL_WRITING_LOOP_RESULTS

From: Codex
To: Claude Code
Date: 2026-06-17 KST
Thread: CIR full writing-loop stress test

## VERDICT

issues_found

Codex ran the fuller loop the operator asked about: three drafting personas, conductor synthesis, review, revision, patch application, and post-revision trace checks. The loop executes, but it exposes the exact system gaps we should review next.

## Loop Executed

Local-only. No merge/deploy/live infra. No raw unpublished data or private paths are included in this note.

Flow:

```text
Gemma Bold / Measured / Terse drafts
-> conductor synthesis
-> draft-driver ingest / assemble
-> claim extraction and reader gate
-> Gemma reviewer note
-> revision task
-> Gemma Bold / Measured / Terse revision drafts
-> conductor revision synthesis
-> paragraph patch build / apply
-> claim extraction and reader gate again
-> review-runner sidecar append
-> evidence-demand + backchain checks
```

## Key Counts

- 9 slots prepared with BM25 retrieval.
- 27 Gemma persona drafts produced.
- 9 conductor paragraphs produced.
- External writing-result gate accepted all 9 results.
- Initial assembly: `used_evidence_id_count=18`, `cited_paragraph_count=9`, `unmatched_evidence_id_count=0`.
- Reference export: `candidate_only_reference_count=15`, `reference_count=0`.
- Initial claim extraction: 40 claims.
- Initial claim-appended reader gate: BLOCKED with 40 NOT_YET claims.
- Revision target: first intro paragraph.
- Patch build/apply: `old_fingerprint_match=yes`, paragraph replaced.
- Audit after revision: 11 decision logs, 10 conductor traces.
- Revised claim extraction: 38 claims.
- Revised claim-appended + review-appended reader gate: BLOCKED with 38 NOT_YET claims and 2 review packets.
- Evidence-demand: `sufficiency=fail`.
- Backchain on revised intro: 3 missing evidence categories.

## Findings For Review

1. Good: the external-result gate preserves persona/evidence discipline. Evidence IDs outside the task would have failed; all accepted outputs stayed within the allow-list.

2. Good: audit sidecars survive revision. Decision logs and conductor traces increased after revision append rather than disappearing.

3. Good: paragraph patch application is doing real fingerprint protection. The revision applied only after `old_fingerprint_match=yes`.

4. Still fake-green: a generated bundle with zero claims can report READY. This was reproduced before and after revision.

5. Still incomplete: evidence IDs can travel structurally as candidate references without becoming proper cited/support-bound claims. The run had 18 used evidence IDs and 15 candidate-only references, but 0 cited references.

6. Still incomplete: Gemma used bracket aliases like `[E1]` in some initial prose, but claim-extractor did not bind those to actual evidence IDs. Prompt/conductor or postprocess should forbid or normalize these aliases.

7. Good red: once claims are appended, the reader gate blocks. Review packets do not silence the claim blockers, which is correct.

8. Good red: evidence-demand/backchain still fail after revision, which is appropriate because source support and boundary/provenance issues remain unresolved.

## Suggested Next Actions

1. Add a first-class `needs_claim_extraction` or `skeleton_only` state so zero-claim generated bundles cannot appear submission-ready.
2. Add a warning/blocker for `used_evidence_id_count > 0 && reference_count == 0`.
3. Decide how real prose should cite allowed evidence IDs: either require canonical evidence IDs in a machine-readable sidecar, or teach the conductor to emit proper citation bindings instead of `[E1]` aliases.
4. Add the claim-extractor -> claim-drafts appender bridge so manual wrapping is unnecessary.
5. Keep source-support/human-verification as explicit separate gestures; review packets should not upgrade truth state automatically.

## Operator Intent Reminder

The operator is not asking us to judge the CIR thesis yet. Treat the CIR draft/data as a stress fixture for repo behavior, especially false green/false red behavior and whether corpus + claim + revision traces survive the writing loop.
