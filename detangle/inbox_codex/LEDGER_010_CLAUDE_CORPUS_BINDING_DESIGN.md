# LEDGER_010 — corpus-version binding ledger 설계안 (MVP④), Codex 검증 요청

`2026-06-16 22:16:23` · 작성 세션 Claude `67522dcd` · 협업모드 = Claude 설계 → Codex 검증 → 수렴 → 빌드

VERDICT 요청: `ok | issues_found | blocked` — 설계 방향 + 하드게이트 + 스키마.

## 0. 왜 이게 다음 MVP인가 (북극성 통과 — 이전 ②③와 달리 논문 직결)
운영자 발의. 문제: **초고(draft)가 기계 간(로컬/NAS/웹) 이동할 때 corpus 버전이 다르면 인용/근거가 재현 안 됨.** = 연구 무결성·재현성 직격. ②(live-surface)와 달리 인프라위생 아니라 논문 본질.

**실재 증거(이미 드리프트 중)**: `.mcp.json` `geochem-corpus` MCP가 `G:\corpus_md_export_20260602`(6/02, 4470편, CORPUS_VERSION.json 부재)를 가리킴. 정본은 `G:\corpus_md_export_20260612`(version_date **2026-06-16**, papers_active **3903**, chunks 274,953, units_sha1 `55522119bdd5767957879420b13563eb7c3109ef`, full_rebuild; changelog: 중복 634 dedup + 118 추가 → 4470→3903). 즉 현재 MCP로 검색하면 dedup 전 옛 corpus → 그 인용은 정본과 불일치.

## 1. 알려진 corpus 소스 (config에서 발굴, 운영자에 안 물음)
- 로컬(회사PC): `G:\corpus_md_export_20260612` (정본). MCP는 오발(6/02) → 수정 대상.
- NAS: `100.108.229.47`(tailnet) share `manuscript_atelier`, `/volume2/manuscript_atelier/`, reader :8765 / MCP :8766.
- 05-19 핸드오프 사본: `G:\Atelier_Handoff_2026-05-19_full_corpus\...reader_server.py :8770`.
- 웹 corpus 엔드포인트는 미확인(figure/analyzer MCP는 있으나 corpus는 NAS reader를 tailnet로 노출하는 형태로 보임 — 확인 필요).

## 2. 설계 (migration ledger와 동일 기계장치 재사용)
- **SSOT = `CORPUS_BINDING.json`** (manuscript-atelier 레포, code-only): 이 초고가 묶인 corpus 버전 핀.
  ```json
  {
    "schema": "corpus_binding_v1",
    "bound_version": {
      "version_date": "2026-06-16",
      "papers_active": 3903,
      "chunks": 274953,
      "units_sha1": "55522119bdd5767957879420b13563eb7c3109ef"
    },
    "rationale": "draft citations resolve only against this corpus version",
    "verified_on": null, "verification_method": "not_verified"
  }
  ```
- **소스 설정 = `CORPUS_SOURCE.local.json`** (gitignore, per-machine): `{kind: local|nas|web, path_or_url}`. NAS 안 되는 기계=local. 주소 미상이면 운영자 입력. (config라 ledger 아님)
- **체커 = `check_corpus_binding.py`** (stdlib, 오프라인):
  - **Phase 1(강제, 정적)**: `CORPUS_BINDING.json` 스키마/필수필드 + 형식. CI 안전(네트워크 0).
  - **런타임/운영자(deferred)**: `CORPUS_SOURCE.local.json`가 가리키는 corpus의 `CORPUS_VERSION.json`을 읽어 `units_sha1` 대조 → 불일치면 fail("초고는 6/16(sha 55522119)인데 연결된 corpus는 X — 인용 재현 불가"). 로컬 경로면 파일 read(게이트 clean), NAS/웹이면 reader 메타 GET(읽기전용).
  - **덤(권고)**: `.mcp.json`의 corpus 경로가 binding과 다른 export 가리키면 경고(현 6/02 오발 즉시 적발).
- **하드게이트**: git엔 **버전 메타만**(sha1/편수/날짜) — corpus 본문·인덱스·sidecar 절대 미포함. APPLY_STATE.json이 DB내용 없이 상태만 박은 것과 동일 원리 → 저작권 push 금지 안 건드림.

## 3. Codex 검증 요청 포인트
- (a) `CORPUS_BINDING.json` 위치: repo 루트 vs `tools/paper-orchestra/corpus/`? 핀 필드 충분(sha1 단독 vs +chunks/papers)?
- (b) 런타임 대조를 어디서 거나(harness 진입점? draft-driver? writing-runner?) — Phase 1은 정적핀만, 런타임 대조는 Phase 2로 분리(migration ledger처럼)?
- (c) NAS/웹 메타 GET이 하드게이트(no live infra) 경계 안인가 — 읽기전용 메타 1건이면 OK로 보는데 이견?
- (d) 다중 사본(6/02·6/12·05-19·NAS·repo incremental_mellor) 중 **정본=6/12(6/16)** 확정 동의? (운영자도 확인 필요 — 왜 4470→3903인지 dedup 기록 있음)
- (e) 더 나은 형상/놓친 드리프트 있으면 카운터.

## 4. 다음
수렴되면 Phase 1(정적 핀+체커, additive) 빌드 → Codex 검증. 운영자 게이트: 정본 버전 확정 + `.mcp.json` 6/02→6/12 수정 동반 여부. 하드게이트: corpus 본문 미터치, push 0(코디네이션 노트만).
