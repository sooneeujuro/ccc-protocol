VERDICT: issues_found

# Follow-up: Nd/Na top-unmatched is a real pre-B bug

Operator asked whether Nd/Na need rework. I checked the current cycle-6 normalizer directly:

```text
'Nd' -> (None, 'junk')
'Na' -> (None, 'junk')
'Nd concentration' -> ('Nd_conc', 'L1c')
'Na concentration' -> ('Na_conc', 'L1c')
```

Root cause:

- `_JUNK_VALUES` includes lower-case `nd` and `na` as "not determined" / "not applicable" sentinels.
- `normalize_variable()` checks `folded.lower() in _JUNK_VALUES` before element matching.
- Therefore uppercase element symbols `Nd` and `Na` become `nd`/`na` and are incorrectly classified as junk.

This explains the visible cycle-6 `top_unmatched` / junk-like behavior:

- `Nd`: 181 occurrences
- `Na`: 46 occurrences

Recommended pre-B patch:

1. Do not case-fold `nd`/`na` junk sentinels blindly.
2. Treat exact lower-case `nd`, `n.d.`, `n/a`, `na`, etc. as junk, but let exact chemical element symbols `Nd` and `Na` route to `Nd_conc` and `Na_conc`.
3. Add regression probes:
   - `Nd -> Nd_conc`
   - `Na -> Na_conc`
   - `nd -> junk`
   - `n.d. -> junk`
   - `N/A -> junk`

This is not a reason to reopen the 90% target or redo the whole ceiling analysis. It is a small, high-confidence pre-B correctness patch and may recover roughly 200+ entries.
