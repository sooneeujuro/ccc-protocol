# Knowledge Base (KB) 연결 가이드

**기준일: 2026-06-29** · 작성: Claude (atelier) · 위치: `ccc-protocol/detangle/KB_CONNECT.md` (정본) + `C:\Users\USER\Documents\knowledge_base\KB_CONNECT.md` (이 PC 동봉본)

논문작성 세션(manuscript-atelier, MA)이 참조하는 **연구 모듈** 전체와 연결 방법을 한 곳에 정리한다.
모듈은 MCP(stdio/http) 서버로 MA의 `.mcp.json`에 등록되며, MA 세션 시작 시 1회 로드된다.

---

## 1. 2026-06-29 기준 최신 버전

| 모듈 | 최신본 | 핵심 스펙 | 연결 |
|---|---|---|---|
| **CorpusP** (논문) | **`corpus_20260626`** (ver 2026-06-26) | articles 3,997(+헬륨19) · retrieval_units 256,569 · DOI 3,896/3,996 · citation_index n_papers 4,013 | MCP `geochem-corpus` (stdio) |
| **CorpusB** (책) | **`book_corpus_20260629`** (ver 2026-06-29) | books 17 · units 10,373 · BGE-M3+BM25 · **serve_as_book 필터(dup 7권/427units 제외)** | MCP `geochem-corpus-book` (stdio) |
| **FGP** | MA 내부 프로토콜 | leak-safe(`raw_fgp_text_in_writer_prompt=forbidden`) — **MCP 아님**, MA가 자체 보유 | (연결 대상 아님) |
| (도구) geochem-analyzer | vercel | 통계/figure 14 tools | MCP http |
| (도구) figures | sooneeujuro.com | TAS/Piper/ternary 등 8 tools | MCP http |
| (도구) pygmt-maps | PYGMT_JYP | 지도 render | MCP stdio (conda) |

> 버전 확인은 **폴더명 신뢰 금지** → 각 모듈 `CORPUS_VERSION.json`의 `corpus_version` 값으로.

---

## 2. canonical vs mirror 정책

- **G: = canonical (SSOT)** — `G:\corpus_20260626`, `G:\book_corpus_20260629`. NAS/타 머신/메모리/핸드오프의 기준.
- **C: = 이 PC 로컬 미러** — `C:\Users\USER\Documents\knowledge_base\` 아래 복제(copy). G 외장이 안 붙어도 이 PC는 동작.
- 미러는 G→C 단방향 동기화(robocopy /E). **C에서 수정 금지** — 변경은 G(canonical)에서 하고 C로 sync.

```
C:\Users\USER\Documents\knowledge_base\
  ├─ corpus_20260626\         (= G:\corpus_20260626 미러)
  ├─ book_corpus_20260629\    (= G:\book_corpus_20260629 미러)
  └─ KB_CONNECT.md            (이 문서)
```

---

## 3. 머신별 연결법

각 corpus 모듈은 `<root>\scripts\corpus_mcp.py`를 stdio로 띄워 **search_papers / get_paper / corpus_info** 3 tool을 노출한다. `EXPORT = <root>` (스크립트 부모) 기준으로 자기 index/articles/sidecars를 읽는다.

### (A) 이 PC (home, MA) — C 미러에 연결
`manuscript-atelier\.mcp.json`:
```jsonc
"geochem-corpus": {
  "command": "python",
  "args": ["C:\\Users\\USER\\Documents\\knowledge_base\\corpus_20260626\\scripts\\corpus_mcp.py"],
  "env": { "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1", "PYTHONUTF8": "1" }
},
"geochem-corpus-book": {
  "command": "python",
  "args": ["C:\\Users\\USER\\Documents\\knowledge_base\\book_corpus_20260629\\scripts\\corpus_mcp.py"],
  "env": { "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1", "PYTHONUTF8": "1" }
}
```

### (B) 타 머신 / NAS — 자기 corpus 체크아웃에 연결
- corpus 폴더를 자기 머신에 이식(G canonical 복제) → `.mcp.json`의 `args`만 **자기 경로**로 repoint.
- **serve_as_book 필터는 `book_corpus\scripts\corpus_mcp.py`에 내장**돼 폴더 이식 시 따라감 (재패치 불필요).
- BGE 모델이 캐시 안 돼 있으면 첫 실행에서 `HF_HUB_OFFLINE`/`TRANSFORMERS_OFFLINE` env를 잠깐 빼고 1회 받아라(안 그러면 hang).

### 공통
- **MCP는 MA 세션 시작 시 로드** → 경로 바꾼 뒤 **MA 세션 재시작**해야 적용.
- MA repo는 커밋하지 않는다(운영자 정책 "manuscript-atelier 커밋0"). `.mcp.json` 변경 전 백업.

---

## 4. CorpusB serve_as_book 필터 (중요)

book corpus 17권 중 **7권은 article corpus 중복본**(single chapter/paper가 책으로도 번들됨):
`german_2010_rainbow, klein_2019_abiotic_methane, mccollom_2006, mcdermott_abiotic_org_synth,`
`rudnick_gao_2003_ccrust, ryan_2009_gmrt, taran_2007_fischer_tropsch`.
- 이들은 sidecar에 `serve_as_book=false` + `dup_of_article` 태깅.
- `corpus_mcp.py` `_search()`가 `_EXCLUDE_BOOK`(serve_as_book=false id 집합)을 검색결과에서 제외 → CorpusP와의 RRF 이중카운트 방지.
- 검증(selftest): dup "continental crust"→n_results 0, genuine "noble gas"→ozima·burnard 정상.
- citation은 이미 article 카피로 resolve되므로 dangling 없음 — 순수 서빙 중복만 차단.

---

## 5. 검증 / 트러블슈팅

```powershell
# 모듈 인덱스 로드 확인 (bm25)
$env:PYTHONUTF8=1
python -c "import sys; sys.path.insert(0, r'<root>\scripts'); import corpus_mcp; print(len(corpus_mcp._get_index().chunks))"
# book 필터 확인
python -c "import sys; sys.path.insert(0, r'<book_root>\scripts'); import corpus_mcp; print(sorted(corpus_mcp._EXCLUDE_BOOK))"
# bm25-only smoke (모델 다운 X)
python <root>\scripts\corpus_mcp.py --selftest "query" bm25 0
```

## 6. 변경 이력
- **2026-06-29**: corpus_20260626으로 MCP flip(was corpus_md_export_20260618), book corpus 번들+등록, serve_as_book 필터, KB(C 미러) 구성. 백업: `.mcp.json.bak_20260629_pre0626flip`, `.bak_20260629_pre_bookadd`, `corpus_mcp.py.bak_20260629_pre_serve_filter`.
- 관련: `inbox_codex/LEDGER_446`, `inbox_deploy/DEPLOY_BOOK_CORPUS_HANDOFF.md`, memory `corpus-ssot-location`·`book-corpus-state`.
