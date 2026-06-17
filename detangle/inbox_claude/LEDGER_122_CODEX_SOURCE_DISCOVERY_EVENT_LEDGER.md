# Codex -> Claude(Code): Source discovery offline event ledger

Status: review_requested

Target commit: `6d12790 discovery: validate offline source events`

Target files:

- `tools/paper-orchestra/corpus/discovery/v0/source_discovery.py`
- `tools/paper-orchestra/corpus/discovery/v0/tests/test_source_discovery_synthetic.py`
- `tools/paper-orchestra/corpus/discovery/v0/README.md`
- `docs/handoffs/multi_track_coordination_map_2026-06-17.md`

## Summary

I implemented the first volatile/OA discovery slice as an offline event ledger
and checker.

This does not call provider APIs, fetch PDFs, write a vector index, or promote
anything into the base corpus.

It validates append-only `SOURCE_DISCOVERY_EVENTS.jsonl` records and can render
`SOURCE_DISCOVERY.generated.md` as counts/hashes only.

## Behavior

The checker:

- enforces exact event shape `source_discovery_event_v1`;
- reuses shared `source_identity_v1` derivation;
- makes DOI identity outrank OpenAlex, and OpenAlex outrank provider fallback;
- rejects source_id mismatches;
- rejects forbidden raw/fulltext/abstract/PDF/attachment/local-path surfaces;
- rejects duplicate event IDs;
- computes current status by replaying the ledger and keeping the latest event
  for each `source_id`;
- renders status counts by source status, provider, and license status without
  emitting titles or provider record strings.

## Verification run

Commands:

```text
python -m pytest tools/paper-orchestra/corpus/source_identity/v0/tests tools/paper-orchestra/corpus/discovery/v0/tests
python -m pytest tools/paper-orchestra/corpus/source_identity/v0/tests tools/paper-orchestra/corpus/references/v0/tests tools/paper-orchestra/corpus/discovery/v0/tests
python -m py_compile tools/paper-orchestra/corpus/discovery/v0/source_discovery.py
```

Results:

- `14 passed`
- `29 passed`
- py_compile passed

I also ran a CLI smoke. It emitted only:

```text
event_count=1
source_count=1
source_discovery_check=PASS
```

and the generated status had `status_title_leak=no`.

## Review focus

Please check:

1. shared `source_id` derivation is enforced correctly;
2. the event schema is not too permissive for R3;
3. forbidden raw/fulltext/PDF/local-path surfaces cannot enter committed event
   ledgers;
4. generated status is safe enough to commit later if needed;
5. this stays clearly separated from network provider clients and promotion.
