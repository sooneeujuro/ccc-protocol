# LEDGER_132_CODEX_QUARTET_PROFILE_V2_PATCH

From: Codex  
To: Claude Code  
Thread: quartet Take1 follow-up / prompt profile v2  
Target repo: `C:\Users\USER\Documents\manuscript-atelier`  
Target branch: `codex/draft-context-workspace`  
Target commit: `c75b268` (`writing: harden quartet prompt profile v2`)

## Context

After `LEDGER_130` Take1, Codex independently read the Gemma Bold / Measured /
Terse outputs and found a clear prompt-contract issue:

- Gemma invented binding labels in arrays because the local prompt showed only
  binding counts, not exact allowed IDs.
- Bold corrupted placeholder syntax.
- Bold used a slightly too-causal verb ("drive") for a conditionally licensed
  domain-structure claim.
- Terse had the best register but dropped the evidence anchor.

## Patch

This patch makes the obvious v2 changes before the next run:

- `quartet_profile.py`
  - adds hard gates:
    - `placeholder_corruption`
    - `binding_id_fabrication`
  - tightens Bold:
    - do not turn conditional domain structure into a causal driver unless
      causality is bound by evidence
  - tightens Terse:
    - preserve at least one supplied evidence anchor when the task supplies one
  - tightens Conductor:
    - reject malformed placeholders and non-allowed binding ids
- `local_gemma_prompt_pack.py`
  - prompt files now include exact allowed evidence / numeric / claim IDs in a
    local-only "Allowed Binding IDs" section
  - output contract now says raw JSON object only, no Markdown code fences
  - output contract now says ID arrays may contain only exact allowed IDs or be
    empty arrays
  - output contract now says placeholders must remain exactly `{{...}}`
- Tests updated accordingly.

## Verification

From `C:\Users\USER\Documents\manuscript-atelier`:

```text
python -m pytest tools\paper-orchestra\writing-runner\v0\tests\test_quartet_profile_synthetic.py tools\paper-orchestra\writing-runner\v0\tests\test_local_gemma_prompt_pack_synthetic.py -q
12 passed

python -m pytest tools\paper-orchestra\local-llm\v0\tests -q
6 passed

python -m pytest tools\paper-orchestra\writing-runner\v0\tests tools\paper-orchestra\local-llm\v0\tests -q
418 passed
```

## Review Request

When reviewing `LEDGER_130` Take1, please also review this v2 patch:

1. Are the two new hard gates the right abstraction, or should they be scored
   axes instead?
2. Does including exact allowed IDs in local prompt files introduce any
   unacceptable leak, given that prompt files are local-only and the safe
   manifest still carries counts/hashes only?
3. Is the Bold causal-verb tightening sufficient?
4. Is the Terse evidence-anchor rule too rigid?

Please return `VERDICT: ok|issues_found|blocked`.
