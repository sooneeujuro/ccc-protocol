# DEPLOY/NAS 핸드오프 — Book corpus 서빙 (G:\book_corpus_20260629)

**From:** Claude (atelier) · **To:** NAS/deploy 이식 세션 · **Date:** 2026-06-29
**상태:** book 번들 빌드 완료 + 독립 게이트 27/27 PASS + CODEX 검토 `ok_with_deploy_condition`.
**근거 문서:** `detangle/inbox_codex/LEDGER_446_CLAUDE_BOOK_BUNDLE.md`, `BOOK_BUNDLE_VERIFY_446.txt`.

> **⚡ UPDATE 2026-06-29 — HOME 머신(MA)은 Claude가 이미 적용 완료.**
> `manuscript-atelier\.mcp.json`에서: (1) `geochem-corpus`를 신정본 `corpus_20260626`으로 flip,
> (2) `geochem-corpus-book` 2nd 서버 추가(`G:\book_corpus_20260629\scripts\corpus_mcp.py`),
> (3) **serve_as_book 필터를 `corpus_mcp.py` `_search()`에 패치**(아래 §CONDITION 코드 그대로) — selftest 검증
> 완료(dup 'continental crust'→n_results 0, genuine 'noble gas'→ozima·burnard). MA 세션 재시작 시 활성.
> **NAS/타 머신이 할 일은 자기 머신에서만**: ⓐ corpus 폴더 이식 시 **필터는 corpus_mcp.py에 이미 내장돼 따라감**
> (재패치 불필요), ⓑ 자기 `.mcp.json`의 args를 **자기 corpus 체크아웃 경로**로 repoint. 아래 §CONDITION은 NAS가
> 별도 빌드본을 쓸 때의 참고용.

이 책 corpus는 article 번들(`G:\corpus_20260626`)과 **스키마 동일한 standalone serving root**다.
CORPUS_POLICY §1: BM25/dense **인덱스 병합 금지**, 별도 reader instance로 띄우고 **retrieval에서만 RRF join**.
`CORPUS_VERSION.json`에 `separate_from_articles=true`.

| 항목 | 값 |
|---|---|
| root | `G:\book_corpus_20260629` |
| books / sidecars | 17 / 17 (`is_book=true`) |
| retrieval_units = bm25 = emb | **10,373** (정렬 검증됨) |
| dense | BAAI/bge-m3, 1024d, L2 normalized, cuda |
| index | `index/bm25_index.pkl`, `index/embeddings_bge_m3.npy` |
| citation_index | `citation_index.json` (article root와 동일 sha1 `91b4f055b9a60e4d`, n_papers 4013) |
| reader/search | `scripts/read_paper_ns.py`, `scripts/corpus_mcp.py` |

---

## ★ CONDITION (필수) — serve_as_book 필터 적용

CODEX 검토에서 확인: **현재 `scripts/corpus_mcp.py`는 `serve_as_book` 필터를 자동 적용하지 않는다.**
17권 중 **7권은 article corpus의 동일 논문 중복본**(sim=1.0)이라 비파괴 태깅돼 있다:
`serve_as_book=false` + `dup_of_article=<article_pid>`. 해당 7권 = **427 retrieval units**
(genuine book units = 9,946 / 전체 10,373).

이 7권을 **책 reader/RRF join에서 제외하지 않으면 같은 내용이 article·book 양쪽에서 잡혀 RRF 이중카운트**가 난다.
인용 자체는 이미 article 카피로 resolve되므로 dangling은 없다 — 순수 **서빙 중복** 문제.

### 적용 지점: `corpus_mcp.py` `_search()` dedup 루프 (line 133–142)
모듈 로드 시 `serve_as_book=false`인 paper_id 집합을 1회 구축하고, dedup 루프에서 제외:

```python
# 모듈 상단(인덱스 로드부)에 1회:
import json as _json
_EXCLUDE_BOOK = set()
_SIDE = EXPORT / "sidecars"          # corpus_mcp의 root 변수에 맞춰 조정
if _SIDE.is_dir():
    for _f in _SIDE.glob("*.json"):
        try:
            _d = _json.load(open(_f, encoding="utf-8"))
            if _d.get("serve_as_book") is False:
                _EXCLUDE_BOOK.add(_d.get("id") or _f.stem)
        except Exception:
            pass

# _search() dedup 루프 안:
    for h in hits:
        pid = h.get("paper_id")
        if pid in seen or pid in _EXCLUDE_BOOK:   # ← serve_as_book=False 제외
            continue
        ...
```

**article reader에는 무해**: article sidecar에는 `serve_as_book=false`가 없어 `_EXCLUDE_BOOK`이 빈 집합 → 동작 변화 0.
(공유 `corpus_mcp.py`에 넣어도 article 인스턴스 영향 없음.)

---

## 서빙 방법
- book reader instance를 book root로 기동: 환경변수/경로를 `G:\book_corpus_20260629`로
  (article과 동일하게 `GEOCHEM_CORPUS_ROOT` 패턴; `run_dense.bat` 참고).
- article 인스턴스와 **별도 프로세스/별도 인덱스**. 사용자 쿼리는 두 인스턴스에 던지고 **RRF로 join**.
- 그림: 각 책 slug 폴더(`<12hex>/`)에 격리됨(1,521장, 충돌 0). `STEM_TO_SLUG.json`으로 매핑.

## C: clone (필요 시)
현재 book corpus는 **G: only**. article 번들은 G:정본 + C:클론 양쪽이라, 동일 패턴이 필요하면:
`robocopy G:\book_corpus_20260629 C:\Users\USER\Documents\book_corpus_20260629 /E /NFL /NDL /NJH /NP`
(robocopy exit 1 = 정상). 클론 후 `serve_as_book` 필터/경로 동일 적용.

## co-citation / bibliographic-coupling 그래프 (여유 작업)
corpus_20260626/book_corpus 어디에도 co-citation **산출물은 아직 없다**. citation_index만 있다.
계산은 **결정론**(LLM 불필요) — `citation_index.json`의 `cites`/`cited_by`로:
- **co-citation(A,B)** = `|cited_by[A] ∩ cited_by[B]|` (같은 논문이 A·B를 함께 인용)
- **biblio-coupling(A,B)** = `|refs(A) ∩ refs(B)|` (A·B가 같은 참고문헌 공유; `cites[*].to`로 계산)

**권고:** NAS가 이미 그린 **논문용 그래프 코드를 재사용**해 책+통합으로 확장하는 게 포맷 통일에 유리.
입력으로 **통합 citation_index**(`G:\corpus_20260626\citation_index.json`, n_papers **4013** = article 3996 + book 17, 책이 1급 타겟)를 주면 **article+book 통합 co-citation 그래프**를 한 번에 그릴 수 있다.
(원하면 atelier에서 결정론 스크립트로 즉석 생성도 가능 — 말만 주면 됨.)
