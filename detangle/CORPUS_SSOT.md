# CORPUS SSOT — 정본 corpus 위치 (단일 진실, 2026-06-23)

여러 세션이 corpus 주소로 헤맴 → **이 파일이 단일 진실(SSOT)**. corpus 작업/검색/배포 전에 여기부터 본다.

## ✅ 정본 (이것만 사용)
**`G:\corpus_md_export_20260618`**
- `CORPUS_VERSION.json` version_date = **2026-06-23**
- **per-paper `<slug>/` 폴더 격리** (그림 bare-hash 충돌 77.4% → 0, gate PASS, 공유hash 2070 물리분리)
- papers **3,902**, retrieval_units **250,766**, units_sha1 **0ea866ae2b1e424a…**
- BM25(826MB) + BGE-M3 dense(980MB, norm pass, **dense rows==units 정렬OK**) **full rebuild (2026-06-23)**
- 검색 검증: bm25 ✅ / hybrid(dense+rerank) ✅. 그림 reader = `scripts/read_paper_ns.py`(slug폴더 렌더, Ulleungdo 검증).
- flat `articles/`(옛stem名)는 index 빌드용 텍스트뷰. 메타데이터는 20260612 sidecars 재사용.

## ⚠️ flip 진행 상태 (2026-06-23)
- ✅ **회사PC `.mcp.json` 재등록**: geochem-corpus args 20260612→**20260618** (MCP/세션 재시작 시 적용).
- ⚠️ **타 머신(홈/노트북/NAS) `.mcp.json` 각자 동일 수정 필요** (args→20260618).
- ⚠️ 잔여: MCP get_paper는 텍스트(articles/)만 — namespace 그림은 read_paper_ns.py로. NAS md_view.py 패치 + co-author 패키징(README/req) + books cook_2000 통합은 후속.
- **20260612는 flip 완전검증(cross-machine)까지 fallback으로 무손상 유지.**

## 🗑️ stale / 이전 (정본 아님 — 폴더명 ≠ 내부 버전 주의!)
| 경로 | ver(내부) | papers | 정체 |
|---|---|---|---|
| `G:\corpus_md_export_20260618` | 2026-06-23 | 3902 | ✅ **정본** (namespace 그림격리) |
| `G:\corpus_md_export_20260612` | 2026-06-16 | 3903 | 직전 정본 → **fallback** (그림 bare-hash 꼬임 있음) |
| `G:\corpus_md_export_20260602` | ? | 3954 | 옛(dedup 전) |
| `G:\corpus_md_export_20260610` | 2026-06-10 | 3954 | 옛(dedup 전) |
| `C:\Users\USER\corpus_md_export_20260610/20260612` | 2026-06-12 | 3903 | C 사본(스크립트는 splitlines 버그 옛본 — G:판 쓸 것) |
| `manuscript-atelier\tools\paper-orchestra\corpus\index` | 5/19 stale | 3339 | 레포 미러(매우 옛, evidence searcher 정렬용 아님) |
| `\\100.108.229.47\...\pilot` | - | - | NAS 배포 미러 |

## 규칙
1. corpus **검색·배포·신규작업 = `G:\corpus_md_export_20260618` 만.**
2. 나머지는 옛/fallback — 정리(삭제) 결정 전까지 **건드리지 말 것**(특히 20260612 fallback), 정본 착각 금지.
3. corpus 새 작업 후엔 `CORPUS_VERSION.json` + 이 파일 둘 다 갱신.
4. 폴더명 신뢰 금지 — 항상 내부 `CORPUS_VERSION.json`의 `version_date`로 확인.
5. corpus image/index/raw **git push 0** (corpus_blueprint 코드/문서만 추적).
