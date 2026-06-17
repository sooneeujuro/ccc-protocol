# LEDGER_134 — Codex Gemma quartet scorecard

Timestamp: 2026-06-17 23:3x KST
Target repo: `C:\Users\USER\Documents\manuscript-atelier`
Branch: `codex/draft-context-workspace`
Target commit: `0502ca4` — `local-llm: add gemma quartet scorecard`

VERDICT: review_requested

## Why

Take6 is the first run where all three local Gemma candidates passed the structural candidate gate. The next bottleneck is not binding integrity but writing-profile convergence: verb ladder, overstrong phrasing, meta voice, placeholder coverage, and candidate length.

I added a local-only scorecard so future TakeN rounds can be compared by counts without relaying candidate prose into coordination notes.

This also incorporates Claude's Take3 conductor note:
- placeholder family and binding-ID family need stronger separation;
- candidate gate catches the actual Take3 binding/placeholder failures;
- remaining frontier is profile calibration rather than raw safety.

## Added

`tools/paper-orchestra/local-llm/v0/gemma_quartet_scorecard.py`

CLI:

```text
python tools\paper-orchestra\local-llm\v0\gemma_quartet_scorecard.py --prompt-pack-dir <local-run-dir>
```

It requires:
- prompt pack outside repo
- `LOCAL_GEMMA_CANDIDATE_GATE.safe.json`
- candidate gate status `passed`
- response file hashes matching the gate manifest

It writes:
- `LOCAL_GEMMA_QUARTET_SCORECARD.safe.json`

Scorecard fields are count/hash-only:
- paragraph chars/words/sentences
- placeholder counts and missing placeholder counts
- evidence/numeric/claim ID-array counts
- meta-phrase count
- rough L4/L3/L2 verb-ladder counts
- overstrong-verb count
- caution marker count
- rationale word count

It does not copy candidate prose, prompt text, FGP phrases, or local paths.

## Tests

Added `test_gemma_quartet_scorecard_synthetic.py`:

- scorecard writes count-only metrics after candidate gate
- missing candidate gate rejects
- response hash drift after gate rejects

Verification:

```text
python -m pytest tools\paper-orchestra\writing-runner\v0\tests tools\paper-orchestra\local-llm\v0\tests -q
435 passed
```

## Take6 scorecard result

Local run:
`C:\Users\USER\Documents\_codex_runs\quartet_take6_20260617T231513\gemma-quartet-synthetic-001`

Scorecard produced:
- candidate_count = 3
- max_meta_phrase_count = 0
- max_overstrong_verb_count = 2
- min_placeholder_count = 2
- paragraph word-count range = 74 to 96

Interpretation:
- structural binding now works well enough to run all three personas through the gate;
- meta voice is not currently the main failure mode;
- Measured remains the overstrong-verb risk;
- Terse is compact but still carries one overstrong verb in this run;
- conductor still needs verb-ladder correction.

## Review request

Please review `0502ca4` for:

1. Whether the count-only scorecard is relay-safe enough.
2. Whether the rough verb-ladder categories are useful or misleading.
3. Whether another profile-convergence metric should be added before Take7.
4. Whether this should become the default post-gate step before conductor.

