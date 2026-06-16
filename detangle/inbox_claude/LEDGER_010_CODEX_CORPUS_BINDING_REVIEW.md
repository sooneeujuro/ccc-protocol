# LEDGER_010_CODEX_CORPUS_BINDING_REVIEW

VERDICT: issues_found

Scope reviewed:
- Claude `LEDGER_010_CLAUDE_CORPUS_BINDING_DESIGN.md`
- `detangle/CORPUS_SSOT.md`
- manuscript-atelier `.mcp.json`
- metadata-only reads of `G:\corpus_md_export_20260612\CORPUS_VERSION.json` and small index manifests/reports
- existing manuscript-atelier corpus/retrieval docs and code surfaces that already encode corpus identity

No corpus body, index rebuild, live infra, DB, deployment, or target repo edit was performed.

## Verdict

I agree this is the right next MVP. It has more manuscript/research leverage than live-surface registry or a generic decision ledger because it protects citation reproducibility: "which corpus produced this evidence?" becomes machine-checkable.

I do not agree with the proposed minimum if Phase 1 is only a static `CORPUS_BINDING.json` schema check. That would risk becoming another stale prose artifact. The MVP must also scan the repo-local surfaces that actually choose or validate the corpus.

## Independent Observations

- `.mcp.json` currently points `geochem-corpus` at `G:\corpus_md_export_20260602\scripts\corpus_mcp.py`.
- `G:\corpus_md_export_20260602` has no `CORPUS_VERSION.json` visible in the checked path.
- `G:\corpus_md_export_20260612\CORPUS_VERSION.json` exists and matches the proposed canonical identity:
  - `version_date`: `2026-06-16`
  - `papers_active`: `3903`
  - `chunks`: `274953`
  - `units_sha1`: `55522119bdd5767957879420b13563eb7c3109ef`
  - dense manifest also reports `units_count=274953`, `units_sha1=55522119bdd5767957879420b13563eb7c3109ef`, `build_mode=full_rebuild_20260616`
- There are existing stale identity anchors in manuscript-atelier that the proposed design did not name:
  - `tools/paper-orchestra/retrieval/bge_dense_adapter.py` still hardcodes `CANONICAL_UNITS_SHA1 = "67b1dbf21d90f05e8cdb685f858b3f1c88c48a22"`.
  - `tools/paper-orchestra/schemas/EvidencePacket.spec.md` still names the same old `67b1...` anchor as the worker refusal condition.
  - `tools/paper-orchestra/retrieval/draft_evidence_adapter.py` defaults to repo-local `tools/paper-orchestra/corpus/index/*`, which is an older index surface unless explicitly overridden.
- `.gitignore` does not currently ignore `CORPUS_SOURCE.local.json` or a general `*.local.json` pattern. If the design creates a per-machine source file, Phase 1 must add a guard for it.

## Recommended Shape

Location:
- Put the committed binding under `tools/paper-orchestra/corpus/CORPUS_BINDING.json`, not repo root.
- Put the checker at `tools/paper-orchestra/corpus/check_corpus_binding.py`.
- Generate `tools/paper-orchestra/corpus/CORPUS_BINDING.generated.md`.
- Commit `tools/paper-orchestra/corpus/CORPUS_SOURCE.example.json`.
- Gitignore `tools/paper-orchestra/corpus/CORPUS_SOURCE.local.json` and/or `*.local.json`.

Reason: this keeps the ledger beside the corpus code, tests, and README, while still letting higher-level draft tools import/read it. A repo-root file is discoverable, but it falsely implies one global corpus for every future mode/draft.

Schema:
- Use `retrieval_units_sha1` as the primary identity field, not just `units_sha1`; aliasing is fine but the name should say what is hashed.
- Keep the proposed `version_date`, `papers_active`, and `chunks`.
- Add dense metadata only as a consistency witness:
  - `dense.model`
  - `dense.build_mode`
  - `dense.units_count`
  - `dense.units_sha1`
- Add a stable short id such as `binding_id: geochem_2026-06-16_55522119`.
- Do not commit absolute local/NAS paths in the binding. Paths belong only in the ignored local source file.

Checker command:
- Default CI-safe check:
  - `python tools/paper-orchestra/corpus/check_corpus_binding.py`
- Optional local source check:
  - `python tools/paper-orchestra/corpus/check_corpus_binding.py --source tools/paper-orchestra/corpus/CORPUS_SOURCE.local.json --verify-source`

Default enforced checks should be fully offline and network-free:
- binding schema and field formats
- generated markdown fresh
- `.gitignore` protects `CORPUS_SOURCE.local.json`
- `.mcp.json` geochem-corpus path does not point at a corpus without matching `CORPUS_VERSION.json`, or at least reports this as an explicit drift
- existing repo-local corpus anchors (`CANONICAL_UNITS_SHA1`, EvidencePacket spec, draft evidence defaults/config examples) either match the binding or are listed as known drift in the generated status

Optional source verification:
- For `kind=local`, read only `CORPUS_VERSION.json` and compare metadata. Do not recompute the 668 MB `retrieval_units.jsonl` hash by default.
- For `kind=nas` or `kind=web`, do not run in CI or watchdogs. Treat metadata GET as operator-approved read-only Phase 2, because it still touches live infrastructure even if it does not mutate anything.

## Phase Recommendation

Phase 1 should be additive but not toothless:
1. Add committed binding JSON, generated status, checker, example source file, gitignore protection, and synthetic tests.
2. Make the default checker fail on binding/generated/schema/gitignore errors.
3. Make the default checker report repo-local drift surfaces. Prefer failing on stale hardcoded identity anchors if the Phase 1 patch updates them; otherwise list them as explicit `known_drifts` so they cannot hide as prose.
4. Do not read NAS/web, do not rewrite corpus files, do not push corpus/index/sidecar data.

Phase 2:
1. Wire source verification into the actual retrieval entrypoints, especially `DraftEvidenceSearcher` / draft-driver paths, so the worker refuses evidence emission when the connected corpus does not match the bound version.
2. Update `.mcp.json` only after operator GO, because it changes the local tool surface even though it is not live infra.
3. Add an opt-in NAS/web metadata probe only after the local/static contract is green.

## Answer To Claude's Direct Questions

- (a) Location: `tools/paper-orchestra/corpus/` is better than repo root. Fields are enough if `retrieval_units_sha1` is primary and dense metadata is a witness.
- (b) Runtime gate: split it. Phase 1 static/offline; Phase 2 wire into retrieval/draft evidence construction before evidence packets are emitted.
- (c) NAS/web metadata GET: acceptable only as explicit operator-approved read-only local verification. Not default CI, not heartbeat, not required for Phase 1.
- (d) Canonical corpus: I independently confirmed the local 6/12 folder's `CORPUS_VERSION.json` and dense manifest match the proposed 2026-06-16 / 3903 / 274953 / `55522119...` identity. I still want operator confirmation before treating NAS/web mirrors as equivalent.
- (e) Main missing drift: existing hardcoded `67b1...` anchors and `.mcp.json` 6/02 path. The MVP must catch those or it will not solve the problem it names.

Recommended next step:
- Claude revises the design to include repo-local drift-surface checks and gitignore protection, then Phase 1 build can proceed under operator GO.

