# Claude(Code) — Zotero/reference R1 closure (LEDGER_039 / `bfb64c6`)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **ok — R1 CLOSED (accept).** build 건전. 1 minor hardening + 2 nit (전부 비-blocker, Windows-local 입력에선 잠재적).

검증: source_identity.py + check_corpus_references.py + build_corpus_references.py 정독 + **라이브 red-path repro**(check_records 직접).

---

## 건전한 부분 (closure 근거)

- **source_id identity 정확 + 내 Q2 구조적으로 honored**: DOI→OpenAlex→base(`namespace:paper_id`)→provider 우선순위. **content-hash가 identity에 절대 안 들어감** — `source_md_sha1`는 `content_version`으로만, `source_identity_from_parts`에 sha1 파라미터 자체가 없음. 라이브 확인: DOI 있는 record → `kind=doi`(paper_id/sha 아님).
- **checker 포괄적**(FGP 표면스캔보다 강함): 재귀 string walk로 전 필드 검사 — E1 source_id 형식/schema/status enum, E2 dup source_id, E4 dup DOI(same_as 예외), E5 citekey 유일, E6 zotero 키 null 강제, E7 path denylist, E8 raw-text 길이(>5000). 라이브 red-path 전부 의도대로(NAS path/Windows path/zotero key/dup/raw-text 거부, valid 통과).
- **dedupe 건전**: `coalesce_source_duplicates`가 source_id로 묶되 `paper_ids[]`(provenance) + content hashes(1→`source_md_sha1`, 多→`source_md_sha1s` 정렬) 보존. 3339→3220 합당.
- **generated 로컬-only(gitignored)** = 커밋 표면 아님. checker는 pre-commit/pre-release 게이트(FGP/DW 커밋표면보다 stakes 낮음).

---

## Codex 4 질문 답

1. **namespace `cccp_geochem`** → 수락. 안정적·ccc 네이밍 일관. 더 넓은 계약 전 바꿀 거면 지금.
2. **dedupe coalescing** → 엔도스. provenance 보존됨.
3. **generated 로컬-only** → 엔도스. 올바른 기본값. release 스냅샷은 checker 통과 후에만.
4. **zotero 키 가드** → 확인(E6, 라이브 non-null 거부).

---

## Minor 1 (비-blocker, 고치면 좋음): `LOCAL_PATH_RE`가 POSIX `/home/`·`/Users/` 놓침

`LOCAL_PATH_RE`는 `/mnt /volume /Volumes /nas` + 드라이브레터(C:/ G:/ \\)는 잡지만 **`/home/`·`/Users/`는 안 잡음**(라이브 확인: `/home/USER/datalab/secret.csv`·`/Users/USER/...` → E7 안 뜸). 운영자 Windows 입력엔 Windows 경로라 지금은 잠재적이지만, **corpus를 Mac/Linux에서 재빌드하거나 release 스냅샷 만들 때 새는 갭**(FGP-class denylist 한계). → 정규식에 `/home/`, `/Users/` 추가 권장(싸고 확실).

## Nit (2)
- `content_version.source_md_sha1`/`source_md_sha1s`가 hex 형식 핀 안 됨(`^[0-9a-f]{40}$`). build가 입력에서 통제하니 저위험. release 스냅샷 강건성용.
- dedupe는 source_id 기준 — 같은 논문이 행마다 DOI 유무가 다르면(한 행 DOI有→doi-id, 한 행 DOI無→base-id) 안 묶이고 **참조 분할** 가능. R1 수용 가능, 후속에 title+year 2차 reconcile 고려.

---

## 결론

**R1 CLOSED.** Zotero/reference 트랙의 다음 단계(R2 alias bridge 등) 진행 가능(minor는 그 전이나 release 스냅샷 전에 끼워넣기). multi-track 지도 트랙1 "R1 closure ACCEPTED(bfb64c6); LOCAL_PATH_RE minor 1건"으로 갱신 권장.

(read-only · manuscript-atelier push0 · 머지0. 라이브 repro=로컬 `.scratch/zot-gate/`.)
