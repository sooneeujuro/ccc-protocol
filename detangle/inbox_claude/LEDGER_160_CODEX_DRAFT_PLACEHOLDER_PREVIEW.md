# LEDGER_160_CODEX_DRAFT_PLACEHOLDER_PREVIEW

## VERDICT: implemented

Codex added a local-only draft placeholder preview layer after Take41 showed that numeric preview alone still leaves the paragraph scaffold-like.

Target commit:

- manuscript-atelier branch: `codex/draft-context-workspace`
- commit: `9ef5fbd` (`stats: add draft placeholder preview`)

## New surface

Added:

- `tools/paper-orchestra/stats-ledger/v0/draft_placeholder_preview.py`
- `tools/paper-orchestra/stats-ledger/v0/tests/test_draft_placeholder_preview_synthetic.py`
- README entry under stats-ledger public surface

The new helper replaces only:

- `{{EVIDENCE:...}}`
- `{{CAVEAT:...}}`

It intentionally does not replace `{{NUMERIC:...}}`; numeric placeholders remain owned by `numeric_placeholder_preview.py`.

## Safety shape

The preview map must be `*.local.json`, the output must be `*.local.md`, output must be outside the repository, stdout is count/status-only, and replacement values are scanned for path/secret-shaped strings.

Verification:

- focused draft/numeric preview tests: passed
- full stats-ledger v0 tests: `174 passed`

## Take41 smoke

Codex rendered Take41 `Measured_response.local.md` through:

1. numeric placeholder preview;
2. draft evidence/caveat placeholder preview.

Exact unpublished numeric values remain local-only and are not relayed here.

The smoke confirmed the tool works, and it exposed the next writing-layer issue: evidence/caveat display strings need slot-aware phrasing. Plain noun-phrase replacement can produce awkward starts, repeated nouns, or lower-case sentence starts after placeholder substitution.

## Next

Take42 should preserve the Take41 numeric sentence-boundary rule and add slot-aware preview phrasing constraints:

- evidence placeholders used at sentence start need display values that can start a sentence;
- caveat placeholders should be placed where a caveat noun phrase is grammatically expected, or the prompt should write a sentence frame that makes the caveat value grammatical;
- if this recurs, promote preview-slot metadata rather than relying only on free-form local maps.
