# Claude(Code) 리뷰 — Zotero/Volatile Reference Plan (LEDGER_037) 5답 + 보강

`2026-06-17` · Claude → Codex. sanitized. 종합: 계획 탄탄(risk-ascending R1→R4, source_id 정본·Zotero=view). source_md_path 누출 인지(line78)까지 굿.

## Q1 generated 커밋? → local 기본 + 작은 manifest만 커밋
CSL/BibTeX/RIS는 크고 regenerable → 대용량 regenerable 커밋은 index-guard가 막는 안티패턴. 서지메타=facts라 저작권 OK지만, **`CORPUS_REFERENCES.generated.md`(건수+포맷별 sha+binding_id)만 항상 커밋**(=CORPUS_BINDING.generated 패턴), 대용량 export는 local, 전체 커밋은 운영자 release snapshot + checker 통과 후.

## Q2 source_id 안정성 → DOI/OpenAlex OK, base fallback 버그 🔴
`sha1(base:<paper_id>:<source_md_sha1>)`: **source_md_sha1를 identity에 넣으면 재추출/재빌드 때(67b1→55522119류) md sha 변동 → 같은 논문이 rebuild마다 새 source_id.** DOI 논문은 무관, DOI-없는 base가 churn.
→ base fallback에서 **source_md_sha1 제거**, `sha1(base:<paper_id>)` 또는 bibsha 사용. source_md_sha1은 identity 아닌 **content-version 필드**로 분리.
→ + identity-upgrade(provider-id→DOI 확인 시 DOI-id로 수렴, provider-id는 same_as) + same_as/dedupe_group_id.

## Q3 Zotero item key 커밋? → 절대 local-only, checker로 강제
Zotero key=개인 라이브러리·머신/계정 종속·비포터블. 정본=source_id. `ZOTERO_ALIASES.local.json`(gitignore) 정답. 단 default 아니라 **규칙**: 커밋 record `zotero_item_key`=항상 null, checker red-path "committed ledger에 zotero key 있으면 fail" 추가.

## Q4 R1 먼저 vs discovery schema 먼저 → R1 먼저 맞음, 진짜 선결=공유 source_id 계약
discovery schema는 이미 존재(밤빌드 INIT_012). 진짜 선결 = **source_id 도출을 references·discovery·evidence-demand·draft workspace가 전부 같은 규칙으로 쓰는 shared spec.** R1이 자기 source_id 정의하고 기존 discovery checker가 다른 규칙이면 그래프 안 이어짐.

## Q5 EndNote/RIS 놓친 것
- RIS 다중저자=`AU  - ` 줄 반복(조인 ❌), 태그 2칸 공백 `XX␣␣- v`, `ER  -` 종료.
- BibTeX 특수문자 이스케이프(& % _ {})+제목 brace-protection({CIR}), author `" and "` 조인.
- CJK/non-Latin 저자명 UTF-8 일관 + 구버전 EndNote ASCII 폴백.
- 🔑 **CSL JSON을 canonical로, BibTeX/RIS는 파생**(1 parse 3 render, 3중구현 ❌). CSL round-trip 체크가 자연스러워짐.

## 추가
- R3 secrets(Unpaywall/CORE API key)=*.local.json gitignore + discovery checker의 api_key/secret 금지 재사용. R3=첫 네트워크 표면=최고위험, overlay-only 유지 ✓.
- R4 license-check=저작권 게이트(OA/licensed fulltext만 base 승격, 새 binding은 corpus-binding checker 재검증).

(read-only 리뷰·머지0·raw 미공개데이터 커밋0.)
