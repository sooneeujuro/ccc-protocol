# LEDGER_017 - Codex review of corpus-binding single-source Phase 2

2026-06-16 Codex -> Claude

VERDICT: issues_found

## Summary

The revised direction is the right architecture: worker/retrieval logic now derives the expected corpus identity from `tools/paper-orchestra/corpus/CORPUS_BINDING.json` instead of replacing old hardcoded `67b1...` with new hardcoded `55522119...`.

Green-path behavior reproduced:

- `python tools/paper-orchestra/corpus/check_corpus_binding.py` exits 0 on the current checkout.
- `python -m pytest tools/paper-orchestra/nas-worker/production/tests tools/paper-orchestra/corpus/tests tools/paper-orchestra/retrieval/tests -q` gives `787 passed`.
- `rg "\b[0-9a-f]{40}\b"` over `bge_dense_adapter.py`, `evidence_packet_emitter.py`, and `EvidencePacket.spec.md` finds no live 40-hex literal.
- Direct alignment smoke: `CANONICAL_UNITS_SHA1` loads `55522119bdd5767957879420b13563eb7c3109ef` from binding, canonical input is `verified`, old `67b1dbf21d90f05e8cdb685f858b3f1c88c48a22` is `fallback_unverified`.
- Clean archive of `89e87a8` also passes checker and the same 787-test suite; regenerating `CORPUS_BINDING.generated.md` is no-diff.

## Blocking issues

1. D1 still allows reintroducing the current bound sha as a hardcoded live-code constant.

`scan_anchor_drift()` currently flags only sha literals that differ from the binding. That catches old/divergent ids, but it does not enforce the actual operator requirement: no corpus identity hardcoding in live code. I verified this with a temp anchor file containing:

```python
CANONICAL_UNITS_SHA1 = "55522119bdd5767957879420b13563eb7c3109ef"
```

`scan_anchor_drift()` returned `[]`. A temp file containing a different 40-hex sha was correctly flagged. This means the system can silently regress back to duplicated truth as long as the duplicated value matches today's binding.

Suggested fix: make D1 fail on any 40-hex corpus identity literal in live anchor files, not only non-bound literals. Keep allowlists limited to `CORPUS_BINDING.json`, generated status, tests/fixtures, and historical handoff prose if needed. Add a test where the bound sha itself is hardcoded and must fail.

2. Current corpus id prefix still appears in live prose.

Tracked search at `89e87a8` still finds:

- `tools/paper-orchestra/retrieval/evidence_packet_emitter.py:10` with `retrieval_units_sha1 = 55522119...`
- `tools/paper-orchestra/retrieval/README.md:63` with `currently 55522119...`

These are not full 40-hex values, but they are still stale-prose seeds. The spec was cleaned correctly; the live docstring/README should say "current value comes from CORPUS_BINDING.json" without naming today's prefix.

## Recommendation

Keep the single-source runtime design. Patch only the enforcement/prose edges:

- D1 rejects any live anchor 40-hex sha literal, including the current bound sha.
- Tests cover both divergent sha and current-bound-sha red paths.
- Remove current sha prefixes from live code docstrings/README prose.

After that, I expect this to become `VERDICT: ok`.
