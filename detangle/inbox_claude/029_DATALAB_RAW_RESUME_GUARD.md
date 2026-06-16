VERDICT: advisory

# Codex advisory — Datalab raw/resume guard before any paid batch

Operator relayed a strong warning from another verifier: with Datalab, every repeated conversion is money. Before any Datalab pilot expands beyond one or two papers, the pipeline must be raw-first and resumable.

## Non-negotiable Datalab rules

1. Save the raw Datalab response before deriving anything.

   Write the complete raw response to a local, non-git corpus workspace, e.g.

   - `G:\datalab_runs_v20260616\raw\<paper_id>.json`
   - `G:\datalab_runs_v20260616\raw\<paper_id>.json.tmp` during write, then atomic rename

   Do not write raw Datalab responses into `ccc-protocol`; raw conversion output may contain paper text/images and must not be pushed.

2. Idempotency is keyed on raw.

   If `raw\<paper_id>.json` exists and passes a JSON/schema sanity check, skip the API call. Regenerate markdown/images/manifests from raw locally as many times as needed.

3. Track in-flight async requests.

   Datalab async submit/poll must have a ledger before/at submit time:

   - `paper_id`
   - `pdf_sha256`
   - `mode` / model / options / page_range
   - request id or `request_check_url`
   - `submitted_at`
   - state: `planned | submitted | polling | raw_saved | derived | failed | manual`
   - output raw path
   - cost/page estimate if available

   If a run dies after submit but before raw save, resume by polling the saved request id/check URL. Do not resubmit unless the ledger proves the prior request is unrecoverable.

4. Separate paid conversion from free derivation.

   Pipeline should be:

   `submit/poll -> raw json saved -> derive images/md/contact sheets -> staged diff -> audit`

   Any bug after raw save should be fixed by rerunning only the derive step, not the API call.

5. Quality-first model choice.

   Operator explicitly said to be conservative about quality, not price. Prefer Datalab `accurate` / highest-quality mode for Seton, difficult PDFs, and initial pilots. Control spend with page ranges, pilots, and batching, not by downgrading quality purely to save money.

## Suggested local layout

Use a run folder outside git:

```text
G:\datalab_runs_v20260616\
  RUN_LEDGER.csv
  raw\
    <paper_id>.json
  derived\
    <paper_id>\
      manifest.csv
      staged.md
      staged_md.diff.txt
      contact_sheet.png
      images\
```

Only small audit summaries/verdicts should be committed to `ccc-protocol`.

## Seton count clarification

Codex independently parsed `Seton,_2012,_Global_continental_and_ocean_basin_reconstructions_since_200_Ma.md`:

- image refs for pid `359cf721d5fa`: 28
- first 2 refs are non-figure artifacts:
  - Elsevier logo
  - Earth-Science Reviews cover image
- actual image refs with Figure identity: 26
- markdown/body text mentions Figure numbers 1 through 29, but image refs are not a clean 1:1 sequence with Figure 1..29.

So Seton must not use `count == 28` as success by itself. The mapping must exclude logo/cover refs and align by figure identity/caption number. This is another reason a Datalab accurate pilot should be compared before batch.

## Batch gate

Do not start any paid Datalab batch until:

- raw-first storage exists;
- in-flight ledger exists;
- resume can recover submitted requests without resubmitting;
- derivation can be rerun from raw with zero API calls;
- Seton pilot proves figure identity mapping, not just count matching.
