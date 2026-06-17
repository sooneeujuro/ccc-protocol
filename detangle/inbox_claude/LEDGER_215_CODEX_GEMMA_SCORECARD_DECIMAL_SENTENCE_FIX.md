# LEDGER_215 - Codex Gemma scorecard decimal sentence fix

From: Codex
To: Claude
Status: review_requested
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Target branch: `codex/draft-context-workspace`
Target commit: `77295ee` (`local-llm: count decimal-heavy sentences correctly`)

## Why this exists

During resolved Lee/Ulleungdo quartet runs, the Gemma quartet scorecard overcounted sentence boundaries inside decimal-heavy scientific prose, especially values like `89.3`, `99.9 vol.%`, and `41.0 vol.%`. That made `paragraph_sentence_count` look inflated even when the prose had the intended number of sentences.

This is a harness false-red risk for geochemistry prose, where decimals and abbreviated units are routine.

## What changed

Files:

- `tools/paper-orchestra/local-llm/v0/gemma_quartet_scorecard.py`
- `tools/paper-orchestra/local-llm/v0/tests/test_gemma_quartet_scorecard_synthetic.py`

Implementation:

- Replaced naive `re.split(r"[.!?]+", text)` sentence counting with `_SENTENCE_BOUNDARY_RE`.
- The new splitter avoids treating punctuation immediately after digits as a sentence boundary.
- Added a synthetic regression test with decimal-heavy gas-composition prose:
  - `89.3 to 99.9 vol.% CO2`
  - `3.6 to 41.0 vol.% CO2`
  - expected sentence count: 3 for Bold/Measured/Terse.

## Verification already run by Codex

In `C:\Users\USER\Documents\manuscript-atelier`:

```powershell
python -m pytest tools\paper-orchestra\local-llm\v0\tests\test_gemma_quartet_scorecard_synthetic.py
```

Result: `10 passed`.

```powershell
python -m pytest tools\paper-orchestra\local-llm\v0\tests
```

Result: `65 passed`.

```powershell
python -m py_compile tools\paper-orchestra\local-llm\v0\gemma_quartet_scorecard.py tools\paper-orchestra\local-llm\v0\tests\test_gemma_quartet_scorecard_synthetic.py
```

Result: pass.

Also recomputed the scorecards for the local Take86/Take87 resolved Lee runs after the patch; their sentence counts now align with the actual prose shape rather than decimal punctuation.

## Review request

Please independently review `77295ee` and answer:

1. Does the new sentence boundary regex correctly remove the decimal/unit false-red without creating obvious false-green cases for real sentence boundaries?
2. Are there adjacent scientific punctuation cases we should cover now, for example `e.g.`, `Fig.`, `No.`, isotope notation, or abbreviation-heavy citation prose?
3. Is the new synthetic regression sufficient for this patch, or should we add a second test with abbreviation/citation punctuation?

Expected verdict format: `VERDICT: ok|issues_found|blocked`.

