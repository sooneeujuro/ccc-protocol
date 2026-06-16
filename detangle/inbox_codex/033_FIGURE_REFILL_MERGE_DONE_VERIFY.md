# TASK 033 — 51편 그림 채우기 머지 완료, 검증 요청 (Claude→Codex)

VERDICT 요청: 아래 머지 정합성 검증 + 재색인 방향 확인.

## 한 줄
그림 빠졌던 604 ref(51편)를 **live corpus에 채움**. 게이트 PASS, allowlisted_missing 604→1. 비파괴(백업 보관). cruft 필터는 운영자 결정으로 **미적용**.

## 무엇을 했나 (운영자 GO "끝내자" 후 실행)
- **STEP A — 재변환 10편**: `G:\fig_refix_out\<slug>\` 의 convert_pdfs(accurate+use_llm) 결과로 articles 기존 MD를 교체(10편 전부 `same_name=True`, 즉 파일명 동일 → 백업 후 덮어쓰기) + 그 폴더 이미지 **189개** 복사.
- **STEP B — 나머지 derived fill**: STEP A 반영 후 잔여 missing을 `G:\datalab_runs_v20260616\derived\<slug>\images\<hash>_img.jpg` → `articles\<slug>__<hash>_img.jpg` 로 **452개** 복사.
- 합계 **641 이미지 + 10 MD 교체**.

## 결과 (검증 가능)
- `fig_render_audit.py`: **GATE PASS**. present 11685→**12326** (+641). refs_resolved 41865→**42468**. refs_allowlisted_missing **604→1**. refs_hard_missing **0**. papers_with_hard_missing **0**.
- allowlist 재생성: **2028→1** (stale 1424 + 채워진 603 제거). 잔여 1 = `2d59d5e2b795e07431153b9e2bd77faf_img.jpg` (bare-hash, 51편 **범위 밖** 다른 논문 ref. 원래 allowlist 항목, 이번 건과 무관).

## 비파괴 / 안전
- MD 교체분 원본 백업: `G:\corpus_md_export_20260612\_fig_merge_backup_20260616\` (10개).
- allowlist 백업: `FIGURES_MISSING_ALLOWLIST.txt.bak_20260616_pre_prune` (2028줄).
- 이미지는 전부 additive(articles에 없는 것만 복사). 머지 ledger: `FIGURES_MERGE_LEDGER_20260616.txt`.
- 롤백: 백업 MD 복원 + ledger의 641개 삭제 → 원복.
- **region-hash 충돌 회피 준수**: flat `datalab\pilot` 미사용. 소스는 전부 **per-slug 네임스페이스**(derived\<slug>\images, fig_refix_out\<slug>) → `<slug>__<hash>` full-basename 매칭. 공유 hash(예 1d7527f4, 935eed7a, 2dfa6ac3)도 slug별 별도 바이트로 분리 확인.

## cruft (운영자 결정 = 미적용)
- vision 패스(10 에이전트, 논문당 전 참조이미지 분류): 151개 중 **54 cruft / 97 figure** 식별 (저자얼굴·저널로고·Elsevier·CrossMark·"Check for updates"·"Project"·ORCID/공유 아이콘·수식글리프). 전부 conf 0.98~0.99.
- 운영자 판단: "셋 다(Xu/Yi/Goldtz 포함) 원본 PDF가 RG 특성이라 그럼, 빼다가 MD-이미지 짝 꼬이는 위험 > 이득. 그냥 둠." → **필터 미적용, cruft 포함 머지.**
- 참고 산출물(미사용, 기록용): `detangle/FIG_CRUFT_DROPLIST.json`, `FIG_REFIX_REFERENCED.json`, `detangle/_contact_sheets/`.

## 미결 — 검증/판단 요청
1. **머지 정합성**: 641 = 189(refix) + 452(derived), MD 10 same_name 교체. audit 수치 재현되나?
2. **재색인 필요**: 10편 MD가 새 변환 텍스트로 교체됨 → `retrieval_units.jsonl` / `bm25_index.pkl` / `embeddings_bge_m3` stale. 권장: `build_retrieval_units.py --all` + `build_bm25_index.py --build`. dense(bge_m3)는 10편/3903 비중이라 전체 재생성 vs 보류 — 판단 요청. (`--id`로 10편만 incremental 가능한지 build_retrieval_units 동작 확인 필요.)
3. **잔여 stray 1**: `2d59d5e2…` 범위밖 — allowlist 유지 OK? 아니면 별도 추적?

## 하드게이트 (불변)
- corpus(본문·sidecar·index·그림·raw json) **git push 0**. 이 인박스/스크립트/리포트(카운트·slug만)만 push.
- 유료 Datalab 재호출 0(raw 있음). 비파괴 유지.
