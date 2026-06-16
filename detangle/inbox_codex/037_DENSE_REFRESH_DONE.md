# TASK 037 — dense BGE-M3 refresh 완료 (035C GO 이행) (Claude→Codex)

VERDICT 요청: dense refresh 무결성 확인.

## 완료
운영자 035C GO대로 dense BGE-M3를 현재 `index/retrieval_units.jsonl`(20260616)에 맞춰 **full rebuild**.

- **명령**: `python scripts/build_bge_m3_dense.py` (GPU, cuda, fp16 model, 1024-dim, normalize, max_seq 1024, batch 32).
- **결과**: 274,953 임베딩, `embeddings_bge_m3.npy` **1074MB**, shape **(274953, 1024) float32**, row==units ✓.
- **manifest**: units_path=현재 `G:\corpus_md_export_20260612\index\retrieval_units.jsonl`, units_count **274,953**, units_sha1 **55522119bdd5767957879420b13563eb7c3109ef**, n_done 274953, build_mode full_rebuild, device cuda, validation norm[0.9998,1.0005] **pass=True**, completed_at 2026-06-16T19:13.
- **smoke**: `dense_search.py "Changbaishan Tianchi volcanic field dikes …"` → **Xu 2024(교체 논문) top1 cos=0.826** (274,953 벡터 0.35s). dense가 교체 텍스트 반영 확인.

## 버그픽스 (중요)
첫 시도가 `JSONDecodeError`로 실패 — `build_bge_m3_dense.py`가 units를 `read_text().splitlines()`로 파싱했는데, **`splitlines()`가 유니코드 줄바꿈(  등)까지 분리**해 7개 JSON 레코드를 깨뜨림(splitlines 274,960 vs `\n` 274,953, diff 7). BM25(`build_bm25_index`)는 `for line in f`(\n만)라 영향 없었음. → dense 스크립트도 **file iteration으로 통일**(bm25와 동일). 백업 `build_bge_m3_dense.py.bak_20260616`.

## 백업 (비파괴)
- `embeddings_bge_m3.npy.bak_20260616`, `embeddings_bge_m3.manifest.json.bak_20260616`
- `CORPUS_VERSION.json.bak_20260616`, `README_DEPLOY.md.bak_20260616`
- (첫 실패는 np.save 전 죽어 원본 npy/manifest 무변경)

## metadata 갱신 (035C: 옛 2026-06-12 광고 제거)
- `CORPUS_VERSION.json`: version_date→2026-06-16, chunks→274,953, units_sha1→55522119, dense→full_rebuild_20260616, changelog 추가.
- `README_DEPLOY.md`: "3903 papers / 274,953 units" + dense full rebuild 노트.

## 불변 확인
- BM25 / retrieval_units.jsonl **불변** (dense만 갱신). Datalab/raw 재변환 0.
- 하드게이트: corpus/index/dense 바이너리 git push 0 (이 노트만 push).
