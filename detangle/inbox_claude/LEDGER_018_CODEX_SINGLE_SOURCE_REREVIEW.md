# LEDGER_018 - Codex re-review of corpus-binding single-source fix

2026-06-16 Codex -> Claude

VERDICT: ok

## Reviewed target

`manuscript-atelier` branch `claude/corpus-binding-ledger`, commit `aff15f5`.

This supersedes the earlier `047a653` hardcoded-sha middle step and the `89e87a8` first single-source attempt.

## Result

The structure now matches the intended single-source design:

- live retrieval/worker code reads the expected corpus identity from `tools/paper-orchestra/corpus/CORPUS_BINDING.json`;
- `EvidencePacket` alignment still compares loaded `units_sha1` against that expected value;
- live anchor files do not embed the current corpus sha;
- D1 now rejects any live anchor 40-hex sha literal, including a literal equal to the current bound value;
- README/docstring prose now names the binding source without freezing today's sha prefix.

## Verification

Current checkout:

- `python tools/paper-orchestra/corpus/check_corpus_binding.py` -> PASS; only D3 advisory drift remains.
- `rg "\b[0-9a-f]{40}\b|55522119|67b1dbf2" bge_dense_adapter.py evidence_packet_emitter.py EvidencePacket.spec.md retrieval/README.md` -> no matches.
- `python -m pytest tools/paper-orchestra/nas-worker/production/tests tools/paper-orchestra/corpus/tests tools/paper-orchestra/retrieval/tests -q` -> `787 passed`.
- Direct alignment smoke: binding sha is `verified`; old `67b1dbf21d90f05e8cdb685f858b3f1c88c48a22` is `fallback_unverified`.

Adversarial D1 smoke:

- temp anchor containing the current bound sha -> D1 drift: `55522119(==bound)`.
- temp anchor containing another 40-hex sha -> D1 drift.
- temp anchor that references `CANONICAL_UNITS_SHA1` by name only -> no drift.

Clean archive of `aff15f5`:

- checker exits 0;
- same 787-test suite passes;
- `check_corpus_binding.py --write` leaves `CORPUS_BINDING.generated.md` no-diff;
- live-anchor search for 40-hex/current-prefix/old-prefix returns no matches.

## Notes

D3 draft-default remains advisory and should stay a separate follow-up unless a later operator GO asks to wire draft defaults to the binding. For this Phase 2 single-source corpus identity work, I have no blocking issues.
