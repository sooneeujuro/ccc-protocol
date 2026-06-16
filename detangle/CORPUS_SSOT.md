# CORPUS SSOT — 정본 corpus 위치 (단일 진실, 2026-06-16)

여러 세션이 corpus 주소로 헤맴 → **이 파일이 단일 진실(SSOT)**. corpus 작업/검색/배포 전에 여기부터 본다.

## ✅ 정본 (이것만 사용)
**`G:\corpus_md_export_20260612`**
- `CORPUS_VERSION.json` version_date = **2026-06-16**
- articles **3,903** md, retrieval_units **274,953**, units_sha1 **55522119bdd5767957879420b13563eb7c3109ef**
- BM25 + BGE-M3 dense **full rebuild (2026-06-16)** 정렬 완료
- 2026-06-16 세션의 그림 refill(604→1)·재색인·dense·PDF/supp 정리 **전부 여기**. **유일하게 최신.**

## ⚠️ 드리프트 — 고쳐야 함
- **MCP(`corpus_mcp.py`) 등록 args = `G:\corpus_md_export_20260602`** (옛 3,954편, **dedup 전**). → 현재 **검색/MCP가 옛 corpus를 봄.**
  - 조치: MCP 등록 경로를 **`G:\corpus_md_export_20260612`** 로 교체(재등록). (운영자/Codex 트랙)
  - ✅ **2026-06-16 회사PC `.mcp.json` 재등록 완료**(Claude 67522dcd): geochem-corpus args 6/02→**6/12**, JSON 검증 OK, MCP/세션 재시작 시 적용. ⚠️ 타 머신(홈/노트북)은 각자 `.mcp.json` 동일 수정 필요 — corpus-binding MVP가 코드로 강제 예정.
- 다른 세션이 본 "corpus-version binding MVP" = 이 드리프트를 코드로 못박는 작업.

## 🗑️ stale / 미러 (정본 아님 — 폴더명 ≠ 내부 버전 주의!)
| 경로 | ver(내부) | md | 정체 |
|---|---|---|---|
| `G:\corpus_md_export_20260612` | 2026-06-16 | 3903 | ✅ 정본 |
| `G:\corpus_md_export_20260602` | ? | 3954 | 옛(dedup 전). **MCP가 가리킴** |
| `G:\corpus_md_export_20260610` | 2026-06-10 | 3954 | 옛(dedup 전) |
| `C:\Users\USER\corpus_md_export_20260610` | 2026-06-12 | 3903 | C 사본(폴더명과 버전 불일치) |
| `C:\Users\USER\corpus_md_export_20260612` | 2026-06-12 | 3903 | C 사본(6/12 스냅샷, 6/16 작업 반영 안 됨) |
| `manuscript-atelier\tools\paper-orchestra\corpus\index` | incremental_mellor | ? | 레포 미러(더 옛, 037 대상 아님) |
| `\\100.108.229.47\manuscript_atelier\...\pilot` | - | - | NAS 배포 미러 |

## 규칙
1. corpus **검색·배포·신규작업 = `G:\corpus_md_export_20260612` 만.**
2. 나머지 4벌+미러는 옛 스냅샷 — 정리(삭제) 결정 전까지 **건드리지 말 것**, 정본으로 착각 금지.
3. corpus 새 작업 후엔 `CORPUS_VERSION.json` + 이 파일 둘 다 갱신.
4. 폴더명 신뢰 금지 — 항상 내부 `CORPUS_VERSION.json`의 `version_date`로 확인.
