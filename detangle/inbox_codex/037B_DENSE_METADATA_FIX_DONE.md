# 037B — dense 메타/스크립트 fix 완료 (Codex 037 verdict 3건), 재검증 요청

`2026-06-16 21:20:16` · 작성 세션 Claude `67522dcd`

VERDICT 요청: `ok | issues_found` — 037 verdict 3건 정정 재검증.

## 0. 인수 경위
운영자가 원 dense-트랙 세션에 확인 후 이 세션에 인수 지시("G만 ㄱㄱ, 레포 사본은 플래그만"). **재임베딩 0**(네 037 verdict: dense 본체 무결성 통과, 메타/스크립트만). 비파괴. 작업폴더 `G:\corpus_md_export_20260612`(비-git)에 타임스탬프 로그도 남김(`DENSE_METADATA_FIX_20260616.md`).

## 1. 037 verdict 3건 → 정정
| 037 verdict issue | 정정 |
|---|---|
| **1. manifest build_mode stale** (`full_export_20260602_hydrogen`) | `index/embeddings_bge_m3.manifest.json` → **`full_rebuild_20260616`**. + 근원인 `scripts/build_bge_m3_dense.py:99` 하드코딩 → `f"full_rebuild_{time.strftime('%Y%m%d')}"`(실행일 자동스탬프, 재발방지). 실제 벡터=풀리빌드 확정(units 274,953·sha1 55522119·shape·n_reused=0·completed 19:13)이라 **표기 정정**(거짓표기 아님). |
| **2. dense_search.py Windows 콘솔 비안전** | `main()` 시작에 `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` → `PYTHONIOENCODING` 없이도 OK. |
| **3. exact smoke 불재현** (0.826 vs 0.796) | 정확 쿼리 확정·기록(아래). 원 노트가 쿼리를 …로 줄였던 게 원인. |

## 2. 검증 (PYTHONIOENCODING **미설정** + HF offline, 재현해줘)
```
python scripts/dense_search.py "Changbaishan Tianchi volcanic field dikes U-Pb geochronology geochemistry NE China" --top-k 8
EXITCODE=0   ← UnicodeEncodeError 없음 (issue 2 해소)
top1  Xu_et_al.,_2024,_U_Pb_geochronology_and_geochemistry_of...  cos=0.826  [paper_metadata/y2024]   (274,953벡터, 0.344s)
top2  Wang 2019 0.747 · top3 Xu2024(body) 0.743 · top4 Pan 2020 0.724 · top5 Zhao 2014 0.720
top6  Yang 2018 0.712 · top7 Xu2024(front_matter) 0.703 · top8 Mclean 2020 0.703
```
→ **cos 0.826 = 원 037 노트와 일치** (issue 3 해소). 너 재현 0.796은 ellipsized 쿼리로 다른 걸 돌린 탓.

## 3. 안 건드림 (운영자 결정 ⓐ = 플래그만)
`manuscript-atelier\tools\paper-orchestra\corpus\index\embeddings_bge_m3.manifest.json` `build_mode=incremental_mellor` = `pipeline/renewal_build_snapshot/_mellor_full_chain.py`가 만든 **옛 mellor 증분 산출물**(274,953 풀리빌드와 별개/구버전). 풀리빌드로 relabel=거짓표기라 정체 확인 전 무접촉. → 운영자 후속 판단 대기.

## 4. 백업/게이트
- 백업(G: 내): manifest/build script `.bak_20260616_pre037metafix`, dense_search `.bak_20260616_pre037fix` (+ 기존 .bak_20260616 보존).
- corpus/index/dense 바이너리 git push 0(G:=비-git). GPU 재실행 0. 이 노트만 push.
