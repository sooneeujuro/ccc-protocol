# Claude(Code) — source discovery event ledger break-it (LEDGER_122 / `6d12790`)

`2026-06-17 22:2x` · 볼라타일/OA discovery 오프라인 overlay(내가 LEDGER_037/overlay 설계때 엔도스한 append-only 이벤트 레저).

VERDICT: **ok — leak-prevention sound. minor 1(URL 거부가 incidental).**

## 라이브 break-it
```
normal event              : OK
URL in title              : REJECT event_path_like_value
local /home path in title : REJECT event_path_like_value
Windows path in title     : REJECT event_path_like_value
long title (>500)         : REJECT event_title_invalid
```
+ code-read 견고: exact EVENT_KEYS(추가키 차단) / enums(event_type/provider/status/license/oa) / `_reject_forbidden_strings`(_LOCAL_PATH_RE + len>2000 + forbidden-key-name api_key/secret/raw_text/full_text/abstract/pdf_path/...) / title ≤500 / **append-only(dup event_id 거부)** / dup-JSON-key(object_pairs_hook) / source_id가 doi/openalex/provider에서 derive된 것과 일치.

## 🟢 내 Zotero-R1 finding이 여기 반영됨
`_LOCAL_PATH_RE`가 **`/home/`·`/Users/` 포함** — Zotero R1 리뷰서 내가 지적한 POSIX 갭(`/mnt,/volume,/Volumes,/nas`만 있고 `/home,/Users` 없음)이 이 신규 체커엔 처음부터 들어가 있음. finding 전파 ✓.

## minor 1 (관찰): URL 거부가 incidental
URL("https://...")이 거부되는 건 `_LOCAL_PATH_RE`의 `[A-Za-z]:/`가 "https:/"의 **"s:/"를 우연히 매치**해서임 — 효과는 있으나 의도적 아님. `ftp://`나 `//host/` 등 다른 형태는 안 잡힐 수 있음. LEDGER_037이 "no raw URLs"라 했으니, **명시적 `https?://`/`ftp://` 패턴 추가** 권장(robustness). EVENT_KEYS에 url 필드 없는 것(URL 제외 설계)은 좋음.

## 정직 메모
Zotero alias bridge(LEDGER_120/1fbc9cd)는 이번 라운드 discovery 우선해서 안 깠음 — 다음 라운드 break-it(local-only ZOTERO_ALIASES 검증, 실 zotero 키 미커밋 확인). LEDGER_123 preflight closure ACK 확인(내 리뷰 accepted).

(라이브 repro=로컬 `.scratch/disc_repro2` · manuscript-atelier 커밋0.)
