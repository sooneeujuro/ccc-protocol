# LEDGER_055_CODEX_LOCAL_ASSET_LAYOUT_PLAN

VERDICT: info

## Target

- Repo: `C:\Users\USER\Documents\manuscript-atelier`
- Branch: `codex/draft-context-workspace`
- Main commit: `641df55` (`docs: add local asset layout plan`)
- Cleanup commit: `3b54a62` (`docs: tidy asset layout plan EOF`)

## What Changed

Added a durable local/NAS asset layout contract:

- `docs/handoffs/local_asset_layout_plan_2026-06-17.md`

Updated the multi-track map to point at that plan:

- `docs/handoffs/multi_track_coordination_map_2026-06-17.md`

## Scope

This is documentation only. It does not:

- connect NAS;
- mutate NAS;
- rebuild corpus;
- run FGP prose ablation;
- sync Zotero;
- write DB/live infra;
- commit raw paper or FGP content.

## Contract Summary

The plan standardizes a placeholder root:

```text
<ARTELIER_ASSET_ROOT>/
```

with top-level areas for:

- `corpus/`
- `fgp/`
- `runs/`
- `zotero/`

The key contract is:

- real paths stay in gitignored `*.local.json` files;
- corpus is verified through `CORPUS_SOURCE.local.json` +
  `CORPUS_VERSION.json` against `CORPUS_BINDING.json`;
- FGP is verified through `FGP_SOURCE.local.json` and the portable FGP source
  checker;
- phrase corpus stays `.local.jsonl` and is treated as raw FGP;
- run outputs stay local unless separately sanitized/promoted.

This should help notebook / home computer / NAS setup sessions follow the same
folder contract without deciding live attachment details again.

