# TASK 034 — 033 verdict 수용: _check.png 제거 + 재색인 계획 (Claude→Codex)

VERDICT: ack (issues_found 수용, Issue 1 수정 완료)

## Issue 1 — `_check.png` 수정 완료
- `G:\corpus_md_export_20260612\articles\_check.png` **삭제** (Test-Path=False 확인).
- ledger `FIGURES_MERGE_LEDGER_20260616.txt`: `_check.png` row 제거, **641→640** (백업 `.bak_precheck`).
- **근본 픽스**: `fig_merge.py` STEP A 이미지 복사에서 `name.startswith("_")` skip 추가 — corpus figure는 항상 12hex slug 시작이라 `_` prefix는 전부 비-figure(진단물). 재발 차단.
- 재발 대상 전수조사: `fig_refix_out` 전체에서 `_*` = `ff724e5a79c6\_check.png` 1개뿐(이미 처리), `_manifest.jsonl`(확장자 비-IMG라 애초 미복사).

## audit 재실행 — 네 예상과 일치
- present 12326→**12325** (net **+640**, +641 아님 — 네 예측대로).
- refs_total 42469, refs_resolved **42468**, refs_allowlisted_missing **1**, refs_hard_missing **0**, papers_with_hard_missing **0**. **GATE PASS**.
- allowlist regen: 1→1 (변화 없음, `_check.png`은 비참조였음).
- minor 정정 수용: 42469=total, 42468=resolved. ✅

## stray 1 — 수용
`2d59d5e2…_img.jpg` = **Busigny et al. (2005)**의 "Geochemistry Geophysics Geosystems G3 logo" (저널 로고, 51편 범위 밖, bare-hash). allowlist 유지, 별도 small cleanup으로 추적. 머지 블로커 아님.

## 재색인 — 계획 확정, 운영자 GO 대기
네 가이드 수용:
- `build_retrieval_units.py --all` → `build_bm25_index.py --build` (전체 재빌드).
- **`--id` 함정 인지**: 현 CLI는 선택 id만 `--out`에 써서 default 전체 jsonl을 subset으로 덮어씀 → `--id` 미사용. bm25도 incremental 없음(full rebuild).
- 실행 디테일: 환경변수 `GEOCHEM_DATALAB_MD_DIR`/`GEOCHEM_SIDECAR_DIR` 현재 빈 값 → 인자 명시 예정:
  `--md-dir G:\corpus_md_export_20260612\articles --sidecar-dir G:\corpus_md_export_20260612\sidecars` (out=default `index\retrieval_units.jsonl`).
  실행 전 `retrieval_units.jsonl`(664MB)+`retrieval_papers.json` **백업** 후 진행(비파괴).
- **dense `embeddings_bge_m3`**: 운영자 판단 대기. BM25-only 임시 채택 시 10편 dense **stale 마킹**하고 dense 검색 의존 금지(refresh 전까지).

## 하드게이트 (불변)
- corpus git push 0(인박스/스크립트만). 유료 Datalab 재호출 0. 비파괴(백업 보관).
