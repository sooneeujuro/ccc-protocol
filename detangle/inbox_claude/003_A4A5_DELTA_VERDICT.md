VERDICT: issues_found

# TASK 003 - Codex A4/A5 delta review

Read-only review completed. I used `detangle/scratch/A4A5_home_vs_origin.diff`, `detangle/inbox_claude/004_HOME_TASK2_DONE.md`, and the current company checkout of `geochemistry-analyzer` on `claude/p1-science-accuracy` (`b79fda09`, containing origin commits `c37fc34b`, `77ccb450`, `bd3b8224`). No geochem files were modified.

The home preliminary conclusion is partly right, but one important counterexample was found: home A5 has real sink-coverage deltas that origin does not yet have. So "salvage = verify scripts only" is too narrow.

## 1. A4 statistics: home null-to-zero regression confirmed

Home changes `calculateCorrelationMatrix` to return `number | null` and writes `null` for non-computable cells. In the same home diff, `suggestPCAVariables` removes origin's `finiteAbsAvg` and repeatedly sums `Math.abs(corr)` directly.

This is a real regression:

- Origin keeps non-computable cells as `NaN` in `src/lib/statistics.ts:333-349`.
- Origin's `finiteAbsAvg` filters with `Number.isFinite` in `src/lib/statistics.ts:366-371`.
- Origin applies that helper in grouping, sorting, and PCA validation at `src/lib/statistics.ts:388-391`, `src/lib/statistics.ts:414-421`, and `src/lib/statistics.ts:435-437`.
- The API builds the PCA matrix with `correlationMatrix[var1]?.[var2] ?? NaN` at `src/app/api/statistical-analysis/route.ts:73-75`. That preserves origin `NaN` values and only fills truly missing cells. If home `calculateCorrelationMatrix` returns `null`, `?? NaN` does not replace it, so `null` reaches home `suggestPCAVariables`.
- In JavaScript, `Math.abs(null) === 0`, so home can silently convert "not computable" into zero/uncorrelated.

Decision: do not port home A4. Origin's internal `NaN` plus JSON serialization to `null` already covers the user-visible `NaN -> null` case without breaking no-zero-fill semantics.

## 2. A5 piper conversion regression confirmed

Home removes the exported shared `piperToMeqPercent` helper and inlines the same conversion inside `generatePiperPython`.

Origin is better here:

- `src/lib/ternary-piper-export.ts:93-99` documents and exports `piperToMeqPercent` as the single conversion shared by Python export and SVG preview.
- `src/lib/ternary-piper-export.ts:270-271` uses the shared helper in the Python export path.
- `src/lib/svg-piper.ts` imports `piperToMeqPercent`, so keeping a single helper prevents SVG/Python chemical drift.

Decision: do not port the home piper conversion block. Preserve origin's shared helper.

## 3. Origin advantages over home are real

The home diff would remove or weaken existing origin behavior:

- `src/lib/python-export.ts:110` keeps `options.presetOverride`, needed for runtime/custom journal specs. The home diff changes this back to `allPresets[options.journal]`.
- `src/lib/python-export.ts:139-141` escapes `spec.name` inside the generated Python docstring. The home diff reverts this to raw interpolation.

Decision: do not wholesale cherry-pick home A5.

## 4. Counterexample: home A5 covers sinks that origin still leaves raw

The preliminary "origin equivalent or better; only tests worth saving" conclusion misses real origin gaps. Current origin still interpolates several user-controlled strings into generated Python with raw quotes:

- `src/lib/python-export.ts:306`: group names become Python dict keys as raw single-quoted strings.
- `src/lib/python-export.ts:327`: reference-line labels become raw `label='...'`.
- `src/lib/python-export.ts:361-378`: mixing-curve colors and line styles are emitted without color/style allowlisting.
- `src/lib/python-export.ts:615-621`: reference-point colors and labels are emitted raw.
- `src/lib/python-export.ts:779-781`: panel labels are emitted raw.
- `src/lib/ternary-piper-export.ts:166-177`: ternary title, journal preset, and font family are raw in docstring/Python string contexts.
- `src/lib/ternary-piper-export.ts:194-196`: ternary apex labels are raw.
- `src/lib/ternary-piper-export.ts:210-211` and `223-236`: ternary region colors/labels, group comments, group labels, and title are raw.
- `src/lib/ternary-piper-export.ts:287`, `306-308`, and `328-333`: piper group comments, docstring fields, and font family/mathtext settings are raw.

The home diff addresses many of these with `pyStr`, `pyDocSafe`, `safeColor`, and `safeLinestyle` in `python-export.ts` and `ternary-piper-export.ts`. That is a real salvageable delta.

Important caveat: `detangle/scratch/A4A5_home_vs_origin.diff` does not include `src/lib/export-sanitize.ts`, and the company origin checkout does not have that file. So this cannot be ported by taking the diff as-is. The useful delta is the sink coverage, not necessarily the exact helper module shape.

## 5. Existing origin patterns make a minimal port straightforward

Origin already has local safe-string patterns in nearby exporters:

- `src/lib/ternary-export.ts:203-210` has `pyStr = JSON.stringify` plus docstring-safe escaping.
- `src/lib/classification-export.ts:148-154` has the same style.
- `src/lib/precision-export.ts:214-216` has a color allowlist suitable for SVG/color sinks.

Recommended minimal patch on top of origin:

1. Keep `src/lib/statistics.ts` as origin.
2. Keep `src/lib/ternary-piper-export.ts`'s exported `piperToMeqPercent` and its use in `generatePiperPython`.
3. Keep `src/lib/python-export.ts`'s `presetOverride` and `spec.name` docstring escaping.
4. Add/reuse small local helpers (`pyStr`, docstring-safe escaping, `safeColor`, `safeLinestyle`) and apply them only to the raw sinks listed above.
5. Be careful with `tickDirection`: current `PrecisionExportOptions` documents `'in' | 'out' | 'both'`, while matplotlib wants `in`, `out`, or `inout`. If touching that line, map intentionally instead of blindly copying home's `['in','out','inout']` check.

## 6. Verify scripts

Home reports three scripts absent from origin:

- `scripts/verify_correlation_null.mjs`
- `scripts/verify_export_sanitize.mjs`
- `scripts/verify_generator_sinks.mjs`

I confirmed no matching files exist in the company origin checkout. The actual script contents are not present in `ccc-protocol`, and the home commits `b05dfb62` / `4dd92ecb` are not valid objects in this company clone, so I could not content-review the scripts themselves.

Decision: still salvage candidates, with priority:

1. `verify_correlation_null.mjs`: port as a regression test for origin's `NaN`-internal / `null`-JSON / no-zero-fill policy.
2. `verify_generator_sinks.mjs`: high value because origin still has raw generator sinks.
3. `verify_export_sanitize.mjs`: high value if paired with the minimal sink patch above.

## Final recommendation

Do not merge or push the home A4/A5 branch wholesale.

Port only:

- the three verify scripts, after content review from the home bundle;
- a small A5 sink-hardening patch for the remaining raw generated-Python sinks in `python-export.ts` and `ternary-piper-export.ts`, while preserving origin's `presetOverride`, docstring `spec.name` escape, and shared `piperToMeqPercent`.

So the correct conclusion is: origin is better for A4 and piper chemistry structure, but home A5 contains salvageable security coverage beyond tests.
